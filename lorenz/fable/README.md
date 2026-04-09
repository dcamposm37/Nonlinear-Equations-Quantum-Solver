# FABLE (Fast Approximate Block-Encodings)

This folder contains solvers that dynamically integrate the `fable-circuits` library framework (`fable_measurements.py` and `fable_statevector.py`).

## Operation Principle
The traditional algorithms in this repository apply an explicit analytical formulation relying on continuous components of the Hamiltonian equivalent (like `$scipy.linalg.sqrtm$`) to generate a theoretical Block Encoding mapping. However, this is only mathematical: translating matrices into explicit gate networks manually requires extensive overhead.

**FABLE** addresses this natively. Instead of explicit analytical operations on classical architectures, FABLE translates unstructured matrices sequentially into rotation angle thresholds (`Ry` gates) and `CNOT` connections dynamically optimized to emulate the initial classical probability transition perfectly within a scalable circuit limit.

Both `Statevector` simulations (exact depth tracking mapping) and `Measurements` frameworks exist to validate empirical accuracy within specific parameters of FABLE's precision bounds vs origin starvation cases.
