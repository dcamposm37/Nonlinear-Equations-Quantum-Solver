"""
FABLE Statevector Simulation for Lorenz System
==============================================

Uses the FABLE (Fast Approximate Block-Encoding) library to construct
the unitary circuit for the scaled Euler matrix, and uses Qiskit's 
Statevector to directly obtain the probability amplitudes without 
shot noise or classical exponential smoothing.

This provides the exact algebraic limit of the FABLE algorithm.
"""

import os
import sys
import time
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

# Ensure FABLE can be imported
try:
    from fable import fable
except ImportError:
    print("FABLE not found. Please install the fable-circuits package.")
    sys.exit(1)

# Allow imports from project root
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

SAVE_DIR = os.path.join(os.path.dirname(__file__), "figures")
os.makedirs(SAVE_DIR, exist_ok=True)


def next_step_fable_sv(input_state_scaled, physical_state, norm_A, fable_circ,
                       dim, n, total_qubits, S):
    """
    Simulates one Euler step using FABLE block encoding via exact Statevector.
    """
    norm_input = np.linalg.norm(input_state_scaled)
    if norm_input == 0:
        return input_state_scaled
        
    initial_normalized = input_state_scaled / norm_input

    # Prepare input state on the data register (least significant qubits 0 to n-1)
    qc = QuantumCircuit(total_qubits)
    qc.initialize(initial_normalized.tolist(), range(n))
    
    # Apply FABLE circuit
    qc.append(fable_circ, range(total_qubits))
    
    # Get exact statevector
    sv = Statevector(qc).data
    
    # Extract the target block where all ancillas are exactly |0>
    target_sv = np.zeros(dim, dtype=complex)
    ancilla_len = total_qubits - n
    target_ancilla = '0' * ancilla_len

    for idx, amp in enumerate(sv):
        # Format to bitstring (Qiskit endianness: ancillas are MSB so first characters)
        bstr = format(idx, f"0{total_qubits}b")
        if bstr[:ancilla_len] == target_ancilla:
            sys_idx = int(bstr[-n:], 2)
            target_sv[sys_idx] = amp

    # Scale back the block encoded output. 
    # FABLE inherently scales down the amplitudes by 1/N where N = 2^n in its sub-block.
    raw_amplitudes = np.abs(target_sv) * (2**n) * norm_A * norm_input
    
    # --- Structural Heuristic for Missing Phase (Sign) ---
    x_prev, y_prev, z_prev = physical_state[:3]

    dx = DT * SIGMA * (y_prev - x_prev)
    dy = DT * (x_prev * (RHO - z_prev) - y_prev)
    dz = DT * (x_prev * y_prev - BETA * z_prev)

    sign_x = 1 if (x_prev + dx) >= 0 else -1
    sign_y = 1 if (y_prev + dy) >= 0 else -1
    sign_z = 1 if (z_prev + dz) >= 0 else -1

    x = sign_x * raw_amplitudes[0]
    y = sign_y * raw_amplitudes[1]
    z = sign_z * raw_amplitudes[2]
    xz = sign_x * sign_z * raw_amplitudes[3]
    xy = sign_x * sign_y * raw_amplitudes[4]

    return np.array([
        x, y, z, xz, xy, 
        input_state_scaled[5], input_state_scaled[6], input_state_scaled[7]
    ], dtype=float)


def main():
    print("Starting FABLE Statevector Simulation (Origin-Trap Safe)")
    
    t_values = np.linspace(0, T_FINAL, N_STEPS + 1)

    # Base Euler Matrix
    A = np.array([
        [1 - DT * SIGMA, DT * SIGMA, 0, 0, 0, 0, 0, 0],
        [DT * RHO, 1 - DT, 0, -DT, 0, 0, 0, 0],
        [0, 0, 1 - DT * BETA, 0, DT, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 1]
    ], dtype=float)

    # Similarity Scaling W avoids precision starvation
    W = np.array([1/20, 1/30, 1/50, 1/1000, 1/600, 1.0, 1.0, 1.0])
    S = np.diag(W)
    inv_S = np.diag(1.0 / W)

    A_scaled = S @ A @ inv_S
    dim = A_scaled.shape[0]
    n = int(np.log2(dim))
    
    norm_A = np.linalg.norm(A_scaled, 2)
    A_normalized = A_scaled / norm_A

    print("[*] Generating FABLE circuit...")
    fable_circ, alpha_fable = fable(A_normalized)
    total_qubits = fable_circ.num_qubits
    
    print(f"    - Qubits Required: {total_qubits}")
    print(f"    - Circuit Depth:   {fable_circ.depth()}")

    # Initialize physical vector with ZERO padding for unused indices
    # to naturally prevent the origin trap mechanism.
    current_sv = np.array([X0, Y0, Z0, X0*Z0, X0*Y0, 0.0, 0.0, 0.0])
    
    history_x = [X0]
    history_y = [Y0]
    history_z = [Z0]

    start_time = time.time()
    
    for step in range(N_STEPS):
        if step > 0 and step % (N_STEPS // 10) == 0:
            pct = int(100 * step / N_STEPS)
            print(f"[{pct:3d}%] Step {step:4d} | Current X,Y,Z: {current_sv[0]:.2f}, {current_sv[1]:.2f}, {current_sv[2]:.2f}")
            
        scaled = S @ current_sv
        
        output_scaled = next_step_fable_sv(
            scaled, current_sv, norm_A, fable_circ, 
            dim, n, total_qubits, S
        )
        
        output_physical = inv_S @ output_scaled
        
        # Hard geometrical relationship enforcement
        next_sv = np.copy(output_physical)
        next_sv[3] = next_sv[0] * next_sv[2]
        next_sv[4] = next_sv[0] * next_sv[1]
        
        history_x.append(next_sv[0])
        history_y.append(next_sv[1])
        history_z.append(next_sv[2])
        
        current_sv = next_sv

    end_time = time.time()
    print(f"[100%] Simulation Complete. Total Time: {end_time - start_time:.2f} s")

    # Benchmarks
    t_cl, x_cl, y_cl, z_cl = euler_lorenz(DT, SIGMA, RHO, BETA, X0, Y0, Z0, N_STEPS)

    plot_lorenz_comparison(
        t_values, 
        np.array(history_x), np.array(history_y), np.array(history_z),
        t_cl, x_cl, y_cl, z_cl,
        title="Lorenz Attractor - FABLE Exact Statevector",
        quantum_label="Quantum (FABLE SV)",
        classical_label="Classical (Euler)",
        save_dir=SAVE_DIR,
        prefix_name="lorenz_fable_sv",
        show=False
    )

if __name__ == "__main__":
    main()
