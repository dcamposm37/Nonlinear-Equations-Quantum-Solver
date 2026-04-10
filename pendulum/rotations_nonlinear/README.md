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

## 4. Results

### Statevector (Exact)
![Rotation Nonlinear SV](figures/rotation_nonlinear_sv.png)

### Measurements (Noisy)
![Rotation Nonlinear Meas](figures/rotation_nonlinear_meas.png)

## 5. Usage

```bash
python -m pendulum.rotations_nonlinear.rotations_nonlinear_measurements
```

## 5. References

1. **Nielsen, M. A. & Chuang, I. L.** (2010). *Quantum Computation and Quantum Information*. Cambridge University Press. (Ch. 4: Basic unitary gates and circuit construction).
2. **Liu, J.-P., Kolden, H. O., Krovi, H. K., Loureiro, N. F., Trivisa, K., & Childs, A. M.** (2021). *Efficient quantum algorithm for dissipative nonlinear differential equations*. Proceedings of the National Academy of Sciences, 118(35). [arXiv:2011.03185](https://arxiv.org/abs/2011.03185) (Theoretical motivation for nonlinear ODE solvers on quantum hardware).
3. **Giovannetti, V., Lloyd, S., & Maccone, L.** (2011). *Advances in quantum metrology*. Nature Photonics, 5(4), 222-229. (Context for hybrid quantum-classical state estimation).
