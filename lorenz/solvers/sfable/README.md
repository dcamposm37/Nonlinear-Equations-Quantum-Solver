# S-FABLE (Sparse FABLE)

This folder contains solvers implementing the Sparse block-encoding architecture (`sfable_measurements.py`, `sfable_measurements_shots.py`, and `sfable_statevector.py`).

## Operation Principle
Based on the paper *S-FABLE and LS-FABLE: Fast approximate block-encoding algorithms for unstructured sparse matrices* (arXiv:2401.04234). 

Ordinary FABLE implementations can scale inefficiently when provided sparsely distributed, unstructured elements (like the specific Euler-discretized representation of the Lorenz Attractor space). The core advantage of **S-FABLE** is the transposition of state distributions.

It operates by performing standard FABLE block-encodings, but directly on a conjugated **Walsh-Hadamard manifold**: $M = H^{\otimes n} \cdot A \cdot H^{\otimes n}$. Since Eulerian transitions show high structural sparsity in the Hadamard basis, the internal FABLE compiler can easily eliminate (prune) trivial Y-rotations (e.g., `< 1e-4`). 

The original Cartesian state representations are recovered by geometrically mapping $H^{\otimes n}$ around the data register bounding the optimized circuit operations:
$$ Circuit = (I \otimes H^{\otimes n}) · FABLE(M) · (I \otimes H^{\otimes n}) $$

This achieves drastically reduced circuit depths while preserving mathematical coherence. The Statevector implementation highlights depth savings, while the Measurements simulations show physical viability over stochastic constraints.
