"""
Pauli-LCU Quantum Circuit -- Lorenz Attractor (Shot-Based Measurements)
=======================================================================

Same LCU block-encoding as pauli_lcu_statevector.py, but state extraction
is done via simulated hardware shots (AerSimulator) instead of exact
statevector amplitudes.

Protocol per time step:
    1. Prepare |psi_sys>|0_anc> in a QuantumCircuit (full Hilbert space init).
    2. Apply the precomputed LCU UnitaryGate.
    3. Measure ALL qubits (Z-basis) using SHOTS samples.
    4. Post-select on ancilla = |0...0> outcomes (system indices only).
    5. Reconstruct |amplitude_j|^2 from frequencies; restore signs via Euler predictor.
    6. Rescale by lambda * norm.

Because Lambda (LCU) = 1.706 << 2^n = 8, the post-selection success
probability is ~34%, versus ~1.6% for FABLE -- meaning 20x fewer shots wasted.

Usage
-----
    python -m lorenz.pauli_lcu.pauli_lcu_measurements

Output
------
    lorenz/pauli_lcu/figures/lorenz_pauli_lcu_meas_3d.png
    lorenz/pauli_lcu/figures/lorenz_pauli_lcu_meas_2d.png
    lorenz/pauli_lcu/figures/lorenz_pauli_lcu_meas_error_log.png
"""

import os
import sys
import time
import numpy as np

# -- Qiskit ----------------------------------------------------------------
from qiskit import QuantumCircuit
from qiskit.circuit.library import UnitaryGate
from qiskit_aer import AerSimulator

# -- Project imports -------------------------------------------------------
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from lorenz.classical import euler_lorenz
from lorenz.plot_results import plot_lorenz_comparison

# Reuse the analytical LCU builders from the statevector module
from lorenz.pauli_lcu.pauli_lcu_statevector import (
    pauli_decompose,
    build_lcu_unitary,
)

# ===========================================================================
# Parameters
# ===========================================================================
DT    = 0.01
SIGMA = 10.0
RHO   = 28.0
BETA  = 8.0 / 3.0

X0, Y0, Z0 = 1.0, 1.0, 1.0
T_FINAL = 10.0
N_STEPS = int(T_FINAL / DT)

SHOTS = 50_000   # Simulated hardware shots per step

SAVE_DIR = os.path.join(os.path.dirname(__file__), "figures")
os.makedirs(SAVE_DIR, exist_ok=True)


# ===========================================================================
# 1.  Shot-based LCU step  (mirrors block_encoding_measurements pattern)
# ===========================================================================
def apply_lcu_step_shots(input_state_scaled, physical_state, lam,
                         lcu_gate, dim, total_qubits, simulator, S):
    """
    Applies the LCU block-encoded gate to the SCALED vector, executes
    Z-basis measurements, and applies a classical continuity heuristic
    using the PHYSICAL vector to reconstruct signs.

    Parameters
    ----------
    input_state_scaled : ndarray (8,)  S @ physical_state
    physical_state     : ndarray (8,)  un-scaled (x,y,z,xz,xy,0,0,0)
    lam                : float         LCU normalization factor (replaces alpha)
    lcu_gate           : UnitaryGate   precomputed LCU circuit
    dim                : int           system dimension (8)
    total_qubits       : int           n_sys + n_anc
    simulator          : AerSimulator
    S                  : ndarray (8,8) similarity scaling matrix

    Returns
    -------
    output_scaled : ndarray (8,)  scaled output state
    """
    norm = np.linalg.norm(input_state_scaled)
    if norm == 0:
        return input_state_scaled

    initial_normalized = input_state_scaled / norm

    # State preparation: |0_garbage> |0_anc> |psi_sys>
    # System qubits are the FIRST `dim` entries of the full 2^total_qubits vector
    padded_state = np.zeros(2**total_qubits, dtype=complex)
    padded_state[0:dim] = initial_normalized

    qc = QuantumCircuit(total_qubits)
    qc.initialize(padded_state.tolist(), range(total_qubits))

    # Apply the LCU unitary
    qc.append(lcu_gate, range(total_qubits))

    # Measure all qubits in Z-basis
    qc.measure_all()

    # Execute
    result = simulator.run(qc, shots=SHOTS).result()
    counts = result.get_counts()

    # ---- Post-selection + amplitude reconstruction ----
    # Only outcomes where ancilla bits = 0 correspond to the physical subspace.
    # In the full bitstring, the system bits are the LOWEST n_sys bits.
    # Bitstring format (Qiskit): bit[total_qubits-1] ... bit[0]
    # We need ancilla bits (the upper bits) to all be zero.
    # For an 8-qubit circuit with 3 system + 5 ancilla:
    #   physical outcomes: '00000xxx'  where xxx are system bits
    n_sys = int(np.log2(dim))
    n_anc = total_qubits - n_sys

    # Min detectable probability (half a shot)
    p_min = 0.5 / SHOTS

    # Build the expected bitstring keys for system indices 0,1,2 (x,y,z)
    # System index j -> binary of j zero-padded to total_qubits bits
    def sys_bitstring(j):
        return format(j, f'0{total_qubits}b')

    p_x = max(counts.get(sys_bitstring(0), 0) / SHOTS, p_min)
    p_y = max(counts.get(sys_bitstring(1), 0) / SHOTS, p_min)
    p_z = max(counts.get(sys_bitstring(2), 0) / SHOTS, p_min)

    hit_floor_x = (counts.get(sys_bitstring(0), 0) == 0)
    hit_floor_y = (counts.get(sys_bitstring(1), 0) == 0)
    hit_floor_z = (counts.get(sys_bitstring(2), 0) == 0)

    # Reconstruct absolute SCALED magnitudes (lam replaces alpha)
    abs_x_scaled = np.sqrt(p_x) * lam * norm
    abs_y_scaled = np.sqrt(p_y) * lam * norm
    abs_z_scaled = np.sqrt(p_z) * lam * norm

    # Auxiliary terms
    p_xz = counts.get(sys_bitstring(3), 0) / SHOTS
    p_xy = counts.get(sys_bitstring(4), 0) / SHOTS
    abs_xz_scaled = np.sqrt(p_xz) * lam * norm
    abs_xy_scaled = np.sqrt(p_xy) * lam * norm

    # ---- Classical Continuity Heuristic (sign recovery) ----
    x_prev, y_prev, z_prev = physical_state[0], physical_state[1], physical_state[2]

    dx = DT * SIGMA * (y_prev - x_prev)
    dy = DT * (x_prev * (RHO - z_prev) - y_prev)
    dz = DT * (x_prev * y_prev - BETA * z_prev)

    sign_x = 1 if (x_prev + dx) >= 0 else -1
    sign_y = 1 if (y_prev + dy) >= 0 else -1
    sign_z = 1 if (z_prev + dz) >= 0 else -1

    # If amplitude hit the floor, preserve previous sign
    sign_x_applied = (1 if x_prev >= 0 else -1) if hit_floor_x else sign_x
    sign_y_applied = (1 if y_prev >= 0 else -1) if hit_floor_y else sign_y
    sign_z_applied = (1 if z_prev >= 0 else -1) if hit_floor_z else sign_z

    x_filtered_scaled = sign_x_applied * abs_x_scaled
    y_filtered_scaled = sign_y_applied * abs_y_scaled
    z_filtered_scaled = sign_z_applied * abs_z_scaled

    xz_new_scaled = sign_x * sign_z * abs_xz_scaled
    xy_new_scaled = sign_x * sign_y * abs_xy_scaled

    final_output_scaled = np.array([
        x_filtered_scaled, y_filtered_scaled, z_filtered_scaled,
        xz_new_scaled, xy_new_scaled,
        input_state_scaled[5], input_state_scaled[6], input_state_scaled[7]
    ], dtype=float)

    return final_output_scaled


# ===========================================================================
# 2.  Main
# ===========================================================================
def main():
    print("=" * 62)
    print("  Pauli-LCU Quantum Circuit -- Lorenz Attractor (Shots)")
    print("=" * 62)
    print(f"  dt = {DT},  T = {T_FINAL},  steps = {N_STEPS},  shots = {SHOTS:,}\n")

    t_values = np.linspace(0, T_FINAL, N_STEPS + 1)

    # -- 1. Euler step matrix ----------------------------------------------
    A = np.array([
        [1 - DT*SIGMA,  DT*SIGMA,  0,             0,   0, 0, 0, 0],
        [DT*RHO,        1 - DT,    0,            -DT,   0, 0, 0, 0],
        [0,             0,         1 - DT*BETA,   0,   DT, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 1],
    ], dtype=float)

    # -- 2. Similarity scaling --------------------------------------------
    W     = np.array([1/20, 1/30, 1/50, 1/1000, 1/600, 1.0, 1.0, 1.0])
    S     = np.diag(W)
    inv_S = np.diag(1.0 / W)
    A_scaled = S @ A @ inv_S

    # -- 3. Pauli decomposition -------------------------------------------
    t0 = time.perf_counter()
    coeffs, pauli_ops, labels = pauli_decompose(A_scaled)
    t_decomp = time.perf_counter() - t0

    n_sys = 3
    lam   = float(np.sum(np.abs(coeffs)))

    print(f"  Pauli terms     : {len(coeffs)} non-zero  ({t_decomp*1e3:.1f} ms)")
    print(f"  Lambda (LCU)    = {lam:.4f}")
    print(f"  P(success/step) ~ {1/lam**2*100:.1f}%  "
          f"(vs FABLE: {1/(2**n_sys)**2*100:.1f}%)\n")

    # -- 4. Build LCU unitary + gate (precomputed once) -------------------
    t0 = time.perf_counter()
    lcu_unitary, n_anc, lam = build_lcu_unitary(coeffs, pauli_ops, 8)
    t_build = time.perf_counter() - t0
    total_qubits = n_anc + n_sys
    dim = 2 ** n_sys   # 8

    print(f"  LCU matrix built: {lcu_unitary.shape[0]}x{lcu_unitary.shape[1]}  "
          f"({t_build*1e3:.1f} ms)")
    print(f"  Ancilla qubits  : {n_anc}")
    print(f"  System  qubits  : {n_sys}")
    print(f"  Total   qubits  : {total_qubits}\n")

    # Gate is reused every step
    lcu_gate  = UnitaryGate(lcu_unitary, label="Pauli_LCU")
    simulator = AerSimulator()

    # -- 5. Time-stepping loop --------------------------------------------
    current_sv = np.array(
        [X0, Y0, Z0, X0 * Z0, X0 * Y0, 0.0, 0.0, 0.0], dtype=float
    )
    hx, hy, hz = [X0], [Y0], [Z0]

    print(f"  Running {N_STEPS} steps (AerSimulator, {SHOTS:,} shots/step) ...")
    t0 = time.perf_counter()

    for step in range(N_STEPS):
        current_sv_scaled = S @ current_sv

        output_scaled = apply_lcu_step_shots(
            current_sv_scaled, current_sv, lam,
            lcu_gate, dim, total_qubits, simulator, S
        )

        output_sv = inv_S @ output_scaled

        # Algebraically enforce auxiliary quadratic constraints
        output_sv[3] = output_sv[0] * output_sv[2]    # xz
        output_sv[4] = output_sv[0] * output_sv[1]    # xy

        hx.append(output_sv[0])
        hy.append(output_sv[1])
        hz.append(output_sv[2])

        current_sv = output_sv

        if step > 0 and step % (N_STEPS // 10) == 0:
            pct = 100 * step // N_STEPS
            print(f"  [{pct:3d}%]  step {step:4d}  |  "
                  f"x = {current_sv[0]:+9.4f}   "
                  f"y = {current_sv[1]:+9.4f}   "
                  f"z = {current_sv[2]:+9.4f}")

    t_sim = time.perf_counter() - t0
    print(f"\n  [100%]  Done -- {t_sim:.1f} s  ({t_sim/N_STEPS*1e3:.1f} ms/step)\n")

    # -- 6. Classical reference and plots ----------------------------------
    x_q, y_q, z_q = np.array(hx), np.array(hy), np.array(hz)
    t_cl, x_cl, y_cl, z_cl = euler_lorenz(
        DT, SIGMA, RHO, BETA, X0, Y0, Z0, N_STEPS
    )

    plot_lorenz_comparison(
        t_values, x_q, y_q, z_q,
        t_cl, x_cl, y_cl, z_cl,
        title="Lorenz Attractor -- Pauli-LCU (Shot-Based)",
        quantum_label=f"Quantum (Pauli-LCU, {SHOTS:,} shots)",
        classical_label="Classical (Euler)",
        save_dir=SAVE_DIR,
        prefix_name="lorenz_pauli_lcu_meas",
        show=False,
    )


if __name__ == "__main__":
    main()
