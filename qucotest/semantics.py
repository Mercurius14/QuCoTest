"""Gate targets and scores; extracted unchanged from the evaluated implementation."""
from __future__ import annotations
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Operator

def control_width(item) -> int:
    """Return the semantic control width, including QASM custom MC gates."""
    operation = item.operation
    width = int(getattr(operation, "num_ctrl_qubits", 0) or 0)
    name = operation.name.lower()
    if not width and (name.startswith("mcx") or name.startswith("mcphase")):
        width = len(item.qubits) - 1
    return width

def controlled_gate_rows(circuit: QuantumCircuit, minimum_controls: int = 2):
    rows = []
    for position, item in enumerate(circuit.data):
        width = control_width(item)
        if width < int(minimum_controls) or width >= len(item.qubits):
            continue
        qubits = [circuit.find_bit(q).index for q in item.qubits]
        state = getattr(item.operation, "ctrl_state", None)
        state = 2**width - 1 if state is None else int(state)
        active = [(state >> i) & 1 for i in range(width)]
        rows.append({
            "gate_position": position,
            "source_gate": item.operation.name,
            "control_width": width,
            "controls": qubits[:width],
            "targets": qubits[width:],
            "active_bits": active,
        })
    return rows
def representative_gates(circuit: QuantumCircuit):
    """Pick the first real gate for each distinct semantic control width."""
    rows = controlled_gate_rows(circuit, minimum_controls=2)
    selected, widths = [], set()
    for row in sorted(rows, key=lambda x: (-x["control_width"], x["gate_position"])):
        if row["control_width"] not in widths:
            selected.append(row); widths.add(row["control_width"])
    return selected
def _qindices(circuit, item):
    return [circuit.find_bit(q).index for q in item.qubits]

def _prefix(circuit, stop):
    result = QuantumCircuit(circuit.num_qubits)
    for item in circuit.data[:stop]:
        if item.operation.name not in {"measure", "barrier", "delay"}:
            result.append(item.operation.copy(), [_qindices(circuit, item)[i] for i in range(len(item.qubits))])
    return result

def product_state(parameters, n_qubits):
    parameters = np.asarray(parameters, dtype=float).reshape(2, n_qubits)
    theta, phi = parameters
    factors = [np.array([np.cos(theta[q] / 2), np.exp(1j * phi[q]) * np.sin(theta[q] / 2)])
               for q in range(n_qubits)]
    state = np.array([1.0 + 0.0j])
    for factor in reversed(factors):
        state = np.kron(state, factor)
    return state

def prefix_unitary(circuit, gate_position):
    return Operator(_prefix(circuit, int(gate_position))).data

def preparation_circuit(parameters, n_qubits):
    values = np.asarray(parameters).reshape(2, n_qubits)
    circuit = QuantumCircuit(n_qubits)
    for q in range(n_qubits):
        circuit.u(float(values[0, q]), float(values[1, q]), 0.0, q)
    return circuit
def obligations(circuit):
    conditions, boundaries = [], []
    for gate in representative_gates(circuit):
        active = list(gate["active_bits"])
        base = {
            key: gate[key]
            for key in ["gate_position", "controls", "targets", "control_width"]
        }
        conditions.append(
            base | {"kind": "C", "bits": active, "active": active, "id": f"g{gate['gate_position']}:C:active"}
        )
        for index in range(len(active)):
            off = active.copy()
            off[index] ^= 1
            conditions.append(
                base | {"kind": "C", "bits": off, "active": active, "id": f"g{gate['gate_position']}:C:off:{index}"}
            )
            boundaries.append(
                base | {"kind": "B", "bits": off, "active": active, "id": f"g{gate['gate_position']}:B:{index}"}
            )
    return conditions, boundaries
def compiled_objectives(n,objs):
    rows=[];idx=np.arange(1<<n)
    for o in objs:
        mask=sum(1<<q for q in o['controls'])
        def pattern(bits):return sum(int(v)<<q for q,v in zip(o['controls'],bits))
        target=pattern(o['bits']);active=pattern(o['active'])
        if o['kind']=='C':rows.append(('C',idx[(idx&mask)==target],None))
        else:
            env=idx[(idx&mask)==0]
            rows.append(('B',env|active,env|target))
    return rows

def scores(states,compiled):
    states=np.atleast_2d(states)
    if not compiled:return np.empty((len(states),0))
    return np.column_stack([(abs(states[:,a])**2).sum(axis=1) if kind=='C' else
                            np.minimum(1,2*abs((states[:,a]*states[:,b].conj()).sum(axis=1)))
                            for kind,a,b in compiled])

def checkpoint_scores(states,prefixes,objs,compiled):
    result=np.empty((len(states),len(objs)))
    for pos,prefix in prefixes.items():
        ids=[i for i,o in enumerate(objs) if o['gate_position']==pos]
        result[:,ids]=scores(states@prefix.T,[compiled[i] for i in ids])
    return result
