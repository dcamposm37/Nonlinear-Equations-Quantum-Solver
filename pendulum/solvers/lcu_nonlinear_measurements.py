"""
LCU Nonlinear Pendulum Solver — Measurement-Based (QST) Simulation
====================================================================

Solves the *nonlinear* pendulum  ẍ + (g/L) sin(x) = 0  using the LCU
algorithm with measurement-based Quantum State Tomography.

Nonlinear trick
---------------
At each step the LCU coefficients are recalculated using a
position-dependent effective frequency:

        ω²_eff(x) = (g/L) · sin(x) / x

This turns the one-step linear LCU operator into a faithful forward-Euler
step for the nonlinear ODE  (see the statevector version for derivation).

Error propagation
-----------------
All the same p_succ-related error mechanisms from the linear
measurement-based solver apply here; additionally, any noise in the
measured x_n feeds back into ω²_eff, slightly altering the *operator
itself* at the next step.  This makes the nonlinear QST solver
somewhat more sensitive to shot noise than its linear counterpart.
See docs/error_propagation_analysis.tex for the full analysis.

Usage
-----
    python -m pendulum.solvers.lcu_nonlinear_measurements

Output
------
    pendulum/figures/lcu_nonlinear_meas.png
"""

import sys
import os
import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit.library import XGate, ZGate
from qiskit_aer import AerSimulator

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from pendulum.classical import euler_nonlinear
from pendulum.plot_results import plot_pendulum_comparison

# ---------------------------------------------------------------------------
# Parameters
# ---------------------------------------------------------------------------
DT = 0.003
G_L = 9.8              # g/L
X0 = np.pi / 2         # Large initial angle to emphasise nonlinearity
Y0 = 0.0
N_STEPS = 1000
SHOTS = 25_000

FIGURE_PATH = os.path.join(
    os.path.dirname(__file__), "..", "figures", "lcu_nonlinear_meas.png"
)


# ---------------------------------------------------------------------------
# Effective frequency
# ---------------------------------------------------------------------------
def w2_eff(x: float) -> float:
    """ω²_eff = (g/L)·sin(x)/x  (Taylor limit for |x| < 1e-6)."""
    if abs(x) < 1e-6:
        return G_L
    return G_L * (np.sin(x) / x)


# ---------------------------------------------------------------------------
# LCU circuit
# ---------------------------------------------------------------------------
def create_lcu_circuit(theta_init: float, x_current: float):
    """Build the 3-qubit LCU circuit with position-dependent ω²_eff."""
    qc = QuantumCircuit(3)
    qc.ry(theta_init, 1)

    w2 = w2_eff(x_current)
    b = DT * (1 - w2) / 2
    c = DT * (1 + w2) / 2
    c0, c1, c2 = 1.0, abs(b), c
    alpha = c0 + c1 + c2
    if alpha == 0:
        raise ValueError("alpha_lcu is zero")

    sign_x = np.sign(b) if b != 0 else 1
    p0, p1, p2 = c0 / alpha, c1 / alpha, c2 / alpha

    qc.ry(2 * np.arcsin(np.sqrt(p2)), 0)
    p_sum = p0 + p1
    theta_q2 = 2 * np.arcsin(np.sqrt(p1 / p_sum) if p_sum > 0 else 0)
    qc.x(0);  qc.cry(theta_q2, 0, 2);  qc.x(0)

    qc.x(0)
    if sign_x == 1:
        qc.append(XGate().control(2, ctrl_state="11"), [0, 2, 1])
    else:
        qc.append(ZGate().control(2, ctrl_state="11"), [0, 2, 1])
        qc.append(XGate().control(2, ctrl_state="11"), [0, 2, 1])
        qc.append(ZGate().control(2, ctrl_state="11"), [0, 2, 1])
    qc.x(0)

    qc.x(2)
    qc.append(XGate().control(2, ctrl_state="11"), [0, 2, 1])
    qc.append(ZGate().control(2, ctrl_state="11"), [0, 2, 1])
    qc.x(2)

    qc.x(0);  qc.cry(-theta_q2, 0, 2);  qc.x(0)
    qc.ry(-2 * np.arcsin(np.sqrt(p2)), 0)

    return qc, alpha


# ---------------------------------------------------------------------------
# Single step (3-basis QST with post-selection)
# ---------------------------------------------------------------------------
def compute_next(x: float, y: float, backend):
    """
    Compute (x', y') via measurement-based QST.

    The circuit now depends on the *measured* x_n through ω²_eff,
    so any noise in x feeds back into the operator at the next step.
    """
    norm = np.sqrt(x**2 + y**2)
    if norm < 1e-10:
        return x, y

    theta = 2 * np.arctan2(y, x)
    qc, alpha = create_lcu_circuit(theta, x)

    def _measure(basis):
        qc_m = qc.copy()
        if basis == "X":
            qc_m.h(1)
        elif basis == "Y":
            qc_m.sdg(1);  qc_m.h(1)
        qc_m.measure_all()
        counts = backend.run(qc_m, shots=SHOTS).result().get_counts()
        c0 = counts.get("000", 0)
        c1 = counts.get("010", 0)
        return c0, c1, c0 + c1

    c0_z, c1_z, succ_z = _measure("Z")
    c0_x, _,    succ_x = _measure("X")
    _,    _,    succ_y = _measure("Y")

    if min(succ_z, succ_x, succ_y) < 10:
        return x, y

    p_succ = np.mean([succ_z, succ_x, succ_y]) / SHOTS
    cond_p0 = c0_z / succ_z
    cond_p1 = c1_z / succ_z
    rx = 2 * (c0_x / succ_x) - 1

    abs_a = np.sqrt(cond_p0)
    abs_b = np.sqrt(cond_p1)
    sign = 1 if (rx / 2) >= 0 else -1

    s = alpha * norm * np.sqrt(p_succ)
    x1, y1 = abs_a * s, sign * abs_b * s
    x2, y2 = -x1, -y1

    if (x1 * x + y1 * y) >= (x2 * x + y2 * y):
        return x1, y1
    return x2, y2


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    backend = AerSimulator()          # Instantiate once for efficiency
    print("Starting nonlinear LCU measurement-based simulation...")

    traj = [(X0, Y0)]
    xc, yc = X0, Y0
    for s in range(N_STEPS):
        if s % 100 == 0:
            print(f"  step {s}/{N_STEPS}")
        xc, yc = compute_next(xc, yc, backend)
        traj.append((xc, yc))

    x_q, y_q = zip(*traj)

    # Classical nonlinear Euler reference
    t_cl, x_cl, y_cl = euler_nonlinear(DT, G_L, X0, Y0, N_STEPS)

    plot_pendulum_comparison(
        t_cl[:len(x_q)], x_q, y_q,
        t_cl, x_cl, y_cl,
        title="LCU Nonlinear Pendulum — Measurement-Based QST",
        quantum_label="Quantum (Measurements)",
        classical_label="Classical (Euler, nonlinear)",
        save_path=FIGURE_PATH,
    )


if __name__ == "__main__":
    main()
