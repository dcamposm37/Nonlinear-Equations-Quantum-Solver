"""
LCU Linear Pendulum Solver — Measurement-Based (QST) Simulation
================================================================

Solves  ẍ + ω² x = 0  using the LCU algorithm with measurement-based
Quantum State Tomography (3-basis QST with post-selection).

IMPORTANT — Error Propagation
------------------------------
Each step multiplies the state-vector norm by √p_succ (< 1).
After n steps the cumulative factor is  (√p̄_succ)^n → 0  exponentially,
causing the quantum trajectory to spiral inward in phase space.
See docs/error_propagation_analysis.tex for details.

Usage
-----
    python -m pendulum.solvers.lcu_linear_measurements

Output
------
    pendulum/figures/lcu_linear_meas.png
"""

import sys
import os
import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit.library import XGate, ZGate
from qiskit_aer import AerSimulator

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from pendulum.classical import analytical_linear
from pendulum.plot_results import plot_pendulum_comparison

# ---------------------------------------------------------------------------
# Parameters
# ---------------------------------------------------------------------------
DT = 0.003
W2 = 9.8
W = np.sqrt(W2)
X0 = np.pi / 4
Y0 = 1.0
N_STEPS = 1000
SHOTS = 25_000

FIGURE_PATH = os.path.join(
    os.path.dirname(__file__), "..", "figures", "lcu_linear_meas.png"
)


# ---------------------------------------------------------------------------
# LCU circuit (identical to statevector version)
# ---------------------------------------------------------------------------
def create_lcu_circuit(theta_init, dt, w2):
    """Build the 3-qubit LCU circuit for one Euler step."""
    qc = QuantumCircuit(3)
    qc.ry(theta_init, 1)

    b = dt * (1 - w2) / 2
    c = dt * (1 + w2) / 2
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
# Single step (measurement-based QST)
# ---------------------------------------------------------------------------
def compute_next(x, y, dt, w2, shots):
    """
    Compute (x', y') via 3-basis QST with post-selection.

    Measures in Z, X, Y bases, post-selects ancillas |00⟩,
    reconstructs amplitudes from the Bloch vector, and resolves
    the global sign via a dot-product continuity heuristic.
    """
    norm = np.sqrt(x**2 + y**2)
    if norm < 1e-10:
        return x, y

    theta = 2 * np.arctan2(y, x)
    qc, alpha = create_lcu_circuit(theta, dt, w2)
    backend = AerSimulator()

    def _measure(qc_base, basis_label):
        qc_m = qc_base.copy()
        if basis_label == "X":
            qc_m.h(1)
        elif basis_label == "Y":
            qc_m.sdg(1);  qc_m.h(1)
        qc_m.measure_all()
        counts = backend.run(qc_m, shots=shots).result().get_counts()
        c0 = counts.get("000", 0)
        c1 = counts.get("010", 0)
        succ = c0 + c1
        return c0, c1, succ

    c0_z, c1_z, succ_z = _measure(qc, "Z")
    c0_x, _, succ_x   = _measure(qc, "X")
    _, _, succ_y       = _measure(qc, "Y")

    if min(succ_z, succ_x, succ_y) < 10:
        return x, y

    p_succ = np.mean([succ_z, succ_x, succ_y]) / shots
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
    traj = [(X0, Y0)]
    xc, yc = X0, Y0
    for s in range(N_STEPS):
        print(s)
        xc, yc = compute_next(xc, yc, DT, W2, SHOTS)
        traj.append((xc, yc))

    x_q, y_q = zip(*traj)
    t = np.arange(0, (N_STEPS + 1) * DT, DT)
    x_cl, y_cl = analytical_linear(W, X0, Y0, t)

    plot_pendulum_comparison(
        t[:len(x_q)], x_q, y_q,
        t[:len(x_cl)], x_cl, y_cl,
        title="LCU Linear Pendulum — Measurement-Based QST",
        quantum_label="Quantum (Measurements)",
        classical_label="Classical (Analytical)",
        save_path=FIGURE_PATH,
    )


if __name__ == "__main__":
    main()
