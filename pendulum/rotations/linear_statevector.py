"""
Linear Pendulum Solver — Rotation Gates (Sequential Simulation)
===============================================================

Solves the *linear* pendulum using unitary rotation gates mapped 
to a 1-qubit circuit, with exact statevector simulation.

Usage
-----
    python -m pendulum.rotations.linear_statevector

Output
------
    pendulum/figures/rotation_linear_sv.png
"""

import os
import sys
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Operator, Statevector

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from pendulum.plot_results import plot_pendulum_comparison


# ---------------------------------------------------------------------------
# Parameters
# ---------------------------------------------------------------------------
OMEGA_0 = 9.8           # Frequency (sqrt(g/l))
EPSILON = 0.01          # Time step (dt)
X0 = np.pi / 2          # Initial position
Y0 = 0.0                # Initial scaled velocity
N_QUBITS = 12           
N_STEPS = 2**(N_QUBITS - 1)

FIGURE_PATH = os.path.join(
    os.path.dirname(__file__), "..", "figures", "rotation_linear_sv.png"
)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    print(f"Starting linear rotation sequential simulation with {N_STEPS} steps...")

    norm = np.sqrt(X0**2 + Y0**2)
    x0, y0 = X0 / norm, Y0 / norm

    x_quantum = []
    y_quantum = []

    current_state = [x0, y0]

    for n in range(N_STEPS):
        if n > 0 and n % 500 == 0:
            print(f"  step {n}/{N_STEPS}")

        x_quantum.append(np.real(current_state[0]))
        y_quantum.append(np.real(current_state[1]))
        
        qc = QuantumCircuit(1)
        qc.initialize(current_state, 0)
        
        phi = -1 * EPSILON * OMEGA_0
        c = np.cos(phi)
        s = np.sin(phi)
        
        rot = np.array([[c, -s], [s, c]], dtype=complex)
        custom_gate = Operator(rot)
        qc.append(custom_gate, [0])
        
        sv = Statevector.from_instruction(qc)
        current_state = sv.data

    x_quantum = np.array(x_quantum)
    y_quantum = np.array(y_quantum)

    t_values = np.arange(N_STEPS) * EPSILON

    phi_values = OMEGA_0 * t_values
    x_class = x0 * np.cos(phi_values) + y0 * np.sin(phi_values)
    y_class = -x0 * np.sin(phi_values) + y0 * np.cos(phi_values)

    plot_pendulum_comparison(
        t_values, x_quantum, y_quantum,
        t_values, x_class, y_class,
        title="Linear Pendulum — Rotation Gates (Sequential)",
        quantum_label="Quantum (Statevector)",
        classical_label="Classical (Exact)",
        save_path=FIGURE_PATH
    )


if __name__ == "__main__":
    main()
