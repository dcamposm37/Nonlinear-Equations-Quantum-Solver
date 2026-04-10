"""
Linear Pendulum Solver — Rotation Gates with Measurements (QST)
===============================================================

Solves the *linear* pendulum using a 1-qubit rotation circuit,
and estimates the resulting state at each step via simulated 
Quantum State Tomography (Z and X basis measurements).

Usage
-----
    python -m pendulum.rotations_linear.rotations_linear_measurements

Output
------
    pendulum/rotations_linear/figures/rotation_linear_meas.png
"""

import sys
import os
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Operator
from qiskit_aer import AerSimulator

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
SHOTS = 25_000

FIGURE_PATH = os.path.join(
    os.path.dirname(__file__), "figures", "rotation_linear_meas.png"
)

# ---------------------------------------------------------------------------
# Main Routine
# ---------------------------------------------------------------------------
def main():
    backend = AerSimulator()
    print(f"Starting linear rotation simulation with measurements ({N_STEPS} steps)...")

    norm = np.sqrt(X0**2 + Y0**2)
    x0, y0 = X0 / norm, Y0 / norm

    x_quantum = []
    y_quantum = []

    current_state = [x0, y0]

    for n in range(N_STEPS):
        if n > 0 and n % 500 == 0:
            print(f"  step {n}/{N_STEPS}")

        x_quantum.append(np.real(current_state[0]) * norm)
        y_quantum.append(np.real(current_state[1]) * norm)
        
        qc = QuantumCircuit(1)
        qc.initialize(current_state, 0)
        
        # Rotation angle for the linear step
        phi = -1 * EPSILON * OMEGA_0
        c = np.cos(phi)
        s = np.sin(phi)
        
        rot = np.array([[c, -s], [s, c]], dtype=complex)
        qc.append(Operator(rot), [0])

        # Measuring (QST)
        def _measure(basis):
            qc_m = qc.copy()
            if basis == "X":
                qc_m.h(0)
            qc_m.measure_all()
            counts = backend.run(qc_m, shots=SHOTS).result().get_counts()
            return counts.get("0", 0), counts.get("1", 0)

        c0_z, c1_z = _measure("Z")
        c0_x, c1_x = _measure("X")

        p0_z = c0_z / SHOTS
        p1_z = c1_z / SHOTS
        rx = (c0_x - c1_x) / SHOTS

        abs_x = np.sqrt(p0_z)
        abs_y = np.sqrt(p1_z)
        sign_y = 1 if rx >= 0 else -1
        
        x_new = abs_x
        y_new = sign_y * abs_y
        
        # Resolve global phase ambiguity
        opt1_dist = (x_new - current_state[0])**2 + (y_new - current_state[1])**2
        opt2_dist = (-x_new - current_state[0])**2 + (-y_new - current_state[1])**2
        
        if opt2_dist < opt1_dist:
            x_new, y_new = -x_new, -y_new

        current_state = [x_new, y_new]

    x_quantum = np.array(x_quantum)
    y_quantum = np.array(y_quantum)

    t_values = np.arange(N_STEPS) * EPSILON

    # Classic exact solution
    phi_values = OMEGA_0 * t_values
    x_class = X0 * np.cos(phi_values) + Y0 * np.sin(phi_values)
    y_class = -X0 * np.sin(phi_values) + Y0 * np.cos(phi_values)

    plot_pendulum_comparison(
        t_values, x_quantum, y_quantum,
        t_values, x_class, y_class,
        title="Linear Pendulum — Rotation Gates (Measurements)",
        quantum_label="Quantum (Rotations + Shots)",
        classical_label="Classical (Exact)",
        save_path=FIGURE_PATH
    )

if __name__ == "__main__":
    main()
