import numpy as np
from fable import fable
from qiskit.quantum_info import Statevector
from qiskit import QuantumCircuit
from scipy.linalg import hadamard

# 1. Create a sparse matrix (e.g. Identity or simple diagonal)
n = 3
N = 2**n
A = np.diag([1.0, 0.0, 2.0, 0.0, 3.0, 0.0, 0.0, 0.0])
A_norm = A / np.linalg.norm(A, 2)

# 2. Hadamard Walsh transform
# Qiskit Hadamard across n qubits is equivalent to scipy.linalg.hadamard / sqrt(2^n)
Hn = hadamard(N) / np.sqrt(N)
M = Hn @ A_norm @ Hn

# 3. Apply FABLE to M
circ_M, alpha_M = fable(M)

total_qubits = circ_M.num_qubits

# 4. Create SFABLE circuit
sfable_circ = QuantumCircuit(total_qubits)
# Apply H^n to data qubits (lowest n qubits 0, 1, 2)
sfable_circ.h(range(n))
sfable_circ.append(circ_M, range(total_qubits))
sfable_circ.h(range(n))

# 5. Extract statevector
qc = QuantumCircuit(total_qubits)
v = np.random.rand(N)
v = v / np.linalg.norm(v)

qc.initialize(v, range(n)) 
qc.append(sfable_circ, range(total_qubits))
sv = Statevector(qc).data

# 6. Check target states
target_sv = np.zeros(N, dtype=complex)
ancilla_len = total_qubits - n
target_ancilla = '0' * ancilla_len

for idx, amp in enumerate(sv):
    bstr = format(idx, f"0{total_qubits}b")
    if bstr[:ancilla_len] == target_ancilla:
        sys_idx = int(bstr[-n:], 2)
        target_sv[sys_idx] = amp

# Theoretical Target
expected = A_norm @ v
print("SFABLE Depth: ", sfable_circ.depth())
print("Ratio (E/T) : ", expected / target_sv)
