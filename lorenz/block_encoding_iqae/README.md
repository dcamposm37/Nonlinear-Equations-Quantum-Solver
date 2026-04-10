# Block Encoding with IQAE: Lorenz System

This directory implements the simulation of the **Lorenz attractor** using **Block Encoding** combined with **Iterative Quantum Amplitude Estimation (IQAE)**. This approach serves as a proof-of-concept for high-precision, **fault-tolerant** quantum computing.

The chaotic 3D Lorenz system is defined as:

$$\frac{dx}{dt} = \sigma(y - x)$$
$$\frac{dy}{dt} = x(\rho - z) - y$$
$$\frac{dz}{dt} = xy - \beta z$$

Where $\sigma = 10.0$ (Prandtl number), $\rho = 28.0$ (Rayleigh number), and $\beta = 8/3$.

---

## 1. Files

| File | Description |
|---|---|
| `block_encoding_iqae.py` | Simulation using iterative amplitude estimation (fault-tolerant proof-of-concept). |

---

## 2. Algorithm Principle

### 2.1 Euler Discretization
The linear propagator $A$ (8×8) is derived from the explicit Euler method:
- $x_{n+1} = x_n + dt \cdot \sigma \cdot (y_n - x_n)$
- $y_{n+1} = y_n + dt \cdot (x_n(\rho - z_n) - y_n)$
- $z_{n+1} = z_n + dt \cdot (x_ny_n - \beta z_n)$

### 2.2 Similarity Scaling
To prevent "precision starvation" in the quantum registers, the matrix is scaled by a diagonal matrix $W$:
$$A_{\text{scaled}} = W \cdot A \cdot W^{-1}$$
This balances the magnitudes of the linear coordinates ($x, y, z$) and the auxiliary nonlinear terms ($xz, xy$).

### 2.3 Unitary Block Encoding
The normalized matrix $A_{norm} = A_{scaled} / \|A\|_2$ is embedded into a larger unitary $U$:
$$U = \begin{pmatrix} A_{norm} & \sqrt{I - A_{norm}A_{norm}^\top} \\ \sqrt{I - A_{norm}^\top A_{norm}} & -A_{norm}^\top \end{pmatrix}$$
This construction requires **1 additional ancilla qubit**.

### 2.4 Iterative Quantum Amplitude Estimation (IQAE)
Instead of relying on direct noisy measurements (shots), this method simulates the IQAE limit:
1.  **Exact Probabilities**: Retrieves $P(i)$ from the statevector.
2.  **Resource Estimation**: Calculates the number of oracle queries $N_{oracle}$ needed to achieve a target relative error (e.g., 1%):
    $$N_{oracle} \approx \frac{\pi}{4 \epsilon}, \quad \epsilon = 0.01 \cdot \sqrt{P}$$
3.  **Reconstruction**: Variables are reconstructed as $\sqrt{P_i} \cdot \alpha \cdot \|state\|$.

### 2.5 Temporal Continuity (Sign Restoration)
IQAE provides the magnitude but not the sign of the variables. Signs are restored using a classical continuity heuristic:
- $\text{sgn}(x_{n+1}) = \text{sgn}(x_n + \Delta x_{Euler})$.

---

## 3. Key Features
- **Shot-Noise Free**: Simulates the near-infinite precision limit of fault-tolerant amplitude estimation.
- **Resource Profiling**: Theoretically predicts the number of Grover/Oracle queries required per step.
- **Fault-Tolerant POC**: Demonstrates the potential overhead and accuracy of simulation on future error-corrected hardware.
- **Single Ancilla**: Uses the standard block-encoding construction with minimal qubit overhead.

---

## 4. Usage

```bash
python -m lorenz.block_encoding_iqae.block_encoding_iqae
```

---

## 5. Comparison: Standard Block Encoding vs. IQAE

| Feature | Standard Block Encoding | Block Encoding + IQAE |
|---|---|---|
| **Measurement** | Direct (Shot Noise) | Estimated (Oracle-based) |
| **Hardware** | NISQ | Fault-Tolerant |
| **Precision** | Limited by $1/\sqrt{N_{shots}}$ | Limited by target $\epsilon$ |
| **Complexity** | $O(1/\epsilon^2)$ shots | $O(1/\epsilon)$ oracle queries |
| **Phase Info** | Required (QPE) | IQAE provides Magnitudes |

---

## 6. References
1. **Nielsen, M. A. & Chuang, I. L.** (2010). *Quantum Computation and Quantum Information*. Cambridge University Press.
2. **Suzuki, Y., et al.** (2020). *Amplitude Estimation without Phase Estimation*. Quantum Information Processing.
3. **Lorenz, E. N.** (1963). *Deterministic Nonperiodic Flow*. Journal of the Atmospheric Sciences.
