"""
LCU Nonlinear Pendulum Solver — Statevector (Exact) Simulation
===============================================================

Solves the *nonlinear* pendulum  ẍ + (g/L) sin(x) = 0  using the LCU
algorithm with exact statevector simulation.

Nonlinear trick
---------------
The standard LCU encodes a *linear* operator A·v.  To handle the
nonlinearity sin(x), we define a position-dependent effective frequency:

        ω²_eff(x) = (g/L) · sin(x) / x

At each step the LCU coefficients are recalculated with ω²_eff instead
of a constant ω².  This makes the one-step operator:

        x_{n+1} = x_n + dt · y_n
        y_{n+1} = y_n − dt · ω²_eff(x_n) · x_n
                = y_n − dt · (g/L) · sin(x_n)

which is exactly the forward-Euler discretisation of the nonlinear ODE.
The statevector simulation therefore matches the nonlinear Euler
trajectory perfectly.

Usage
-----
    python -m pendulum.solvers.lcu_nonlinear_statevector

Output
------
    pendulum/figures/lcu_nonlinear_sv.png
"""

import sys
import os
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from qiskit.circuit.library import XGate, ZGate

# Allow imports from the project root
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from pendulum.classical import euler_nonlinear
from pendulum.plot_results import plot_pendulum_comparison

# ---------------------------------------------------------------------------
# Parameters
# ---------------------------------------------------------------------------
DT = 0.003
G_L = 9.8              # g/L  (gravitational constant / pendulum length)
X0 = np.pi / 2         # Large initial angle (90°) to emphasise nonlinearity
Y0 = 0.0               # Initial velocity
N_STEPS = 1000

FIGURE_PATH = os.path.join(
    os.path.dirname(__file__), "..", "figures", "lcu_nonlinear_sv.png"
)


# ---------------------------------------------------------------------------
# Position-dependent effective frequency
# ---------------------------------------------------------------------------
def w2_eff(x: float) -> float:
    """
    Effective ω² for the nonlinear pendulum.

    ω²_eff(x) = (g/L) · sin(x)/x

    Uses the Taylor limit  sin(x)/x → 1  for |x| < 1e-6 to avoid
    division by zero.
    """
    if abs(x) < 1e-6:
        return G_L
    return G_L * (np.sin(x) / x)


# ---------------------------------------------------------------------------
# LCU circuit (nonlinear: coefficients depend on current x)
# ---------------------------------------------------------------------------
def create_lcu_circuit(theta_init: float, x_current: float):
    """
    Build the 3-qubit LCU circuit for one *nonlinear* Euler step.

    Parameters
    ----------
    theta_init : float – RY angle encoding the state on q1.
    x_current  : float – current position θ_n (needed for ω²_eff).

    Returns
    -------
    (qc, alpha) : tuple
    """
    qc = QuantumCircuit(3)
    qc.ry(theta_init, 1)

    # Dynamic LCU coefficients
    w2 = w2_eff(x_current)
    b = DT * (1 - w2) / 2
    c = DT * (1 + w2) / 2
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
# Single evolution step (statevector)
# ---------------------------------------------------------------------------
def next_step(x: float, y: float):
    """Compute (x', y') via exact statevector post-selection."""
    norm = np.sqrt(x**2 + y**2)
    if norm < 1e-10:
        return x, y

    theta = 2 * np.arctan2(y, x)
    qc, alpha = create_lcu_circuit(theta, x)

    sv = Statevector.from_instruction(qc)
    # Post-selection: ancillas |00⟩ → indices 0 (|000⟩) and 2 (|010⟩)
    amp_x = sv.data[0].real
    amp_y = sv.data[2].real

    return norm * alpha * amp_x, norm * alpha * amp_y


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    print("Starting nonlinear LCU statevector simulation...")
    traj = [(X0, Y0)]
    xc, yc = X0, Y0
    for s in range(N_STEPS):
        if s % 100 == 0:
            print(f"  step {s}/{N_STEPS}")
        xc, yc = next_step(xc, yc)
        traj.append((xc, yc))

    x_q, y_q = zip(*traj)

    # Classical nonlinear Euler (the exact discretisation the circuit implements)
    t_cl, x_cl, y_cl = euler_nonlinear(DT, G_L, X0, Y0, N_STEPS)

    plot_pendulum_comparison(
        t_cl, x_q, y_q,
        t_cl, x_cl, y_cl,
        title="LCU Nonlinear Pendulum — Statevector",
        quantum_label="Quantum (Statevector)",
        classical_label="Classical (Euler, nonlinear)",
        save_path=FIGURE_PATH,
    )


if __name__ == "__main__":
    main()