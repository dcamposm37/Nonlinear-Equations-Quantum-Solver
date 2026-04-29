"""
Pauli-LCU Quantum Circuit -- Lorenz Attractor (Neural-EKF Mitigation)
=====================================================================

Extends pauli_lcu_obs.py with a Neural Extended Kalman Filter (Neural-EKF)
to mitigate shot noise in Pauli observable estimation.

Architecture:
  - NeuralCovarianceEstimator: MLP (sklearn) maps [x,y,z] -> diag(R_t)
    Pre-trained analytically on 100k phase-space samples.
  - LorenzEKF: 3D EKF with analytic Jacobian for covariance propagation.
  - USE_EKF toggle for A/B comparison.
"""

import os, sys, time, warnings, faulthandler
import numpy as np
faulthandler.enable()
warnings.filterwarnings("ignore", category=DeprecationWarning)

from sklearn.neural_network import MLPRegressor
import joblib

# -- Qiskit ----------------------------------------------------------------
from qiskit import QuantumCircuit, transpile
from qiskit.circuit import Parameter
from qiskit.circuit.library import UnitaryGate, RYGate
from qiskit_aer import AerSimulator
from qiskit.quantum_info import SparsePauliOp
from qiskit_aer.primitives import Estimator

# -- Project imports -------------------------------------------------------
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from lorenz.classical import euler_lorenz
from lorenz.plot_results import plot_lorenz_comparison
from lorenz.pauli_lcu.pauli_lcu_statevector import (
    pauli_decompose, build_lcu_unitary,
)

# ===========================================================================
# Global Parameters
# ===========================================================================
DT    = 0.01
SIGMA = 10.0
RHO   = 28.0
BETA  = 8.0 / 3.0

X0, Y0, Z0 = 1.0, 1.0, 1.0
T_FINAL = 8.0
N_STEPS = int(T_FINAL / DT)

SHOTS = 50000

SAVE_DIR = os.path.join(os.path.dirname(__file__), "figures")
os.makedirs(SAVE_DIR, exist_ok=True)

C_ANCHOR = 2.0

# -- Neural-EKF parameters ------------------------------------------------
USE_EKF          = True
Q_SCALE          = 1e-8
P0_SCALE         = 0.0
PRETRAIN_SAMPLES = 100_000
R_FLOOR          = 1e-10
PRETRAIN_CACHE   = os.path.join(os.path.dirname(__file__), "neural_cov_cache.pkl")


# ===========================================================================
# Neural Covariance Estimator
# ===========================================================================
class NeuralCovarianceEstimator:
    """MLP: [x, y, z] -> diagonal measurement noise covariance R_t."""

    def __init__(self, hidden_layers=(128, 64, 32), max_iter=2000, r_floor=R_FLOOR):
        self.model = MLPRegressor(
            hidden_layer_sizes=hidden_layers,
            activation='tanh',
            solver='adam',
            max_iter=max_iter,
            random_state=42,
        )
        self.r_floor = r_floor
        self._trained = False

    def pretrain(self, num_samples=100000, shots=50000, lam=1.706,
                 C_ANCHOR=2.0, S_diag=[1/20, 1/30, 1/50]):
        """Analytical pre-training: no quantum circuit execution needed."""
        X = np.random.uniform(
            low=[-25.0, -30.0, 0.0],
            high=[25.0, 30.0, 55.0],
            size=(num_samples, 3),
        )
        y_var = np.zeros((num_samples, 3))
        for i in range(num_samples):
            x_val, y_val, z_val = X[i]
            sv = np.array([x_val, y_val, z_val,
                           x_val*z_val, x_val*y_val, C_ANCHOR, 0.0, 0.0])
            S = np.diag([S_diag[0], S_diag[1], S_diag[2],
                         1/1000, 1/600, 1.0, 1.0, 1.0])
            norm = np.linalg.norm(S @ sv)
            factor_x = (lam * norm)**2 / (2 * C_ANCHOR * S_diag[0])
            factor_y = (lam * norm)**2 / (2 * C_ANCHOR * S_diag[1])
            factor_z = (lam * norm)**2 / (2 * C_ANCHOR * S_diag[2])
            base_variance = 0.25 / shots
            y_var[i, 0] = (factor_x**2) * base_variance
            y_var[i, 1] = (factor_y**2) * base_variance
            y_var[i, 2] = (factor_z**2) * base_variance
        self.model.fit(X, y_var)
        self._trained = True

    def predict(self, state):
        """Return R_t as 3x3 diagonal matrix from state [x, y, z]."""
        x = np.array(state).reshape(1, -1)
        if not self._trained:
            return np.diag(np.full(3, 0.5))
        variances = self.model.predict(x)[0]
        variances = np.maximum(variances, self.r_floor)
        return np.diag(variances)

    def save(self, path):
        joblib.dump({'model': self.model, 'trained': self._trained}, path)

    def load(self, path):
        if os.path.exists(path):
            data = joblib.load(path)
            self.model = data['model']
            self._trained = data['trained']
            return True
        return False


# ===========================================================================
# Extended Kalman Filter for Lorenz
# ===========================================================================
class LorenzEKF:
    """3D EKF with analytic Jacobian for the Lorenz system."""

    def __init__(self, x0, dt, sigma, rho, beta, Q_scale=Q_SCALE,
                 P0_scale=P0_SCALE):
        self.x = np.array(x0, dtype=float)   # state [x, y, z]
        self.dt = dt
        self.sigma = sigma
        self.rho = rho
        self.beta = beta
        self.P = np.eye(3) * P0_scale        # state covariance
        self.Q_base = np.eye(3) * Q_scale    # base process noise

    def _f(self, x):
        """Lorenz forward-Euler transition."""
        dt, s, r, b = self.dt, self.sigma, self.rho, self.beta
        return np.array([
            x[0] + dt * s * (x[1] - x[0]),
            x[1] + dt * (x[0] * (r - x[2]) - x[1]),
            x[2] + dt * (x[0] * x[1] - b * x[2]),
        ])

    def _jacobian(self, x):
        """Analytic Jacobian F_t = df/dx evaluated at x."""
        dt, s, r, b = self.dt, self.sigma, self.rho, self.beta
        return np.array([
            [1 - dt*s,       dt*s,        0          ],
            [dt*(r - x[2]),  1 - dt,      -dt*x[0]   ],
            [dt*x[1],        dt*x[0],     1 - dt*b   ],
        ])

    def predict(self):
        """EKF predict step with adaptive Q. Returns a-priori state estimate."""
        F = self._jacobian(self.x)
        x_next = self._f(self.x)
        
        # Adaptive Process Noise: scale by velocity magnitude
        velocity = (x_next - self.x) / self.dt
        vel_mag = np.linalg.norm(velocity)
        # Add small epsilon (1.0) to avoid Q becoming zero at fixed points
        adaptive_Q = self.Q_base * max(vel_mag, 1.0)
        
        self.x = x_next
        self.P = F @ self.P @ F.T + adaptive_Q
        return self.x.copy()

    def update(self, z_meas, R_t):
        """EKF update step. H = I (direct observation)."""
        # Innovation
        y = z_meas - self.x
        # Innovation covariance  S = P + R  (since H = I)
        S = self.P + R_t
        # Kalman gain
        K = self.P @ np.linalg.inv(S)
        # State update
        self.x = self.x + K @ y
        # Covariance update
        self.P = (np.eye(3) - K) @ self.P
        return self.x.copy()


# ===========================================================================
# Euler Matrix & Parametric Circuit (unchanged from pauli_lcu_obs.py)
# ===========================================================================
def build_euler_matrix(dt, sigma, rho, beta):
    return np.array([
        [1-dt*sigma, dt*sigma, 0,        0,  0, 0, 0, 0],
        [dt*rho,     1-dt,     0,       -dt,  0, 0, 0, 0],
        [0,          0,        1-dt*beta, 0,  dt, 0, 0, 0],
        [0,          0,        0,         1,   0, 0, 0, 0],
        [0,          0,        0,         0,   1, 0, 0, 0],
        [0,          0,        0,         0,   0, 1, 0, 0],
        [0,          0,        0,         0,   0, 0, 1, 0],
        [0,          0,        0,         0,   0, 0, 0, 1],
    ], dtype=float)


def build_parametric_template(n_sys, total_qubits, lcu_gate):
    theta_2    = Parameter('θ_2')
    theta_1_0  = Parameter('θ_1_0')
    theta_1_1  = Parameter('θ_1_1')
    theta_0_00 = Parameter('θ_0_00')
    theta_0_01 = Parameter('θ_0_01')
    theta_0_10 = Parameter('θ_0_10')
    params = [theta_2, theta_1_0, theta_1_1, theta_0_00, theta_0_01, theta_0_10]

    qc = QuantumCircuit(total_qubits)
    qc.ry(theta_2, 2)
    qc.append(RYGate(theta_1_0).control(1, ctrl_state='0'), [2, 1])
    qc.append(RYGate(theta_1_1).control(1, ctrl_state='1'), [2, 1])
    qc.append(RYGate(theta_0_00).control(2, ctrl_state='00'), [1, 2, 0])
    qc.append(RYGate(theta_0_01).control(2, ctrl_state='01'), [1, 2, 0])
    qc.append(RYGate(theta_0_10).control(2, ctrl_state='10'), [1, 2, 0])
    qc.append(lcu_gate, range(total_qubits))
    return qc, params


def compute_angles(v):
    norm_00 = np.hypot(v[0], v[1])
    norm_01 = np.hypot(v[2], v[3])
    norm_10 = np.hypot(v[4], v[5])
    norm_11 = 0.0
    norm_low  = np.hypot(norm_00, norm_01)
    norm_high = np.hypot(norm_10, norm_11)

    theta_2    = 2*np.arctan2(norm_high, norm_low) if np.hypot(norm_high, norm_low) > 0 else 0.0
    theta_1_0  = 2*np.arctan2(norm_01, norm_00)    if norm_low > 0 else 0.0
    theta_1_1  = 2*np.arctan2(norm_11, norm_10)    if norm_high > 0 else 0.0
    theta_0_00 = 2*np.arctan2(v[1], v[0])          if norm_00 > 0 else 0.0
    theta_0_01 = 2*np.arctan2(v[3], v[2])          if norm_01 > 0 else 0.0
    theta_0_10 = 2*np.arctan2(v[5], v[4])          if norm_10 > 0 else 0.0
    return [theta_2, theta_1_0, theta_1_1, theta_0_00, theta_0_01, theta_0_10]


# ===========================================================================
# Main
# ===========================================================================
def main():
    print("=" * 70)
    print("  Pauli-LCU Lorenz (Neural-EKF Shot Noise Mitigation)")
    print("=" * 70)
    print(f"  dt={DT}, T={T_FINAL}, steps={N_STEPS}, "
          f"shots={SHOTS if SHOTS is None else f'{SHOTS:,}'}")
    print(f"  USE_EKF={USE_EKF}, Q_SCALE={Q_SCALE:.0e}, P0_SCALE={P0_SCALE}\n")

    t_values = np.linspace(0, T_FINAL, N_STEPS + 1)

    # -- 1. Base Euler matrix -----------------------------------------------
    A = build_euler_matrix(DT, SIGMA, RHO, BETA)

    # -- 2. Similarity scaling ----------------------------------------------
    W = np.array([1/20, 1/30, 1/50, 1/1000, 1/600, 1.0, 1.0, 1.0])
    S     = np.diag(W)
    inv_S = np.diag(1.0 / W)
    A_scaled = S @ A @ inv_S

    # -- 3. Pauli decomposition ---------------------------------------------
    t0 = time.perf_counter()
    coeffs, pauli_ops, labels = pauli_decompose(A_scaled)
    t_decomp = time.perf_counter() - t0
    n_sys = 3
    lam   = float(np.sum(np.abs(coeffs)))
    print(f"  Pauli terms     : {len(coeffs)} non-zero  ({t_decomp*1e3:.1f} ms)")
    print(f"  Lambda (LCU)    = {lam:.4f}")

    # -- 4. LCU unitary -----------------------------------------------------
    t0 = time.perf_counter()
    lcu_unitary, n_anc, lam = build_lcu_unitary(coeffs, pauli_ops, 8)
    t_build = time.perf_counter() - t0
    total_qubits = n_anc + n_sys
    print(f"  LCU matrix built: {lcu_unitary.shape[0]}x{lcu_unitary.shape[1]}  "
          f"({t_build*1e3:.1f} ms)")
    print(f"  Ancilla={n_anc}, System={n_sys}, Total={total_qubits}\n")

    # -- 5. Pauli observables -----------------------------------------------
    P_0 = SparsePauliOp.from_list([("I", 0.5), ("Z", 0.5)])
    P_anc = P_0
    for _ in range(n_anc - 1):
        P_anc = P_anc.tensor(P_0)

    O_sys_x = SparsePauliOp.from_list([
        ("XIX", 0.25), ("XZX", 0.25), ("YIY", -0.25), ("YZY", -0.25)])
    O_sys_y = SparsePauliOp.from_list([
        ("XII", 0.25), ("XIZ", -0.25), ("XZI", 0.25), ("XZZ", -0.25)])
    O_sys_z = SparsePauliOp.from_list([
        ("XXX", 0.25), ("XYY", 0.25), ("YXY", -0.25), ("YYX", 0.25)])

    obs_x = P_anc.tensor(O_sys_x)
    obs_y = P_anc.tensor(O_sys_y)
    obs_z = P_anc.tensor(O_sys_z)

    # -- 6. Circuit template ------------------------------------------------
    lcu_gate  = UnitaryGate(lcu_unitary, label="Pauli_LCU")
    simulator = AerSimulator()

    print("  Building parametric circuit template...")
    t0_templ = time.perf_counter()
    template_qc, params = build_parametric_template(n_sys, total_qubits, lcu_gate)
    transpiled_template = transpile(template_qc, simulator, optimization_level=1)
    t_templ = time.perf_counter() - t0_templ
    print(f"  Template transpiled: depth={transpiled_template.depth()}, "
          f"gates={transpiled_template.size()}  ({t_templ:.1f} s)\n")

    # -- 6b. Estimator ------------------------------------------------------
    if SHOTS is None:
        estimator = Estimator(approximation=True)
        mode_label = "Estimator (exact statevector)"
    else:
        estimator = Estimator(run_options={"shots": SHOTS})
        mode_label = f"Estimator (shot-based, {SHOTS:,} shots)"

    # -- 7. Neural-EKF initialization ---------------------------------------
    if USE_EKF:
        neural_cov = NeuralCovarianceEstimator()
        loaded = neural_cov.load(PRETRAIN_CACHE)
        if loaded:
            print("  Neural covariance model loaded from cache.")
        else:
            print(f"  Pre-training Neural Covariance Estimator "
                  f"({PRETRAIN_SAMPLES:,} analytical samples)...")
            t0_pt = time.perf_counter()
            neural_cov.pretrain(
                num_samples=PRETRAIN_SAMPLES, shots=SHOTS, lam=lam,
                C_ANCHOR=C_ANCHOR, S_diag=[W[0], W[1], W[2]],
            )
            t_pt = time.perf_counter() - t0_pt
            print(f"  MLP trained in {t_pt:.1f} s")
            neural_cov.save(PRETRAIN_CACHE)
            print(f"  Model cached to {PRETRAIN_CACHE}\n")

        ekf = LorenzEKF(
            x0=[X0, Y0, Z0], dt=DT, sigma=SIGMA, rho=RHO, beta=BETA,
            Q_scale=Q_SCALE, P0_scale=P0_SCALE,
        )
        hx_raw, hy_raw, hz_raw = [X0], [Y0], [Z0]

    # -- 8. State vector initialization -------------------------------------
    current_sv = np.array(
        [X0, Y0, Z0, X0*Z0, X0*Y0, C_ANCHOR, 0.0, 0.0], dtype=float)
    hx, hy, hz = [X0], [Y0], [Z0]

    # -- 9. Time iteration loop ---------------------------------------------
    print(f"  Mode: {mode_label}")
    print(f"  Running {N_STEPS} steps "
          f"({SHOTS if SHOTS is None else f'{SHOTS:,}'} shots/step) ...")
    t0 = time.perf_counter()

    for step in range(N_STEPS):
        # 9a. Fix anchor
        current_sv[5] = C_ANCHOR

        # 9b. Scale & normalize
        current_sv_scaled = S @ current_sv
        norm = np.linalg.norm(current_sv_scaled)
        if norm == 0:
            initial_normalized = current_sv_scaled
        else:
            initial_normalized = current_sv_scaled / norm

        # 9c. Compute angles & bind
        angles = compute_angles(initial_normalized)
        param_dict = dict(zip(params, angles))
        bound_qc = transpiled_template.assign_parameters(param_dict)

        # --- EKF STEP 1: Predict ---
        if USE_EKF:
            x_prior = ekf.predict()
            R_t = neural_cov.predict(x_prior)

        # 9d. Quantum observation
        job = estimator.run(
            circuits=[bound_qc] * 3,
            observables=[obs_x, obs_y, obs_z],
        )
        values = job.result().values

        # 9e. Extract physical coordinates
        scale_factor = (lam * norm)**2 / (2 * C_ANCHOR)
        x_real = values[0] * scale_factor / (S[0,0] * S[5,5])
        y_real = values[1] * scale_factor / (S[1,1] * S[5,5])
        z_real = values[2] * scale_factor / (S[2,2] * S[5,5])

        # --- EKF STEP 4: Update ---
        if USE_EKF:
            hx_raw.append(x_real)
            hy_raw.append(y_real)
            hz_raw.append(z_real)

            z_meas = np.array([x_real, y_real, z_real])
            x_filtered = ekf.update(z_meas, R_t)
            x_real, y_real, z_real = x_filtered

        # 9f. Save filtered coordinates
        hx.append(x_real)
        hy.append(y_real)
        hz.append(z_real)

        # 9g. Strict algebraic reconstruction with filtered values
        current_sv[0] = x_real
        current_sv[1] = y_real
        current_sv[2] = z_real
        current_sv[3] = x_real * z_real   # recompute with filtered values
        current_sv[4] = x_real * y_real   # recompute with filtered values
        current_sv[5] = C_ANCHOR
        current_sv[6] = 0.0
        current_sv[7] = 0.0

        # 9h. Progress
        pct = 100 * step // N_STEPS
        tag = " [EKF]" if USE_EKF else ""
        print(f"\r  [{pct:3d}%]  step {step:4d}/{N_STEPS}  |  "
              f"x={x_real:+9.4f}  y={y_real:+9.4f}  z={z_real:+9.4f}{tag}",
              end="", flush=True)

    t_sim = time.perf_counter() - t0
    print(f"\n  [100%]  Done -- {t_sim:.1f} s  ({t_sim/N_STEPS*1e3:.1f} ms/step)\n")

    # -- 10. Classical reference --------------------------------------------
    x_q, y_q, z_q = np.array(hx), np.array(hy), np.array(hz)
    t_cl, x_cl, y_cl, z_cl = euler_lorenz(
        DT, SIGMA, RHO, BETA, X0, Y0, Z0, N_STEPS)

    # -- 11. RMSE summary ---------------------------------------------------
    n_pts = min(len(x_q), len(x_cl))
    rmse = lambda a, b: np.sqrt(np.mean((a[:n_pts] - b[:n_pts])**2))

    if USE_EKF:
        x_raw, y_raw, z_raw = np.array(hx_raw), np.array(hy_raw), np.array(hz_raw)
        print("  RMSE (raw vs classical):")
        print(f"    x={rmse(x_raw, x_cl):.6f}  y={rmse(y_raw, y_cl):.6f}  "
              f"z={rmse(z_raw, z_cl):.6f}")
        print("  RMSE (Neural-EKF vs classical):")
        print(f"    x={rmse(x_q, x_cl):.6f}  y={rmse(y_q, y_cl):.6f}  "
              f"z={rmse(z_q, z_cl):.6f}")
        rx = rmse(x_raw, x_cl) / max(rmse(x_q, x_cl), 1e-15)
        ry = rmse(y_raw, y_cl) / max(rmse(y_q, y_cl), 1e-15)
        rz = rmse(z_raw, z_cl) / max(rmse(z_q, z_cl), 1e-15)
        print(f"  Improvement factor: x={rx:.2f}x  y={ry:.2f}x  z={rz:.2f}x\n")
    else:
        print("  RMSE (quantum vs classical):")
        print(f"    x={rmse(x_q, x_cl):.6f}  y={rmse(y_q, y_cl):.6f}  "
              f"z={rmse(z_q, z_cl):.6f}\n")

    # -- 12. Plots ----------------------------------------------------------
    ekf_label = "Neural-EKF" if USE_EKF else "Quantum"
    plot_lorenz_comparison(
        t_values, x_q, y_q, z_q,
        t_cl, x_cl, y_cl, z_cl,
        title=f"Lorenz — Pauli-LCU ({ekf_label})",
        quantum_label=f"Quantum ({ekf_label})",
        classical_label="Classical (Euler)",
        save_dir=SAVE_DIR,
        prefix_name="lorenz_pauli_lcu_neural_ekf",
        show=False,
    )

    if USE_EKF:
        plot_lorenz_comparison(
            t_values, x_raw, y_raw, z_raw,
            t_cl, x_cl, y_cl, z_cl,
            title="Lorenz — Pauli-LCU (Raw, no EKF)",
            quantum_label="Quantum (raw)",
            classical_label="Classical (Euler)",
            save_dir=SAVE_DIR,
            prefix_name="lorenz_pauli_lcu_raw_no_ekf",
            show=False,
        )


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        import traceback
        traceback.print_exc()
        sys.exit(1)
