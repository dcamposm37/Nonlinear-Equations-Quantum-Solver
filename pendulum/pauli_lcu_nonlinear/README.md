# Pauli-LCU: Nonlinear Pendulum Solver

This directory solves the full nonlinear pendulum equation using the LCU algorithm:

$$\ddot{x} + \frac{g}{L} \sin(x) = 0$$

## 1. The "Effective Frequency" Trick

Traditional LCU encodes linear operators. To solve the nonlinear $\sin(x)$ term, we define a position-dependent **effective frequency** $\omega^2_{\text{eff}}(x)$:

$$\omega^2_{\text{eff}}(x) = \frac{g}{L} \cdot \frac{\sin(x)}{x}$$

At each time step $n$, the algorithm:
1. Calculates $\omega^2_{\text{eff}}(x_n)$.
2. Updates the LCU coefficients $\{c_0, c_1, c_2\}$.
3. Re-prepares the `PREP` and `SELECT` operators with these dynamic coefficients.

This makes the one-step quantum evolution:
$$x_{n+1} = x_n + \Delta t \, y_n$$
$$y_{n+1} = y_n - \Delta t \, \omega^2_{\text{eff}}(x_n) \, x_n = y_n - \Delta t \frac{g}{L} \sin(x_n)$$

which is exactly the nonlinear forward-Euler discretization.

## 2. Implementation Modes

### 2.1 Statevector (`pauli_lcu_nonlinear_statevector.py`)
- Exact amplitude evolution.
- Demonstrates that the LCU circuit faithfully recovers the nonlinear trajectory when large swinging angles (e.g., $90^\circ$) make the $\sin(x) \approx x$ approximation fail.

### 2.2 Measurement-Based (`pauli_lcu_nonlinear_measurements.py`)
- Simulates shot noise and QST.
- **Sensitivity**: In the nonlinear regime, measurement noise in $x_n$ feeds back into the dynamic $\omega^2_{\text{eff}}$ calculation, potentially amplifying trajectory drift.

## 3. Usage

```bash
python -m pendulum.pauli_lcu_nonlinear.pauli_lcu_nonlinear_measurements
```

## 4. References

1. **Liu, J.-P., Kolden, H. O., Krovi, H. K., Loureiro, N. F., Trivisa, K., & Childs, A. M.** (2021). *Efficient quantum algorithm for dissipative nonlinear differential equations*. Proceedings of the National Academy of Sciences, 118(35). [arXiv:2011.03185](https://arxiv.org/abs/2011.03185)
2. **Krovi, H.** (2023). *Improved quantum algorithms for linear and nonlinear differential equations*. Quantum, 7, 913. [arXiv:2202.01054](https://arxiv.org/abs/2202.01054)
3. **Childs, A. M. & Wiebe, N.** (2012). *Hamiltonian simulation using linear combinations of unitary operations*. Quantum Information & Computation, 12(11-12), 901-924.
