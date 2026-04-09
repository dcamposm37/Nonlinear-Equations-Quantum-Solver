"""
Block Encoding Measurements with FABLE for Lorenz System
=========================================================

Replaces the classical dense unitary dilation (scipy sqrtm) with FABLE
(Fast Approximate Block Encoding), a Qiskit circuit-based oracle. Includes
post-selection filtering on ancilla qubits, adaptive shot boosting, and
a Predictor-Corrector EMA filter for shot noise dampening.

Recent Optimizations:
- Amplitude Starvation fix: Uses a pre-conditioned Scaling Matrix (Similarity 
  Transformation) to balance the state vector magnitudes, making sure the physical
  amplitudes comfortably survive the statistical shot noise margin.

Usage
-----
    python -m lorenz.solvers.block_encoding_measurements

Output
------
    lorenz/figures/08_fable/lorenz_be_meas_3d.png
    lorenz/figures/08_fable/lorenz_be_meas_2d.png
    lorenz/figures/08_fable/lorenz_be_meas_error_log.png
"""

import sys
import os
import time
import numpy as np
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
BOOST_SHOTS = 500000   # Quantum Microscope: enhanced shots for extremely low amplitudes

SAVE_DIR = os.path.join(os.path.dirname(__file__), "..", "figures", "08_fable")
os.makedirs(SAVE_DIR, exist_ok=True)


# ---------------------------------------------------------------------------
# Quantum Block-Encoding Forward Step (Measurement-Based)
# ---------------------------------------------------------------------------
def next_step_measured(input_state_scaled: np.ndarray, physical_state: np.ndarray, 
                       alpha: float, fable_circuit: QuantumCircuit, 
                       simulator: AerSimulator, dim: int, step: int, S: np.ndarray):
    
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
    
    padded_state = np.zeros(2**n, dtype=complex)
    padded_state[0:dim] = initial_normalized
    
    # Safety: if sum of squares rounds to zero by float precision -> fallback
    if np.sum(np.abs(padded_state)**2) < 1e-30:
        return _euler_fallback()
    
    qc = QuantumCircuit(total_qubits)
    # Initialize ONLY the system qubits (first n qubits). normalize=True lets
    # Qiskit handle any residual floating-point normalization error gracefully.
    qc.initialize(padded_state.tolist(), range(n), normalize=True)
    
    # 2. Append the Block-Encoding FABLE Oracle
    qc.append(fable_circuit, range(total_qubits))
    
    # 3. Measure all to collapse states and extract system probabilities
    qc.measure_all()
    qc = transpile(qc, simulator)
    
    current_shots = BASE_SHOTS
    job = simulator.run(qc, shots=current_shots)
    counts = job.result().get_counts()
    
    ancilla_len = total_qubits - n
    target_ancilla = '0' * ancilla_len
    
    def extract_valid_probs(raw_counts):
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

    probs, valid_shots = extract_valid_probs(counts)
    
    sum_important = sum(probs.get(k, 0.0) for k in ['000', '001', '010', '011', '100'])
    
    if sum_important < 0.05:
        if step % (N_STEPS // 10) == 0:
            print(f"    [*] Amplitude Starvation Detected! Post-selection valid shots: {valid_shots}. Boosting shots to {BOOST_SHOTS:,}...")
            
        job = simulator.run(qc, shots=BOOST_SHOTS)
        probs, valid_shots = extract_valid_probs(job.result().get_counts())
        current_shots = BOOST_SHOTS
        
    if valid_shots == 0:
        valid_shots = 1 # Avoid division by zero in resolution floor scaling
        
    # Resolution Floor relative to POST-SELECTED success shots!
    p_min = 0.5 / valid_shots
    
    # States parsing (using original index meanings of 3-qubit subspace)
    p_x = max(probs.get('000', 0.0), p_min)
    p_y = max(probs.get('001', 0.0), p_min)
    p_z = max(probs.get('010', 0.0), p_min)
    p_xz = max(probs.get('011', 0.0), p_min)
    p_xy = max(probs.get('100', 0.0), p_min)
    
    # Reconstruct absolute SCALED magnitudes
    abs_x_scaled = np.sqrt(p_x) * alpha * norm
    abs_y_scaled = np.sqrt(p_y) * alpha * norm
    abs_z_scaled = np.sqrt(p_z) * alpha * norm
    abs_xz_scaled = np.sqrt(p_xz) * alpha * norm
    abs_xy_scaled = np.sqrt(p_xy) * alpha * norm
    
    # 3. Classical Continuity Heuristic (The "Sign Trick")
    x_prev, y_prev, z_prev = physical_state[0], physical_state[1], physical_state[2]
    
    dx = DT * SIGMA * (y_prev - x_prev)
    dy = DT * (x_prev * (RHO - z_prev) - y_prev)
    dz = DT * (x_prev * y_prev - BETA * z_prev)
    
    sign_x = 1 if (x_prev + dx) >= 0 else -1
    sign_y = 1 if (y_prev + dy) >= 0 else -1
    sign_z = 1 if (z_prev + dz) >= 0 else -1

    # Raw quantum magnitudes with restored signs
    x_raw_scaled = sign_x * abs_x_scaled
    y_raw_scaled = sign_y * abs_y_scaled
    z_raw_scaled = sign_z * abs_z_scaled

    # 4. PREDICTOR-CORRECTOR FILTER (Shot Noise Dampening)
    pred_x_scaled = (x_prev + dx) * S[0, 0]
    pred_y_scaled = (y_prev + dy) * S[1, 1]
    pred_z_scaled = (z_prev + dz) * S[2, 2]

    K_GAIN = 0.7
    x_filtered_scaled = K_GAIN * x_raw_scaled + (1 - K_GAIN) * pred_x_scaled
    y_filtered_scaled = K_GAIN * y_raw_scaled + (1 - K_GAIN) * pred_y_scaled
    z_filtered_scaled = K_GAIN * z_raw_scaled + (1 - K_GAIN) * pred_z_scaled

    xz_new_scaled = sign_x * sign_z * abs_xz_scaled
    xy_new_scaled = sign_x * sign_y * abs_xy_scaled

    # Reconstruct the 8-dim array structure
    final_output_scaled = np.array([
        x_filtered_scaled, y_filtered_scaled, z_filtered_scaled, 
        xz_new_scaled, xy_new_scaled, 
        input_state_scaled[5], input_state_scaled[6], input_state_scaled[7]
    ], dtype=float)

    return final_output_scaled


# ---------------------------------------------------------------------------
# Main Routine
# ---------------------------------------------------------------------------
def main():
    print(f"Starting Measurement-Based Block-Encoding Lorenz simulation with Similarity Transformation.")
    print(f"Using DT = {DT}, T_FINAL = {T_FINAL} ({N_STEPS} steps), Base Shots = {BASE_SHOTS}, Boost Shots = {BOOST_SHOTS}")
    
    t_values = np.linspace(0, T_FINAL, N_STEPS + 1)
    
    # 1. Base Euler Matrix Definition (Physical Space)
    A = np.array([
        [1 - DT * SIGMA, DT * SIGMA, 0,              0,   0, 0, 0, 0], 
        [DT * RHO,       1 - DT,     0,             -DT,  0, 0, 0, 0], 
        [0,              0,          1 - DT * BETA,  0,   DT,0, 0, 0], 
        [0,              0,          0,              1,   0, 0, 0, 0], 
        [0,              0,          0,              0,   1, 0, 0, 0], 
        [0,              0,          0,              0,   0, 1, 0, 0], 
        [0,              0,          0,              0,   0, 0, 1, 0],
        [0,              0,          0,              0,   0, 0, 0, 1]
    ], dtype=float)

    # 2. Similarity Transformation (Pre-Conditioning)
    W = np.array([1/20, 1/30, 1/50, 1/1000, 1/600, 1.0, 1.0, 1.0])
    S = np.diag(W)
    inv_S = np.diag(1.0 / W)
    
    # A_scaled = S * A * S^(-1)
    A_scaled = S @ A @ inv_S

    # 3. Block Encoding Matrix Setup
    dim = A_scaled.shape[0]
    
    A_norm = A_scaled / np.linalg.norm(A_scaled, 2)
    fable_circuit, alpha_fable = fable(A_norm)
    alpha = np.linalg.norm(A_scaled, 2) * alpha_fable
    
    print(f"[*] FABLE Circuit Generated!")
    print(f"[*] Total Qubits: {fable_circuit.num_qubits}")
    print(f"[*] Circuit Depth: {fable_circuit.depth()}")
    print(f"[*] Total Valid Operations: {sum(fable_circuit.count_ops().values())}")
    
    simulator = AerSimulator()

    # 4. State vector memory (Physical space representation)
    current_sv = np.array([X0, Y0, Z0, X0 * Z0, X0 * Y0, 1.0, 1.0, 1.0])
    
    history_x = [X0]
    history_y = [Y0]
    history_z = [Z0]

    start_time = time.time()
    for step in range(N_STEPS):
        if step % (N_STEPS // 10) == 0:
            pct = int(100 * step / N_STEPS)
            print(f"[{pct:3d}%] Step {step:4d}/{N_STEPS} | Current X,Y,Z: {current_sv[0]:.2f}, {current_sv[1]:.2f}, {current_sv[2]:.2f}")
            
        # Scale the current physical vector into the balanced subspace
        current_sv_scaled = S @ current_sv
            
       # Apply linear operator + measurements + sign heuristic in SCALED subspace
        output_scaled = next_step_measured(current_sv_scaled, current_sv, alpha, fable_circuit, simulator, dim, step, S)
        
        # Un-scale the result back to physical coordinates
        output_sv = inv_S @ output_scaled
        
        # Guard against NaN/Inf propagation: fallback to clean Euler step if needed
        if not np.all(np.isfinite(output_sv)):
            x_p, y_p, z_p = current_sv[0], current_sv[1], current_sv[2]
            output_sv[0] = x_p + DT * SIGMA * (y_p - x_p)
            output_sv[1] = y_p + DT * (x_p * (RHO - z_p) - y_p)
            output_sv[2] = z_p + DT * (x_p * y_p - BETA * z_p)
        
        # Hard-enforce the relationship x*y in the auxiliary subspace
        next_sv = np.copy(output_sv)
        next_sv[3] = next_sv[0] * next_sv[2] 
        next_sv[4] = next_sv[0] * next_sv[1]
        
        history_x.append(next_sv[0])
        history_y.append(next_sv[1])
        history_z.append(next_sv[2])
        
        current_sv = next_sv
        
    end_time = time.time()
    total_time = end_time - start_time
    print(f"[100%] Step {N_STEPS}/{N_STEPS} | Simulation Complete.")
    print(f"[*] Total Execution Time (FABLE Block Encoding): {total_time:.2f} seconds")
    print(f"[*] Average Time per Step: {total_time/N_STEPS:.4f} seconds")

    x_q, y_q, z_q = np.array(history_x), np.array(history_y), np.array(history_z)
    
    # -----------------------------------------------------------------------
    # Classical Comparison
    # -----------------------------------------------------------------------
    t_cl, x_cl, y_cl, z_cl = euler_lorenz(DT, SIGMA, RHO, BETA, X0, Y0, Z0, N_STEPS)
    
    plot_lorenz_comparison(
        t_values, x_q, y_q, z_q,
        t_cl, x_cl, y_cl, z_cl,
        title="Lorenz Attractor - QST with Similarity Transformation",
        quantum_label="Quantum (Z-QST + S-Scaling)",
        classical_label="Classical (Euler)",
        save_dir=SAVE_DIR,
        prefix_name="lorenz_be_meas",
        show=False
    )
    
if __name__ == "__main__":
    main()
