from qpi_lib import qsphere_funcs
from qiskit import QuantumCircuit

def test_qsphere_funcs():
    qc = QuantumCircuit(3)
    # Apply H-gate to the first:
    qc.x(0)
    qc.x(1)
    qc.h(0)

    # Apply a CNOT:
    qc.cx(0,1)
    qc.cx(0,2)

    qc.z(0)
    qc.z(1)

    qsphere_funcs.plot_qsphere_full(qc)