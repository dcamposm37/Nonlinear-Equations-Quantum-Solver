"""
Pauli-LCU Quantum Circuit — Lorenz Attractor (Statevector)
==========================================================

Solves the nonlinear Lorenz system using a genuine quantum circuit
based on the Linear Combination of Unitaries (LCU) protocol.

The Euler step matrix A is decomposed into the Pauli basis:
    A = Σ_j  c_j P_j          (every P_j is a native quantum gate)
    λ = Σ_j |c_j|             (LCU normalization — replaces FABLE's 2^n)

The block-encoding circuit U_LCU has the structure:

    |0_anc⟩ ─── PREP ──── SELECT ──── PREP† ─── measure ⟨0|
    |ψ_sys⟩ ─── ───── ──── P_j's ──── ───── ─── output

    ⟨0_anc| U_LCU |0_anc⟩  =  A / λ

The circuit's unitary is built analytically (Householder PREP +
controlled-Pauli SELECT) and wrapped as a Qiskit UnitaryGate /
Operator.  Each Euler step is executed via Statevector.evolve(Operator),
which IS quantum statevector simulation — identical to AerSimulator
in statevector mode, but without per-step transpilation overhead.
"""

import os
import sys
import time
import numpy as np

# ── Qiskit quantum-information framework ──────────────────────────────────
from qiskit import QuantumCircuit
from qiskit.quantum_info import Operator, Statevector
from qiskit.circuit.library import UnitaryGate

# ── Project imports ───────────────────────────────────────────────────────
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from lorenz.classical import euler_lorenz
from lorenz.plot_results import plot_lorenz_comparison

# ═══════════════════════════════════════════════════════════════════════════
# Physical & Numerical Parameters
# ═══════════════════════════════════════════════════════════════════════════
DT    = 0.01
SIGMA = 10.0
RHO   = 28.0
BETA  = 8.0 / 3.0

X0, Y0, Z0 = 1.0, 1.0, 1.0
T_FINAL = 10.0
N_STEPS = int(T_FINAL / DT)

SAVE_DIR = os.path.join(os.path.dirname(__file__), "figures")
os.makedirs(SAVE_DIR, exist_ok=True)


# ═══════════════════════════════════════════════════════════════════════════
# 1.  Pauli Basis  (pure numpy — zero Qiskit overhead)
# ═══════════════════════════════════════════════════════════════════════════
_I = np.eye(2, dtype=complex)
_X = np.array([[0, 1], [1, 0]], dtype=complex)
_Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
_Z = np.array([[1, 0], [0, -1]], dtype=complex)
_PAULIS_1Q = [_I, _X, _Y, _Z]
_LABELS_1Q = ["I", "X", "Y", "Z"]


def _pauli_basis(n_qubits):
    """Generate all 4^n  n-qubit Pauli matrices and label strings."""
    if n_qubits == 1:
        return list(_PAULIS_1Q), list(_LABELS_1Q)
    sub_mats, sub_labs = _pauli_basis(n_qubits - 1)
    mats, labs = [], []
    for p, pl in zip(_PAULIS_1Q, _LABELS_1Q):
        for sm, sl in zip(sub_mats, sub_labs):
            mats.append(np.kron(p, sm))
            labs.append(pl + sl)
    return mats, labs


def pauli_decompose(A):
    """
    Exact Pauli decomposition:  A = Σ_j c_j P_j,   c_j = Tr(P_j · A) / 2^n.
    Returns only non-zero terms.
    """
    dim = A.shape[0]
    n_q = int(np.log2(dim))
    basis, labels = _pauli_basis(n_q)

    coeffs, ops, labs = [], [], []
    for P, lab in zip(basis, labels):
        c = np.trace(P @ A) / dim
        if np.abs(c) > 1e-15:
            coeffs.append(c)
            ops.append(P)
            labs.append(lab)
    return np.array(coeffs), ops, labs


# ═══════════════════════════════════════════════════════════════════════════
# 2.  LCU Block-Encoding Unitary Construction
# ═══════════════════════════════════════════════════════════════════════════
def _householder_prep(target):
    """
    Householder unitary U such that  U |0⟩ = |target⟩.
    |target⟩ must be a unit vector.  U is Hermitian and unitary.
    """
    n = len(target)
    e0 = np.zeros(n, dtype=complex)
    e0[0] = 1.0

    if np.abs(np.vdot(target, e0) - 1.0) < 1e-14:
        return np.eye(n, dtype=complex)

    v = e0 - target
    v_norm_sq = np.vdot(v, v)
    if np.abs(v_norm_sq) < 1e-30:
        return np.eye(n, dtype=complex)

    return np.eye(n, dtype=complex) - 2.0 * np.outer(v, v.conj()) / v_norm_sq


def build_lcu_unitary(coeffs, pauli_ops, dim):
    """
    Build the full unitary LCU block-encoding matrix.

    Convention:  kron(ancilla_space, system_space)
        index = ancilla_state · D  +  system_state

    The ancilla-0 sub-block satisfies:
        U_LCU[:D, :D]  ≈  A / λ

    Returns
    -------
    lcu_unitary : ndarray  (M·D × M·D),  guaranteed unitary
    n_anc       : int       number of ancilla qubits
    lam         : float     the λ scaling factor
    """
    m   = len(coeffs)
    lam = float(np.sum(np.abs(coeffs)))

    n_anc = int(np.ceil(np.log2(max(m, 2))))
    M     = 2 ** n_anc                     # ancilla Hilbert-space dimension

    # ── PREP:  U_prep |0⟩ = Σ_j  sqrt(|c_j| / λ)  |j⟩  ─────────────────
    prep_vec = np.zeros(M, dtype=complex)
    for j in range(m):
        prep_vec[j] = np.sqrt(np.abs(coeffs[j]) / lam)

    PREP      = _householder_prep(prep_vec)
    PREP_full = np.kron(PREP, np.eye(dim))          # (M·D) × (M·D)

    # ── SELECT = Σ_j  e^{iφ_j} |j⟩⟨j| ⊗ P_j   +  I-padding  ────────────
    total  = M * dim
    SELECT = np.zeros((total, total), dtype=complex)

    for j in range(m):
        proj       = np.zeros((M, M), dtype=complex)
        proj[j, j] = 1.0
        phase      = np.exp(1j * np.angle(coeffs[j]))
        SELECT    += np.kron(proj, phase * pauli_ops[j])

    for j in range(m, M):                           # identity for unused
        proj       = np.zeros((M, M), dtype=complex)
        proj[j, j] = 1.0
        SELECT    += np.kron(proj, np.eye(dim))

    # ── U_LCU = PREP† · SELECT · PREP  ───────────────────────────────────
    lcu = PREP_full.conj().T @ SELECT @ PREP_full

    return lcu, n_anc, lam


# ═══════════════════════════════════════════════════════════════════════════
# 3.  Single Euler Time-Step via Quantum Circuit
# ═══════════════════════════════════════════════════════════════════════════
def apply_lcu_step(state_scaled, lcu_op, n_anc, n_sys, lam):
    """
    One time-step of the Lorenz system via the LCU quantum circuit.

    1. Normalise the input → |ψ⟩
    2. Embed into |ψ⟩|0_anc⟩  (full Hilbert space)
    3. Evolve through the LCU circuit   (Statevector.evolve)
    4. Project onto ancilla = |0⟩
    5. Rescale by λ · ‖input‖

    Returns  A · state_scaled   (un-normalised physical state).
    """
    norm = np.linalg.norm(state_scaled)
    if norm < 1e-30:
        return state_scaled

    psi = state_scaled / norm
    D   = 2 ** n_sys
    M   = 2 ** n_anc

    # Embed  |ψ⟩ ⊗ |0_anc⟩   →   first D entries of the full vector
    full_state      = np.zeros(M * D, dtype=complex)
    full_state[:D]  = psi

    # ── Quantum evolution ─────────────────────────────────────────────────
    sv_in  = Statevector(full_state)
    sv_out = sv_in.evolve(lcu_op)           # ← this IS the circuit execution

    # ── Post-select ancilla = |0⟩  (first D amplitudes) ──────────────────
    result = sv_out.data[:D]

    return np.real(result) * lam * norm


# ═══════════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════════
def main():
    print("=" * 62)
    print("  Pauli-LCU Quantum Circuit — Lorenz Attractor")
    print("=" * 62)
    print(f"  dt = {DT},  T = {T_FINAL},  steps = {N_STEPS}\n")

    t_values = np.linspace(0, T_FINAL, N_STEPS + 1)

    # ── 1. Euler step matrix  (v_{k+1} = A · v_k) ────────────────────────
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

    # ── 2. Similarity scaling  ────────────────────────────────────────────
    W     = np.array([1/20, 1/30, 1/50, 1/1000, 1/600, 1.0, 1.0, 1.0])
    S     = np.diag(W)
    inv_S = np.diag(1.0 / W)
    A_scaled = S @ A @ inv_S

    # ── 3. Pauli decomposition ────────────────────────────────────────────
    t0 = time.perf_counter()
    coeffs, pauli_ops, labels = pauli_decompose(A_scaled)
    t_decomp = time.perf_counter() - t0

    n_sys = 3
    lam   = float(np.sum(np.abs(coeffs)))

    print(f"  Pauli terms     : {len(coeffs)} non-zero  ({t_decomp*1e3:.1f} ms)")
    print(f"  Lambda (LCU)    = {lam:.4f}")
    print(f"  2^n (FABLE)     = {2**n_sys}")
    print(f"  Advantage ratio ~ {2**n_sys / lam:.1f}x\n")

    # ── 4. Build LCU quantum unitary ──────────────────────────────────────
    t0 = time.perf_counter()
    lcu_unitary, n_anc, lam = build_lcu_unitary(coeffs, pauli_ops, 8)
    t_build = time.perf_counter() - t0

    total_qubits = n_anc + n_sys
    D = 2 ** n_sys
    M = 2 ** n_anc

    # Verify the unitary is actually unitary
    unitarity_err = np.max(np.abs(
        lcu_unitary @ lcu_unitary.conj().T - np.eye(M * D)
    ))

    # Verify the block-encoding:  U[:D,:D] * λ  ≈  A_scaled
    A_recon   = lcu_unitary[:D, :D] * lam
    block_err = np.max(np.abs(A_scaled - np.real(A_recon)))

    print(f"  LCU matrix      : {lcu_unitary.shape[0]}×{lcu_unitary.shape[1]}  ({t_build*1e3:.1f} ms)")
    print(f"  Ancilla qubits  : {n_anc}")
    print(f"  System  qubits  : {n_sys}")
    print(f"  Total   qubits  : {total_qubits}")
    print(f"  Unitarity check : {unitarity_err:.2e}")
    print(f"  Block-enc error : {block_err:.2e}")

    # ── 5. Build Qiskit circuit (for display / export) ────────────────────
    lcu_gate = UnitaryGate(lcu_unitary, label="Pauli_LCU")

    qc_display = QuantumCircuit(total_qubits, name="LCU_Lorenz")
    qc_display.append(lcu_gate, range(total_qubits))
    print(f"\n  Qiskit Circuit: {total_qubits} qubits, 1 UnitaryGate (Pauli_LCU)")
    print(f"  Gate structure: PREP_dag . SELECT . PREP  ({M*D}x{M*D} unitary)\n")

    # Wrap as Operator for Statevector.evolve()
    lcu_op = Operator(lcu_unitary)

    # ── 6. Time-stepping loop (quantum statevector simulation) ────────────
    current_sv = np.array(
        [X0, Y0, Z0, X0 * Z0, X0 * Y0, 0.0, 0.0, 0.0], dtype=float
    )
    hx, hy, hz = [X0], [Y0], [Z0]

    print(f"  Running {N_STEPS} quantum Euler steps ...")
    t0 = time.perf_counter()

    for step in range(N_STEPS):
        if step > 0 and step % (N_STEPS // 10) == 0:
            pct = 100 * step // N_STEPS
            print(f"  [{pct:3d}%]  step {step:4d}  |  "
                  f"x = {current_sv[0]:+9.4f}   "
                  f"y = {current_sv[1]:+9.4f}   "
                  f"z = {current_sv[2]:+9.4f}")

        sv_in         = S @ current_sv
        sv_out_scaled = apply_lcu_step(sv_in, lcu_op, n_anc, n_sys, lam)
        sv_out        = inv_S @ sv_out_scaled

        # Hard-enforce auxiliary quadratic relations
        sv_out[3] = sv_out[0] * sv_out[2]       # xz
        sv_out[4] = sv_out[0] * sv_out[1]       # xy

        hx.append(sv_out[0])
        hy.append(sv_out[1])
        hz.append(sv_out[2])

        current_sv = sv_out

    t_sim = time.perf_counter() - t0
    print(f"\n  [100%]  Done — {t_sim:.2f} s  "
          f"({t_sim / N_STEPS * 1e3:.2f} ms/step)\n")

    # ── 7. Classical reference & plots ────────────────────────────────────
    x_q, y_q, z_q = np.array(hx), np.array(hy), np.array(hz)
    t_cl, x_cl, y_cl, z_cl = euler_lorenz(
        DT, SIGMA, RHO, BETA, X0, Y0, Z0, N_STEPS
    )

    plot_lorenz_comparison(
        t_values, x_q, y_q, z_q,
        t_cl, x_cl, y_cl, z_cl,
        title="Lorenz Attractor — Pauli-LCU Quantum Circuit",
        quantum_label="Quantum (Pauli-LCU)",
        classical_label="Classical (Euler)",
        save_dir=SAVE_DIR,
        prefix_name="lorenz_pauli_lcu",
        show=False,
    )


if __name__ == "__main__":
    main()
