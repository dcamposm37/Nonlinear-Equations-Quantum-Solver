# Rotation Gates: Linear Pendulum Solver

This directory implements the quantum simulation of a **linear pendulum** (simple harmonic oscillator) using native unitary rotation gates on a 1-qubit register. The solver integrates the following second-order differential equation:

$$\ddot{x} + \omega_0^2 x = 0$$

Where:
- $x$ is the angular position $\theta$.
- $\omega_0 = \sqrt{g/L}$ is the natural frequency.
- $\ddot{x}$ is the angular acceleration.

---

## 1. Files

| File | Description |
|---|---|
| `rotations_linear_statevector.py` | Exact simulation using the statevector method (no measurement noise). |
| `rotations_linear_measurements.py`| Realistic simulation using **Quantum State Tomography (QST)** with 25,000 shots. |

---

## 2. Algorithm Principle

### 2.1 State Encoding

The physical state of the pendulum $(\theta, \dot{\theta})$ is mapped to a single qubit as:

$$|\psi\rangle = \tilde{x}|0\rangle + \tilde{y}|1\rangle$$

Where:
- $\tilde{x} = x / r$ is the normalized position.
- $\tilde{y} = \dot{x} / (\omega_0 r)$ is the scaled and normalized velocity.
- $r = \sqrt{x^2 + \tilde{y}^2}$ is the state norm (which remains constant in the linear case).

### 2.2 Temporal Evolution

Since the linear system conserves the $L_2$ norm (energy), its evolution is a pure rotation in the phase space plane:

1.  **Rotation Angle**: For each time step $\Delta t$, the state rotates by an angle:
    $$\Delta \phi = - \Delta t \cdot \omega_0$$
2.  **Unitary Operator**: The evolution is implemented using the standard $SO(2)$ rotation matrix (mapped to an $RY$ gate):
    $$R(\Delta \phi) = \begin{pmatrix} \cos(\Delta \phi) & -\sin(\Delta \phi) \\ \sin(\Delta \phi) & \cos(\Delta \phi) \end{pmatrix}$$
3.  **Step-by-Step**: The quantum state evolves as $|\psi(t+\Delta t)\rangle = R(\Delta \phi)|\psi(t)\rangle$.

---

## 3. Quantum State Tomography (QST) for 1 Qubit

The measurement-based solver reconstructs the continuous state from discrete binary outcomes using two different bases:

### 3.1 Z-Basis Measurement (Magnitudes)
- Measures probabilities in the computational basis $\{|0\rangle, |1\rangle\}$.
- Yields: $P(0) \approx |\tilde{x}|^2$ and $P(1) \approx |\tilde{y}|^2$.
- The absolute amplitudes are extracted as: $|\tilde{x}| = \sqrt{count_0 / shots}$.

### 3.2 X-Basis Measurement (Sign/Phase)
- Applies a **Hadamard (H)** gate before measurement.
- Yields the expectation value $\langle X \rangle = (count_0 - count_1) / shots$.
- This provides information about the relative phase: $\langle X \rangle = 2 \text{Re}(\tilde{x} \tilde{y})$.

### 3.3 Reconstruction Heuristic
1.  **Amplitudes**: Calculated from the Z-basis counts.
2.  **Relative Sign**: The sign of $\tilde{y}$ relative to $\tilde{x}$ is dictated by the sign of $\langle X \rangle$.
3.  **Spatial Continuity**: To resolve the global $\pm 1$ phase ambiguity, the algorithm compares the candidate states to the previous state's trajectory. The global sign that minimizes the distance in the phase space is selected.

---

## 4. Standard Parameters

| Parameter | Value | Description |
|---|---|---|
| `OMEGA_0` | 9.8 | Natural frequency $\sqrt{g/L}$ |
| `EPSILON` | 0.001 | Time step ($dt$) |
| `X0` | $\pi/2$ | Initial position (90 degrees) |
| `Y0` | 0.0 | Initial velocity |
| `N_STEPS` | 5000 | Number of simulation steps |
| `SHOTS` | 25,000 | QST sampling budget |

---

## 5. Results

### Statevector (Exact)
![Rotation Linear SV](figures/rotation_linear_sv.png)

### Measurements (Noisy)
![Rotation Linear Meas](figures/rotation_linear_meas.png)

---

## 6. Usage

```bash
# Exact simulation
python -m pendulum.rotations_linear.rotations_linear_statevector

# Measurement-based simulation
python -m pendulum.rotations_linear.rotations_linear_measurements
```

---

## 7. References

1. **Nielsen, M. A. & Chuang, I. L.** (2010). *Quantum Computation and Quantum Information*. Cambridge University Press.
2. **Born, M.** (1926). *Zur Quantenmechanik der Stossvorgange*. Zeitschrift fur Physik, 37(12), 863-867. (Amplitude extraction via Born's Rule).
3. **Qiskit Contributors.** (2023). *Qiskit: An open-source framework for quantum computing*.
