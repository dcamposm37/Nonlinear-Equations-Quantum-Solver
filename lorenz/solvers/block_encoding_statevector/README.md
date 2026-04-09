# Block Encoding Statevector

This folder contains the `block_encoding_statevector.py` solver.

## Operation Principle
This solver mathematically implements the exact quantum behavior bypassing the physical noise characteristics of quantum hardware entirely. 

It constructs the analytical `sqrtm` Block Encoded matrix and allows the differential equations to evolve perfectly over time by direct algorithmic extraction of probability amplitudes from Qiskit's `Statevector`. It is purely used to establish the idealized theoretical baseline for solving the Lorenz equations on a quantum computer, proving that the Carleman linearization and mapping correctly preserves the chaotic attractor structure over time if hardware constraints were removed.
