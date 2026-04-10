"""
Nonlinear Pendulum Solver — Rotation Gates (Sequential Simulation)
==================================================================

Integrates the nonlinear pendulum using a hybrid approach:
1. Calculates the required phase evolution and amplitude via the classical 
   nonlinear Euler step.
2. Applies this phase shift (\\Delta\\theta) as a unitary rotation gate.
3. Uses exact statevector simulation to extract the target without measurement noise.
4. Re-scales the reconstructed state with the classical norm to incorporate
   the non-unitary dynamics typical of the physical model.

Usage
-----
    python -m pendulum.rotations_nonlinear.rotations_nonlinear_statevector

Output
------
    pendulum/rotations_nonlinear/figures/rotation_nonlinear_sv.png
"""

import sys
import os
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Operator, Statevector

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from pendulum.classical import euler_nonlinear
from pendulum.plot_results import plot_pendulum_comparison

# ---------------------------------------------------------------------------
# Parameters
# ---------------------------------------------------------------------------
DT = 0.003
G_L = 9.8
X0 = np.pi / 2
Y0 = 0.0
N_STEPS = 1000

FIGURE_PATH = os.path.join(
    os.path.dirname(__file__), "figures", "rotation_nonlinear_sv.png"
)

# ---------------------------------------------------------------------------
# Single Step Evolution
# ---------------------------------------------------------------------------
def compute_next(x_current: float, v_current: float, w0: float):
    # 1. Target nonlinear Euler step
    x_targ = x_current + DT * v_current
    v_targ = v_current - DT * G_L * np.sin(x_current)
    y_targ = v_targ / w0
    
    y_current = v_current / w0
    
    # 2. Extract angles and norm
    theta_curr = np.arctan2(y_current, x_current)
    theta_targ = np.arctan2(y_targ, x_targ)
    delta_theta = theta_targ - theta_curr
    
    r_targ = np.sqrt(x_targ**2 + y_targ**2)
    r_curr = np.sqrt(x_current**2 + y_current**2)
    
    if r_curr < 1e-10 or r_targ < 1e-10:
        return x_targ, v_targ

    # Current normalized quantum state
    state_norm = [x_current / r_curr, y_current / r_curr]

    # 3. Quantum circuit with rotation
    qc = QuantumCircuit(1)
    qc.initialize(state_norm, 0)
    
    c = np.cos(delta_theta)
    s = np.sin(delta_theta)
    rot = np.array([[c, -s], [s, c]], dtype=complex)
    qc.append(Operator(rot), [0])

    # 4. Statevector reconstruction
    sv = Statevector.from_instruction(qc)
    
    x_new = np.real(sv.data[0]) * r_targ
    y_new = np.real(sv.data[1]) * r_targ
    v_new = y_new * w0

    return x_new, v_new

# ---------------------------------------------------------------------------
# Main Routine
# ---------------------------------------------------------------------------
def main():
    print("Starting nonlinear simulation with statevector (exact)...")

    w0 = np.sqrt(G_L)
    
    traj = [(X0, Y0)]
    xc, vc = X0, Y0
    
    for s in range(N_STEPS):
        if s > 0 and s % 100 == 0:
            print(f"  step {s}/{N_STEPS}")
            
        xc, vc = compute_next(xc, vc, w0)
        traj.append((xc, vc))

    x_q, v_q = zip(*traj)

    t_cl, x_cl, y_cl = euler_nonlinear(DT, G_L, X0, Y0, N_STEPS)

    plot_pendulum_comparison(
        t_cl[:len(x_q)], x_q, v_q,
        t_cl, x_cl, y_cl,
        title="Nonlinear Pendulum — Rotation Gates (Statevector)",
        quantum_label="Quantum (Rotations SV)",
        classical_label="Classical (Exact Euler)",
        save_path=FIGURE_PATH,
    )

if __name__ == "__main__":
    main()
