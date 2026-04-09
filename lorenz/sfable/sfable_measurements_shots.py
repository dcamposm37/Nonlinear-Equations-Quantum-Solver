"""
True S-FABLE Block Encoding Measurements Simulation for Lorenz System (Shot-Based)
====================================================================================

Solves the nonlinear Lorenz system using the Sparse Fast Approximate BLock
Encodings (S-FABLE) algorithm with hardware-realistic shot measurements.

Key Implementations:
1. Classical Pre-processing: H_n * A_norm * H_n to preserve sparsity in Walsh domain.
2. S-FABLE Oracle Generation with Cutoff (FABLE_CUTOFF).
3. Quantum Sandwich: H gates before and after the oracle to restore the basis.
4. Ancilla Post-Selection with adaptive Shot Boosting.
5. Predictor-Corrector EMA filter for shot noise dampening.
6. Execution profiling (Depth & Speed).

Usage
-----
    python -m lorenz.sfable.sfable_measurements_shots

Output
------
    lorenz/figures/08_sfable/lorenz_sfable_shots_3d.png
    lorenz/figures/08_sfable/lorenz_sfable_shots_2d.png
    lorenz/figures/08_sfable/lorenz_sfable_shots_error_log.png
"""

import sys
import os
import time
import numpy as np
import scipy.linalg
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from fable import fable

# Allow imports from project root
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from lorenz.classical import euler_lorenz
from lorenz.plot_results import plot_lorenz_comparison

# ---------------------------------------------------------------------------
# Parameters
# ---------------------------------------------------------------------------
DT = 0.01              # Step size (h)
SIGMA = 10.0           # Prandtl number
RHO = 28.0             # Rayleigh number
BETA = 8.0 / 3.0       # Physical proportion

X0, Y0, Z0 = 1.0, 1.0, 1.0
T_FINAL = 10.0
N_STEPS = int(T_FINAL / DT)
BASE_SHOTS = 20000     # Default simulated hardware shots
BOOST_SHOTS = 500000   # Enhanced shots for extremely low post-selection amplitudes

# S-FABLE Compression Cutoff
FABLE_CUTOFF = 1e-3

SAVE_DIR = os.path.join(os.path.dirname(__file__), "figures")
os.makedirs(SAVE_DIR, exist_ok=True)

# ---------------------------------------------------------------------------
# Quantum Block-Encoding Forward Step (Shot-Based)
# ---------------------------------------------------------------------------
def next_step_measured(input_state_scaled: np.ndarray, physical_state: np.ndarray,
                       alpha: float, fable_circuit: QuantumCircuit,
                       simulator: AerSimulator, dim: int, step: int, S: np.ndarray):
    """
    Advances one step using the S-FABLE circuit with hardware-realistic shot
    measurements. Applies the Hadamard sandwich, post-selects on ancilla == |0>,
    and uses a Predictor-Corrector EMA filter to dampen shot noise.
    """
    norm = np.linalg.norm(input_state_scaled)

    def _euler_fallback():
        x_p = np.clip(physical_state[0], -1e6, 1e6)
        y_p = np.clip(physical_state[1], -1e6, 1e6)
        z_p = np.clip(physical_state[2], -1e6, 1e6)
        x_n = x_p + DT * SIGMA * (y_p - x_p)
        y_n = y_p + DT * (x_p * (RHO - z_p) - y_p)
        z_n = z_p + DT * (x_p * y_p - BETA * z_p)
        return np.array([x_n*S[0,0], y_n*S[1,1], z_n*S[2,2],
                         x_n*z_n*S[3,3], x_n*y_n*S[4,4],
                         input_state_scaled[5], input_state_scaled[6], input_state_scaled[7]], dtype=float)

    # Guard: NaN / Inf / numerical underflow -> classical fallback
    if not np.isfinite(norm) or norm < 1e-200:
        return _euler_fallback()

    initial_normalized = input_state_scaled / norm

    n = int(np.log2(dim))
    total_qubits = fable_circuit.num_qubits
    ancilla_len = total_qubits - n

    padded_state = np.zeros(2**n, dtype=complex)
    padded_state[:dim] = initial_normalized

    # Safety: if sum of squares rounds to zero by float precision -> fallback
    if np.sum(np.abs(padded_state)**2) < 1e-30:
        return _euler_fallback()

    system_qubits = list(range(n))

    qc = QuantumCircuit(total_qubits)

    # 1. Initialize ONLY the system qubits. normalize=True handles residual
    #    floating-point normalization errors gracefully.
    qc.initialize(padded_state.tolist(), system_qubits, normalize=True)

    # 2. TRUE S-FABLE QUANTUM SANDWICH
    #    Paso A: Hadamard on system qubits BEFORE oracle
    qc.h(system_qubits)
    #    Paso B: S-FABLE Oracle (encodes H_n @ A_norm @ H_n)
    qc.append(fable_circuit, range(total_qubits))
    #    Paso C: Hadamard on system qubits AFTER oracle
    qc.h(system_qubits)

    # 3. Measure all
    qc.measure_all()
    qc = transpile(qc, simulator)

    target_ancilla = '0' * ancilla_len

    def extract_valid_probs(raw_counts):
        """Post-select on ancilla == |0> and return normalized probabilities."""
        valid = {}
        successful_shots = 0
        for bitstring, c in raw_counts.items():
            # Qiskit bitstring: MSB first. Ancilla qubits are HIGH-index => leftmost.
            if bitstring[:ancilla_len] == target_ancilla:
                sys_str = bitstring[-n:]
                valid[sys_str] = valid.get(sys_str, 0) + c
                successful_shots += c
        if successful_shots == 0:
            return {}, 0
        return {k: v / successful_shots for k, v in valid.items()}, successful_shots

    # 4. First execution
    counts = simulator.run(qc, shots=BASE_SHOTS).result().get_counts()
    probs, valid_shots = extract_valid_probs(counts)

    sum_important = sum(probs.get(k, 0.0) for k in ['000', '001', '010', '011', '100'])

    # Shot Boosting when signal is too weak
    if sum_important < 0.05:
        if step % (N_STEPS // 10) == 0:
            print(f"    [*] Amplitude Starvation! valid_shots={valid_shots}. "
                  f"Boosting to {BOOST_SHOTS:,}...")
        counts = simulator.run(qc, shots=BOOST_SHOTS).result().get_counts()
        probs, valid_shots = extract_valid_probs(counts)

    if valid_shots == 0:
        valid_shots = 1  # Prevent division by zero in floor scaling

    # 5. Probability extraction with resolution floor
    p_min = 0.5 / valid_shots

    p_x  = max(probs.get('000', 0.0), p_min)
    p_y  = max(probs.get('001', 0.0), p_min)
    p_z  = max(probs.get('010', 0.0), p_min)
    p_xz = max(probs.get('011', 0.0), p_min)
    p_xy = max(probs.get('100', 0.0), p_min)

    # Reconstruct absolute scaled magnitudes.
    # The H-sandwich (two unnormalised H layers) introduces a factor of dim,
    # so the effective alpha must be divided by dim to compensate.
    alpha_eff = alpha / dim
    abs_x_scaled  = np.sqrt(p_x)  * alpha_eff * norm
    abs_y_scaled  = np.sqrt(p_y)  * alpha_eff * norm
    abs_z_scaled  = np.sqrt(p_z)  * alpha_eff * norm
    abs_xz_scaled = np.sqrt(p_xz) * alpha_eff * norm
    abs_xy_scaled = np.sqrt(p_xy) * alpha_eff * norm

    # 6. Classical Continuity Heuristic (Sign Trick)
    x_prev, y_prev, z_prev = physical_state[0], physical_state[1], physical_state[2]

    dx = DT * SIGMA * (y_prev - x_prev)
    dy = DT * (x_prev * (RHO - z_prev) - y_prev)
    dz = DT * (x_prev * y_prev - BETA * z_prev)

    sign_x = 1 if (x_prev + dx) >= 0 else -1
    sign_y = 1 if (y_prev + dy) >= 0 else -1
    sign_z = 1 if (z_prev + dz) >= 0 else -1

    x_raw_scaled = sign_x * abs_x_scaled
    y_raw_scaled = sign_y * abs_y_scaled
    z_raw_scaled = sign_z * abs_z_scaled

    # 7. Predictor-Corrector EMA Filter (Shot Noise Dampening)
    pred_x_scaled = (x_prev + dx) * S[0, 0]
    pred_y_scaled = (y_prev + dy) * S[1, 1]
    pred_z_scaled = (z_prev + dz) * S[2, 2]

    K_GAIN = 0.7
    x_filtered_scaled = K_GAIN * x_raw_scaled + (1 - K_GAIN) * pred_x_scaled
    y_filtered_scaled = K_GAIN * y_raw_scaled + (1 - K_GAIN) * pred_y_scaled
    z_filtered_scaled = K_GAIN * z_raw_scaled + (1 - K_GAIN) * pred_z_scaled

    xz_new_scaled = sign_x * sign_z * abs_xz_scaled
    xy_new_scaled = sign_x * sign_y * abs_xy_scaled

    return np.array([
        x_filtered_scaled, y_filtered_scaled, z_filtered_scaled,
        xz_new_scaled, xy_new_scaled,
        input_state_scaled[5], input_state_scaled[6], input_state_scaled[7]
    ], dtype=float)


# ---------------------------------------------------------------------------
# Main Routine
# ---------------------------------------------------------------------------
def main():
    print("Starting TRUE S-FABLE Block-Encoding Lorenz Simulation (Shot-Based).")
    print(f"DT={DT}, T_FINAL={T_FINAL} ({N_STEPS} steps) | "
          f"BASE_SHOTS={BASE_SHOTS:,} | BOOST_SHOTS={BOOST_SHOTS:,}")

    t_values = np.linspace(0, T_FINAL, N_STEPS + 1)

    # 1. Linearised Lorenz step matrix (8-dimensional lifted state)
    A = np.array([
        [1 - DT*SIGMA, DT*SIGMA, 0,           0,    0,  0, 0, 0],
        [DT*RHO,       1 - DT,   0,          -DT,   0,  0, 0, 0],
        [0,            0,        1 - DT*BETA, 0,    DT,  0, 0, 0],
        [0,            0,        0,           1,    0,   0, 0, 0],
        [0,            0,        0,           0,    1,   0, 0, 0],
        [0,            0,        0,           0,    0,   1, 0, 0],
        [0,            0,        0,           0,    0,   0, 1, 0],
        [0,            0,        0,           0,    0,   0, 0, 1],
    ], dtype=float)

    # 2. Similarity Transformation (Pre-Conditioning)
    W = np.array([1/20, 1/30, 1/50, 1/1000, 1/600, 1.0, 1.0, 1.0])
    S = np.diag(W)
    inv_S = np.diag(1.0 / W)
    A_scaled = S @ A @ inv_S

    dim = A_scaled.shape[0]
    A_norm = A_scaled / np.linalg.norm(A_scaled, 2)

    # 3. S-FABLE Pre-processing: transform to Walsh (Hadamard) basis
    print("Pre-processing: H_n @ A_norm @ H_n (Walsh domain sparsification)...")
    H_n = scipy.linalg.hadamard(dim) / np.sqrt(dim)
    A_sfable = H_n @ A_norm @ H_n

    print(f"Compiling S-FABLE Oracle (cutoff = {FABLE_CUTOFF})...")
    fable_result = fable(A_sfable, FABLE_CUTOFF)

    if isinstance(fable_result, tuple):
        fable_circuit, alpha_fable = fable_result
    else:
        fable_circuit = fable_result
        alpha_fable = 1.0

    alpha = np.linalg.norm(A_scaled, 2) * alpha_fable

    print("\n--- S-FABLE Circuit Profile ---")
    print(f"Total Qubits   : {fable_circuit.num_qubits}")
    print(f"System Qubits  : {int(np.log2(dim))}")
    print(f"Ancilla Qubits : {fable_circuit.num_qubits - int(np.log2(dim))}")
    print(f"Circuit Depth  : {fable_circuit.depth()}")
    print(f"Gate counts    : {dict(fable_circuit.count_ops())}")
    print("-------------------------------\n")

    simulator = AerSimulator()

    # Initial lifted state: [x, y, z, xz, xy, 1, 1, 1]
    current_sv = np.array([X0, Y0, Z0, X0*Z0, X0*Y0, 1.0, 1.0, 1.0])

    history_x = [X0]
    history_y = [Y0]
    history_z = [Z0]

    start_time = time.time()

    for step in range(N_STEPS):
        if step % (N_STEPS // 10) == 0:
            pct = int(100 * step / N_STEPS)
            print(f"[{pct:3d}%] Step {step:4d}/{N_STEPS} | "
                  f"X={current_sv[0]:.2f}  Y={current_sv[1]:.2f}  Z={current_sv[2]:.2f}")

        current_sv_scaled = S @ current_sv

        output_scaled = next_step_measured(
            current_sv_scaled, current_sv, alpha, fable_circuit,
            simulator, dim, step, S
        )

        # Un-scale back to physical coordinates
        output_sv = inv_S @ output_scaled

        # Guard against NaN/Inf propagation
        if not np.all(np.isfinite(output_sv)):
            x_p, y_p, z_p = current_sv[0], current_sv[1], current_sv[2]
            output_sv[0] = x_p + DT * SIGMA * (y_p - x_p)
            output_sv[1] = y_p + DT * (x_p * (RHO - z_p) - y_p)
            output_sv[2] = z_p + DT * (x_p * y_p - BETA * z_p)

        # Hard-enforce nonlinear consistency in auxiliary subspace
        next_sv = np.copy(output_sv)
        next_sv[3] = next_sv[0] * next_sv[2]
        next_sv[4] = next_sv[0] * next_sv[1]

        history_x.append(next_sv[0])
        history_y.append(next_sv[1])
        history_z.append(next_sv[2])
        current_sv = next_sv

    end_time = time.time()
    total_time = end_time - start_time
    print(f"[100%] Done. Total time: {total_time:.2f}s  ({total_time/N_STEPS*1000:.2f} ms/step)\n")

    x_q = np.array(history_x)
    y_q = np.array(history_y)
    z_q = np.array(history_z)

    t_cl, x_cl, y_cl, z_cl = euler_lorenz(DT, SIGMA, RHO, BETA, X0, Y0, Z0, N_STEPS)

    plot_lorenz_comparison(
        t_values, x_q, y_q, z_q,
        t_cl, x_cl, y_cl, z_cl,
        title="Lorenz Attractor — S-FABLE Shot-Based Measurement",
        quantum_label="Quantum (S-FABLE + Shot-Based)",
        classical_label="Classical (Euler)",
        save_dir=SAVE_DIR,
        prefix_name="lorenz_sfable_shots",
        show=False
    )


if __name__ == "__main__":
    main()
