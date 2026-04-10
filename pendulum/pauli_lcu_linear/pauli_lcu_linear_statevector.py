"""
LCU Linear Pendulum Solver — Statevector (Exact) Simulation
============================================================

Solves  ẍ + ω² x = 0  using the Linear Combination of Unitaries (LCU)
algorithm with exact statevector simulation (no measurement noise).

The LCU circuit decomposes the forward-Euler operator
    A = I + dt·[[0, 1], [-ω², 0]]
as  A = c₀·I + c₁·(±X) + c₂·(ZX)  on a 3-qubit register
(2 ancillas + 1 system qubit).

Post-selecting on ancillas |00⟩ yields the evolved state scaled
by α = c₀ + c₁ + c₂.  Because the simulation is exact, the quantum
trajectory matches the classical Euler discretisation perfectly.

Usage
-----
    python -m pendulum.pauli_lcu_linear.pauli_lcu_linear_statevector

Output
------
    pendulum/pauli_lcu_linear/figures/lcu_linear_sv.png
"""

import sys
import os
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from qiskit.circuit.library import XGate, ZGate

# Allow imports from the project root
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from pendulum.classical import euler_linear
from pendulum.plot_results import plot_pendulum_comparison

# ---------------------------------------------------------------------------
# Parameters
# ---------------------------------------------------------------------------
DT = 0.001
W2 = 9.8
X0 = np.pi / 2
Y0 = 1.0
N_STEPS = 5000

FIGURE_PATH = os.path.join(
    os.path.dirname(__file__), "figures", "lcu_linear_sv.png"
)


# ---------------------------------------------------------------------------
# LCU circuit
# ---------------------------------------------------------------------------
def create_lcu_circuit(theta_init: float, dt: float, w2: float):
    """Build the 3-qubit LCU circuit for one Euler step."""
    qc = QuantumCircuit(3)
    qc.ry(theta_init, 1)

    b = dt * (1 - w2) / 2
    c = dt * (1 + w2) / 2
    c0, c1, c2 = 1.0, abs(b), c
    alpha = c0 + c1 + c2

    sign_x = np.sign(b) if b != 0 else 1
    p0, p1, p2 = c0 / alpha, c1 / alpha, c2 / alpha

    # Ancilla preparation
    qc.ry(2 * np.arcsin(np.sqrt(p2)), 0)
    p_sum = p0 + p1
    theta_q2 = 2 * np.arcsin(np.sqrt(p1 / p_sum) if p_sum > 0 else 0)
    qc.x(0);  qc.cry(theta_q2, 0, 2);  qc.x(0)

    # Select-V: U₁ on |01⟩
    qc.x(0)
    if sign_x == 1:
        qc.append(XGate().control(2, ctrl_state="11"), [0, 2, 1])
    else:
        qc.append(ZGate().control(2, ctrl_state="11"), [0, 2, 1])
        qc.append(XGate().control(2, ctrl_state="11"), [0, 2, 1])
        qc.append(ZGate().control(2, ctrl_state="11"), [0, 2, 1])
    qc.x(0)

    # Select-V: U₂ on |10⟩ (ZX)
    qc.x(2)
    qc.append(XGate().control(2, ctrl_state="11"), [0, 2, 1])
    qc.append(ZGate().control(2, ctrl_state="11"), [0, 2, 1])
    qc.x(2)

    # Inverse preparation
    qc.x(0);  qc.cry(-theta_q2, 0, 2);  qc.x(0)
    qc.ry(-2 * np.arcsin(np.sqrt(p2)), 0)

    return qc, alpha


# ---------------------------------------------------------------------------
# Single evolution step
# ---------------------------------------------------------------------------
def next_step(x: float, y: float, dt: float, w2: float):
    """Compute (x', y') via exact statevector post-selection."""
    norm = np.sqrt(x**2 + y**2)
    if norm == 0:
        return 0.0, 0.0
    theta = 2 * np.arctan2(y, x)
    qc, alpha = create_lcu_circuit(theta, dt, w2)
    amps = Statevector(qc).data
    return (np.real(amps[0] * alpha * norm),
            np.real(amps[2] * alpha * norm))


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    traj = [X0, Y0]
    xc, yc = X0, Y0
    for s in range(N_STEPS):
        if s % 500 == 0:
            print(f"  step {s}/{N_STEPS}")
        xc, yc = next_step(xc, yc, DT, W2)
        traj.extend([xc, yc])

    x_q = traj[0::2]
    y_q = traj[1::2]

    t_cl, x_cl, y_cl = euler_linear(DT, W2, X0, Y0, N_STEPS)

    plot_pendulum_comparison(
        t_cl, x_q, y_q,
        t_cl, x_cl, y_cl,
        title="LCU Linear Pendulum — Statevector",
        quantum_label="Quantum (Statevector)",
        classical_label="Classical (Euler)",
        save_path=FIGURE_PATH,
    )


if __name__ == "__main__":
    main()
