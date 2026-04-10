# Rotation Gates: Nonlinear Pendulum Solver

This directory implements a **hybrid quantum-classical algorithm** for the nonlinear pendulum using unitary rotation gates on a 1-qubit register. The solver integrates the full nonlinear ODE:

$$\ddot{x} + \omega_0^2 \sin(x) = 0$$

Where:
- $x$ is the angular position $\theta$ (large-angle regime, e.g., $\pi/2$).
- $\omega_0 = \sqrt{g/L}$ is the natural frequency.
- The $\sin(x)$ term introduces the essential physical nonlinearity.

---

## 1. Files

| File | Description |
|---|---|
| `rotations_nonlinear_statevector.py` | Exact simulation using the statevector method. |
| `rotations_nonlinear_measurements.py`| Simulation with **Quantum State Tomography (QST)** and shot noise. |

---

## 2. Hybrid Quantum-Classical Strategy

We overcome these restrictions via a **step-by-step delegation** protocol:

1.  **Classical Nonlinear Handling**: At each time-step $dt$, the classical processor computes the physically accurate non-linear update based on the Euler method: $v_{target} = v - dt \cdot \omega_0^2 \sin(x)$.
2.  **Phase Translation**: It then determines the **target geometric coordinate** $(\theta_{target}, \dot{\theta}_{target})$ and the required angular shift $\Delta \phi$.
3.  **Unitary Geometric Rotation**: This $\Delta \phi$ is passed to the quantum processor as a linear $RY$ gate. The quantum circuit performs the geometric rotation, carrying the state to the correct phase-plane location.
4.  **Classical Norm Restoration**: Since pure rotations preserve the radius, we **track the physical norm classically**. The quantum measurement provides the data on the unit circle, which is then re-scaled to the correct physical energy level (radius) predicted by the classical host.

---

## 3. Quantum State Tomography (QST) for 1 Qubit

The measurement-based solver (`measurements.py`) reconstructs the complex state amplitudes using two projections:

1.  **Z-Basis (Magnitudes)**: $\{|0\rangle, |1\rangle\}$ counts provide $|x|$ (position) and $|y|$ (velocity).
2.  **X-Basis (Relative Sign)**: A Hadamard-preceded measurement estimates $\langle X \rangle$, used to determine if the pendulum is moving "up" or "down" relative to its position.
3.  **Eulerian Continuity Restoration**: To resolve the global $\pm 1$ phase ambiguity without wasting ancillas, the algorithm selects the global sign that best aligns with the classical Euler prediction, ensuring a smooth trajectory.

---

## 4. Standard Parameters

| Parameter | Value | Description |
|---|---|---|
| `G_L` | 9.8 | $g/L$ (natural frequency squared) |
| `DT` | 0.003 | Simulation time step |
| `X0` | $\pi/2$ | Initial position (90 degrees - highly nonlinear) |
| `Y0` | 0.0 | Initial velocity |
| `N_STEPS` | 1000 | Number of simulation steps |
| `SHOTS` | 25,000 | QST sampling budget |

---

## 5. Results

### Statevector (Exact)
![Rotation Nonlinear SV](figures/rotation_nonlinear_sv.png)

### Measurements (Noisy)
![Rotation Nonlinear Meas](figures/rotation_nonlinear_meas.png)

---

## 6. Usage

```bash
# Exact simulation
python -m pendulum.rotations_nonlinear.rotations_nonlinear_statevector

# Measurement-based simulation
python -m pendulum.rotations_nonlinear.rotations_nonlinear_measurements
```

---

## 7. References

1. **Nielsen, M. A. & Chuang, I. L.** (2010). *Quantum Computation and Quantum Information*. Cambridge University Press.
2. **Liu, J.-P., et al.** (2021). *Efficient quantum algorithm for dissipative nonlinear differential equations*. PNAS, 118(35). [arXiv:2011.03185](https://arxiv.org/abs/2011.03185)
3. **Qiskit Contributors.** (2023). *Qiskit: An open-source framework for quantum computing*.
