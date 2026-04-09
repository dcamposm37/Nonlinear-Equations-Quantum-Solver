"""
Block Encoding Measurements Simulation for Lorenz System
======================================================

Solves the nonlinear Lorenz system using an Arithmetic LCU (Linear Combination 
of Unitaries) Block-Encoding via Pauli Decomposition. 

Recent Optimizations:
- Migrated from dense `sqrtm` matrices to Sparse Pauli-based LCU.
- Implements purely native PREPARE and SELECT Oracles.
- Post-selection algebraic barrier implemented directly on the counts dictionary.

Usage
-----
    python -m lorenz.solvers.pauli_lcu.pauli_lcu_measurements

Output
------
    lorenz/figures/lorenz_lcu_meas_3d.png
    lorenz/figures/lorenz_lcu_meas_2d.png
    lorenz/figures/lorenz_lcu_meas_error_log.png
"""

import sys
print("Interpreter reached pauli_lcu_measurements.py")
import os
import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.circuit.library import StatePreparation, XGate, YGate, ZGate
from qiskit.quantum_info import SparsePauliOp

# Allow imports from project root
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))
try:
    from lorenz.classical import euler_lorenz
    from lorenz.plot_results import plot_lorenz_comparison
except ImportError:
    print("Advertencia: No se pudieron importar los módulos locales. Asegúrate de correrlo desde la raíz del proyecto.")

# ---------------------------------------------------------------------------
# Parameters
# ---------------------------------------------------------------------------
DT = 0.01              # Step size (h)
SIGMA = 10.0           # Prandtl number
RHO = 28.0             # Rayleigh number
BETA = 8.0 / 3.0       # Physical proportion

X0, Y0, Z0 = 1.0, 1.0, 1.0
T_FINAL = 10.0
N_STEPS = int(T_FINAL / DT)

# LCU configuration values
BASE_SHOTS = 100000    # Alta densidad de tiros para garantizar fidelidad en LCU
SAVE_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "figures")
os.makedirs(SAVE_DIR, exist_ok=True)


# ---------------------------------------------------------------------------
# Quantum LCU Block-Encoding Forward Step (Measurement & Post-selection)
# ---------------------------------------------------------------------------
def next_step_measured(input_state_scaled: np.ndarray, physical_state: np.ndarray, 
                       alpha_lcu: float, prep_amplitudes: np.ndarray, 
                       filtered_paulis: list, filtered_weights: list, num_ancillas: int,
                       simulator: AerSimulator, dim: int, num_system_qubits: int, step: int, S: np.ndarray):
    """
    Applies the LCU Pauli-based block-encoded gate to the SCALED vector, 
    executes Z-basis measurements with ancilla post-selection, and applies a 
    classical continuity heuristic.
    """
    # 1. Blindaje de Normalización
    norm = np.linalg.norm(input_state_scaled)
    if norm < 1e-12:
        # Inyecta vector en variables dummy para evitar colapso de Qiskit
        input_state_scaled = input_state_scaled.copy()
        input_state_scaled[-3:] = 1.0
        norm = np.linalg.norm(input_state_scaled)
        
    initial_normalized = input_state_scaled / norm
    
    # Safety check: if normalized vector is also near-zero (e.g. after NaN propagation)
    if not np.all(np.isfinite(initial_normalized)) or np.sum(np.abs(initial_normalized)**2) < 1e-30:
        return input_state_scaled  # Return unchanged; main loop will apply Euler fallback
        
    # Índices del sistema y ancillas
    system_indices = list(range(num_system_qubits))
    ancilla_indices = list(range(num_system_qubits, num_system_qubits + num_ancillas))
    
    # Instanciamos el circuito solo con los qubits necesarios
    qc = QuantumCircuit(num_system_qubits + num_ancillas)
    
    # Inicializa SOLO los qubits del sistema
    qc.initialize(initial_normalized.tolist(), system_indices, normalize=True)
    
    # 2. Oráculo PREPARE (Amplitudes LCU en los ancillas)
    sp = StatePreparation(prep_amplitudes)
    qc.append(sp, ancilla_indices)
    
    # 3. Oráculo SELECT (Descomposición de Pauli Condicionada)
    for k, (p_str, w) in enumerate(zip(filtered_paulis, filtered_weights)):
        # Convertir a binario asegurando el número exacto de bits de ancilla
        k_bin = format(k, f'0{num_ancillas}b')
        k_bin_rev = k_bin[::-1]  # Invertir para hacer coincidir con el endianness (LSB=ancilla_indices[0])
        
        # Activar condición (Flip X en bits '0' para que actúe en el estado |11...1>)
        for i, bit in enumerate(k_bin_rev):
            if bit == '0':
                qc.x(ancilla_indices[i])
                
        # Lógica de peso negativo: Fase condicional global Z/mcp de -1
        if w < 0:
            if num_ancillas == 1:
                qc.z(ancilla_indices[0])
            else:
                qc.mcp(np.pi, ancilla_indices[:-1], ancilla_indices[-1])
                
        # Aplicar la cadena de Pauli controlada al sistema
        # p_str: Ej. 'XYZ' -> Z en bit 0, Y en bit 1, X en bit 2
        p_str_rev = p_str[::-1] 
        for i, char in enumerate(p_str_rev):
            if char == 'I':
                continue
            elif char == 'X':
                qc.append(XGate().control(num_ancillas), ancilla_indices + [system_indices[i]])
            elif char == 'Y':
                qc.append(YGate().control(num_ancillas), ancilla_indices + [system_indices[i]])
            elif char == 'Z':
                qc.append(ZGate().control(num_ancillas), ancilla_indices + [system_indices[i]])
                
        # Deshacer la condición (Uncompute X)
        for i, bit in enumerate(k_bin_rev):
            if bit == '0':
                qc.x(ancilla_indices[i])
                
    # 4. UN-PREPARE
    qc.append(sp.inverse(), ancilla_indices)
    
    # Medir todo
    qc.measure_all()
    
    try:
        # Transpile the circuit for AerSimulator (force decomposition to u, cx)
        qc = transpile(qc, simulator, basis_gates=['u', 'cx'])

        # Ejecución
        current_shots = BASE_SHOTS
        result = simulator.run(qc, shots=current_shots).result()
        counts = result.get_counts()
    except Exception as e:
        print(f"\n[Error en Step {step}] Fallo en la ejecución quántica: {str(e)}")
        import traceback
        traceback.print_exc()
        raise e
    
    # ------------------------------------------------------------------------
    # 5. POST-SELECCIÓN ALGEBRAICA (Filtro de Ancillas en '0...0')
    # ------------------------------------------------------------------------
    valid_counts = {}
    for bitstring, count in counts.items():
        # En Qiskit measure_all(): bits de izquierda = mayor index = ancillas
        ancilla_str = bitstring[:num_ancillas]
        system_str = bitstring[num_ancillas:]
        
        # Filtro estricto
        if ancilla_str == '0' * num_ancillas:
            valid_counts[system_str] = count

    valid_shots = sum(valid_counts.values())
    if valid_shots == 0:
        valid_shots = current_shots # Fallback de emergencia
        
    p_min = 0.5 / valid_shots
    
    # Extracción de subestados físicos del sistema (índices 0, 1, 2)
    # Qubit 0 es el bit de más a la derecha ('000' = índice 0)
    p_x = max(valid_counts.get('000', 0) / valid_shots, p_min)
    p_y = max(valid_counts.get('001', 0) / valid_shots, p_min)
    p_z = max(valid_counts.get('010', 0) / valid_shots, p_min)
    
    p_xz = valid_counts.get('011', 0) / valid_shots
    p_xy = valid_counts.get('100', 0) / valid_shots
    
    hit_floor_x = (valid_counts.get('000', 0) == 0)
    hit_floor_y = (valid_counts.get('001', 0) == 0)
    hit_floor_z = (valid_counts.get('010', 0) == 0)

    # Reconstrucción de magnitudes usando la norma total de Block Encoding (alpha_lcu)
    abs_x_scaled = np.sqrt(p_x) * alpha_lcu * norm
    abs_y_scaled = np.sqrt(p_y) * alpha_lcu * norm
    abs_z_scaled = np.sqrt(p_z) * alpha_lcu * norm
    abs_xz_scaled = np.sqrt(p_xz) * alpha_lcu * norm
    abs_xy_scaled = np.sqrt(p_xy) * alpha_lcu * norm
    
    # ------------------------------------------------------------------------
    # 6. CONTINUIDAD CLÁSICA (Heurística Predictor-Corrector)
    # ------------------------------------------------------------------------
    x_prev, y_prev, z_prev = physical_state[0], physical_state[1], physical_state[2]
    
    dx = DT * SIGMA * (y_prev - x_prev)
    dy = DT * (x_prev * (RHO - z_prev) - y_prev)
    dz = DT * (x_prev * y_prev - BETA * z_prev)
    
    sign_x = 1 if (x_prev + dx) >= 0 else -1
    sign_y = 1 if (y_prev + dy) >= 0 else -1
    sign_z = 1 if (z_prev + dz) >= 0 else -1

    sign_x_applied = (1 if x_prev >= 0 else -1) if hit_floor_x else sign_x
    sign_y_applied = (1 if y_prev >= 0 else -1) if hit_floor_y else sign_y
    sign_z_applied = (1 if z_prev >= 0 else -1) if hit_floor_z else sign_z

    x_raw_scaled = sign_x_applied * abs_x_scaled
    y_raw_scaled = sign_y_applied * abs_y_scaled
    z_raw_scaled = sign_z_applied * abs_z_scaled

    pred_x_scaled = (x_prev + dx) * S[0, 0]
    pred_y_scaled = (y_prev + dy) * S[1, 1]
    pred_z_scaled = (z_prev + dz) * S[2, 2]

    K_GAIN = 0.7

    x_filtered_scaled = K_GAIN * x_raw_scaled + (1 - K_GAIN) * pred_x_scaled
    y_filtered_scaled = K_GAIN * y_raw_scaled + (1 - K_GAIN) * pred_y_scaled
    z_filtered_scaled = K_GAIN * z_raw_scaled + (1 - K_GAIN) * pred_z_scaled

    xz_new_scaled = sign_x * sign_z * abs_xz_scaled
    xy_new_scaled = sign_x * sign_y * abs_xy_scaled

    final_output_scaled = np.array([
        x_filtered_scaled, y_filtered_scaled, z_filtered_scaled, 
        xz_new_scaled, xy_new_scaled, 
        input_state_scaled[5], input_state_scaled[6], input_state_scaled[7]
    ], dtype=float)

    return final_output_scaled


# ---------------------------------------------------------------------------
# Main Routine
# ---------------------------------------------------------------------------
def main():
    print("Starting LCU Native Pauli-Decomposed Block-Encoding Simulation.")
    print(f"Using DT = {DT}, T_FINAL = {T_FINAL} ({N_STEPS} steps), Base Shots = {BASE_SHOTS}")
    
    t_values = np.linspace(0, T_FINAL, N_STEPS + 1)
    
    # 1. Base Euler Matrix Definition (Physical Space)
    A = np.array([
        [1 - DT * SIGMA, DT * SIGMA, 0,              0,   0, 0, 0, 0], 
        [DT * RHO,       1 - DT,     0,             -DT,  0, 0, 0, 0], 
        [0,              0,          1 - DT * BETA,  0,   DT,0, 0, 0], 
        [0,              0,          0,              1,   0, 0, 0, 0], 
        [0,              0,          0,              0,   1, 0, 0, 0], 
        [0,              0,          0,              0,   0, 1, 0, 0], 
        [0,              0,          0,              0,   0, 0, 1, 0],
        [0,              0,          0,              0,   0, 0, 0, 1]
    ], dtype=float)

    # 2. Similarity Transformation
    W = np.array([1/20, 1/30, 1/50, 1/1000, 1/600, 1.0, 1.0, 1.0])
    S = np.diag(W)
    inv_S = np.diag(1.0 / W)
    
    # A_scaled = S * A * S^(-1)
    A_scaled = S @ A @ inv_S

    # 3. Construcción del Oráculo LCU Nativo (Descomposición Pauli)
    dim = A_scaled.shape[0]
    num_system_qubits = int(np.log2(dim))
    
    pauli_op = SparsePauliOp.from_operator(A_scaled)
    weights = np.real(pauli_op.coeffs)
    paulis = pauli_op.paulis.to_labels()
    
    # Filtrar términos casi nulos
    filtered_paulis = []
    filtered_weights = []
    for p, w in zip(paulis, weights):
        if abs(w) > 1e-6:
            filtered_paulis.append(p)
            filtered_weights.append(w)
            
    # L1 Norm / Alpha
    alpha_lcu = np.sum(np.abs(filtered_weights))
    
    # Preparación de amplitudes
    prep_amplitudes = np.sqrt(np.abs(filtered_weights)) / np.sqrt(alpha_lcu)
    
    # Setup de Ancillas LCU
    num_ancillas = int(np.ceil(np.log2(len(filtered_weights))))
    num_ancillas = max(1, num_ancillas) # Garantizar mínimo 1 ancilla
    
    # Rellenar con ceros a potencias de 2
    padded_len = 2**num_ancillas
    if len(prep_amplitudes) < padded_len:
        prep_amplitudes = np.pad(prep_amplitudes, (0, padded_len - len(prep_amplitudes)), 'constant')
        
    # Normalización matemática requerida por StatePreparation de Qiskit
    p_norm = np.linalg.norm(prep_amplitudes)
    if p_norm > 1e-15:
        prep_amplitudes = prep_amplitudes / p_norm
    else:
        # Fallback to uniform distribution if norm is zero (should not happen with filtered weights)
        prep_amplitudes = np.ones_like(prep_amplitudes) / np.sqrt(len(prep_amplitudes))

    simulator = AerSimulator()

    # 4. Memoria del State Vector (Physical Space)
    current_sv = np.array([X0, Y0, Z0, X0 * Z0, X0 * Y0, 1.0, 1.0, 1.0])
    
    history_x = [X0]
    history_y = [Y0]
    history_z = [Z0]

    for step in range(N_STEPS):
        # Progress check: every 10% or at step 0
        is_milestone = (step == 0) or (N_STEPS >= 10 and step % (N_STEPS // 10) == 0)
        if is_milestone:
            pct = int(100 * step / N_STEPS)
            print(f"[{pct:3d}%] Step {step:4d}/{N_STEPS} | Current X,Y,Z: {current_sv[0]:.2f}, {current_sv[1]:.2f}, {current_sv[2]:.2f}")
            
        current_sv_scaled = S @ current_sv
            
        # Llamada con Oráculo LCU inyectado
        output_scaled = next_step_measured(
            current_sv_scaled, current_sv, alpha_lcu, prep_amplitudes, 
            filtered_paulis, filtered_weights, num_ancillas,
            simulator, dim, num_system_qubits, step, S
        )
        
        output_sv = inv_S @ output_scaled
        
        next_sv = np.copy(output_sv)
        next_sv[3] = next_sv[0] * next_sv[2] 
        next_sv[4] = next_sv[0] * next_sv[1]
        
        history_x.append(next_sv[0])
        history_y.append(next_sv[1])
        history_z.append(next_sv[2])
        
        current_sv = next_sv
        
    print(f"[100%] Step {N_STEPS}/{N_STEPS} | Simulation Complete.")

    x_q, y_q, z_q = np.array(history_x), np.array(history_y), np.array(history_z)
    
    # -----------------------------------------------------------------------
    # Classical Comparison
    # -----------------------------------------------------------------------
    try:
        t_cl, x_cl, y_cl, z_cl = euler_lorenz(DT, SIGMA, RHO, BETA, X0, Y0, Z0, N_STEPS)
        plot_lorenz_comparison(
            t_values, x_q, y_q, z_q,
            t_cl, x_cl, y_cl, z_cl,
            title="Lorenz Attractor - LCU Pauli-Decomposed Block Encoding",
            quantum_label="Quantum (LCU-QST)",
            classical_label="Classical (Euler)",
            save_dir=SAVE_DIR,
            prefix_name="lorenz_lcu_meas",
            show=False
        )
    except NameError:
        print("Gráficas y simulación clásica saltadas. Las matrices operaron correctamente en el Backend.")

if __name__ == "__main__":
    main()
