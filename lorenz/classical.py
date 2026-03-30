"""
Classical reference solutions for the Lorenz system.
====================================================

Provides:
  - Forward Euler discretisation of the Lorenz system (matching the 
    block-encoding quantum circuit directly).
"""

import numpy as np

def euler_lorenz(dt: float, sigma: float, rho: float, beta: float,
                 x0: float, y0: float, z0: float, n_steps: int):
    """
    Solve the Lorenz system using the forward-Euler method:
        dx/dt = sigma * (y - x)
        dy/dt = x * (rho - z) - y
        dz/dt = x * y - beta * z

    This implementation mirrors the exact discretisation enacted by 
    the block-encoding algorithm's `A` matrix.

    Parameters
    ----------
    dt      : float – time step (h).
    sigma   : float – Prandtl number.
    rho     : float – Rayleigh number.
    beta    : float – physical proportion.
    x0, y0, z0: float – initial coordinates.
    n_steps : int   – number of time steps.

    Returns
    -------
    t : ndarray of shape (n_steps+1,)
    x : ndarray of shape (n_steps+1,) 
    y : ndarray of shape (n_steps+1,)
    z : ndarray of shape (n_steps+1,)
    """
    t = np.array([i * dt for i in range(n_steps + 1)])
    x = np.zeros_like(t)
    y = np.zeros_like(t)
    z = np.zeros_like(t)
    
    x[0], y[0], z[0] = x0, y0, z0

    for n in range(n_steps):
        # Explicit Euler equations exactly as encoded in the quantum matrix A:
        # x_{n+1} = (1 - h*sigma)*x_n + h*sigma*y_n
        # y_{n+1} = h*rho*x_n + (1 - h)*y_n - h*(x_n * z_n)
        # z_{n+1} = (1 - h*beta)*z_n + h*(x_n * y_n)
        
        x[n + 1] = x[n] + dt * sigma * (y[n] - x[n])
        y[n + 1] = y[n] + dt * (x[n] * (rho - z[n]) - y[n])
        z[n + 1] = z[n] + dt * (x[n] * y[n] - beta * z[n])

    return t, x, y, z
