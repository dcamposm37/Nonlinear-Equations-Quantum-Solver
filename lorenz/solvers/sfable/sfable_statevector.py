"""
Local S-FABLE methodology implemented with analytical Statevector extraction.
===========================================================================

S-FABLE operates by performing the standard FABLE block-encoding on the 
Hadamard-conjugated matrix: M = H^n * A * H^n.
Since Lorenz and many sparse systems exhibit high sparsity in the Walsh-Hadamard 
basis, FABLE effectively compresses M better than A. The physical state is 
recovered by bounding the circuit with H^n on the target register.

This script uses Statevector to directly compute the probabilities (noise-free).
"""

import os
import sys
import time
import numpy as np
import scipy.linalg as la
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

try:
    from fable import fable
except ImportError:
    print("FABLE not found. Please install the fable-circuits package.")
    sys.exit(1)

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

SAVE_DIR = os.path.join(os.path.dirname(__file__), "..", "figures", "11_sfable_sv")
os.makedirs(SAVE_DIR, exist_ok=True)


def next_step_sfable_sv(input_state_scaled, physical_state, norm_A, sfable_circ, 
                        dim, n, total_qubits, S):

    norm_input = np.linalg.norm(input_state_scaled)
    if norm_input == 0:
        return input_state_scaled
        
    initial_normalized = input_state_scaled / norm_input

    # Prepare input state on the data register (least significant qubits 0 to n-1)
    qc = QuantumCircuit(total_qubits)
    qc.initialize(initial_normalized.tolist(), range(n))
    
    # Apply S-FABLE block encoding
    qc.append(sfable_circ, range(total_qubits))
    
    # Retrieve algebraic Statevector
    sv = Statevector(qc).data
    
    # Extract target block where ancillas = 0
    target_sv = np.zeros(dim, dtype=complex)
    ancilla_len = total_qubits - n
    target_ancilla = '0' * ancilla_len

    for idx, amp in enumerate(sv):
        bstr = format(idx, f"0{total_qubits}b")
        if bstr[:ancilla_len] == target_ancilla:
            sys_idx = int(bstr[-n:], 2)
            target_sv[sys_idx] = amp

    # Scale back the block encoded output (SFABLE preserves the 1/N internal FABLE scaling)
    raw_amplitudes = np.abs(target_sv) * (2**n) * norm_A * norm_input
    
    # Heuristic constraint for Sign (+ / -) using Eulerian inertia
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


def build_sfable_circuit(A_normalized, n):
    """
    Constructs the S-FABLE circuit: (I x H^n) * FABLE(H^n * A * H^n) * (I x H^n)
    using the installed 'fable' library.
    """
    N = 2**n
    
    # 1. Hadamard Transformation of Matrix A
    # Qiskit's Hadamard over n qubits equals scipy's normalized hadamard
    Hn = la.hadamard(N) / np.sqrt(N)
    M = Hn @ A_normalized @ Hn

    # 2. Block-encode the Walsh-domain matrix M via FABLE
    # Compression threshold cutoff = 1e-4 targets sparse un-rotatable elements
    try:
        fable_circ, alpha_m = fable(M, 1e-4)
    except TypeError:
        # Fallback if fable doesn't accept a cutoff argument easily
        fable_circ, alpha_m = fable(M)
        
    total_qubits = fable_circ.num_qubits

    # 3. Form S-FABLE Circuit by wrapping with data-register Hadamards
    sfable_circ = QuantumCircuit(total_qubits, name="S-FABLE")
    sfable_circ.h(range(n))
    sfable_circ.append(fable_circ, range(total_qubits))
    sfable_circ.h(range(n))
    
    return sfable_circ, total_qubits


def main():
    print("Starting S-FABLE Statevector Simulation (Origin-Trap Safe)")
    
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
    ], dtype=float)

    W = np.array([1/20, 1/30, 1/50, 1/1000, 1/600, 1.0, 1.0, 1.0])
    S = np.diag(W)
    inv_S = np.diag(1.0 / W)

    A_scaled = S @ A @ inv_S
    dim = A_scaled.shape[0]
    n = int(np.log2(dim))
    
    norm_A = np.linalg.norm(A_scaled, 2)
    A_normalized = A_scaled / norm_A

    print("[*] Generating S-FABLE circuit...")
    
    sfable_circ, total_qubits = build_sfable_circuit(A_normalized, n)
    sfable_transpiled = sfable_circ.decompose()
    
    print(f"    - Qubits Required: {total_qubits}")
    print(f"    - Circuit Depth:   {sfable_transpiled.depth()}")

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
        
        output_scaled = next_step_sfable_sv(
            scaled, current_sv, norm_A, sfable_circ, 
            dim, n, total_qubits, S
        )
        
        output_physical = inv_S @ output_scaled
        
        next_sv = np.copy(output_physical)
        next_sv[3] = next_sv[0] * next_sv[2]
        next_sv[4] = next_sv[0] * next_sv[1]
        
        history_x.append(next_sv[0])
        history_y.append(next_sv[1])
        history_z.append(next_sv[2])
        
        current_sv = next_sv

    end_time = time.time()
    print(f"[100%] Simulation Complete. Total Time: {end_time - start_time:.2f} s")

    t_cl, x_cl, y_cl, z_cl = euler_lorenz(DT, SIGMA, RHO, BETA, X0, Y0, Z0, N_STEPS)

    plot_lorenz_comparison(
        t_values, 
        np.array(history_x), np.array(history_y), np.array(history_z),
        t_cl, x_cl, y_cl, z_cl,
        title="Lorenz Attractor - S-FABLE Exact Statevector",
        quantum_label="Quantum (S-FABLE SV)",
        classical_label="Classical (Euler)",
        save_dir=SAVE_DIR,
        prefix_name="lorenz_sfable_sv",
        show=False
    )

if __name__ == "__main__":
    main()
