# Rotation Gates: Linear Pendulum Solver

This directory implements the linear pendulum simulation using native **unitary rotation gates** on a 1-qubit register.

## 1. Unitary Mapping

Because the linear pendulum's phase space is circular ($x^2 + y^2 = 1$ in scaled coordinates), its time evolution is a pure rotation in $\mathbb{R}^2$. This is naturally mapped to a single-qubit unitary gate:

$$ U(\Delta \theta) = \exp(-i \sigma_y \Delta \theta) = \begin{pmatrix} \cos(\Delta \theta) & -\sin(\Delta \theta) \\ \sin(\Delta \theta) & \cos(\Delta \theta) \end{pmatrix} $$

where $\Delta \theta = - \omega \Delta t$.

### 1.1 Advantages
- **Strict Unitarity**: Unlike LCU or Block Encoding, this method has a success probability of $P=1$ (no post-selection or ancilla overhead).
- **Conserved Norm**: The quantum state naturally stays on the unit circle, matching the conservation of energy in the ideal linear pendulum.

## 2. Implementation Modes

### 2.1 Statevector (`rotations_linear_statevector.py`)
- Simulates the exact unitary rotation.
- Demonstrates perfect energy conservation across many cycles.

### 2.2 Measurement-Based (`rotations_linear_measurements.py`)
- Reconstructs $x$ and $y$ via 2-basis tomography ($Z$ for magnitudes, $X$ for relative sign).
- Shows how shot noise introduces jitter without the catastrophic "spiraling" decay seen in post-selected methods.

## 3. Usage

```bash
python -m pendulum.rotations_linear.rotations_linear_statevector
python -m pendulum.rotations_linear.rotations_linear_measurements
```
