"""
Local S-FABLE methodology implemented with measurement-based (shot-based) extraction.
===========================================================================

S-FABLE operates by performing the standard FABLE block-encoding on the 
Hadamard-conjugated matrix: M = H^n * A * H^n.

This script executes pure Z-basis measurements. It mimics physical hardware execution,
handling statistical shot scaling, "Origin Trap" starvation, and dynamic sign
reconstruction using Eulerian inertia.
"""

import os
import sys
import time
import numpy as np
import scipy.linalg as la
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

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
SHOTS = 1000     # Default simulated hardware shots
FABLE_CUTOFF = 1e-4    # Sparse FABLE threshold cutoff

SAVE_DIR = os.path.join(os.path.dirname(__file__), "figures")
os.makedirs(SAVE_DIR, exist_ok=True)


def next_step_sfable_meas(input_state_scaled, physical_state, norm_A, sfable_circ, 
                        dim, n, total_qubits, S, simulator, step):

    norm_input = np.linalg.norm(input_state_scaled)
    if norm_input == 0:
        return input_state_scaled
        
    initial_normalized = input_state_scaled / norm_input

    # Prepare input state on the data register (least significant qubits 0 to n-1)
    qc = QuantumCircuit(total_qubits)
    qc.initialize(initial_normalized.tolist(), range(n))
    
    # Apply S-FABLE block encoding (using decomposed circuit inline)
    qc.compose(sfable_circ, inplace=True)
    
    # Measure
    qc.measure_all()

    # Determine state bitstrings
    ancilla_len = total_qubits - n
    str_ancilla = '0' * ancilla_len

    st_x = str_ancilla + format(0, f"0{n}b")
    st_y = str_ancilla + format(1, f"0{n}b")
    st_z = str_ancilla + format(2, f"0{n}b")
    st_xz = str_ancilla + format(3, f"0{n}b")
    st_xy = str_ancilla + format(4, f"0{n}b")

    current_shots = SHOTS
    result = simulator.run(qc, shots=current_shots).result()
    counts = result.get_counts()

    # Floor mitigation removed to avoid artificial scaling multiplier error
    p_min = 0.0
    p_x = max(counts.get(st_x, 0) / current_shots, p_min)
    p_y = max(counts.get(st_y, 0) / current_shots, p_min)
    p_z = max(counts.get(st_z, 0) / current_shots, p_min)
    
    hit_floor_x = (counts.get(st_x, 0) == 0)
    hit_floor_y = (counts.get(st_y, 0) == 0)
    hit_floor_z = (counts.get(st_z, 0) == 0)

    # Reconstruct un-signed amplitudes
    # Same scaling as logic proven in Statevector implementation
    scale_factor = (2**n) * norm_A * norm_input
    abs_x = np.sqrt(p_x) * scale_factor
    abs_y = np.sqrt(p_y) * scale_factor
    abs_z = np.sqrt(p_z) * scale_factor
    
    # Non-critical elements do not need floor boundaries explicitly
    p_xz = counts.get(st_xz, 0) / current_shots
    p_xy = counts.get(st_xy, 0) / current_shots
    abs_xz = np.sqrt(p_xz) * scale_factor
    abs_xy = np.sqrt(p_xy) * scale_factor

    # Heuristic constraint for Sign (+ / -) using Eulerian inertia
    x_prev, y_prev, z_prev = physical_state[:3]

    dx = DT * SIGMA * (y_prev - x_prev)
    dy = DT * (x_prev * (RHO - z_prev) - y_prev)
    dz = DT * (x_prev * y_prev - BETA * z_prev)

    sign_x = 1 if (x_prev + dx) >= 0 else -1
    sign_y = 1 if (y_prev + dy) >= 0 else -1
    sign_z = 1 if (z_prev + dz) >= 0 else -1

    sign_x_applied = (1 if x_prev >= 0 else -1) if hit_floor_x else sign_x
    sign_y_applied = (1 if y_prev >= 0 else -1) if hit_floor_y else sign_y
    sign_z_applied = (1 if z_prev >= 0 else -1) if hit_floor_z else sign_z

    x = sign_x_applied * abs_x
    y = sign_y_applied * abs_y
    z = sign_z_applied * abs_z
    xz = sign_x_applied * sign_z_applied * abs_xz
    xy = sign_x_applied * sign_y_applied * abs_xy

    return np.array([
        x, y, z, xz, xy, 
        input_state_scaled[5], input_state_scaled[6], input_state_scaled[7]
    ], dtype=float)


def build_sfable_circuit(A_normalized, n):
    """
    Constructs the S-FABLE circuit: (I x H^n) * FABLE(H^n * A * H^n) * (I x H^n)
    """
    N = 2**n
    
    # 1. Hadamard Transformation of Matrix A
    Hn = la.hadamard(N) / np.sqrt(N)
    M = Hn @ A_normalized @ Hn

    # 2. Block-encode the Walsh-domain matrix M via FABLE
    try:
        fable_circ, _ = fable(M, FABLE_CUTOFF)
    except TypeError:
        # Fallback if fable doesn't accept a cutoff argument easily
        fable_circ, _ = fable(M)
        
    total_qubits = fable_circ.num_qubits

    # 3. Form S-FABLE Circuit by wrapping with data-register Hadamards
    sfable_circ = QuantumCircuit(total_qubits, name="S-FABLE")
    sfable_circ.h(range(n))
    sfable_circ.append(fable_circ, range(total_qubits))
    sfable_circ.h(range(n))
    
    return sfable_circ, total_qubits


def main():
    print("Starting S-FABLE Measurements Simulation")
    print(f"Using Shots = {SHOTS}")
    
    t_values = np.linspace(0, T_FINAL, N_STEPS + 1)
    simulator = AerSimulator()

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
        
        output_scaled = next_step_sfable_meas(
            scaled, current_sv, norm_A, sfable_transpiled, 
            dim, n, total_qubits, S, simulator, step
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
        title="Lorenz Attractor - S-FABLE Measurements",
        quantum_label="Quantum (S-FABLE Meas)",
        classical_label="Classical (Euler)",
        save_dir=SAVE_DIR,
        prefix_name="lorenz_sfable_meas",
        show=False
    )

if __name__ == "__main__":
    main()
