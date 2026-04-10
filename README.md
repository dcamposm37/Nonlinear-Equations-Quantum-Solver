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
| **Block encoding** | Lorenz system | ✅ | ✅ |

## Repository structure

```
├── pendulum/
│   ├── classical.py            Classical reference solutions (Euler, RK4, analytical)
│   ├── plot_results.py         Standardised 2-panel and 3-panel comparison plots
│   ├── pauli_lcu_linear/       Linear pendulum via LCU
│   ├── pauli_lcu_nonlinear/    Nonlinear pendulum via LCU + Effective Frequency
│   ├── rotations_linear/       Linear pendulum via unitary rotations (1-qubit)
│   └── rotations_nonlinear/    Nonlinear pendulum via hybrid rotations
│
├── lorenz/                     Lorenz system methods
│   ├── pauli_lcu/              Optimized Pauli-LCU with MLE
│   ├── sfable/                 S-FABLE legacy solver
│   ├── block_encoding/         Standard block-encoding routines
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

# 2. Run the latest optimized LCU solver for Lorenz
python -m lorenz.pauli_lcu.pauli_lcu_measurements

# 3. Run a pendulum solver
python -m pendulum.pauli_lcu_linear.pauli_lcu_linear_statevector

# 4. Or use Make
make run-lcu-lin-sv
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

## Análisis de Divergencia Caótica (Chaotic Divergence Analysis)

The block-encoding quantum solver for the Lorenz system serves as an excellent case study in simulating chaos. By mapping the Euclidean distance $d(t) = \sqrt{(x_{cl}-x_q)^2 + (y_{cl}-y_q)^2 + (z_{cl}-z_q)^2}$ between the classical reference and quantum-reconstructed statevectors on a logarithmic scale, we observe the macroscopic propagation of computational noise. 

![Error vs Time](lorenz/figures/lorenz_be_statevector_error_log.png)

The divergence mathematically encapsulates the deterministic chaos through 3 distinct phases:
1. **Fidelidad Inicial (Initial Fidelity)**: The algorithmic error rests at the noise floor limit ($\sim 10^{-13}$), validating the extremely high precision of the `sqrtm` block-encoding protocol for the matrix linear transformations.
2. **Divergencia de Lyapunov (Lyapunov Divergence)**: Starting around $t = 13$, the truncation error and physical floating-point noise compound exponentially. This constant-slope linear ascent in the logarithmic plot is a direct visual proof of the system's dominant positive Lyapunov exponent.
3. **Saturación (Saturation)**: Approaching $t = 40$, the error divergence reaches a limit around $10^1$. This maximum boundary is imposed purely by the finite geometric topology of the "butterfly" strange attractor.

## The Origin Trap (Trampa de Estado Absorbente)

During QST Measurement-based Block Encoding, we observed a mathematically fascinating phenomenon called an **Absorbing State Trap**. 

Because algorithms like Carleman Embeddings or Block Encoding require padding the vector with nonlinear cross terms (like $x_1 x_3 \approx 500$), the fundamental physical probabilities for $x, y, z$ suffer from **Amplitude Starvation**. Under finite statistical discretization (e.g., 20,000 shots), any chaotic crossing close to zero mathematically rounds to exactly $0$ counts. 

Since $(0,0,0)$ is a saddle-point equilibrium of the Lorenz continuous equations, truncating the variable to true absolute $0.0$ permanently zeroes the differential matrix. Consequently, the chaotic repulsion is neutralized and the system becomes perpetually "trapped" at the origin. 
**Mitigation:** We implement a $10^{-6}$ stochastic Microscopic Dithering to prevent physical dimensions from becoming flawlessly zero, restoring the true continuous topology on discrete quantum hardware.
