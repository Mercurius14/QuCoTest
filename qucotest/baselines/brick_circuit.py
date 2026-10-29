"""Brick-work structured random circuit generator (Phase 12 characterization).

Frozen pre-registered spec (no existing brick generator was present in this
repo, so the spec is defined here and frozen in the Phase 12 protocol):

For every test (salted by seed):
    for layer in range(brick_layers):
        RY(theta_q) on every qubit,   theta_q ~ Uniform(-pi, pi)
        brickwork CX layer:
            offset = layer % 2
            for i in range(offset, n_qubits - 1, 2):  CX(i, i+1)
    final RY(theta_q) on every qubit

With brick_layers = 2 the logical depth is <= 5 (RY,CX,RY,CX,RY), matching the
project's max_prep_depth = 5 and RQC depth scale. Angles use only RY + CX, a
subset of the frozen allowed gate vocabulary {H,X,RX,RY,RZ,CX}.

Determinism: per-test Python `random.Random(seed*100000 + salt)`; tests are
deduplicated by circuit signature, mirroring the QuraTest adapter.
"""

import random

import numpy as np
from qiskit import QuantumCircuit


def _signature(circuit):
    return tuple((inst.operation.name,
                  tuple(circuit.find_bit(q).index for q in inst.qubits),
                  tuple(float(p) for p in inst.operation.params))
                 for inst in circuit.data)


class BrickCircuitGenerator:
    def __init__(self, n_qubits, seed, layers=2):
        self.n_qubits = int(n_qubits)
        self.seed = int(seed)
        self.layers = int(layers)

    def _generate_one(self, salt):
        rng = random.Random(self.seed * 100000 + salt)
        circuit = QuantumCircuit(self.n_qubits)
        for layer in range(self.layers):
            for qubit in range(self.n_qubits):
                circuit.ry(rng.uniform(-np.pi, np.pi), qubit)
            offset = layer % 2
            for i in range(offset, self.n_qubits - 1, 2):
                circuit.cx(i, i + 1)
        for qubit in range(self.n_qubits):
            circuit.ry(rng.uniform(-np.pi, np.pi), qubit)
        return circuit

    def generate(self, n, max_tries=300):
        out, seen = [], set()
        tries = 0
        while len(out) < n and tries < max_tries:
            tries += 1
            circuit = self._generate_one(tries)
            signature = _signature(circuit)
            if signature in seen:
                continue
            seen.add(signature)
            out.append(circuit)
        return out
