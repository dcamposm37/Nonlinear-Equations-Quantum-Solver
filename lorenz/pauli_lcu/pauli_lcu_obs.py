"""
Pauli-LCU Quantum Circuit -- Lorenz Attractor (Pro, No OAA)
=======================================================================

Implementation with Direct Measurement of Pauli Observables
(without shift preconditioning).

Measurement technique:
    Expected values are extracted by isolating amplitudes using
    Pauli operators (e.g., XIX) against an "anchor" in column 5.
    This allows measuring amplitudes with their intrinsic sign, without the
    need for classical heuristics or adding a constant shift.

    After quantum measurement, the coordinates are scaled back to 
    recover the real physical variables.

Eliminates count-based tomography and sign heuristics.
"""

import os
import sys
import time
import numpy as np
import warnings
import faulthandler
faulthandler.enable()
warnings.filterwarnings("ignore", category=DeprecationWarning)

# -- Qiskit ----------------------------------------------------------------
from qiskit import QuantumCircuit, transpile
from qiskit.circuit.library import UnitaryGate, StatePreparation
from qiskit_aer import AerSimulator
from qiskit.quantum_info import SparsePauliOp
from qiskit_aer.primitives import Estimator

# -- Project imports -------------------------------------------------------
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from lorenz.classical import euler_lorenz
from lorenz.plot_results import plot_lorenz_comparison

# Reuse analytical builders from the statevector module
from lorenz.pauli_lcu.pauli_lcu_statevector import (
    pauli_decompose,
    build_lcu_unitary,
)

# ===========================================================================
# Global Parameters
# ===========================================================================

# -- Lorenz system parameters ----------------------------------------------
DT    = 0.01       # Euler time step
SIGMA = 10.0       # Lorenz σ parameter
RHO   = 28.0       # Lorenz ρ parameter
BETA  = 8.0 / 3.0  # Lorenz β parameter

# -- Initial conditions and duration --------------------------------------
X0, Y0, Z0 = 1.0, 1.0, 1.0
T_FINAL = 5.0
N_STEPS = int(T_FINAL / DT)

# -- Simulator configuration ------------------------------------------
SHOTS = None  # Number of shots per step; None = exact simulation

# -- Output directory for figures -------------------------------------
SAVE_DIR = os.path.join(os.path.dirname(__file__), "figures")
os.makedirs(SAVE_DIR, exist_ok=True)

# -- Preconditioning constants ------------------------------------
C_ANCHOR = 2.0   # Fixed anchor value (index 5 of the state vector)

# ===========================================================================
# Base Euler Matrix Construction
# ===========================================================================
def build_euler_matrix(dt, sigma, rho, beta):
    """
    Builds the standard Euler evolution matrix (8x8) for Lorenz.

    Returns
    -------
    A : ndarray (8, 8)   Evolution matrix.
    """
    A = np.array([
        # x            y           z          xz     xy    C_ANC  0  0
        [1 - dt*sigma,  dt*sigma,  0,          0,     0,     0,   0, 0],
        [dt*rho,        1 - dt,    0,         -dt,    0,     0,   0, 0],
        [0,             0,         1 - dt*beta, 0,    dt,    0,   0, 0],
        [0,             0,         0,          1,     0,     0,   0, 0],
        [0,             0,         0,          0,     1,     0,   0, 0],
        [0,             0,         0,          0,     0,     1,   0, 0],
        [0,             0,         0,          0,     0,     0,   1, 0],
        [0,             0,         0,          0,     0,     0,   0, 1]
    ], dtype=float)
    return A


# ===========================================================================
# Main
# ===========================================================================
def main():
    print("=" * 70)
    print("  Pauli-LCU Lorenz (Pro, No OAA)")
    print("=" * 70)
    print(f"  dt={DT}, T={T_FINAL}, steps={N_STEPS}, "
          f"shots={SHOTS if SHOTS is None else f'{SHOTS:,}'}\n")

    t_values = np.linspace(0, T_FINAL, N_STEPS + 1)

    # -- 1. Base Euler matrix -------------------------------------------
    A = build_euler_matrix(DT, SIGMA, RHO, BETA)

    # -- 2. Static similarity scaling -------------------------------
    W = np.array([1/20, 1/30, 1/50, 1/1000, 1/600, 1.0, 1.0, 1.0])
    S     = np.diag(W)
    inv_S = np.diag(1.0 / W)
    A_scaled = S @ A @ inv_S

    # -- 3. Pauli decomposition ----------------------------------------
    t0 = time.perf_counter()
    coeffs, pauli_ops, labels = pauli_decompose(A_scaled)
    t_decomp = time.perf_counter() - t0

    n_sys = 3   # 3 system qubits -> dim = 8
    lam   = float(np.sum(np.abs(coeffs)))

    print(f"  Pauli terms     : {len(coeffs)} non-zero  ({t_decomp*1e3:.1f} ms)")
    print(f"  Lambda (LCU)    = {lam:.4f}")

    # -- 4. LCU unitary construction (precomputed once) -----------
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

    # -- 5. Pauli observables for direct measurement ---------------------
    P_0 = SparsePauliOp.from_list([("I", 0.5), ("Z", 0.5)])
    P_anc = P_0
    for _ in range(n_anc - 1):
        P_anc = P_anc.tensor(P_0)

    O_sys_x = SparsePauliOp.from_list([
        ("XIX", 0.25), ("XZX", 0.25), ("YIY", -0.25), ("YZY", -0.25)
    ])
    O_sys_y = SparsePauliOp.from_list([
        ("XII", 0.25), ("XIZ", -0.25), ("XZI", 0.25), ("XZZ", -0.25)
    ])
    O_sys_z = SparsePauliOp.from_list([
        ("XXX", 0.25), ("XYY", 0.25), ("YXY", -0.25), ("YYX", 0.25)
    ])

    obs_x = P_anc.tensor(O_sys_x)
    obs_y = P_anc.tensor(O_sys_y)
    obs_z = P_anc.tensor(O_sys_z)

    # -- 6. Reusable components (gate, simulator, estimator) ---------
    lcu_gate  = UnitaryGate(lcu_unitary, label="Pauli_LCU")
    simulator = AerSimulator()

    # -- 7. State vector initialization ----------------------------
    #    v = [x₀, y₀, z₀, x₀·z₀, x₀·y₀, C_ANCHOR, 0, 0]
    current_sv = np.array(
        [X0, Y0, Z0, X0 * Z0, X0 * Y0, C_ANCHOR, 0.0, 0.0], dtype=float
    )

    # History of physical coordinates
    hx, hy, hz = [X0], [Y0], [Z0]

    # -- 8. Time iteration loop ------------------------------------
    print(f"  Running {N_STEPS} steps "
          f"(Estimator, {SHOTS if SHOTS is None else f'{SHOTS:,}'} shots/step) ...")
    t0 = time.perf_counter()

    for step in range(N_STEPS):
        # 8a. Fix the anchor in the state vector
        current_sv[5] = C_ANCHOR

        # 8b. Scale with similarity matrix S and normalize
        current_sv_scaled = S @ current_sv
        norm = np.linalg.norm(current_sv_scaled)

        if norm == 0:
            initial_normalized = current_sv_scaled
        else:
            initial_normalized = current_sv_scaled / norm

        # 8c. Prepare full quantum state (system + ancillas)
        padded_state = np.zeros(2**total_qubits, dtype=complex)
        padded_state[0:dim] = initial_normalized

        sp_circ = QuantumCircuit(total_qubits)
        sp_circ.append(
            StatePreparation(padded_state.tolist()), range(total_qubits)
        )
        sp_circ = transpile(
            sp_circ, basis_gates=['u', 'cx'], optimization_level=3
        )

        # 8d. Build circuit: preparation + LCU
        qc = QuantumCircuit(total_qubits)
        qc.compose(sp_circ, inplace=True)
        qc.append(lcu_gate, range(total_qubits))

        # 8e. Transpile for the simulator
        transpiled_qc = transpile(qc, simulator)

        # 8f. Execute with Estimator
        if SHOTS is None:
            estimator = Estimator(approximation=True)
        else:
            estimator = Estimator(run_options={"shots": SHOTS})

        job = estimator.run(
            circuits=[transpiled_qc] * 3,
            observables=[obs_x, obs_y, obs_z],
        )
        values = job.result().values

        # 8g. Extract coordinates from Pauli observables
        x_real = values[0] * (lam * norm)**2 / (2 * C_ANCHOR * S[0,0] * S[5,5])
        y_real = values[1] * (lam * norm)**2 / (2 * C_ANCHOR * S[1,1] * S[5,5])
        z_real = values[2] * (lam * norm)**2 / (2 * C_ANCHOR * S[2,2] * S[5,5])

        # 8i. Save physical coordinates
        hx.append(x_real)
        hy.append(y_real)
        hz.append(z_real)

        # 8j. Algebraic reconstruction of the exact state vector
        current_sv[0] = x_real
        current_sv[1] = y_real
        current_sv[2] = z_real
        current_sv[3] = x_real * z_real
        current_sv[4] = x_real * y_real
        current_sv[5] = C_ANCHOR
        current_sv[6] = 0.0
        current_sv[7] = 0.0

        # 8k. Progress update
        pct = 100 * step // N_STEPS
        print(f"\r  [{pct:3d}%]  step {step:4d}/{N_STEPS}  |  "
              f"x={x_real:+9.4f}  "
              f"y={y_real:+9.4f}  "
              f"z={z_real:+9.4f}", end="", flush=True)

    t_sim = time.perf_counter() - t0
    print(f"\n  [100%]  Done -- {t_sim:.1f} s  ({t_sim/N_STEPS*1e3:.1f} ms/step)\n")

    # -- 9. Classical reference and plots ----------------------------------
    x_q, y_q, z_q = np.array(hx), np.array(hy), np.array(hz)
    t_cl, x_cl, y_cl, z_cl = euler_lorenz(
        DT, SIGMA, RHO, BETA, X0, Y0, Z0, N_STEPS
    )

    plot_lorenz_comparison(
        t_values, x_q, y_q, z_q,
        t_cl, x_cl, y_cl, z_cl,
        title="Lorenz — Pauli-LCU (Pro, No OAA)",
        quantum_label=f"Quantum (Pauli-LCU Pro",
        classical_label="Classical (Euler)",
        save_dir=SAVE_DIR,
        prefix_name="lorenz_pauli_lcu_pro_no_oaa",
        show=False,
    )


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        import traceback
        traceback.print_exc()
        sys.exit(1)
