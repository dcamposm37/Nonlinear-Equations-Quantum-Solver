import numpy as np
from fable import fable
from qiskit.quantum_info import Statevector
from qiskit import QuantumCircuit

A = np.random.rand(8, 8)
A_norm = A / np.linalg.norm(A, 2)
circ, alpha_fable = fable(A_norm)

n = 3
total_qubits = circ.num_qubits
print(f"n = {n}, total_qubits = {total_qubits}, alpha_fable = {alpha_fable}")

qc = QuantumCircuit(total_qubits)
v = np.random.rand(8)
v = v / np.linalg.norm(v)

qc.initialize(v, range(n)) 
qc.append(circ, range(total_qubits))
sv = Statevector(qc).data

# Get the target states (ancillas = 0)
target_sv = np.zeros(8, dtype=complex)
ancilla_len = total_qubits - n
target_ancilla = '0' * ancilla_len

for idx, amp in enumerate(sv):
    bstr = format(idx, f"0{total_qubits}b")
    # Qiskit endianness: ancillas are the first characters in bitstring (MSB)
    if bstr[:ancilla_len] == target_ancilla:
        sys_idx = int(bstr[-n:], 2)
        target_sv[sys_idx] = amp

# Theoretical Target
expected = A_norm @ v
print("Expected       : ", expected)
print("target_sv      : ", target_sv)
print("Ratio (E/T)    : ", expected / target_sv)
