"""Paper baseline preparations; QuCAT replays its frozen native PICT suite."""
import json,os
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from .workflow import ROOT,subject_record,embed
from .baselines.brick_circuit import BrickCircuitGenerator
from .baselines.diversity_baselines import RandomCandidateGenerator
from .baselines.quratest_adapter import QuraTestGenerator,GENERATORS
def _ops_to_circuit(n_qubits, operations):
    circuit = QuantumCircuit(n_qubits)
    for operation in operations:
        gate = operation["gate"].upper()
        qubits = operation["qubits"]
        params = operation.get("params", [])
        if gate == "H":
            circuit.h(qubits[0])
        elif gate == "X":
            circuit.x(qubits[0])
        elif gate == "RX":
            circuit.rx(params[0], qubits[0])
        elif gate == "RY":
            circuit.ry(params[0], qubits[0])
        elif gate == "RZ":
            circuit.rz(params[0], qubits[0])
        elif gate == "CX":
            circuit.cx(qubits[0], qubits[1])
        else:
            raise ValueError(f"unsupported gate: {gate}")
    return circuit

def generate_baseline(subject,method,replicate=1):
 record=subject_record(subject);folder=ROOT/'data/pools'/subject/f'seed{replicate}'
 with np.load(folder/f'{method}.npz') as z:
  seed=int(z['seed']);frozen=z['states'].copy()
 ni=int(record['input_qubits'])
 if method=='qucat_pairwise':return frozen
 if method=='brick_circuit':circuits=BrickCircuitGenerator(ni,seed,layers=2).generate(30)
 elif method=='random_circuit':
  cfg={'generation':json.loads((ROOT/'data/benchmark/baseline_configuration.json').read_text())}
  circuits=[_ops_to_circuit(ni,x['operations']) for x in RandomCandidateGenerator(cfg,ni,seed,depth=3).generate(30)]
 else:circuits=QuraTestGenerator(ni,GENERATORS[method],seed).generate(30)
 states=np.asarray([Statevector.from_instruction(q).data for q in circuits])
 assert states.shape==frozen.shape
 assert np.min(abs(np.sum(states.conj()*frozen,axis=1))**2)>1-1e-8
 return states
