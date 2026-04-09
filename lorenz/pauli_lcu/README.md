# Pauli-LCU: Linear Combination of Unitaries for the Lorenz System

This solver implements a **quantum block-encoding** of the Lorenz system's Euler evolution matrix using the **Linear Combination of Unitaries (LCU)** protocol with Pauli basis decomposition. It exploits the sparse algebraic structure of the physical matrix to achieve high-performance state tracking.

---

## 1. Theoretical Foundation

### 1.1 The LCU Lemma

The LCU lemma [1, 2] is a cornerstone of quantum algorithm design. Given any matrix $A$ that can be written as a weighted sum of unitary operators $\{U_j\}$:

$$A = \sum_{j=0}^{m-1} c_j \, U_j, \qquad c_j \in \mathbb{C}$$

there exists a quantum circuit $\mathcal{U}_{\text{LCU}}$ acting on an enlarged Hilbert space (system + ancilla qubits) such that the matrix $A/\lambda$ is **exactly** encoded in the ancilla-zero subblock:

$$\langle 0_{\text{anc}} | \, \mathcal{U}_{\text{LCU}} \, | 0_{\text{anc}} \rangle = \frac{A}{\lambda}$$

where $\lambda = \sum_j |c_j|$ is the **1-norm** of the coefficient vector. This factor $\lambda$ controls the **probability of success** of the block-encoding: $P_{\text{success}} \propto 1/\lambda^2$. Smaller $\lambda$ means higher success probability and fewer measurement shots required.

### 1.2 Why Pauli Strings as the Unitary Basis?

Any $2^n \times 2^n$ matrix admits a unique decomposition in the **Pauli basis** [3]:

$$A = \sum_{P \in \{I, X, Y, Z\}^{\otimes n}} c_P \, P, \qquad c_P = \frac{\text{Tr}(P \cdot A)}{2^n}$$

This choice is natural for quantum computing because:

- Every $n$-qubit Pauli string $P = \sigma_{i_1} \otimes \sigma_{i_2} \otimes \cdots \otimes \sigma_{i_n}$ is **unitary and Hermitian**, hence directly implementable as a quantum gate.
- The decomposition is **exact** (by completeness of the Pauli group as an operator basis).
- For structured/sparse matrices (such as our Euler step matrix), many coefficients $c_P$ vanish, yielding a compact decomposition with a small $\lambda$.

---

## 2. Circuit Architecture

The LCU circuit consists of three sub-routines applied sequentially on $n_{\text{anc}} + n_{\text{sys}}$ qubits:

```
|0>_anc  --- PREP ---- SELECT ---- PREP_dag --- <0| projection
|psi>_sys --- ---- ---- P_j's  ---- ----    --- output state
```

### 2.1 PREP (State Preparation)

The PREP unitary maps the ancilla register from $|0\rangle$ to a superposition encoding the coefficient magnitudes:

$$\text{PREP} \, |0\rangle_{\text{anc}} = \sum_{j=0}^{m-1} \sqrt{\frac{|c_j|}{\lambda}} \, |j\rangle_{\text{anc}}$$

In our implementation, PREP is constructed via a **Householder reflection** [4], which is a single unitary operator $H = I - 2\mathbf{v}\mathbf{v}^\dagger / \|\mathbf{v}\|^2$ that maps $|0\rangle$ exactly to the target state. This avoids the overhead of multi-level state preparation circuits.

### 2.2 SELECT (Controlled Pauli Application)

The SELECT operator conditionally applies the $j$-th Pauli string (with its phase factor) based on the ancilla register state:

$$\text{SELECT} = \sum_{j=0}^{m-1} e^{i\phi_j} \, |j\rangle\langle j|_{\text{anc}} \otimes P_j + \sum_{j=m}^{M-1} |j\rangle\langle j|_{\text{anc}} \otimes I_{\text{sys}}$$

where $\phi_j = \arg(c_j)$ absorbs the complex phase of each coefficient, and unused ancilla indices are padded with the identity to ensure unitarity.

### 2.3 Full LCU Operator

The complete block-encoding unitary is assembled as:

$$\mathcal{U}_{\text{LCU}} = \text{PREP}^\dagger \cdot \text{SELECT} \cdot \text{PREP}$$

By construction, $\mathcal{U}_{\text{LCU}}$ is unitary (product of three unitary operators), and satisfies the block-encoding relation:

$$\langle 0_{\text{anc}} | \, \mathcal{U}_{\text{LCU}} \, | 0_{\text{anc}} \rangle = \frac{1}{\lambda} \sum_j |c_j| \, e^{i\phi_j} \, P_j = \frac{A}{\lambda}$$

---

## 3. Application to the Lorenz System

### 3.1 Carleman Linearization

The nonlinear Lorenz equations are transformed into a closed linear system via truncated **Carleman linearization** [5, 6], introducing auxiliary variables $v_4 = xz$ and $v_5 = xy$ to capture the quadratic nonlinearities:

$$\vec{v} = (x, \, y, \, z, \, xz, \, xy, \, 0, \, 0, \, 0)^T$$

The Euler time-stepping then becomes a matrix-vector multiplication: $\vec{v}(t + dt) = A \cdot \vec{v}(t)$.

### 3.2 Similarity Transformation

A diagonal preconditioning matrix $S = \text{diag}(w_1, \ldots, w_8)$ is applied to balance the magnitudes of different state components and reduce the spectral radius of the scaled matrix:

$$A_{\text{scaled}} = S \, A \, S^{-1}$$

This is a standard similarity transformation that preserves the eigenvalues of $A$ while improving the numerical conditioning of the block-encoding.

### 3.3 Quantum Simulation Loop

At each Euler time step:

1. **Scale** the current physical state: $\vec{v}_{\text{sc}} = S \cdot \vec{v}$
2. **Normalize**: $|\psi\rangle = \vec{v}_{\text{sc}} / \|\vec{v}_{\text{sc}}\|$
3. **Embed** into the full Hilbert space: $|\Psi\rangle = |\psi\rangle_{\text{sys}} \otimes |0\rangle_{\text{anc}}$
4. **Evolve** through the LCU circuit: $|\Psi'\rangle = \mathcal{U}_{\text{LCU}} \, |\Psi\rangle$
5. **Project** onto ancilla $= |0\rangle$ and extract the system amplitudes
6. **Rescale**: multiply by $\lambda \cdot \|\vec{v}_{\text{sc}}\|$ and apply $S^{-1}$
7. **Re-enforce** auxiliary quadratic constraints: $v_4 \leftarrow xz$, $v_5 \leftarrow xy$

### 3.4 Implementation Details

| Parameter | Value |
|-----------|-------|
| System qubits ($n_{\text{sys}}$) | 3 |
| Ancilla qubits ($n_{\text{anc}}$) | 5 |
| Total qubits | 8 |
| Non-zero Pauli terms | 32 |
| LCU normalization ($\lambda$) | 1.7058 |
| Block-encoding error | $5.55 \times 10^{-16}$ |
| Unitarity error | $8.88 \times 10^{-16}$ |
| Simulation time (1000 steps) | ~0.15 s |

---

## 4. Shot-Based Measurement Protocol (NISQ Simulation)

The measurement-based implementation (`pauli_lcu_measurements.py`) replaces exact statevector extraction with **stochastic sampling**, modeling the execution flow of a physical quantum device.

### 4.1 Circuit Execution Model

At each time step, the full 8-qubit circuit is executed on `AerSimulator` [8] with a fixed number of shots $N_{\text{shots}}$. The circuit layout is:

1. **State Initialization**: The scaled, normalized physical state $|\psi\rangle$ is loaded into the system register (lowest 3 qubits), with the ancilla register (upper 5 qubits) initialized to $|0\rangle$.
2. **LCU Application**: The precomputed `UnitaryGate` is applied to all 8 qubits.
3. **Z-Basis Measurement**: All qubits are measured simultaneously in the computational basis (`measure_all`).

### 4.2 Post-Selection and Amplitude Reconstruction

From the resulting shot counts, only outcomes where the **ancilla bits are all zero** correspond to the physical subspace of the block-encoding [1, 2]. The empirical post-selection probability is:

$$P_{\text{success}} = \frac{N_{\text{anc}=0}}{N_{\text{shots}}}$$

For the Pauli-LCU with $\lambda = 1.706$, the theoretical success probability per step is $P \approx 1/\lambda^2 \approx 34\%$, meaning roughly 6,800 out of 20,000 shots survive post-selection -- providing ample statistics for amplitude reconstruction.

The physical amplitude magnitudes are reconstructed from the conditional probability distribution via Born's rule [9]:

$$|a_j| = \sqrt{p_j} \cdot \lambda \cdot \|\vec{v}_{\text{sc}}\|$$

where $p_j = N_j / N_{\text{anc}=0}$ is the conditional frequency of system outcome $j$ among the post-selected shots.

### 4.3 The Origin Trap Mitigation

A minimum detectable probability floor is enforced at $p_{\min} = 0.5 / N_{\text{shots}}$ to prevent amplitude starvation when a physical variable's probability drops below the shot-noise resolution. This hard-threshold prevents the **"Origin Trap"** where variables irreversibly collapse to zero due to statistical undersampling [10].

### 4.4 Sign Recovery via Eulerian Continuity Heuristic

Z-basis measurements intrinsically destroy phase information (the sign of each amplitude). A classical continuity heuristic recovers the signs using a one-step Euler predictor:

$$\text{sign}(x_{k+1}) = \text{sign}\left(x_k + dt \cdot f_x(x_k, y_k, z_k)\right)$$

where $f_x, f_y, f_z$ are the Lorenz vector field components. When a variable hits the shot-noise floor (zero measured counts), the sign from the previous time step is preserved to avoid spurious sign flips.

### 4.5 Shot-Noise Scaling

The estimation error for each amplitude component follows the **Standard Quantum Limit** [10]:

$$\epsilon_j \sim \mathcal{O}\left(\frac{1}{\sqrt{N_{\text{shots}} \cdot P_{\text{success}}}}\right)$$

The effective post-selected sample size is $N_{\text{eff}} = N_{\text{shots}} \cdot P_{\text{success}}$. For the Pauli-LCU this is $\sim 6{,}800$ effective samples per step (vs. $\sim 320$ for a generic $2^n$ block-encoding), leading to a **~4.6x reduction in statistical error** at equal shot budget.

### 4.6 Measurement Results

| Parameter | Value |
|-----------|-------|
| Shots per step | 20,000 |
| Post-selection probability | ~34% |
| Effective samples per step | ~6,800 |
| Simulation time (1000 steps) | ~58 s |
| Trajectory tracking | Active through all 1000 steps |

---

## 5. Qiskit Integration

### 5.1 Statevector Mode

The LCU unitary is constructed analytically via NumPy (Householder PREP + projector-based SELECT) and wrapped as a Qiskit `UnitaryGate` and `Operator`. Each time step is executed via:

```python
from qiskit.quantum_info import Operator, Statevector

lcu_op = Operator(lcu_unitary)          # Qiskit quantum operator
sv_in  = Statevector(full_state)        # Initial quantum state
sv_out = sv_in.evolve(lcu_op)           # Quantum circuit evolution
```

This is mathematically equivalent to running the 8-qubit circuit on `AerSimulator(method="statevector")`, but avoids the per-step overhead of Qiskit's transpiler decomposing the multi-controlled Pauli gates (which have 5 control qubits each).

### 5.2 Shot-Based Mode

The same `UnitaryGate` is reused in a standard `QuantumCircuit` with `measure_all()`, executed on `AerSimulator` with a configurable shot count:

```python
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

qc = QuantumCircuit(total_qubits)
qc.initialize(padded_state, range(total_qubits))
qc.append(lcu_gate, range(total_qubits))
qc.measure_all()

counts = AerSimulator().run(qc, shots=20000).result().get_counts()
```

---

## 6. Files

| File | Description |
|------|-------------|
| `pauli_lcu_statevector.py` | Exact statevector simulation (ideal quantum computer) |
| `pauli_lcu_measurements.py` | Shot-based simulation (NISQ hardware model, 20k shots) |
| `figures/` | Auto-generated comparison plots (3D attractor, 2D projections, error analysis) |
| `README.md` | This document |

---

## 7. References

1. **Childs, A. M. & Wiebe, N.** (2012). *Hamiltonian simulation using linear combinations of unitary operations*. Quantum Information & Computation, 12(11-12), 901-924. [arXiv:1202.5822](https://arxiv.org/abs/1202.5822)

2. **Berry, D. W., Childs, A. M., Cleve, R., Kothari, R., & Somma, R. D.** (2015). *Simulating Hamiltonian dynamics with a truncated Taylor series*. Physical Review Letters, 114(9), 090502. [arXiv:1412.4687](https://arxiv.org/abs/1412.4687)

3. **Nielsen, M. A. & Chuang, I. L.** (2010). *Quantum Computation and Quantum Information* (10th Anniversary Edition). Cambridge University Press. Ch. 4: The Pauli group as an operator basis for the space of $2^n \times 2^n$ matrices.

4. **Householder, A. S.** (1958). *Unitary Triangularization of a Nonsymmetric Matrix*. Journal of the ACM, 5(4), 339-342. Foundation for the Householder reflection used in our PREP construction.

5. **Liu, J.-P., Kolden, H. O., Krovi, H. K., Loureiro, N. F., Trivisa, K., & Childs, A. M.** (2021). *Efficient quantum algorithm for dissipative nonlinear differential equations*. Proceedings of the National Academy of Sciences, 118(35). [arXiv:2011.03185](https://arxiv.org/abs/2011.03185)

6. **Krovi, H.** (2023). *Improved quantum algorithms for linear and nonlinear differential equations*. Quantum, 7, 913. [arXiv:2202.01054](https://arxiv.org/abs/2202.01054)

7. **Gilyen, A., Su, Y., Low, G. H., & Wiebe, N.** (2019). *Quantum singular value transformation and beyond: exponential improvements for quantum matrix arithmetics*. Proceedings of the 51st Annual ACM STOC, 193-204. [arXiv:1806.01838](https://arxiv.org/abs/1806.01838) -- Establishes the block-encoding framework unifying LCU, quantum walk, and QSP.

8. **Qiskit Contributors.** (2023). *Qiskit: An open-source framework for quantum computing*. [doi:10.5281/zenodo.2573505](https://doi.org/10.5281/zenodo.2573505) -- AerSimulator backend for shot-based circuit simulation.

9. **Born, M.** (1926). *Zur Quantenmechanik der Stossvorgange*. Zeitschrift fur Physik, 37(12), 863-867. -- Born's rule: measurement outcome probabilities as squared amplitudes $p_j = |\langle j | \psi \rangle|^2$.

10. **Giovannetti, V., Lloyd, S., & Maccone, L.** (2006). *Quantum metrology*. Physical Review Letters, 96(1), 010401. [arXiv:quant-ph/0509179](https://arxiv.org/abs/quant-ph/0509179) -- Standard Quantum Limit and Heisenberg Limit for parameter estimation from quantum measurements.

