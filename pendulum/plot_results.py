"""
Standardised plotting for pendulum quantum simulations.
=======================================================

Provides a single function that generates the canonical 3-panel
comparison figure used throughout the project:

  Panel 1 – θ(t)    (position vs time)
  Panel 2 – θ̇(t)    (velocity vs time)
  Panel 3 – phase space  (θ vs θ̇)

All solvers call this function so that every figure in the
repository / paper has the same look and feel.
"""

import os
import numpy as np
import matplotlib.pyplot as plt


def plot_pendulum_comparison(
    t_quantum,
    x_quantum,
    y_quantum,
    t_classical,
    x_classical,
    y_classical,
    *,
    title: str = "Pendulum Simulation",
    quantum_label: str = "Quantum",
    classical_label: str = "Classical",
    save_path: str | None = None,
    show: bool = True,
):
    """
    Generate the standard 3-panel comparison plot.

    Parameters
    ----------
    t_quantum      : array-like – time grid for the quantum trajectory.
    x_quantum      : array-like – quantum positions θ.
    y_quantum      : array-like – quantum velocities θ̇.
    t_classical    : array-like – time grid for the classical reference.
    x_classical    : array-like – classical positions.
    y_classical    : array-like – classical velocities.
    title          : str        – figure super-title.
    quantum_label  : str        – legend label for quantum data.
    classical_label: str        – legend label for classical data.
    save_path      : str | None – if given, save figure to this path.
    show           : bool       – whether to call plt.show().

    Returns
    -------
    fig : matplotlib.figure.Figure
    """

    fig, axes = plt.subplots(1, 3, figsize=(12, 5))

    # --- Panel 1: position vs time ---
    axes[0].plot(t_quantum, x_quantum, "b-", label=quantum_label)
    axes[0].plot(t_classical, x_classical, "r--", label=classical_label)
    axes[0].set_xlabel("t")
    axes[0].set_ylabel(r"$\theta$")
    axes[0].set_title(r"Evolution of $\theta$")
    axes[0].legend()
    axes[0].grid(True)

    # --- Panel 2: velocity vs time ---
    axes[1].plot(t_quantum, y_quantum, "b-", label=quantum_label)
    axes[1].plot(t_classical, y_classical, "r--", label=classical_label)
    axes[1].set_xlabel("t")
    axes[1].set_ylabel(r"$\dot{\theta}$")
    axes[1].set_title(r"Evolution of $\dot{\theta}$")
    axes[1].legend()
    axes[1].grid(True)

    # --- Panel 3: phase space ---
    axes[2].plot(x_quantum, y_quantum, "b-", label=quantum_label)
    axes[2].plot(x_classical, y_classical, "r--", label=classical_label)
    axes[2].set_xlabel(r"$\theta$")
    axes[2].set_ylabel(r"$\dot{\theta}$")
    axes[2].set_title("Phase space")
    axes[2].legend()
    axes[2].grid(True)
    axes[2].set_aspect("equal")

    fig.suptitle(title, fontsize=14)
    fig.tight_layout()

    if save_path is not None:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        fig.savefig(save_path, dpi=150, bbox_inches="tight")
        print(f"[plot_results] Figure saved -> {save_path}")

    if show:
        plt.show()

    return fig
