"""
Classical reference solutions for the pendulum system.
======================================================

Provides:
  - Forward Euler discretisation of the *linear* pendulum.
  - Exact analytical solution of the *linear* harmonic oscillator.
  - 4th-order Runge-Kutta integration of the *nonlinear* pendulum.

All functions return the same signature:
    (t_values, positions, velocities)
so that callers can treat them interchangeably.
"""

import numpy as np


def euler_linear(dt: float, w2: float, x0: float, y0: float,
                 n_steps: int):
    """
    Solve  ẍ + ω² x = 0  with the forward-Euler method.

    This is the *exact* discretisation that the LCU quantum circuit
    implements, so the statevector simulation should match it perfectly.

    Parameters
    ----------
    dt      : float – time step.
    w2      : float – ω² (square of the angular frequency).
    x0      : float – initial position θ₀.
    y0      : float – initial velocity θ̇₀.
    n_steps : int   – number of time steps.

    Returns
    -------
    t : ndarray of shape (n_steps+1,)
    x : ndarray of shape (n_steps+1,) – positions.
    y : ndarray of shape (n_steps+1,) – velocities.
    """
    t = np.array([i * dt for i in range(n_steps + 1)])
    x = np.zeros_like(t)
    y = np.zeros_like(t)
    x[0], y[0] = x0, y0

    for n in range(n_steps):
        x[n + 1] = x[n] + dt * y[n]
        y[n + 1] = y[n] + dt * (-w2 * x[n])

    return t, x, y


def euler_nonlinear(dt: float, w2: float, x0: float, y0: float,
                    n_steps: int):
    """
    Solve  ẍ + ω² sin(x) = 0  with the forward-Euler method.

    This is the discretisation that the *nonlinear* LCU quantum circuit
    implements (via the ω²_eff = ω²·sin(x)/x trick), so the statevector
    simulation should match it perfectly.

    Parameters
    ----------
    dt      : float – time step.
    w2      : float – ω² (g/L for a physical pendulum).
    x0      : float – initial position θ₀.
    y0      : float – initial velocity θ̇₀.
    n_steps : int   – number of time steps.

    Returns
    -------
    t : ndarray of shape (n_steps+1,)
    x : ndarray of shape (n_steps+1,) – positions.
    y : ndarray of shape (n_steps+1,) – velocities.
    """
    t = np.array([i * dt for i in range(n_steps + 1)])
    x = np.zeros_like(t)
    y = np.zeros_like(t)
    x[0], y[0] = x0, y0

    for n in range(n_steps):
        x[n + 1] = x[n] + dt * y[n]
        y[n + 1] = y[n] + dt * (-w2 * np.sin(x[n]))

    return t, x, y


def analytical_linear(w: float, x0: float, y0: float,
                      t_values):
    """
    Exact closed-form solution of the linear harmonic oscillator.

        x(t) = x₀ cos(ωt) + (y₀/ω) sin(ωt)
        y(t) = y₀ cos(ωt) − ω x₀ sin(ωt)

    Parameters
    ----------
    w        : float   – angular frequency ω = √(ω²).
    x0       : float   – initial position θ₀.
    y0       : float   – initial velocity θ̇₀.
    t_values : ndarray – time grid.

    Returns
    -------
    x : ndarray – positions.
    y : ndarray – velocities.
    """
    t = np.asarray(t_values)
    x = x0 * np.cos(w * t) + (y0 / w) * np.sin(w * t)
    y = y0 * np.cos(w * t) - w * x0 * np.sin(w * t)
    return x, y


def rk4_nonlinear(dt: float, w2: float, x0: float, y0: float,
                  n_steps: int):
    """
    Solve  ẍ + ω² sin(x) = 0  with the classic 4th-order Runge-Kutta.

    Parameters
    ----------
    dt      : float – time step.
    w2      : float – ω².
    x0      : float – initial position θ₀.
    y0      : float – initial velocity θ̇₀.
    n_steps : int   – number of time steps.

    Returns
    -------
    t : ndarray of shape (n_steps+1,)
    x : ndarray of shape (n_steps+1,) – positions.
    y : ndarray of shape (n_steps+1,) – velocities.
    """
    t = np.array([i * dt for i in range(n_steps + 1)])
    x = np.zeros_like(t)
    y = np.zeros_like(t)
    x[0], y[0] = x0, y0

    def f_x(_x, _y):
        return _y

    def f_y(_x, _y):
        return -w2 * np.sin(_x)

    for n in range(n_steps):
        k1x = dt * f_x(x[n], y[n])
        k1y = dt * f_y(x[n], y[n])

        k2x = dt * f_x(x[n] + k1x / 2, y[n] + k1y / 2)
        k2y = dt * f_y(x[n] + k1x / 2, y[n] + k1y / 2)

        k3x = dt * f_x(x[n] + k2x / 2, y[n] + k2y / 2)
        k3y = dt * f_y(x[n] + k2x / 2, y[n] + k2y / 2)

        k4x = dt * f_x(x[n] + k3x, y[n] + k3y)
        k4y = dt * f_y(x[n] + k3x, y[n] + k3y)

        x[n + 1] = x[n] + (k1x + 2 * k2x + 2 * k3x + k4x) / 6
        y[n + 1] = y[n] + (k1y + 2 * k2y + 2 * k3y + k4y) / 6

    return t, x, y
