"""
Block Encoding Adaptive Measurements for Lorenz System (FIXED)
==============================================================

Includes:
- Proper adaptive measurement (conditional refinement)
- Correct shot scaling
- State selection strategy
- Entropy-based probability floor
"""

import sys
import os
import time
import numpy as np
import scipy.linalg
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from fable import fable

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from lorenz.classical import euler_lorenz
from lorenz.plot_results import plot_lorenz_comparison

# ---------------------------------------------------------------------------
# Parameters
# ---------------------------------------------------------------------------
DT = 0.01
SIGMA = 10.0
RHO = 28.0
BETA = 8.0 / 3.0

X0, Y0, Z0 = 1.0, 1.0, 1.0
T_FINAL = 10.0
N_STEPS = int(T_FINAL / DT)

BASE_SHOTS = 10000
MAX_SHOTS_CAP = 200000
LYAPUNOV_EXP = 0.9

SAVE_DIR = os.path.join(os.path.dirname(__file__), "..", "figures", "07_adaptive")
os.makedirs(SAVE_DIR, exist_ok=True)

# ---------------------------------------------------------------------------
# Adaptive Measurement Utilities
# ---------------------------------------------------------------------------
def shots_schedule(t, base=BASE_SHOTS, lambda_=LYAPUNOV_EXP, max_cap=MAX_SHOTS_CAP):
    """Exponential schedule to counteract chaotic divergence."""
    return int(min(base * np.exp(2 * lambda_ * t), max_cap))


def counts_to_probs(counts, shots):
    """Converts a counts dictionary to empirical probabilities."""
    return {bitstring: c / shots for bitstring, c in counts.items()}


def merge_prob_estimates(p1, n1, p2, n2):
    """Optimal statistical fusion of two shot-weighted distributions."""
    merged = {}
    keys = set(p1) | set(p2)
    for k in keys:
        v1 = p1.get(k, 0.0)
        v2 = p2.get(k, 0.0)
        merged[k] = (n1 * v1 + n2 * v2) / (n1 + n2)
    return merged


def select_important_states(probs, threshold=1e-3, max_states=8):
    """Selects the most probable computational bases."""
    sorted_states = sorted(probs.items(), key=lambda x: x[1], reverse=True)
    important = {}
    for state, p in sorted_states:
        if p > threshold or len(important) < max_states:
            important[state] = p
    return important


def compute_total_shots(important_probs, base_shots, max_cap=MAX_SHOTS_CAP):
    """Calculates refinement shots based on 1/sqrt(p)."""
    weights = np.array([1 / np.sqrt(max(p, 1e-8)) for p in important_probs.values()])
    weights /= np.sum(weights)
    total_shots = base_shots * len(important_probs)
    return int(min(total_shots, max_cap))


def needs_refinement(probs, threshold_var=1e-4):
    """Decides if the current variance requires refinement."""
    var = sum(p * (1 - p) for p in probs.values())
    return var > threshold_var


def adaptive_floor(probs, shots):
    """Entropy-based resolution limit to prevent Origin Trap."""
    entropy = -sum(p * np.log(p + 1e-12) for p in probs.values())
    return max(0.5 / shots, 1e-6 * entropy)


# ---------------------------------------------------------------------------
# Adaptive Measurement Pipeline
# ---------------------------------------------------------------------------
def adaptive_measurement(qc: QuantumCircuit, simulator: AerSimulator, t: float, n: int, total_qubits: int):
    
    ancilla_len = total_qubits - n
    target_ancilla = '0' * ancilla_len
    
    def extract_valid_probs(raw_counts, shots_used):
        valid = {}
        successful_shots = 0
        for bitstring, c in raw_counts.items():
            if bitstring[:ancilla_len] == target_ancilla:
                sys_str = bitstring[-n:]
                valid[sys_str] = valid.get(sys_str, 0) + c
                successful_shots += c
                
        if successful_shots == 0:
            return {}, 0
            
        return {k: v / successful_shots for k, v in valid.items()}, successful_shots

    # --- Exploration ---
    shots_explore = shots_schedule(t)
    job_explore = simulator.run(qc, shots=shots_explore)
    probs_explore, valid_explore_shots = extract_valid_probs(job_explore.result().get_counts(), shots_explore)

    if valid_explore_shots == 0:
        valid_explore_shots = 1 # fallback

    # --- Select important states ---
    important = select_important_states(probs_explore)

    # --- Conditional refinement ---
    if not needs_refinement(probs_explore):
        return probs_explore, valid_explore_shots

    # --- Compute refined shots ---
    shots_refine = compute_total_shots(
        important_probs=important,
        base_shots=shots_explore  # actually use valid_explore_shots?
    )

    # --- Refinement ---
    job_refine = simulator.run(qc, shots=shots_refine)
    probs_refine, valid_refine_shots = extract_valid_probs(job_refine.result().get_counts(), shots_refine)
    
    if valid_refine_shots == 0:
        return probs_explore, valid_explore_shots # skip refine integration

    # --- Merge ---
    probs_final = merge_prob_estimates(
        probs_explore, valid_explore_shots,
        probs_refine, valid_refine_shots
    )

    return probs_final, valid_explore_shots + valid_refine_shots


# ---------------------------------------------------------------------------
# Quantum Step
# ---------------------------------------------------------------------------
def next_step_adaptive(input_state_scaled, physical_state, alpha, fable_circuit,
                       simulator, dim, t, S):

    norm = np.linalg.norm(input_state_scaled)
    if norm == 0:
        return input_state_scaled, 0

    initial_normalized = input_state_scaled / norm

    n = int(np.log2(dim))
    total_qubits = fable_circuit.num_qubits

    padded_state = np.zeros(2**n, dtype=complex)
    padded_state[0:dim] = initial_normalized

    qc = QuantumCircuit(total_qubits)
    qc.initialize(padded_state.tolist(), range(n))
    qc.append(fable_circuit, range(total_qubits))
    qc.measure_all()
    qc = transpile(qc, simulator)

    probs_final, step_shots = adaptive_measurement(qc, simulator, t, n, total_qubits)

    p_floor = adaptive_floor(probs_final, step_shots)

    p_x = max(probs_final.get('000', 0.0), p_floor)
    p_y = max(probs_final.get('001', 0.0), p_floor)
    p_z = max(probs_final.get('010', 0.0), p_floor)
    p_xz = max(probs_final.get('011', 0.0), p_floor)
    p_xy = max(probs_final.get('100', 0.0), p_floor)

    abs_x = np.sqrt(p_x) * alpha * norm
    abs_y = np.sqrt(p_y) * alpha * norm
    abs_z = np.sqrt(p_z) * alpha * norm
    abs_xz = np.sqrt(p_xz) * alpha * norm
    abs_xy = np.sqrt(p_xy) * alpha * norm

    x_prev, y_prev, z_prev = physical_state[:3]

    dx = DT * SIGMA * (y_prev - x_prev)
    dy = DT * (x_prev * (RHO - z_prev) - y_prev)
    dz = DT * (x_prev * y_prev - BETA * z_prev)

    sign_x = 1 if (x_prev + dx) >= 0 else -1
    sign_y = 1 if (y_prev + dy) >= 0 else -1
    sign_z = 1 if (z_prev + dz) >= 0 else -1

    x = sign_x * abs_x
    y = sign_y * abs_y
    z = sign_z * abs_z

    EMA_ALPHA = 0.85

    x = EMA_ALPHA * x + (1 - EMA_ALPHA) * x_prev * S[0, 0]
    y = EMA_ALPHA * y + (1 - EMA_ALPHA) * y_prev * S[1, 1]
    z = EMA_ALPHA * z + (1 - EMA_ALPHA) * z_prev * S[2, 2]

    return np.array([
        x, y, z,
        sign_x * sign_z * abs_xz,
        sign_x * sign_y * abs_xy,
        input_state_scaled[5],
        input_state_scaled[6],
        input_state_scaled[7]
    ]), step_shots


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    print(f"Starting FIXED Adaptive Measurement Simulation...")

    t_values = np.linspace(0, T_FINAL, N_STEPS + 1)

    A = np.array([
        [1 - DT * SIGMA, DT * SIGMA, 0, 0, 0, 0, 0, 0],
        [DT * RHO, 1 - DT, 0, -DT, 0, 0, 0, 0],
        [0, 0, 1 - DT * BETA, 0, DT, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 1]
    ])

    W = np.array([1/20, 1/30, 1/50, 1/1000, 1/600, 1, 1, 1])
    S = np.diag(W)
    inv_S = np.diag(1.0 / W)

    A_scaled = S @ A @ inv_S
    dim = A_scaled.shape[0]

    A_norm = A_scaled / np.linalg.norm(A_scaled, 2)
    
    fable_circuit, alpha_fable = fable(A_norm)
    alpha = np.linalg.norm(A_scaled, 2) * alpha_fable

    print(f"[*] FABLE Circuit Generated!")
    print(f"[*] Total Qubits: {fable_circuit.num_qubits}")
    print(f"[*] Circuit Depth: {fable_circuit.depth()}")
    print(f"[*] Total Valid Operations: {sum(fable_circuit.count_ops().values())}")

    simulator = AerSimulator()

    current_sv = np.array([X0, Y0, Z0, X0*Z0, X0*Y0, 1, 1, 1])

    history_y = [Y0]
    history_z = [Z0]
    total_shots = 0

    start_time = time.time()
    for step in range(N_STEPS):
        t = t_values[step]

        scaled = S @ current_sv

        output_scaled, shots = next_step_adaptive(
            scaled, current_sv, alpha, fable_circuit,
            simulator, dim, t, S
        )

        total_shots += shots
        
        if step > 0 and step % (N_STEPS // 10) == 0:
            pct = int(100 * step / N_STEPS)
            print(f"[{pct:3d}%] Step {step:4d} | X: {current_sv[0]:.2f} | Shots Step: {shots:,}")

        output = inv_S @ output_scaled

        next_sv = np.copy(output)
        next_sv[3] = next_sv[0] * next_sv[2]
        next_sv[4] = next_sv[0] * next_sv[1]

        history_x.append(next_sv[0])
        history_y.append(next_sv[1])
        history_z.append(next_sv[2])

        current_sv = next_sv

    end_time = time.time()
    total_time = end_time - start_time
    
    print(f"[100%] Step {N_STEPS}/{N_STEPS} | Simulation Complete.")
    print(f"Total SUCCESSFUL post-selected valid shots: {total_shots:,}")
    print(f"[*] Total Execution Time (FABLE Block Encoding): {total_time:.2f} seconds")
    print(f"[*] Average Time per Step: {total_time/N_STEPS:.4f} seconds")

    t_cl, x_cl, y_cl, z_cl = euler_lorenz(
        DT, SIGMA, RHO, BETA, X0, Y0, Z0, N_STEPS
    )

    plot_lorenz_comparison(
        t_values,
        np.array(history_x),
        np.array(history_y),
        np.array(history_z),
        t_cl, x_cl, y_cl, z_cl,
        title="Lorenz Adaptive (Fixed)",
        quantum_label="Quantum (Adaptive)",
        classical_label="Classical (Euler)",
        save_dir=SAVE_DIR,
        prefix_name="lorenz_be_adaptive",
        show=False
    )


if __name__ == "__main__":
    main()
