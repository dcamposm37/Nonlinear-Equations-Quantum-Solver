# Quantum Solvers for Nonlinear Dynamical Systems

This repository implements quantum algorithms for solving nonlinear ordinary 
  differential equations (ODEs), with particular focus on the simple pendulum and
   the Lorenz system. The project explores different block-encoding methodologies
   and linear combinations of unitaries to simulate nonlinear dynamics on quantum
   hardware.


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
 # 1. Clone the repository
  git clone
  https://github.com/your-username/Nonlinear-Equations-Quantum-Solver.git        
  cd Nonlinear-Equations-Quantum-Solver

  # 2. Create virtual environment (recommended)
  python -m venv venv
  source venv/bin/activate  # Linux/Mac
  # or: venv\Scripts\activate  # Windows

  # 3. Install dependencies
  pip install -r requirements.txt

  # 4. (Optional) Install FABLE for S-FABLE solver
  pip install fable-circuits
 ---
  Dependencies

  numpy>=1.24
  matplotlib>=3.7
  qiskit>=1.0
  qiskit-aer>=0.13
  scipy>=1.10
```
## Usage

### Run individual solvers
```bash
  # Linear pendulum - LCU statevector
  python -m pendulum.pauli_lcu_linear.pauli_lcu_linear_statevector

  # Nonlinear pendulum - LCU statevector
  python -m pendulum.pauli_lcu_nonlinear.pauli_lcu_nonlinear_statevector

  # Lorenz - Block Encoding statevector
  python -m lorenz.block_encoding.block_encoding_statevector

  # Lorenz - Pauli-LCU (optimized method)
  python -m lorenz.pauli_lcu.pauli_lcu_statevector

  # Lorenz - S-FABLE
  python -m lorenz.sfable.sfable_statevector
```
Using Make
```bash
  make run-lcu-lin-sv       # LCU linear statevector
  make run-lcu-nlin-sv      # LCU nonlinear statevector
  make run-lorenz-be-sv     # Lorenz block encoding statevector
  make run-all-sv           # All statevector simulations
  make figures              # Regenerate all figures
  make clean                # Clean figures and cache
```
  ---
  ## Method Descriptions

  1. LCU (Linear Combination of Unitaries)

  Decomposes the forward Euler operator as a linear combination of unitaries:    

  A = I + Δt·[[0, 1], [-ω², 0]] = c₀·I + c₁·(±X) + c₂·(ZX)

  - Circuit: 3 qubits (2 ancillas + 1 system)
  - Post-selection: project ancillas to |00⟩
  - Normalization factor: α = c₀ + c₁ + c₂

  2. Block Encoding (sqrtm completion)

  Encodes a non-unitary matrix A inside a unitary U:

  U = [[A/α,  √(I-AA†)]
       [√(I-A†A), -A†/α]]

  - Qubits: n + 1 (n system + 1 ancilla)
  - Method: Completion via scipy.linalg.sqrtm

  3. Pauli-LCU for Lorenz

  Decomposition in the Pauli basis:

  A = Σⱼ cⱼ Pⱼ,    λ = Σⱼ |cⱼ|

  - Advantage over FABLE: λ ≪ 2ⁿ for sparse matrices
  - PREP circuit: Householder unitary
  - SELECT: Controlled Paulis with phase

  4. Rotation Gates (Hybrid)

  For the nonlinear pendulum:

  - Phase: Encoded in Ry rotations (unitary)
  - Amplitude: Tracked classically (non-unitary factor)
  - Leverages norm conservation in pure rotations

  5. S-FABLE

  FABLE applied to the Hadamard-transformed matrix:

  M = Hⁿ · A · Hⁿ

  Better compression for systems sparse in the Walsh-Hadamard basis.

  ---
  Physical Systems

  Simple Pendulum

  Linear: θ̈ + ω²θ = 0

  Nonlinear: θ̈ + (g/L)sin(θ) = 0

  - Trick: ω²_eff(x) = (g/L)·sin(x)/x

  Lorenz System

  dx/dt = σ(y - x)
  dy/dt = x(ρ - z) - y
  dz/dt = xy - βz

  Standard parameters: σ=10, ρ=28, β=8/3 (chaotic regime)

  ---
  Visualizations

  Scripts automatically generate:

  1. 3D Plot: Attractor trajectory
  2. 2D Panel: XY, XZ, YZ projections
  3. Error Log: Euclidean distance vs time (logarithmic scale)

  ---
  License

  MIT License - Copyright (c) 2025 Diego Alejandro Campos
---


