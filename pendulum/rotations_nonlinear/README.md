# Rotation Gates: Nonlinear Pendulum Solver

This directory implements a **hybrid quantum-classical algorithm** for the nonlinear pendulum.

## 1. The Challenge of Non-Unitarity

The nonlinear pendulum phase space is not circular; trajectories are elongated (pendular) or open (rotational) and do not strictly conserve the $L_2$ norm on a single 2D plane. Since quantum gates are strictly unitary, they cannot naturally describe this "amplitude stretch" on a single qubit.

## 2. Hybrid Methodology

We overcome this restriction via a decomposition of the dynamics:
1. **Classical Amplitude Prediction**: The algorithm calculates the target $L_2$ norm $\|\mathbf{v}_{n+1}\|$ classically at each step.
2. **Quantum Geometric Phase**: The intricate phase angle change $\Delta \theta$ is mapped to a calibrated `Ry` rotation gate.
3. **Rescaling**: The quantum measurement provides the components $x$ and $y$ on the unit circle, which are then rescaled by the classically predicted norm.

This allows simulating complex nonlinear oscillations on a single qubit without needing the ancillas or the probabilistic overhead of LCU.

## 3. Implementation Modes

### 3.1 Statevector (`rotations_nonlinear_statevector.py`)
- Demonstrates how the hybrid approach matches the exact Euler trajectory.

### 3.2 Measurement-Based (`rotations_nonlinear_measurements.py`)
- Reconstructs variables via QST with finite shots.
- Evaluates the stability of the hybrid normalization under stochastic sampling noise.

## 4. Usage

```bash
python -m pendulum.rotations_nonlinear.rotations_nonlinear_statevector
python -m pendulum.rotations_nonlinear.rotations_nonlinear_measurements
```
