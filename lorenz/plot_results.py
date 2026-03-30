"""
Standardised plotting for Lorenz quantum simulations.
=====================================================

Provides functions to generate standard graphical output for the 
Lorenz system, including both 3D perspective plots and 2D panel 
projections.
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def plot_lorenz_comparison(
    t_quantum, x_quantum, y_quantum, z_quantum,
    t_classical, x_classical, y_classical, z_classical,
    *,
    title: str = "Lorenz System Simulation",
    quantum_label: str = "Quantum",
    classical_label: str = "Classical",
    save_dir: str,
    prefix_name: str,
    show: bool = True,
):
    """
    Generates two figures:
      1. A 3D phase-space trajectory overlay (Classical vs Quantum).
      2. A 1x3 grid of 2D projections (XY, XZ, YZ planes).

    Saves them as `<prefix_name>_3d.png` and `<prefix_name>_2d.png`.
    """
    os.makedirs(save_dir, exist_ok=True)
    
    # -----------------------------------------------------------------
    # Figure 1: 3D Attractor Overlay
    # -----------------------------------------------------------------
    fig3d = plt.figure(figsize=(8, 6))
    ax3d = fig3d.add_subplot(111, projection='3d')
    
    # Plot Classical underneath
    ax3d.plot(x_classical, y_classical, z_classical, 
              color='red', linestyle='--', alpha=0.7, label=classical_label)
    # Plot Quantum on top
    ax3d.plot(x_quantum, y_quantum, z_quantum, 
              color='blue', linestyle='-', alpha=0.8, label=quantum_label)
    
    ax3d.set_xlabel("X")
    ax3d.set_ylabel("Y")
    ax3d.set_zlabel("Z")
    ax3d.set_title(f"{title} (3D View)")
    ax3d.legend()
    
    fig3d.tight_layout()
    path_3d = os.path.join(save_dir, f"{prefix_name}_3d.png")
    fig3d.savefig(path_3d, dpi=150, bbox_inches="tight")
    print(f"[plot_results] 3D Figure saved -> {path_3d}")
    
    # -----------------------------------------------------------------
    # Figure 2: Standard 3-Panel 2D Projections (XY, XZ, YZ)
    # -----------------------------------------------------------------
    fig2d, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    # XY Plane
    axes[0].plot(x_quantum, y_quantum, 'b-', label=quantum_label)
    axes[0].plot(x_classical, y_classical, 'r--', label=classical_label)
    axes[0].set_xlabel("X")
    axes[0].set_ylabel("Y")
    axes[0].set_title("XY Projection")
    axes[0].grid(True)
    axes[0].legend()
    
    # XZ Plane
    axes[1].plot(x_quantum, z_quantum, 'b-', label=quantum_label)
    axes[1].plot(x_classical, z_classical, 'r--', label=classical_label)
    axes[1].set_xlabel("X")
    axes[1].set_ylabel("Z")
    axes[1].set_title("XZ Projection")
    axes[1].grid(True)
    axes[1].legend()

    # YZ Plane
    axes[2].plot(y_quantum, z_quantum, 'b-', label=quantum_label)
    axes[2].plot(y_classical, z_classical, 'r--', label=classical_label)
    axes[2].set_xlabel("Y")
    axes[2].set_ylabel("Z")
    axes[2].set_title("YZ Projection")
    axes[2].grid(True)
    axes[2].legend()
    
    fig2d.suptitle(f"{title} (2D Projections)", fontsize=14)
    fig2d.tight_layout()
    path_2d = os.path.join(save_dir, f"{prefix_name}_2d.png")
    fig2d.savefig(path_2d, dpi=150, bbox_inches="tight")
    print(f"[plot_results] 2D Projections saved -> {path_2d}")
    
    # -----------------------------------------------------------------
    # Figure 3: Euclidean Error Log Plot
    # -----------------------------------------------------------------
    fig_err, ax_err = plt.subplots(figsize=(8, 5))
    
    # Calculate Euclidean distance between quantum and classical trajectories
    # Ensure they are the same length
    min_len = min(len(x_quantum), len(x_classical))
    dist = np.sqrt(
        (x_classical[:min_len] - x_quantum[:min_len])**2 + 
        (y_classical[:min_len] - y_quantum[:min_len])**2 + 
        (z_classical[:min_len] - z_quantum[:min_len])**2
    )
    t_plot = t_quantum[:min_len]
    
    # Plot distance
    ax_err.plot(t_plot, dist, 'k-', label="Euclidean Distance (Classic vs Quantum)")
    
    # Avoid log(0) issues by capping the minimum display value or computing mean of first few steps appropriately
    # The block encoding algorithm generally introduces an error on step 1 > 0
    # Let's take the mean of the first 50 steps (or min_len/10 if trajectory is short) to be our "initial average error"
    initial_window = max(1, min_len // 50)
    initial_error_avg = np.mean(dist[1:initial_window+1]) if len(dist) > 1 else dist[0]
    # Fallback if somehow it's exact 0
    if initial_error_avg == 0:
        initial_error_avg = 1e-15
        
    ax_err.axhline(initial_error_avg, color='r', linestyle='--', 
                   label=f"Avg Initial Error ({initial_error_avg:.1e})")
    
    ax_err.set_yscale('log')
    ax_err.set_xlabel("Time (t)")
    ax_err.set_ylabel("Distance (Log Scale)")
    ax_err.set_title(f"{title} - Error Divergence")
    ax_err.grid(True, which="both", ls="-", alpha=0.2)
    ax_err.legend()
    
    fig_err.tight_layout()
    path_err = os.path.join(save_dir, f"{prefix_name}_error_log.png")
    fig_err.savefig(path_err, dpi=150, bbox_inches="tight")
    print(f"[plot_results] Error Log Plot saved -> {path_err}")
    
    if show:
        plt.show()

    return fig3d, fig2d, fig_err
