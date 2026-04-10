# Comparative Analysis of Shot Noise Precision: Pauli-LCU vs. S-FABLE

This report analyzes the statistical precision and noise resilience of the two primary block-encoding methodologies implemented for the Lorenz system: **Pauli-LCU** and **S-FABLE**.

---

## 1. The Theoretical Framework: Standard Quantum Limit

In any measurement-based quantum algorithm, the reconstruction of physical variables $x_i$ depends on estimating amplitudes from a finite number of samples (shots). According to the **Standard Quantum Limit (SQL)**, the estimation error $\epsilon$ scales as:

$$\epsilon \propto \frac{1}{\sqrt{N_{\text{eff}}}}$$

Where $N_{\text{eff}}$ is the **effective number of successful samples**.

## 2. Effective Shot Count ($N_{eff}$)

Since both methods rely on post-selection (measuring an ancilla in the $|0\rangle$ state), not all $N_{\text{total}}$ shots contribute to the result. The effective count is:

$$N_{\text{eff}} = N_{\text{total}} \cdot P_{\text{success}}$$

The probability of success $P_{\text{success}}$ is the critical differentiator between these methods.

### 2.1 S-FABLE Success Probability

S-FABLE (and standard FABLE) normalizes the matrix $A$ by the dimension of the Hilbert space $2^n$ to ensure it can be embedded into a unitary. For the Lorenz system ($n=3$):

- **Normalization factor**: $\alpha = 2^n = 8$
- **Success Probability**: $P_{\text{S-FABLE}} \approx \frac{1}{\alpha^2} = \frac{1}{64} \approx \mathbf{0.0156}$

### 2.2 Pauli-LCU Success Probability

Pauli-LCU normalizes the matrix by the sum of the absolute values of the Pauli coefficients ($\lambda$). Because the Lorenz propagator is sparse and well-conditioned under similarity scaling:

- **Normalization factor**: $\lambda \approx 1.71$
- **Success Probability**: $P_{\text{LCU}} \approx \frac{1}{\lambda^2} \approx \frac{1}{2.92} \approx \mathbf{0.3424}$

---

## 3. The Precision Gap: A 4.6x Advantage

Comparing the two probabilities, we can calculate the ratio of effective samples for the same total shot budget (e.g., $N=100,000$):

- **S-FABLE effective shots**: $\sim 1,560$
- **Pauli-LCU effective shots**: $\sim 34,240$

The LCU method provides approximately **22 times more useful data** than S-FABLE for the same amount of physical hardware time. Applying this to the SQL error formula:

$$\frac{\epsilon_{\text{S-FABLE}}}{\epsilon_{\text{LCU}}} = \sqrt{\frac{P_{\text{LCU}}}{P_{\text{S-FABLE}}}} = \sqrt{\frac{0.3424}{0.0156}} \approx \mathbf{4.68}$$

> [!IMPORTANT]
> At equal shot budgets, **Pauli-LCU is approximately 4.7 times more precise** than S-FABLE. In terms of hardware resources, S-FABLE would need $\sim 22$ times more shots to reach the same level of precision as LCU.

---

## 4. Why this matters for the Lorenz System

The Lorenz system is chaotic. Small errors in the initial steps don't just add up; they multiply exponentially (Lyapunov divergence). 

1.  **Noise Floor**: The lower precision of S-FABLE means its "noise floor" is higher. The trajectory begins to diverge from the classical reference much earlier.
2.  **Origin Trap**: S-FABLE is significantly more susceptible to the "Origin Trap." Because its success probability is so low ($1.5\%$), it is much more likely that a variable with a small physical value (like $x=0.1$) returns **zero counts** and permanently traps the system at the equilibrium point.

## 5. Summary Table

| Metric | S-FABLE | Pauli-LCU | Advantage |
| :--- | :--- | :--- | :--- |
| **Ancilla Qubits** | 1 | 5 | S-FABLE (Width) |
| **Logic Basis** | Walsh-Hadamard | Pauli Sum | - |
| **Norm Factor** | $2^n = 8$ | $\lambda \approx 1.71$ | LCU (Stability) |
| **$P_{success}$** | ~1.5% | ~34% | **LCU (~22x)** |
| **Shot-Noise Error** | $\sim 4.7\sigma$ | $\sigma$ | **LCU (High Precision)** |

**Conclusion**: S-FABLE is a superior choice for **constrained hardware** (limited qubits), but Pauli-LCU is the superior choice for **simulating physical chaos** where statistical precision is the limiting factor.
