"""
Block Encoding Statevector Simulation for Lorenz System
=======================================================

Solves the nonlinear Lorenz system using manual quantum block-encoding via
the `sqrtm` completion method. The algorithm isolates the linear operator 
step-by-step and treats the nonlinear $xy$ and $xz$ products as classically
updated auxiliary variables within the statevector.

Usage
-----
    python -m lorenz.solvers.block_encoding_statevector

Output
------
    lorenz/figures/lorenz_be_statevector_3d.png
    lorenz/figures/lorenz_be_statevector_2d.png
"""

import sys
import os
import numpy as np
import scipy.linalg
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.circuit.library import UnitaryGate
from scipy.linalg import sqrtm

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
T_FINAL = 50.0
N_STEPS = int(T_FINAL / DT)

SAVE_DIR = os.path.join(os.path.dirname(__file__), "..", "figures")


# ---------------------------------------------------------------------------
# Quantum Block-Encoding Forward Step
# ---------------------------------------------------------------------------
def next_step(A: np.ndarray, input_state: np.ndarray):
    """
    Applies the linear matrix A to the input_state via quantum block-encoding.
    """
    # 1. Validation and Setup
    dim = A.shape[0]
    num_qubits = int(np.log2(dim))
    if 2**num_qubits != dim:
        raise ValueError("Matrix dimension must be a power of 2.")
    
    norm = np.linalg.norm(input_state)
    if norm == 0:
        return input_state
    
    initial_normalized = input_state / norm
    
    # 2. Manual block-encoding (Szegedy-like / sqrtm approach)
    alpha = np.linalg.norm(A, 2)  # Spectral norm
    if alpha == 0:
        alpha = 1e-6
        
    A_norm = A / alpha
    I = np.eye(dim)
    
    # sqrtm might return small imaginary parts due to float precision
    term1 = scipy.linalg.sqrtm((I - A_norm @ A_norm.T).astype(complex))
    term2 = scipy.linalg.sqrtm((I - A_norm.T @ A_norm).astype(complex))
    
    # Block matrix U = [[A/a, .], [., -A^T/a]]
    U = np.block([
        [A_norm, term1],
        [term2, -A_norm.T]
    ])
    
    # 3. Quantum Circuit Definition
    total_qubits = num_qubits + 1  # 1 ancilla qubit for 2x2 block structure
    qc = QuantumCircuit(total_qubits)
    
    # State preparation: |0> \otimes |psi>
    padded_state = np.zeros(2**total_qubits, dtype=complex)
    padded_state[0:dim] = initial_normalized
    qc.initialize(padded_state.tolist(), range(total_qubits))
    
    # Apply unitary U
    qc.append(UnitaryGate(U), range(total_qubits))
    
    # 4. Statevector Simulation
    simulator = AerSimulator(method='statevector')
    qc = transpile(qc, simulator)
    qc.save_statevector()
    
    result = simulator.run(qc).result()
    state = result.get_statevector()
    
    # 5. Post-selection & Re-scaling (Ancilla=0)
    output_state = state.data[0:dim]
    final_state = np.real(output_state) * alpha * norm
    
    return final_state


# ---------------------------------------------------------------------------
# Main Routine
# ---------------------------------------------------------------------------
def main():
    print(f"Starting Block-Encoding Lorenz simulation with {N_STEPS} steps...")
    
    t_values = np.linspace(0, T_FINAL, N_STEPS + 1)
    
    # A Matrix definition corresponding to Euler discretization of Lorenz
    A = np.array([
        [1 - DT * SIGMA, DT * SIGMA, 0,              0,   0, 0, 0, 0],   # x_new
        [DT * RHO,       1 - DT,     0,             -DT,  0, 0, 0, 0],   # y_new (uses xz as 4th element)
        [0,              0,          1 - DT * BETA,  0,   DT,0, 0, 0],   # z_new (uses xy as 5th element)
        [0,              0,          0,              1,   0, 0, 0, 0],   # Dummy padded dimension
        [0,              0,          0,              0,   1, 0, 0, 0],   # Dummy padded dimension
        [0,              0,          0,              0,   0, 1, 0, 0],   # Identity for constants
        [0,              0,          0,              0,   0, 0, 1, 0],
        [0,              0,          0,              0,   0, 0, 0, 1]
    ], dtype=float)

    # State vector memory: [x, y, z, x*z, x*y, 1, 1, 1]
    current_sv = np.array([X0, Y0, Z0, X0 * Z0, X0 * Y0, 1.0, 1.0, 1.0])
    
    history_x = [X0]
    history_y = [Y0]
    history_z = [Z0]

    for step in range(N_STEPS):
        if step > 0 and step % (N_STEPS // 10) == 0:
            pct = int(100 * step / N_STEPS)
            print(f"[{pct:3d}%] Step {step:4d}/{N_STEPS} | Current X,Y,Z: {current_sv[0]:.2f}, {current_sv[1]:.2f}, {current_sv[2]:.2f}")
            
        # 1. Apply linear operator via quantum block-encoding
        output_sv = next_step(A, current_sv)
        
        # 2. Update non-linear tracking (Classical memory element)
        next_sv = np.copy(output_sv)
        next_sv[3] = next_sv[0] * next_sv[2]  # update x*z
        next_sv[4] = next_sv[0] * next_sv[1]  # update x*y
        
        # Store physical coordinates
        history_x.append(next_sv[0])
        history_y.append(next_sv[1])
        history_z.append(next_sv[2])
        
        # Step forward
        current_sv = next_sv
        
    print(f"[100%] Step {N_STEPS}/{N_STEPS} | Simulation Complete.")

    # Convert to arrays
    x_q, y_q, z_q = np.array(history_x), np.array(history_y), np.array(history_z)
    
    # -----------------------------------------------------------------------
    # Classical Comparison
    # -----------------------------------------------------------------------
    t_cl, x_cl, y_cl, z_cl = euler_lorenz(DT, SIGMA, RHO, BETA, X0, Y0, Z0, N_STEPS)
    
    # Plot results
    plot_lorenz_comparison(
        t_values, x_q, y_q, z_q,
        t_cl, x_cl, y_cl, z_cl,
        title="Lorenz Attractor - Block Encoding Statevector",
        quantum_label="Quantum (Block Enc)",
        classical_label="Classical (Euler)",
        save_dir=SAVE_DIR,
        prefix_name="lorenz_be_statevector",
        show=False
    )
    
if __name__ == "__main__":
    main()
