# Block Encoding ZNE (Zero-Noise Extrapolation)

This folder contains the `block_encoding_zne.py` solver.

## Operation Principle
Zero-Noise Extrapolation (ZNE) is a prominent error mitigation technique aimed at NISQ-era hardware. When running quantum circuits, inevitable gate errors accumulate. 

ZNE artificially increases the hardware noise logically (often by identity-folding circuits, adding noise levels) and evaluates the degraded results. By analyzing the trajectory of the error at noise points $N_1, N_2, N_3...$, classical statistical extrapolation techniques can trace the error curve backward towards the zero-noise limit to approximate an error-free readout.

This application pairs ZNE principles with the generalized nonlinear transition model, proving statistical noise resilience across extended numerical evolutions.
