# Quantum Solvers for Nonlinear Dynamical Systems

This repository implements quantum algorithms for solving nonlinear ordinary differential equations (ODEs), with a focus on high-fidelity simulation of the **simple pendulum** and the **Lorenz system**.


---

## 📂 Repository Structure

```text
Nonlinear-Equations-Quantum-Solver/
├── pendulum/                   # Pendulum dynamics solvers
│   ├── classical.py            # Reference solutions (Euler, RK4, Analytical)
│   ├── plot_results.py         # Standardized 2-panel visualizations
│   ├── pauli_lcu_linear/       # Linear case via LCU
│   ├── pauli_lcu_nonlinear/    # Nonlinear case via LCU + ω²_eff
│   ├── rotations_linear/       # Linear case via 1-qubit Ry rotations
│   └── rotations_nonlinear/    # Nonlinear case via Hybrid Rotations
│
├── lorenz/                     # Lorenz system solvers
│   ├── classical.py            # Forward Euler reference
│   ├── plot_results.py         # 3D Trajectory + Error Log plots
│   ├── block_encoding/         # Standard BE routines
│   ├── pauli_lcu/              # Optimized Pauli-LCU with Phase-Prep
│   ├── sfable/                 # Sparse FABLE implementations
│   └── fable/                  # Legacy FABLE solver
│
├── Makefile                    # Execution automation
├── requirements.txt            # Project dependencies
└── README.md
```

---

## 🚀 Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run an optimized pendulum solver
python -m pendulum.pauli_lcu_linear.pauli_lcu_linear_statevector

# 3. Run the latest Lorenz solver (Pauli-LCU)
python -m lorenz.pauli_lcu.pauli_lcu_measurements

# 4. Use Automation (Make)
make run-all-sv   # Run all statevector simulations
make figures      # Regenerate all project figures
```

---


