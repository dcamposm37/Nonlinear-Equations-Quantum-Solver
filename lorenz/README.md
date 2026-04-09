# Quantum Solvers for the Lorenz System: NISQ vs. Fault-Tolerant Approaches

This directory contains two distinct quantum block-encoding solvers for the nonlinear Lorenz system. Both approaches transform the nonlinear differential equations into an augmented linear system via Carleman linearization and embed the resulting evolution matrix into a larger unitary operator via block encoding. However, they drastically differ in how they extract information from the final quantum state.

## 1. The Block Encoding Framework (Common Ground)

Both solvers follow the same algorithmic backbone for time-evolution:

1. **Carleman Linearization**: The nonlinear Lorenz equations are strictly mapped to a larger, closed linear subset by introducing auxiliary variables corresponding to the nonlinear terms (e.g., $xy$, $xz$).
2. **Euler Discretization**: A discrete-time transition matrix $A$ is constructed such that $\vec{v}(t+dt) \approx A \vec{v}(t)$.
3. **Similarity Transformation**: A diagonal scaling matrix $S$ is applied to safely bound amplitudes and prevent premature amplitude starvation in the quantum register: $A_{scaled} = S A S^{-1}$.
4. **Block Encoding**: Because the transition matrix $A_{scaled}$ is strictly non-unitary, it is embedded into a higher-dimensional unitary matrix $U$ (the "Oracle") using matrix square roots:
   $$ U = \begin{pmatrix} A_{scaled}/\alpha & \cdot \\ \cdot & \cdot \end{pmatrix} $$
   where $\alpha$ is a normalization factor ($\alpha \geq ||A_{scaled}||_2$).

---

## 2. Measurement-Based Approach (NISQ Era)
**File:** `solvers/block_encoding_measurements.py`

This approach relies on **stochastic sampling (hardware shots)**, modeling the execution flow of Noisy Intermediate-Scale Quantum (NISQ) devices.

*   **Amplitude Extraction**: The circuit is executed thousands of times, and all measurement operations are performed in the computational (Z) basis. The absolute magnitudes of the state variables ($x, y, z$) are reconstructed from the observed probability distributions.
*   **The Shot Noise Problem**: The estimator follows the standard quantum limit, meaning the estimation error scales as $\mathcal{O}(1/\sqrt{N_{shots}})$. To reduce the error by one order of magnitude, the required number of measurements increases quadratically.
*   **Noise Mitigation**: Given the high sensitivity to initial conditions inherent in chaotic systems like the Lorenz attractor, stochastic peaks in the sampling noise can easily destabilize the trajectory. This solver mitigates the problem using a **Predictor-Corrector Filter** to dampen statistical jitter and an **Adaptive Quantum Microscope** that dynamically boosts shot counts when amplitudes critically approach the finite hardware resolution floor.
*   **The Phase Reversal Protocol**: Z-basis measurements intrinsically destroy complex phase information (thereby losing mathematical signs). A classical continuity heuristic uses a local predictor to estimate the expected directional flow of the physical system, subsequently restoring the corresponding signs to the unsigned quantum magnitudes.

---

## 3. Iterative Quantum Amplitude Estimation (Fault-Tolerant Era)
**File:** `solvers/block_encoding_iqae.py`

This proof-of-concept (PoC) model anticipates the Fault-Tolerant Era, fundamentally replacing naive stochastic sampling with **Iterative Quantum Amplitude Estimation (IQAE)**.

### The Oracle and The Grover Operator
Let $\mathcal{A}$ be the composite operator performing the initial state preparation and applying the block-encoded unitary $U$. The fundamental goal is to precisely estimate the amplitude $a$ of a specified "target" subspace $|\Psi_1\rangle$:

$$ \mathcal{A}|0\rangle_{n+1} = \sqrt{a}|\Psi_1\rangle + \sqrt{1-a}|\Psi_0\rangle $$

where $a = \sin^2(\theta)$ for some intrinsic angle $\theta \in [0, \pi/2]$.

IQAE evaluates this via the Grover operator $Q$, defined mathematically as:

$$ Q = -\mathcal{A}\mathcal{S}_0\mathcal{A}^\dagger \mathcal{S}_\chi $$

where $\mathcal{S}_0$ is the reflection about the zero state and $\mathcal{S}_\chi$ is the reflection about the target state $|\Psi_1\rangle$. Iteratively applying $Q$ induces a deterministic rotation of the quantum state vector by an angle of exactly $2\theta$ per iteration step:

$$ Q^k \mathcal{A} |0\rangle = \sin((2k+1)\theta) |\Psi_1\rangle + \cos((2k+1)\theta) |\Psi_0\rangle $$

### Why IQAE is Superior: Reaching the Heisenberg Limit
*   **Algorithm Efficiency**: Standard Amplitude Estimation relies on Quantum Phase Estimation (QPE), demanding impractically deep circuits and many auxiliary qubits. Iterative QAE (IQAE) adaptively applies $Q^{k_i}$ for changing values of $k_i$ and employs classical statistical inference to tighten the confidence limits around $\theta$—eliminating the need for QPE entirely.
*   **Scaling Advantage**: The defining advantage of IQAE lies in shifting the fundamental error bound from the Standard Quantum Limit to the **Heisenberg Limit**. The error $\epsilon$ scales tightly as:
    $$ \epsilon \sim \mathcal{O}\left(\frac{1}{N_{queries}}\right) $$
    where $N_{queries}$ is the absolute number of oracle calls. Under this regime, reducing the error bound by a factor of 10 incurs only a $10\times$ linear increase in oracle calls, bypassing the heavy $\mathcal{O}(1/\epsilon^2)$ computational penalty of direct NISQ sampling.

### Implementation Details in the PoC
To circumvent the current computational impossibility of classically simulating deep IQAE circuits, `block_encoding_iqae.py` implements a hybrid simulation logic. It uses `qiskit.quantum_info.Statevector` to directly pull the exact algebraic amplitudes ("ideal fault-tolerant limit"). Simultaneously, it analytically estimates the strict theoretical oracle query cost: $N_{oracle} \approx \frac{\pi}{4 \epsilon_{target}}$. This computes the hardware cost a future fault-tolerant device would pay to sustain a $1\%$ relative error bound tracking the chaotic trajectory.

---

## References
1. Brassard, G., Hoyer, P., Mosca, M., & Tapp, A. (2002). Quantum Amplitude Amplification and Estimation. *Contemporary Mathematics*, 305, 53-74. [arXiv:quant-ph/0005055](https://arxiv.org/abs/quant-ph/0005055)
2. Grinko, A., Gacon, J., Zoufal, C., & Woerner, S. (2019). Iterative Quantum Amplitude Estimation. *npj Quantum Information*, 5(1), 1-6. [https://doi.org/10.1038/s41534-019-0230-z](https://doi.org/10.1038/s41534-019-0230-z)
3. Liu, J. P., Kothari, R., Novo, L., & Berry, D. W. (2021). Toward prospectively useful quantum algorithms for nonlinear differential equations. *PRX Quantum*, 2(4), 040321. [https://doi.org/10.1103/PRXQuantum.2.040321](https://doi.org/10.1103/PRXQuantum.2.040321)
