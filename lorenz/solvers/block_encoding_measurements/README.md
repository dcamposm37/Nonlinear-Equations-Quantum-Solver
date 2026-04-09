# Block Encoding Measurements

This folder contains the `block_encoding_measurements.py` solver.

## Operation Principle
This solver is designed for Noisy Intermediate-Scale Quantum (NISQ) devices. It resolves the nonlinear Lorenz system by first linearizing it via Carleman linearization, embedding the resulting non-unitary matrix evolution step into a larger unitary Operator $U$ (Block Encoding using the standard analytical `sqrtm` method), and retrieving the state sequentially over time.

## Measurement and Sampling
Information extraction models physical quantum hardware, utilizing **stochastic sampling (Z-basis measurements)**. Since probabilities dictate the state amplitudes ($\sqrt{P} \propto \text{amplitude}$), this method scales poorly with error requirements ($\mathcal{O}(1/\sqrt{N_{shots}})$).

To combat the "Origin Trap" phenomenon (where amplitudes drop below the statistical noise floor), this algorithm avoids zero-padding overhead and focuses all measurements exclusively on the active system variables.

The sign (+/-) of each variable, which is necessarily lost during quantum measurement, is reconstructed dynamically at each step using a classical continuity heuristic based strictly on Eulerian inertia.
