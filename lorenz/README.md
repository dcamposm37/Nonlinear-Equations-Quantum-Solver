# Lorenz System Quantum Solvers

Quantum algorithms for solving the chaotic Lorenz system using block-encoding and LCU techniques.

---

## Physical System

The Lorenz system is a set of three coupled nonlinear ODEs:

$$\frac{dx}{dt} = \sigma (y - x)$$

$$\frac{dy}{dt} = x(\rho - z) - y$$

$$\frac{dz}{dt} = xy - \beta z$$

**Standard chaotic parameters**: $\sigma = 10$, $\rho = 28$, $\beta = 8/3$     

This system exhibits deterministic chaos with sensitive dependence on initial conditions (positive Lyapunov exponent).

---

## Classical Reference

### Forward Euler Discretization

Implemented in `classical.py`:

```python
def euler_lorenz(dt, sigma, rho, beta, x0, y0, z0, n_steps):
    """
    Explicit Euler update:
        x_{n+1} = x_n + dt·σ(y_n - x_n)
        y_{n+1} = y_n + dt·[x_n(ρ - z_n) - y_n]
        z_{n+1} = z_n + dt·(x_n·y_n - β·z_n)
    """
```

This is the exact discretization that all quantum solvers implement for fair comparison.

---

## Common Quantum Initialization

### State Vector Structure

The Lorenz system requires tracking both the physical variables and their nonlinear products:

$$\mathbf{v} = \begin{pmatrix} x \\ y \\ z \\ xz \\ xy \\ 1 \\ 1 \\ 1 \end{pmatrix}$$ 

- Elements 0-2: Physical coordinates $(x, y, z)$
- Element 3: Nonlinear product $xz$ (used in $\dot{y}$ equation)
- Element 4: Nonlinear product $xy$ (used in $\dot{z}$ equation)
- Elements 5-7: Padding constants for 8-dimensional space

### Euler Step Matrix

The linear part of the Euler update can be written as:

$$\mathbf{v}_{n+1} = A \cdot \mathbf{v}_n$$

```python
A = np.array([
    [1 - dt*sigma,  dt*sigma,    0,        0,    0,  0, 0, 0],   # x_{n+1}
    [dt*rho,        1 - dt,      0,       -dt,   0,  0, 0, 0],   # y_{n+1} (uses xz)  
    [0,             0,           1 - dt*beta, 0,  dt,  0, 0, 0], # z_{n+1} (uses xy)  
    [0,             0,           0,        1,    0,  0, 0, 0],   # Dummy
    [0,             0,           0,        0,    1,  0, 0, 0],   # Dummy
    [0,             0,           0,        0,    0,  1, 0, 0],   # Identity
    [0,             0,           0,        0,    0,  0, 1, 0],   # Identity
    [0,             0,           0,        0,    0,  0, 0, 1]    # Identity
])
```

### Nonlinear Update (Classical)

After each quantum linear step, the nonlinear products are updated classically:

```python
next_sv[3] = next_sv[0] * next_sv[2]  # xz = x · z
next_sv[4] = next_sv[0] * next_sv[1]  # xy = x · y
```

This hybrid approach separates:
- **Linear dynamics**: Quantum block-encoded matrix multiplication
- **Nonlinear terms**: Classical memory update

---

## Block Encoding Structure

All solvers use a common block-encoding pattern:

### Matrix Embedding

Given matrix $A$ with spectral norm $\alpha = \|A\|_2$, construct unitary $U$:   

$$U = \begin{pmatrix} A/\alpha & \sqrt{I - AA^\dagger}/\alpha \\ \sqrt{I - A^\dagger A}/\alpha & -A^\dagger/\alpha \end{pmatrix}$$

### Quantum Circuit

```text
|0_anc⟩ ─────── U_block ─────── measure ⟨0|
|ψ_sys⟩ ─────── U_block ─────── output
|ψ_sys⟩ ─────── U_block ─────── output
|ψ_sys⟩ ─────── U_block ─────── output
... (n qubits total)
```

Post-selecting ancilla $= |0\rangle$ yields $A|\psi\rangle / \alpha$.

### Implementation

```python
alpha = np.linalg.norm(A, 2)  # Spectral norm
A_norm = A / alpha

I = np.eye(dim)
term1 = scipy.linalg.sqrtm(I - A_norm @ A_norm.T)
term2 = scipy.linalg.sqrtm(I - A_norm.T @ A_norm)

U = np.block([
    [A_norm,  term1],
    [term2,  -A_norm.T]
])
```

---

## Similarity Scaling

To improve numerical stability, a similarity transformation is applied:        

```python
W = np.array([1/20, 1/30, 1/50, 1/1000, 1/600, 1.0, 1.0, 1.0])
S = np.diag(W)          # Scaling matrix
inv_S = np.diag(1.0 / W) # Inverse scaling

A_scaled = S @ A @ inv_S  # Scaled matrix (better conditioned)
```

This reduces the spectral norm without changing the physics.

---

## Standard Parameters

- **DT = 0.01**           # Time step
- **SIGMA = 10.0**        # Prandtl number
- **RHO = 28.0**          # Rayleigh number
- **BETA = 8.0 / 3.0**    # Geometric factor
- **X0, Y0, Z0 = 1.0, 1.0, 1.0**    # Initial conditions
- **T_FINAL = 10.0**      # Simulation time
- **N_STEPS = int(T_FINAL / DT)**    # Number of steps

---

## Visualization

All solvers use `plot_results.py` for standardized output:

### 3D Phase Space Plot
Trajectory in $(x, y, z)$ space showing the famous "butterfly" attractor.      

### 2D Projections
Three-panel figure with:
- XY plane: $y$ vs $x$
- XZ plane: $z$ vs $x$
- YZ plane: $z$ vs $y$

### Error Divergence Plot
Logarithmic plot of Euclidean distance:
$$d(t) = \sqrt{(x_{cl} - x_q)^2 + (y_{cl} - y_q)^2 + (z_{cl} - z_q)^2}$$       

Reveals three phases:
1. Initial fidelity: Error at floating-point precision floor
2. Lyapunov divergence: Exponential growth (positive Lyapunov exponent)        
3. Saturation: Bounded by attractor geometry

```python
from lorenz.plot_results import plot_lorenz_comparison

plot_lorenz_comparison(
    t_quantum, x_q, y_q, z_q,
    t_classical, x_cl, y_cl, z_cl,
    title="Lorenz Attractor — Block Encoding",
    quantum_label="Quantum",
    classical_label="Classical (Euler)",
    save_dir="figures/",
    prefix_name="output",
)
```

---

## Origin Trap Phenomenon

When using finite-shot measurements, variables can become exactly zero due to discretization. Since $(0, 0, 0)$ is a saddle-point equilibrium of the Lorenz equations, the system may become permanently trapped.

**Mitigation**: Apply stochastic micro-dithering:

```python
EPSILON = 1e-6
# Prevent exact zero
x = x if abs(x) > EPSILON else x + np.random.uniform(-EPSILON, EPSILON)        
```

---

## Solvers in this Directory

| Subdirectory | Method | Description |
| :--- | :--- | :--- |
| `block_encoding/` | `sqrtm` BE | Standard block-encoding via matrix completion |
| `pauli_lcu/` | Pauli-LCU | LCU with Pauli decomposition (optimized) |
| `sfable/` | S-FABLE | Sparse FABLE in Walsh-Hadamard basis |
| `fable/` | FABLE | Original FABLE block-encoding |
| `block_encoding_iqae/` | IQAE | Iterative Quantum Amplitude Estimation |
