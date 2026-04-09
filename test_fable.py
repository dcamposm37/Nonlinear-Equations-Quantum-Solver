import numpy as np
from fable import fable
from qiskit.quantum_info import Statevector
from qiskit import QuantumCircuit

A = np.array([[1.0, 2.0], [3.0, 4.0]])
A_norm = A / np.linalg.norm(A, 2)
circ, alpha_fable = fable(A_norm)
print("alpha_fable:", alpha_fable)

n = 1
total_qubits = circ.num_qubits
qc = QuantumCircuit(total_qubits)
# Try input state |1> on qubit 0
v = np.array([0.0, 1.0])
qc.initialize(v, range(n)) 
qc.append(circ, range(total_qubits))
sv = Statevector(qc).data

# Print non-zero amplitudes to see where the payload is
for idx, amp in enumerate(sv):
    if abs(amp) > 1e-6:
        bstr = format(idx, f"0{total_qubits}b")
        print(f"State {bstr}: {amp}")

# Theoretical Target
print("Expected A_norm * v: ", A_norm @ v)
