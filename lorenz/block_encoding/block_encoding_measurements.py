"""
Block Encoding Measurements Simulation for Lorenz System
======================================================

Solves the nonlinear Lorenz system using manual quantum block-encoding via
the `sqrtm` completion method. Unlike the exact statevector sim, this script 
reconstructs the step-by-step magnitudes by executing purely Z-basis 
measurements (simulated hardware shots) and tracks the physical phase 
(sign) via a classical continuity heuristic.

Recent Optimizations:
- Amplitude Starvation fix: Uses a pre-conditioned Scaling Matrix (Similarity 
  Transformation) to balance the state vector magnitudes, making sure the physical
  amplitudes comfortably survive the statistical shot noise margin.

Usage
-----
    python -m lorenz.block_encoding.block_encoding_measurements

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
from qiskit.circuit.library import UnitaryGate

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
SHOTS = 20000     # Default simulated hardware shots

SAVE_DIR = os.path.join(os.path.dirname(__file__), "figures")


# ---------------------------------------------------------------------------
# Quantum Block-Encoding Forward Step (Measurement-Based)
# ---------------------------------------------------------------------------
def next_step_measured(input_state_scaled: np.ndarray, physical_state: np.ndarray, 
                       alpha: float, U_gate: UnitaryGate, 
                       simulator: AerSimulator, dim: int, total_qubits: int, step: int, S: np.ndarray):
    """
    Applies the unitary block-encoded gate to the SCALED vector, executes 
    Z-basis measurements, and applies a classical continuity heuristic using 
    the PHYSICAL vector to reconstruct the signed SCALED vector components.
    """
    norm = np.linalg.norm(input_state_scaled)
    if norm == 0:
        return input_state_scaled
    
    initial_normalized = input_state_scaled / norm
    
    # State preparation: |0> \otimes |psi>
    padded_state = np.zeros(2**total_qubits, dtype=complex)
    padded_state[0:dim] = initial_normalized
    
    qc = QuantumCircuit(total_qubits)
    qc.initialize(padded_state.tolist(), range(total_qubits))
    
    # Apply unitary U
    qc.append(U_gate, range(total_qubits))
    
    # Measure all qubits in the Z basis
    qc.measure_all()
    
    current_shots = SHOTS
    result = simulator.run(qc, shots=current_shots).result()
    counts = result.get_counts()
    
    # ------------------------------------------------------------------------
    # THE "ORIGIN TRAP" MITIGATION: QST Resolution Limit (Hard-Thresholding)
    # ------------------------------------------------------------------------
    # Calculate the minimum physical detectable probability (half a shot)
    p_min = 0.5 / current_shots
    
    # Extract magnitudes via frequency, enforcing the topological floor
    p_x = max(counts.get('0000', 0) / current_shots, p_min)
    p_y = max(counts.get('0001', 0) / current_shots, p_min)
    p_z = max(counts.get('0010', 0) / current_shots, p_min)
    
    # Check if we hit the hardware resolution floor even after potential boost
    hit_floor_x = (counts.get('0000', 0) == 0)
    hit_floor_y = (counts.get('0001', 0) == 0)
    hit_floor_z = (counts.get('0010', 0) == 0)
    
    # Reconstruct absolute SCALED magnitudes
    abs_x_scaled = np.sqrt(p_x) * alpha * norm
    abs_y_scaled = np.sqrt(p_y) * alpha * norm
    abs_z_scaled = np.sqrt(p_z) * alpha * norm
    
    # Reconstruct magnitudes for nonlinear auxiliary terms (can stay naturally 0)
    p_xz = counts.get('0011', 0) / current_shots
    p_xy = counts.get('0100', 0) / current_shots
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

    sign_x_applied = (1 if x_prev >= 0 else -1) if hit_floor_x else sign_x
    sign_y_applied = (1 if y_prev >= 0 else -1) if hit_floor_y else sign_y
    sign_z_applied = (1 if z_prev >= 0 else -1) if hit_floor_z else sign_z

    # Raw quantum magnitudes with restored signs
    x_raw_scaled = sign_x_applied * abs_x_scaled
    y_raw_scaled = sign_y_applied * abs_y_scaled
    z_raw_scaled = sign_z_applied * abs_z_scaled

    # 4. PREDICTOR-CORRECTOR FILTER (Shot Noise Dampening)
    # ELIMINADO para evitar condicionamiento clásico. El estado natural cuántico evita
    # el 'Origin Trap' al no diluir probabilidad en variables constantes de relleno.

    x_filtered_scaled = x_raw_scaled
    y_filtered_scaled = y_raw_scaled
    z_filtered_scaled = z_raw_scaled

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
    print(f"Using DT = {DT}, T_FINAL = {T_FINAL} ({N_STEPS} steps), Shots = {SHOTS}")
    
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
    # Weights target mapping variables that can grow to O(10) or O(100) down towards O(1)
    W = np.array([1/20, 1/30, 1/50, 1/1000, 1/600, 1.0, 1.0, 1.0])
    S = np.diag(W)
    inv_S = np.diag(1.0 / W)
    
    # A_scaled = S * A * S^(-1)
    A_scaled = S @ A @ inv_S

    # 3. Block Encoding Matrix Setup
    dim = A_scaled.shape[0]
    num_qubits = int(np.log2(dim))
    total_qubits = num_qubits + 1  
    
    alpha = np.linalg.norm(A_scaled, 2)  
    if alpha == 0:
        alpha = 1e-6
        
    A_norm = A_scaled / alpha
    I = np.eye(dim)
    
    term1 = np.real(scipy.linalg.sqrtm((I - A_norm @ A_norm.T).astype(complex)))
    term2 = np.real(scipy.linalg.sqrtm((I - A_norm.T @ A_norm).astype(complex)))
    
    U = np.block([
        [A_norm, term1],
        [term2, -A_norm.T]
    ])
    
    U_gate = UnitaryGate(U)
    simulator = AerSimulator()

    # 4. State vector memory (Physical space representation)
    current_sv = np.array([X0, Y0, Z0, X0 * Z0, X0 * Y0, 0.0, 0.0, 0.0])
    
    history_x = [X0]
    history_y = [Y0]
    history_z = [Z0]

    for step in range(N_STEPS):
        if step > 0 and step % (N_STEPS // 10) == 0:
            pct = int(100 * step / N_STEPS)
            print(f"[{pct:3d}%] Step {step:4d}/{N_STEPS} | Current X,Y,Z: {current_sv[0]:.2f}, {current_sv[1]:.2f}, {current_sv[2]:.2f}")
            
        # Scale the current physical vector into the balanced subspace
        current_sv_scaled = S @ current_sv
            
       # Apply linear operator + measurements + sign heuristic in SCALED subspace
        output_scaled = next_step_measured(current_sv_scaled, current_sv, alpha, U_gate, simulator, dim, total_qubits, step, S)
        
        # Un-scale the result back to physical coordinates
        output_sv = inv_S @ output_scaled
        
        # Hard-enforce the relationship x*y in the auxiliary subspace geometrically
        # to prevent compounding independent statistical jitter.
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
        title="Lorenz Attractor - QST with Similarity Transformation",
        quantum_label="Quantum (Z-QST + S-Scaling)",
        classical_label="Classical (Euler)",
        save_dir=SAVE_DIR,
        prefix_name="lorenz_be_meas",
        show=False
    )
    
if __name__ == "__main__":
    main()
