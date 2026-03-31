import sys
import os
import time
import numpy as np
import scipy.linalg
from qiskit import QuantumCircuit
from qiskit.circuit.library import UnitaryGate, StatePreparation
from qiskit.quantum_info import Statevector

# Allow imports from project root
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from lorenz.classical import euler_lorenz
from lorenz.plot_results import plot_lorenz_comparison

# ---------------------------------------------------------------------------
# Parameters (IQAE POC)
# ---------------------------------------------------------------------------
DT = 0.01              # Step size (h)
SIGMA = 10.0           # Prandtl number
RHO = 28.0             # Rayleigh number
BETA = 8.0 / 3.0       # Physical proportion

X0, Y0, Z0 = 1.0, 1.0, 1.0
T_FINAL = 10.0
N_STEPS = int(T_FINAL / DT)

SAVE_DIR = os.path.join(os.path.dirname(__file__), "..", "figures", "06_iqae")
os.makedirs(SAVE_DIR, exist_ok=True)

# ---------------------------------------------------------------------------
# Quantum Block-Encoding Forward Step (IQAE)
# ---------------------------------------------------------------------------
def next_step_iqae(input_state_scaled: np.ndarray, physical_state: np.ndarray, 
                   alpha: float, U_gate: UnitaryGate, 
                   dim: int, total_qubits: int, step: int):
    """
    Extracts underlying probabilities using Iterative Quantum Amplitude Estimation
    instead of raw hardware shots, effectively eliminating stochastic sample noise.
    """
    norm = np.linalg.norm(input_state_scaled)
    if norm == 0:
        return input_state_scaled
    
    initial_normalized = input_state_scaled / norm
    
    # State preparation: |0> \otimes |psi>
    padded_state = np.zeros(2**total_qubits, dtype=complex)
    padded_state[0:dim] = initial_normalized
    
    # Base circuit for state preparation (A)
    # The A circuit simply initializes and applies U, no measurement
    A = QuantumCircuit(total_qubits)
    A.append(StatePreparation(padded_state.tolist()), range(total_qubits))
    A.append(U_gate, range(total_qubits))

    # Extract exact probabilities simulating infinite-precision Fault-Tolerant IQAE
    sv = Statevector(A)
    probs = sv.probabilities_dict()
    
    p_x = probs.get('0000', 0.0)
    p_y = probs.get('0001', 0.0)
    p_z = probs.get('0010', 0.0)
    p_xz = probs.get('0011', 0.0)
    p_xy = probs.get('0100', 0.0)
    
    # Analytical Resource Estimation (1% relative error on Amplitude)
    def estimate_oracle_calls(p_val):
        if p_val <= 0.0:
            return 0
        amp = np.sqrt(p_val)
        epsilon_target = 0.01 * amp  # 1% relative error
        # Formula: N_oracle ~ pi / (4 * epsilon_target)
        n_oracle = np.pi / (4.0 * epsilon_target)
        return int(n_oracle)

    queries_x = estimate_oracle_calls(p_x)
    queries_y = estimate_oracle_calls(p_y)
    queries_z = estimate_oracle_calls(p_z)
    queries_xz = estimate_oracle_calls(p_xz)
    queries_xy = estimate_oracle_calls(p_xy)
    
    total_queries = queries_x + queries_y + queries_z + queries_xz + queries_xy
    if step % (1000 // 10) == 0:
        print(f"    [IQAE Resource Est.] Step {step:4d} | Consultas de Oraculo teoricas (1% error relativo): {total_queries}")
    
    # Reconstruct absolute SCALED magnitudes
    abs_x_scaled = np.sqrt(max(p_x, 0)) * alpha * norm
    abs_y_scaled = np.sqrt(max(p_y, 0)) * alpha * norm
    abs_z_scaled = np.sqrt(max(p_z, 0)) * alpha * norm
    abs_xz_scaled = np.sqrt(max(p_xz, 0)) * alpha * norm
    abs_xy_scaled = np.sqrt(max(p_xy, 0)) * alpha * norm
    
    # 3. Classical Continuity Heuristic (The "Sign Trick")
    x_prev, y_prev, z_prev = physical_state[0], physical_state[1], physical_state[2]
    
    dx = DT * SIGMA * (y_prev - x_prev)
    dy = DT * (x_prev * (RHO - z_prev) - y_prev)
    dz = DT * (x_prev * y_prev - BETA * z_prev)
    
    sign_x = 1 if (x_prev + dx) >= 0 else -1
    sign_y = 1 if (y_prev + dy) >= 0 else -1
    sign_z = 1 if (z_prev + dz) >= 0 else -1

    # Apply signs to scaled amplitudes
    x_new_scaled = sign_x * abs_x_scaled
    y_new_scaled = sign_y * abs_y_scaled
    z_new_scaled = sign_z * abs_z_scaled
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
    print(f"Starting QST Lorenz IQAE Simulation (Fault-Tolerant Proof-of-Concept)")
    print(f"Using DT = {DT}, T_FINAL = {T_FINAL} ({N_STEPS} steps)")
    
    t_values = np.linspace(0, T_FINAL, N_STEPS + 1)
    
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

    # Similarity Transformation
    W = np.array([1/20, 1/30, 1/50, 1/1000, 1/600, 1.0, 1.0, 1.0])
    S = np.diag(W)
    inv_S = np.diag(1.0 / W)
    
    A_scaled = S @ A @ inv_S

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

    current_sv = np.array([X0, Y0, Z0, X0 * Z0, X0 * Y0, 1.0, 1.0, 1.0])
    history_x = [X0]
    history_y = [Y0]
    history_z = [Z0]

    start_time = time.time()

    for step in range(N_STEPS):
        pct = int(100 * step / N_STEPS)
        print(f"[{pct:3d}%] Step {step:4d}/{N_STEPS} | Current X,Y,Z: {current_sv[0]:.2f}, {current_sv[1]:.2f}, {current_sv[2]:.2f}")
        
        current_sv_scaled = S @ current_sv
        
        output_scaled = next_step_iqae(current_sv_scaled, current_sv, alpha, U_gate, dim, total_qubits, step)
        
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
    print(f"[*] Total Execution Time with IQAE: {total_sec:.2f} seconds")

    x_q, y_q, z_q = np.array(history_x), np.array(history_y), np.array(history_z)
    
    # Classical Comparison
    t_cl, x_cl, y_cl, z_cl = euler_lorenz(DT, SIGMA, RHO, BETA, X0, Y0, Z0, N_STEPS)
    
    plot_lorenz_comparison(
        t_values, x_q, y_q, z_q,
        t_cl, x_cl, y_cl, z_cl,
        title="Lorenz Attractor - IQAE Fault-Tolerant POC",
        quantum_label="Quantum IQAE",
        classical_label="Classical (Euler)",
        save_dir=SAVE_DIR,
        prefix_name="lorenz_be_iqae",
        show=False
    )
    
if __name__ == "__main__":
    main()
