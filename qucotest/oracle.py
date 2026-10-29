"""Exact XYZ oracle and original calibrated finite-shot sampling functions."""
import hashlib
import hashlib
import numpy as np
from qiskit import QuantumCircuit,transpile,qasm2
from qiskit_aer import AerSimulator
BASES=["X","Y","Z"]
def tvd(a,b):return float(.5*np.abs(a-b).sum())

def hadamard_all(states):
    """Apply H tensor n to the last axis using a vectorized FWHT."""
    result = np.asarray(states, dtype=complex).copy()
    width = result.shape[-1]
    step = 1
    scale = np.sqrt(2.0)
    while step < width:
        view = result.reshape(*result.shape[:-1], -1, 2 * step)
        left = view[..., :step].copy()
        right = view[..., step:].copy()
        view[..., :step] = (left + right) / scale
        view[..., step:] = (left - right) / scale
        step *= 2
    return result

def measurement_probabilities(states, basis):
    states = np.asarray(states, dtype=complex)
    if basis == "Z":
        transformed = states
    elif basis == "X":
        transformed = hadamard_all(states)
    elif basis == "Y":
        dimension = states.shape[-1]
        phase = np.asarray([(-1j) ** int(index).bit_count()
                            for index in range(dimension)], dtype=complex)
        transformed = hadamard_all(states * phase)
    else:
        raise ValueError(basis)
    return np.abs(transformed) ** 2
def probabilities(states,circuit):
    # Restrict the simulator target to avoid costly generic target construction.
    # Optimization level zero preserves the circuit unitary and the original oracle.
    sim=AerSimulator(method='statevector',max_parallel_threads=1,max_parallel_experiments=1)
    native=set(sim.configuration().basis_gates)
    used={item.operation.name for item in circuit.data}
    sim.set_options(basis_gates=sorted((native & used) | {'u','cx'}))
    compiled=transpile(circuit,sim,optimization_level=0)
    jobs=[]
    for state in states:
        q=QuantumCircuit(circuit.num_qubits);q.set_statevector(state);q.compose(compiled,inplace=True);q.save_statevector();jobs.append(q)
    result=sim.run(jobs).result();assert result.success
    output=np.asarray([result.get_statevector(i).data for i in range(len(jobs))])
    vals={b:measurement_probabilities(output,b) for b in ['X','Y','Z']}
    for v in vals.values():
        assert np.isfinite(v).all() and v.min()>=0
        assert np.allclose(v.sum(axis=1),1,atol=1e-9)
    return [{b:v[i] for b,v in vals.items()} for i in range(len(states))]

def null_threshold(probabilities,shots,seed,repeats=2000):
    """Same draws and 0.995 quantile, with bounded contiguous allocations."""
    rng=np.random.default_rng(seed);statistics=np.zeros(repeats);chunk=8
    for basis in ['X','Y','Z']:
        p=probabilities[basis]
        left=[rng.multinomial(shots,p,size=min(chunk,repeats-start)) for start in range(0,repeats,chunk)]
        for start,a in zip(range(0,repeats,chunk),left):
            b=rng.multinomial(shots,p,size=len(a))
            values=.5*np.abs(a-b).sum(axis=1)/shots
            statistics[start:start+len(a)]=np.maximum(statistics[start:start+len(a)],values)
    return float(np.quantile(statistics,.995,method='higher'))
def sampled_statistic(a, b, shots, rng):
    return max(tvd(rng.multinomial(shots, a[k]) / shots, rng.multinomial(shots, b[k]) / shots) for k in BASES)
def flatten(qc):
    result=QuantumCircuit(qc.num_qubits)
    def append(item,qargs):
        op=item.operation
        if op.name=='barrier':return
        if op.name in {'measure','reset','initialize'}:raise ValueError('nonunitary program')
        if getattr(op,'num_ctrl_qubits',0)>0 or op.name in {'x','y','z','h','p','rx','ry','rz','s','t','sdg','tdg','sx','sxdg','u','u1','u2','u3','swap','id'} or op.definition is None:
            result.append(op,qargs);return
        definition=op.definition;result.global_phase+=float(definition.global_phase)
        for child in definition.data:append(child,[qargs[definition.find_bit(q).index] for q in child.qubits])
    result.global_phase=float(qc.global_phase)
    for item in qc.data:append(item,[qc.find_bit(q).index for q in item.qubits])
    return result

def load_circuit(path,flatten_program=False):
 qc=qasm2.load(path,custom_instructions=qasm2.LEGACY_CUSTOM_INSTRUCTIONS,custom_classical=qasm2.LEGACY_CUSTOM_CLASSICAL).remove_final_measurements(inplace=False)
 return flatten(qc) if flatten_program else qc

def seed_for(namespace: str, *parts: object) -> int:
    payload = "|".join([namespace, *map(str, parts)]).encode()
    return int.from_bytes(hashlib.sha256(payload).digest()[:8], "little")

def seed_for(namespace: str, *parts: object) -> int:
    payload = "|".join([namespace, *map(str, parts)]).encode()
    return int.from_bytes(hashlib.sha256(payload).digest()[:8], "little")
