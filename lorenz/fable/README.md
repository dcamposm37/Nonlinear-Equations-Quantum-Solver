# FABLE: Fast Approximate Block Encoding for Lorenz System

This directory implements the simulation of the **Lorenz attractor** using **FABLE** (Fast Approximate Block Encoding), an efficient technique for encoding matrices into quantum circuits. FABLE is particularly effective for matrices that are approximately unitary or have a clear block-unitary structure.

The chaotic 3D Lorenz system is described by:

$$\frac{dx}{dt} = \sigma(y - x)$$
$$\frac{dy}{dt} = x(\rho - z) - y$$
$$\frac{dz}{dt} = xy - \beta z$$

---

## 1. Files

| File | Description |
|---|---|
| `fable_statevector.py` | Exact simulation using the statevector method via the FABLE library. |

---

## 2. What is FABLE?

**FABLE** (Fast Approximate Block Encoding) is an algorithm that constructs quantum circuits to encode matrices efficiently. It is designed to exploit the structure of the target matrix (such as sparsity or near-unitarity) to minimize circuit depth.

### Key Advantages
- **Efficiency**: Significantly lower circuit depth compared to standard block encoding.
- **No Additional Ancilla Qubits**: Uses only the qubits required to represent the matrix.
- **Controlled Approximation**: Allows setting a "cutoff" threshold to prune small elements, further reducing complexity.

---

## 3. Algorithm Principle

### 3.1 Lorenz System Encoding
The 8×8 Euler evolution matrix $A$ is constructed as:

$$A = \begin{pmatrix} 
1-\Delta t \sigma & \Delta t \sigma & 0 & 0 & 0 & 0 & 0 & 0 \\ 
\Delta t \rho & 1-\Delta t & 0 & -\Delta t & 0 & 0 & 0 & 0 \\ 
0 & 0 & 1-\Delta t \beta & 0 & \Delta t & 0 & 0 & 0 \\ 
0 & 0 & 0 & 1 & 0 & 0 & 0 & 0 \\ 
0 & 0 & 0 & 0 & 1 & 0 & 0 & 0 \\ 
\vdots & \vdots & \vdots & \vdots & \vdots & \ddots & \vdots & \vdots
\end{pmatrix}$$

This includes auxiliary variables to capture technical nonlinearities (products $xz$ and $xy$).

### 3.2 Similarity Transformation
To ensure numerical stability on quantum hardware, a diagonal scaling is applied:
$$W = \text{diag}[1/20, 1/30, 1/50, 1/1000, 1/600, 1, 1, 1]$$
$$A_{\text{scaled}} = W \cdot A \cdot W^{-1}$$

### 3.3 Step-by-Step Evolution
For each time step:
1.  **State Preparation**: $|\psi_0\rangle = \text{scaled\_state} / \|\text{scaled\_state}\|$
2.  **Circuity Generation**: The FABLE compiler generates a circuit such that $U|0\rangle|\psi_0\rangle \approx |\Phi\rangle$, where the $|0\rangle$ sub-block contains $A_{scaled}$.
3.  **Amplitude Extraction**: Amplitudes are retrieved from the statevector where ancillas are in the $|0\rangle$ state.
4.  **Rescaling**: The variables are mapped back to their physical range: $x_{new} = |x_{sv}| \cdot 2^n \cdot \|A\| \cdot \|\text{state}\|$.

### 3.4 Structural Sign Heuristic
Since block-encoding typically provides magnitudes, signs are determined by temporal continuity (inertia):
- $\Delta x = \Delta t \cdot \sigma \cdot (y_{prev} - x_{prev})$
- $\text{sign}_x = +1$ if $(x_{prev} + \Delta x) \ge 0$, else $-1$.
- Auxiliary variables are updated as: $xz = \text{sign}_x \cdot \text{sign}_z \cdot |xz_{raw}|$.

---

## 4. Key Features
- **Measurement-Noise Free**: Uses the exact statevector simulator.
- **Circuit Optimization**: FABLE minimizes depth by exploiting matrix regularity.
- **Origin Trap Mitigation**: Initial conditions are padded to prevent zero-amplitude starvation at the saddle point.
- **Automatic Compression**: Elements smaller than the `FABLE_CUTOFF` (e.g., $10^{-4}$) are automatically ignored.

---

## 5. Usage

```bash
python -m lorenz.fable.fable_statevector
```

### Dependencies
```bash
pip install fable-circuits
```

---

## 6. Comparison: Standard Block Encoding vs. FABLE

| Aspect | Standard Block Encoding | FABLE |
|---|---|---|
| **Ancilla Qubits** | 1+ | 0 (data qubits only) |
| **Depth** | Higher | Lower (Optimized) |
| **Precision** | Exact (Unitary) | Approximate (Threshold-based) |
| **Construction** | Manual (Extended Matrix) | Automatic (Compiler-based) |
| **Compression** | No | Yes (Threshold Pruning) |

---

## 7. References
1. **Camps, E., et al.** (2022). *FABLE: Fast Approximate Block Encodings*. arXiv preprint.
2. **Lorenz, E. N.** (1963). *Deterministic Nonperiodic Flow*. Journal of the Atmospheric Sciences.
3. **Qiskit Contributors.** (2023). *Qiskit: An open-source framework for quantum computing*.
