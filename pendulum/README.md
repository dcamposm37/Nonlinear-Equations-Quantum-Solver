# Pendulum Quantum Solvers

Quantum algorithms for solving the simple pendulum differential equation using various block-encoding techniques.

---

## Physical System

### Linear Pendulum

The linearized harmonic oscillator:

$$\ddot{\theta} + \omega^2 \theta = 0$$

where $\omega^2 = g/L$ (gravitational acceleration divided by pendulum length).

### Nonlinear Pendulum

The full nonlinear equation:

$$\ddot{\theta} + \frac{g}{L} \sin(\theta) = 0$$

---

## Classical Reference Solutions

All quantum solvers are benchmarked against classical discretizations implemented in `classical.py`:

### Forward Euler (Linear)

```python
def euler_linear(dt, w2, x0, y0, n_steps):
    """
    Discretization:
        θ_{n+1} = θ_n + Δt · θ̇_n
        θ̇_{n+1} = θ̇_n - Δt · ω² · θ_n

    This is the EXACT discretization that the LCU quantum circuit implements.  
    """
```

### Forward Euler (Nonlinear)

```python
def euler_nonlinear(dt, w2, x0, y0, n_steps):
    """
    Discretization:
        θ_{n+1} = θ_n + Δt · θ̇_n
        θ̇_{n+1} = θ̇_n - Δt · ω² · sin(θ_n)
    """
```

### Analytical Solution (Linear)

```python
def analytical_linear(w, x0, y0, t_values):
    """
    Exact closed-form solution:
        θ(t) = θ₀ cos(ωt) + (θ̇₀/ω) sin(ωt)
        θ̇(t) = θ̇₀ cos(ωt) - ω·θ₀ sin(ωt)
    """
```

### 4th-Order Runge-Kutta (Nonlinear)

High-accuracy classical reference for the nonlinear case:

```python
def rk4_nonlinear(dt, w2, x0, y0, n_steps):
    """Standard RK4 integration."""
```

---

## Common Quantum Initialization

### State Encoding

The 2D phase-space state $(\theta, \dot{\theta})$ is encoded in a single qubit using polar coordinates:

```python
norm = np.sqrt(x**2 + y**2)          # radial distance
theta = 2 * np.arctan2(y, x)          # Bloch sphere angle

# State preparation via Ry gate
qc.ry(theta, system_qubit)
```

This maps:
- $(x, y) \rightarrow |\psi\rangle$ on the Bloch sphere
- Phase space position ↔ quantum state amplitude

### Forward Euler as a Matrix

The Euler step can be written as matrix multiplication:

$$\mathbf{v}_{n+1} = A \cdot \mathbf{v}_n$$

where:

$$A = I + \Delta t \begin{pmatrix} 0 & 1 \\ -\omega^2 & 0 \end{pmatrix}$$       

For the nonlinear case, $\omega^2$ becomes position-dependent:

$$\omega^2_{\text{eff}}(x) = \frac{g}{L} \cdot \frac{\sin(x)}{x}$$

---

## Quantum Method Overview

### LCU (Linear Combination of Unitaries)

Decomposes matrix $A$ as:

$$A = c_0 I + c_1 (\pm X) + c_2 (ZX)$$

Circuit structure (3 qubits total):
- $q_0, q_2$: Ancillas for LCU superposition
- $q_1$: System qubit encoding $(\theta, \dot{\theta})$

```text
|0⟩ ─── PREP ──── SELECT ──── PREP† ─── measure ⟨0|
|ψ⟩ ─── ───── ──── Paulis ──── ───── ─── output
|0⟩ ─── PREP ──── SELECT ──── PREP† ─── measure ⟨0|
```

Post-selecting ancillas $= |00\rangle$ yields $A|\psi\rangle / \alpha$.        

### Rotation Gates

Unitary-only approach using Ry rotations:

- Encodes phase evolution in the rotation angle
- Naturally preserves $x^2 + y^2 = 1$ (norm conservation)
- For nonlinear: hybrid approach tracking amplitude classically

---

## Standard Parameters

- **DT = 0.001**          # Time step (linear)
- **DT = 0.003**          # Time step (nonlinear)
- **W2 = 9.8**            # $\omega^2 = g/L$ (rad/s)²
- **X0 = \pi / 2**        # Initial angle: 90° (nonlinear emphasis)
- **Y0 = 1.0**            # Initial velocity (linear)
- **Y0 = 0.0**            # Initial velocity (nonlinear, starts at rest)
- **N_STEPS = 5000**      # Simulation steps (linear)
- **N_STEPS = 1000**      # Simulation steps (nonlinear)

---

## Visualization

All solvers use `plot_results.py` to generate standardized 3-panel figures:      

1. Panel 1: $\theta(t)$ — position vs time
2. Panel 2: $\dot{\theta}(t)$ — velocity vs time
3. Panel 3: Phase space $(\theta, \dot{\theta})$

```python
from pendulum.plot_results import plot_pendulum_comparison

plot_pendulum_comparison(
    t_quantum, x_quantum, y_quantum,
    t_classical, x_classical, y_classical,
    title="LCU Linear Pendulum — Statevector",
    quantum_label="Quantum (Statevector)",
    classical_label="Classical (Euler)",
    save_path="figures/output.png",
)
```

---

## Solvers in this Directory

| Subdirectory | Method | Description |
| :--- | :--- | :--- |
| `pauli_lcu_linear/` | LCU Statevector | Exact quantum simulation of linear pendulum |
| `pauli_lcu_linear/` | LCU Measurements | Noisy reconstruction via QST |
| `pauli_lcu_nonlinear/`| LCU + $\omega^2_{\text{eff}}$ | Effective frequency trick for nonlinearity |
| `rotations_linear/` | Ry gates | Pure unitary evolution (linear) |
| `rotations_nonlinear/`| Hybrid | Classical amplitude + quantum phase |