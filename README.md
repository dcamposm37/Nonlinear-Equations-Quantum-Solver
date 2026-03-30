# Quantum Solvers for Nonlinear Dynamical Systems

This repository implements quantum algorithms for solving nonlinear ordinary
differential equations (ODEs), with a focus on the simple pendulum and the
Lorenz system.

## Methods

| Method | System | Statevector | Measurements |
|---|---|---|---|
| **LCU** (Linear Combination of Unitaries) | Linear pendulum | ✅ | ✅ |
| **LCU** | Nonlinear pendulum | ✅ | ✅ |
| **Rotation gates** | Linear pendulum | ✅ | ✅ |
| **Rotation gates** | Nonlinear pendulum | ✅ | ✅ |
| **Block encoding** | Lorenz system | ✅ | 🔲 |

## Repository structure

```
├── pendulum/
│   ├── classical.py            Classical reference solutions (Euler, RK4, analytical)
│   ├── plot_results.py         Standardised 3-panel comparison plots
│   ├── solvers/
│   │   ├── lcu_linear_statevector.py
│   │   ├── lcu_linear_measurements.py
│   │   ├── lcu_nonlinear_statevector.py
│   │   └── lcu_nonlinear_measurements.py
│   ├── rotations/
│   │   ├── linear_statevector.py
│   │   ├── linear_measurements.py
│   │   ├── nonlinear_statevector.py
│   │   └── nonlinear_measurements.py
│   └── figures/                Generated plots
│
├── lorenz/                     Lorenz system (TODO)
│   ├── solvers/
│   ├── plot_results.py
│   ├── classical.py
│   └── figures/
│
├── docs/
│   └── error_propagation_analysis.tex
│
├── Makefile
├── requirements.txt
└── README.md
```

## Quick start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run one solver
python -m pendulum.solvers.lcu_linear_statevector

# 3. Or use Make
make run-lcu-lin-sv
make figures          # regenerate all statevector figures
make docs             # compile LaTeX → PDF
```

## Key results

The **LCU statevector** simulation reproduces the classical forward-Euler
discretisation *exactly*, validating the LCU circuit construction.

The **LCU measurement-based** simulation diverges over time due to the
cumulative effect of the post-selection probability `p_succ < 1`:
after `n` steps the norm decays as `(√p̄_succ)^n → 0`.
See `docs/error_propagation_analysis.tex` for a full derivation.

The **Rotation gates** approach explores a unitary-only methodology natively available on 1-qubit hardware. Because pure quantum rotations strictly conserve the geometrical norm $x^2 + y^2 = 1$, they cannot naturally describe the anharmonic potential of a physical pendulum using a single qubit without ancillas. To overcome this limitation:
1. The **linear** rotations naturally match the circular phase space, conserving amplitude intrinsically.
2. The **nonlinear** rotations implement a *hybrid quantum-classical algorithm*: the amplitude stretch (non-unitary factor) is tracked purely classically while the intricate geometrical phase angles are mapped directly onto the `Ry` unitary gates.
