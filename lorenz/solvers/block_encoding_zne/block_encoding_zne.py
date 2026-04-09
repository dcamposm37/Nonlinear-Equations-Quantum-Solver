import sys
import os
import time
import numpy as np
import scipy.linalg
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.circuit.library import UnitaryGate
from qiskit_aer.noise import NoiseModel, depolarizing_error

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
BASE_SHOTS = 20000     # Reduced hardware shots for ZNE performance comparison
P_ERROR = 0.0001       # Physical unitary gate error (Disabled in Phase 1)

SAVE_DIR = os.path.join(os.path.dirname(__file__), "..", "figures")


# ---------------------------------------------------------------------------
# Quantum Block-Encoding Forward Step (ZNE Mitigated)
# ---------------------------------------------------------------------------
def next_step_zne(input_state_scaled: np.ndarray, physical_state: np.ndarray, 
                  alpha: float, U_gate: UnitaryGate, 
                  simulator: AerSimulator, dim: int, total_qubits: int, 
                  step: int, noise_model: NoiseModel):
    """
    Applies the unitary block-encoded gate with physical noise using ZNE.
    Evaluates at noise scales lambda = 1 and lambda = 3 via unitary folding.
    Uses Richardson extrapolation to reconstruct ideal probabilities.
    """
    norm = np.linalg.norm(input_state_scaled)
    if norm == 0:
        return input_state_scaled
    
    initial_normalized = input_state_scaled / norm
    
    # State preparation: |0> \otimes |psi>
    padded_state = np.zeros(2**total_qubits, dtype=complex)
    padded_state[0:dim] = initial_normalized
    
    # --- Lambda = 1 Circuit (Normal U) ---
    qc1 = QuantumCircuit(total_qubits)
    qc1.initialize(padded_state.tolist(), range(total_qubits))
    qc1.append(U_gate, range(total_qubits))
    qc1.measure_all()
    
    # --- Lambda = 3 Circuit (U_dagger U U -> conceptually)
    # Folds the unitary effectively tripling the gate time and its noise.
    qc3 = QuantumCircuit(total_qubits)
    qc3.initialize(padded_state.tolist(), range(total_qubits))
    qc3.append(U_gate, range(total_qubits))
    qc3.append(U_gate.inverse(), range(total_qubits))
    qc3.append(U_gate, range(total_qubits))
    qc3.measure_all()
    
    # Run with Noise Model (Phase 2: Calibrated Device Noise)
    # Both circuits are executed sequentially simulating physical extraction time
    result1 = simulator.run(qc1, shots=BASE_SHOTS, noise_model=noise_model).result()
    counts1 = result1.get_counts()
    
    result3 = simulator.run(qc3, shots=BASE_SHOTS, noise_model=noise_model).result()
    counts3 = result3.get_counts()
    
    # ------------------------------------------------------------------------
    # ZNE: Richardson Extrapolation & The Origin Trap Mitigation
    # ------------------------------------------------------------------------
    p_min = 0.5 / BASE_SHOTS
    
    # Extract raw noisy probabilities
    p_x1 = counts1.get('0000', 0) / BASE_SHOTS
    p_y1 = counts1.get('0001', 0) / BASE_SHOTS
    p_z1 = counts1.get('0010', 0) / BASE_SHOTS
    
    p_x3 = counts3.get('0000', 0) / BASE_SHOTS
    p_y3 = counts3.get('0001', 0) / BASE_SHOTS
    p_z3 = counts3.get('0010', 0) / BASE_SHOTS
    
    p_xz1 = counts1.get('0011', 0) / BASE_SHOTS
    p_xy1 = counts1.get('0100', 0) / BASE_SHOTS
    p_xz3 = counts3.get('0011', 0) / BASE_SHOTS
    p_xy3 = counts3.get('0100', 0) / BASE_SHOTS
    
    # Exponential Richardson Extrapolation: P_ideal = P1 * sqrt(P1 / P3)
    def exp_extrapolate(p1, p3):
        if p3 > 0 and p1 >= p3:
            p_ideal = p1 * np.sqrt(p1 / p3)
        else:
            p_ideal = p1  # Si la estadística se invierte o P3 muere, confiamos en P1
        return min(p_ideal, 1.0) # Clip superior
    
    p_x_ideal = exp_extrapolate(p_x1, p_x3)
    p_y_ideal = exp_extrapolate(p_y1, p_y3)
    p_z_ideal = exp_extrapolate(p_z1, p_z3)
    p_xz_ideal = exp_extrapolate(p_xz1, p_xz3)
    p_xy_ideal = exp_extrapolate(p_xy1, p_xy3)
    
    # Check if idealized probability effectively hit structural floor
    hit_floor_x = (p_x_ideal == 0.0)
    hit_floor_y = (p_y_ideal == 0.0)
    hit_floor_z = (p_z_ideal == 0.0)
    
    # Enforce topological floor to prevent Origin Trap divergence
    p_x_safe = max(p_x_ideal, p_min)
    p_y_safe = max(p_y_ideal, p_min)
    p_z_safe = max(p_z_ideal, p_min)

    # Reconstruct absolute SCALED magnitudes
    abs_x_scaled = np.sqrt(p_x_safe) * alpha * norm
    abs_y_scaled = np.sqrt(p_y_safe) * alpha * norm
    abs_z_scaled = np.sqrt(p_z_safe) * alpha * norm
    
    abs_xz_scaled = np.sqrt(p_xz_ideal) * alpha * norm
    abs_xy_scaled = np.sqrt(p_xy_ideal) * alpha * norm
    
    # 3. Classical Continuity Heuristic (The "Sign Trick")
    x_prev, y_prev, z_prev = physical_state[0], physical_state[1], physical_state[2]
    
    dx = DT * SIGMA * (y_prev - x_prev)
    dy = DT * (x_prev * (RHO - z_prev) - y_prev)
    dz = DT * (x_prev * y_prev - BETA * z_prev)
    
    sign_x = 1 if (x_prev + dx) >= 0 else -1
    sign_y = 1 if (y_prev + dy) >= 0 else -1
    sign_z = 1 if (z_prev + dz) >= 0 else -1

    # Topological Inertia Conservation
    sign_x_applied = (1 if x_prev >= 0 else -1) if hit_floor_x else sign_x
    sign_y_applied = (1 if y_prev >= 0 else -1) if hit_floor_y else sign_y
    sign_z_applied = (1 if z_prev >= 0 else -1) if hit_floor_z else sign_z

    # Apply signs to scaled amplitudes
    x_new_scaled = sign_x_applied * abs_x_scaled
    y_new_scaled = sign_y_applied * abs_y_scaled
    z_new_scaled = sign_z_applied * abs_z_scaled
    
    xz_new_scaled = sign_x * sign_z * abs_xz_scaled
    xy_new_scaled = sign_x * sign_y * abs_xy_scaled

    # Reconstruct the 8-dim array structure
    final_output_scaled = np.array([
        x_new_scaled, y_new_scaled, z_new_scaled, xz_new_scaled, xy_new_scaled, 
        input_state_scaled[5], input_state_scaled[6], input_state_scaled[7]
    ], dtype=float)

    return final_output_scaled


# ---------------------------------------------------------------------------
# Main Routine
# ---------------------------------------------------------------------------
def main():
    print(f"Starting QST Lorenz ZNE Simulation with Similarity Transformation.")
    print(f"Using DT = {DT}, T_FINAL = {T_FINAL} ({N_STEPS} steps), Shots = {BASE_SHOTS}")
    
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
    
    print(f"Adding Global Depolarizing Error Model (p_error = {P_ERROR}) to U_gate...")
    noise_model = NoiseModel()
    error_q = depolarizing_error(P_ERROR, total_qubits)
    # Target all unitaries specifically
    noise_model.add_all_qubit_quantum_error(error_q, ['unitary'])

    # 4. State vector memory
    current_sv = np.array([X0, Y0, Z0, X0 * Z0, X0 * Y0, 1.0, 1.0, 1.0])
    
    history_x = [X0]
    history_y = [Y0]
    history_z = [Z0]

    start_time = time.time()

    for step in range(N_STEPS):
        if step > 0 and step % (N_STEPS // 10) == 0:
            pct = int(100 * step / N_STEPS)
            print(f"[{pct:3d}%] Step {step:4d}/{N_STEPS} | Current X,Y,Z: {current_sv[0]:.2f}, {current_sv[1]:.2f}, {current_sv[2]:.2f}")
            
        current_sv_scaled = S @ current_sv
            
        # Execute ZNE routine
        output_scaled = next_step_zne(current_sv_scaled, current_sv, alpha, U_gate, simulator, dim, total_qubits, step, noise_model)
        
        output_sv = inv_S @ output_scaled
        
        next_sv = np.copy(output_sv)
        next_sv[3] = next_sv[0] * next_sv[2] 
        next_sv[4] = next_sv[0] * next_sv[1]
        
        history_x.append(next_sv[0])
        history_y.append(next_sv[1])
        history_z.append(next_sv[2])
        
        current_sv = next_sv
        
    end_time = time.time()
    total_sec = end_time - start_time
    print(f"[100%] Step {N_STEPS}/{N_STEPS} | Simulation Complete.")
    print(f"[*] Total Execution Time with ZNE: {total_sec:.2f} seconds")

    x_q, y_q, z_q = np.array(history_x), np.array(history_y), np.array(history_z)
    
    # -----------------------------------------------------------------------
    # Classical Comparison
    # -----------------------------------------------------------------------
    t_cl, x_cl, y_cl, z_cl = euler_lorenz(DT, SIGMA, RHO, BETA, X0, Y0, Z0, N_STEPS)
    
    plot_lorenz_comparison(
        t_values, x_q, y_q, z_q,
        t_cl, x_cl, y_cl, z_cl,
        title="Lorenz ZNE Phase 2: Exponential Mitigation (Device Noise)",
        quantum_label="Quantum ZNE Exp (p=0.0001)",
        classical_label="Classical (Euler)",
        save_dir=SAVE_DIR,
        prefix_name="lorenz_be_zne_exp",
        show=False
    )
    
if __name__ == "__main__":
    main()
