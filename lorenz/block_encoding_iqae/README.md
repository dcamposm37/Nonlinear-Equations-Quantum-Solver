# Block Encoding IQAE (Iterative Quantum Amplitude Estimation)

This folder contains the `block_encoding_iqae.py` solver.

## Operation Principle
This solver acts as a Proof-of-Concept (PoC) for the Fault-Tolerant Era. It utilizes the same Carleman linearization and analytical `sqrtm` Block Encoding framework as the standard measurements solver.

Instead of extracting state amplitudes through stochastic samples, it uses **IQAE**, an advanced algorithm that applies the **Grover reflection operator** repeatedly to precisely estimate amplitudes.

## Fault-Tolerant Scaling
IQAE evades the Standard Quantum Limit ($\mathcal{O}(1/\sqrt{N})$) typical of basic measurements and reaches the **Heisenberg Limit**, where precision scales linearly with oracle query complexity ($\mathcal{O}(1/N)$).

The script uses exact `Statevector` simulations to analytically emulate an ideal fault-tolerant computer running IQAE. Concurrently, it calculates the theoretical number of Oracle calls (Grover iterations) needed in real hardware to maintain a bounded $1\%$ precision requirement per step, proving its superior feasibility over brute-force sampling for deep chaotic time evolutions.
