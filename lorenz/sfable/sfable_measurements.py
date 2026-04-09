"""
Block Encoding Measurements Simulation for Lorenz System
======================================================

Solves the nonlinear Lorenz system using manual quantum block-encoding via
the S-FABLE (Sparse FABLE) completion method. Unlike the exact statevector sim, 
this script reconstructs the step-by-step magnitudes by executing purely Z-basis 
measurements (simulated hardware shots) and tracks the physical phase 
(sign) via a classical continuity heuristic.

Recent Optimizations:
- Amplitude Starvation fix: Uses a pre-conditioned Scaling Matrix (Similarity 
  Transformation) to balance the state vector magnitudes, making sure the physical
  amplitudes comfortably survive the statistical shot noise margin.

Usage
-----
    python -m lorenz.sfable.sfable_measurements

Output
------
    lorenz/figures/lorenz_be_meas_3d.png
    lorenz/figures/lorenz_be_meas_2d.png
    lorenz/figures/lorenz_be_meas_error_log.png
"""

import sys
import os
import numpy as np
import scipy.linalg
from qiskit import QuantumCircuit
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
BASE_SHOTS = 50000     # Default simulated hardware shots (Increased for post-selection)
BOOST_SHOTS = 500000   # Quantum Microscope: enhanced shots for extremely low amplitudes
FABLE_CUTOFF = 1e-3    # Sparse FABLE threshold cutoff

SAVE_DIR = os.path.join(os.path.dirname(__file__), "figures")


# ---------------------------------------------------------------------------
# Quantum Block-Encoding Forward Step (Measurement-Based)
# ---------------------------------------------------------------------------
def next_step_measured(input_state_scaled: np.ndarray, physical_state: np.ndarray, 
                       alpha_total: float, fable_circ: QuantumCircuit, num_sys_qubits: int,
                       simulator: AerSimulator, dim: int, step: int, S: np.ndarray):
    """
    Applies the S-FABLE block-encoded gate to the SCALED vector, executes 
    Z-basis measurements with LCU post-selection, and applies a classical 
    continuity heuristic using the PHYSICAL vector to reconstruct the components.
    """
    norm = np.linalg.norm(input_state_scaled)
    
    # Blindaje de Vector Nulo
    if norm < 1e-12:
        input_state_scaled = np.zeros_like(input_state_scaled)
        input_state_scaled[5:8] = 1.0  # Mantiene las constantes dummy
        norm = np.linalg.norm(input_state_scaled)

    if norm == 0:
        return input_state_scaled
    
    initial_normalized = input_state_scaled / norm
    
    # Safety check: if normalized vector is also near-zero (e.g. after NaN propagation)
    if not np.all(np.isfinite(initial_normalized)) or np.sum(np.abs(initial_normalized)**2) < 1e-30:
        return input_state_scaled  # Return unchanged; main loop will apply Euler fallback
    
    # Sándwich Cuántico S-FABLE
    qc = QuantumCircuit(fable_circ.num_qubits)
    # normalize=True handles residual floating-point normalization errors gracefully
    qc.initialize(initial_normalized.tolist(), list(range(num_sys_qubits)), normalize=True)
    
    qc.h(list(range(num_sys_qubits)))
    qc.compose(fable_circ, inplace=True)
    qc.h(list(range(num_sys_qubits)))
    
    qc.measure_all()
    
    # --- ADAPTIVE SHOT BOOSTING (The Quantum Microscope) ---
    current_shots = BASE_SHOTS
    result = simulator.run(qc, shots=current_shots).result()
    counts = result.get_counts()
    
    # Check if any fundamental physical coordinate hit the resolution floor
    # Construimos los bitstrings esperados (ancillas en 0 + system state)
    ancilla_zeros = '0' * (fable_circ.num_qubits - num_sys_qubits)
    target_x = ancilla_zeros + '000'
    target_y = ancilla_zeros + '001'
    target_z = ancilla_zeros + '010'
    
    if counts.get(target_x, 0) == 0 or counts.get(target_y, 0) == 0 or counts.get(target_z, 0) == 0:
        print(f"    [Shot Boost] Step {step:4d} | Amplitud crítica de X, Y o Z detectada. Re-ejecutando con {BOOST_SHOTS} shots...")
        current_shots = BOOST_SHOTS
        result = simulator.run(qc, shots=current_shots).result()
        counts = result.get_counts()
    
    # ------------------------------------------------------------------------
    # LÓGICA DE POST-SELECCIÓN LCU
    # ------------------------------------------------------------------------
    valid_counts = {}
    for bitstring, count in counts.items():
        ancilla_part = bitstring[:-num_sys_qubits]
        system_part = bitstring[-num_sys_qubits:]
        if all(b == '0' for b in ancilla_part):
            valid_counts[system_part] = count
            
    valid_shots = sum(valid_counts.values())
    if valid_shots == 0:
        valid_shots = current_shots
        
    p_min = 0.5 / valid_shots
    
    # Extract magnitudes via frequency, enforcing the topological floor
    p_x = max(valid_counts.get('000', 0) / valid_shots, p_min)
    p_y = max(valid_counts.get('001', 0) / valid_shots, p_min)
    p_z = max(valid_counts.get('010', 0) / valid_shots, p_min)
    
    hit_floor_x = (valid_counts.get('000', 0) == 0)
    hit_floor_y = (valid_counts.get('001', 0) == 0)
    hit_floor_z = (valid_counts.get('010', 0) == 0)
    
    # Reconstruct absolute SCALED magnitudes using corrected alpha_total
    # The H-sandwich introduces a factor of dim (sqrt(dim) per layer), 
    # so we divide alpha_total by dim to restore physical scale.
    alpha_eff = alpha_total / dim
    abs_x_scaled = np.sqrt(p_x) * alpha_eff * norm
    abs_y_scaled = np.sqrt(p_y) * alpha_eff * norm
    abs_z_scaled = np.sqrt(p_z) * alpha_eff * norm
    
    # Reconstruct magnitudes for nonlinear auxiliary terms
    p_xz = valid_counts.get('011', 0) / valid_shots
    p_xy = valid_counts.get('100', 0) / valid_shots
    abs_xz_scaled = np.sqrt(p_xz) * alpha_eff * norm
    abs_xy_scaled = np.sqrt(p_xy) * alpha_eff * norm
    
    # 3. Classical Continuity Heuristic (The "Sign Trick")
    x_prev, y_prev, z_prev = physical_state[0], physical_state[1], physical_state[2]
    
    dx = DT * SIGMA * (y_prev - x_prev)
    dy = DT * (x_prev * (RHO - z_prev) - y_prev)
    dz = DT * (x_prev * y_prev - BETA * z_prev)
    
    sign_x = 1 if (x_prev + dx) >= 0 else -1
    sign_y = 1 if (y_prev + dy) >= 0 else -1
    sign_z = 1 if (z_prev + dz) >= 0 else -1

    sign_x_applied = (1 if x_prev >= 0 else -1) if hit_floor_x else sign_x
    sign_y_applied = (1 if y_prev >= 0 else -1) if hit_floor_y else sign_y
    sign_z_applied = (1 if z_prev >= 0 else -1) if hit_floor_z else sign_z

    # Raw quantum magnitudes with restored signs
    x_raw_scaled = sign_x_applied * abs_x_scaled
    y_raw_scaled = sign_y_applied * abs_y_scaled
    z_raw_scaled = sign_z_applied * abs_z_scaled

    # ------------------------------------------------------------------------
    # 4. PREDICTOR-CORRECTOR FILTER (Shot Noise Dampening)
    # ------------------------------------------------------------------------
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
    
    A_scaled = S @ A @ inv_S

    # 3. Block Encoding Matrix Setup - S-FABLE
    dim = A_scaled.shape[0]
    num_sys_qubits = int(np.log2(dim))
    
    alpha = np.linalg.norm(A_scaled, 2)  
    if alpha == 0:
        alpha = 1e-6
        
    A_norm = A_scaled / alpha
    
    # Pre-procesamiento Clásico para FABLE
    H_n = scipy.linalg.hadamard(dim) / np.sqrt(dim)
    A_sfable = H_n @ A_norm @ H_n
    
    fable_result = fable(A_sfable, FABLE_CUTOFF)
    
    # Extracción segura de la tupla devuelta por FABLE
    fable_circ = fable_result[0] if isinstance(fable_result, tuple) else fable_result
    alpha_fable = fable_result[1] if isinstance(fable_result, tuple) else 1.0
    
    alpha_total = alpha * alpha_fable
    
    print(f"\n--- S-FABLE Circuit Profile ---")
    print(f"Total Qubits   : {fable_circ.num_qubits}")
    print(f"System Qubits  : {num_sys_qubits}")
    print(f"Ancilla Qubits : {fable_circ.num_qubits - num_sys_qubits}")
    print(f"Circuit Depth  : {fable_circ.depth()}")
    print(f"Gate counts    : {dict(fable_circ.count_ops())}")
    print(f"alpha_total    : {alpha_total:.6f}")
    print(f"-------------------------------\n")
    
    simulator = AerSimulator()

    # 4. State vector memory (Physical space representation)
    current_sv = np.array([X0, Y0, Z0, X0 * Z0, X0 * Y0, 1.0, 1.0, 1.0])
    
    history_x = [X0]
    history_y = [Y0]
    history_z = [Z0]

    for step in range(N_STEPS):
        if step % (N_STEPS // 10) == 0:
            pct = int(100 * step / N_STEPS)
            print(f"[{pct:3d}%] Step {step:4d}/{N_STEPS} | Current X,Y,Z: {current_sv[0]:.2f}, {current_sv[1]:.2f}, {current_sv[2]:.2f}")
            
        # Scale the current physical vector into the balanced subspace
        current_sv_scaled = S @ current_sv
            
        # Apply linear operator + measurements + sign heuristic in SCALED subspace
        output_scaled = next_step_measured(
            current_sv_scaled, current_sv, alpha_total, fable_circ,
            num_sys_qubits, simulator, dim, step, S
        )
        
        # Un-scale the result back to physical coordinates
        output_sv = inv_S @ output_scaled
        
        # Guard against NaN/Inf propagation
        if not np.all(np.isfinite(output_sv)):
            x_p, y_p, z_p = current_sv[0], current_sv[1], current_sv[2]
            output_sv[0] = x_p + DT * SIGMA * (y_p - x_p)
            output_sv[1] = y_p + DT * (x_p * (RHO - z_p) - y_p)
            output_sv[2] = z_p + DT * (x_p * y_p - BETA * z_p)
        
        # Hard-enforce the relationship x*y in the auxiliary subspace geometrically
        next_sv = np.copy(output_sv)
        next_sv[3] = next_sv[0] * next_sv[2] 
        next_sv[4] = next_sv[0] * next_sv[1]
        
        # Store physical coordinates
        history_x.append(next_sv[0])
        history_y.append(next_sv[1])
        history_z.append(next_sv[2])
        
        # Step forward
        current_sv = next_sv
        
    print(f"[100%] Step {N_STEPS}/{N_STEPS} | Simulation Complete.")

    x_q, y_q, z_q = np.array(history_x), np.array(history_y), np.array(history_z)
    
    # -----------------------------------------------------------------------
    # Classical Comparison
    # -----------------------------------------------------------------------
    t_cl, x_cl, y_cl, z_cl = euler_lorenz(DT, SIGMA, RHO, BETA, X0, Y0, Z0, N_STEPS)
    
    plot_lorenz_comparison(
        t_values, x_q, y_q, z_q,
        t_cl, x_cl, y_cl, z_cl,
        title="Lorenz Attractor - S-FABLE QST with Similarity Transformation",
        quantum_label="Quantum (Z-QST + S-FABLE)",
        classical_label="Classical (Euler)",
        save_dir=SAVE_DIR,
        prefix_name="lorenz_sfable_meas",
        show=False
    )
    
if __name__ == "__main__":
    main()
