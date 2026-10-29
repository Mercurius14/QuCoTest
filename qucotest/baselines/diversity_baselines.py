"""Non-LLM candidate generators for Phase 3.

  RandomCandidateGenerator  — plain random prep circuits (RQC-style)
  RandomBasisGenerator      — random computational-basis states
"""

import random

import numpy as np

PARAM_GATES = {"rx", "ry", "rz"}


class RandomCandidateGenerator:
    """Generate random state-preparation candidates over the allowed gate set."""

    def __init__(self, cfg, n_qubits, seed, depth=3):
        g = cfg["generation"]
        self.gates = [x.lower() for x in g["allowed_gates"]]
        self.param_range = tuple(g.get("param_range", [-3.141592653589793, 3.141592653589793]))
        self.n_qubits = int(n_qubits)
        self.depth = int(depth)
        self.seed = seed

    def generate(self, n, max_tries=200):
        rng = random.Random(self.seed)
        nrng = np.random.default_rng(self.seed)
        preps, seen = [], set()
        tries = 0
        while len(preps) < n and tries < max_tries:
            tries += 1
            ops = []
            for _ in range(self.depth):
                gate = rng.choice(self.gates)
                if gate == "cx" and self.n_qubits >= 2:
                    qs = rng.sample(range(self.n_qubits), 2)
                    ops.append({"gate": "CX", "qubits": qs})
                else:
                    q = rng.randrange(self.n_qubits)
                    op = {"gate": gate.upper(), "qubits": [q]}
                    if gate in PARAM_GATES:
                        op["params"] = [round(float(nrng.uniform(*self.param_range)), 6)]
                    ops.append(op)
            prep = {"operations": ops}
            sig = tuple((o["gate"], tuple(o["qubits"]), tuple(o.get("params", [])))
                        for o in ops)
            if sig in seen:
                continue
            seen.add(sig)
            preps.append(prep)
        return preps


class RandomBasisGenerator:
    """Random computational-basis state-preparation candidates."""

    def __init__(self, n_qubits, seed):
        self.n_qubits = int(n_qubits)
        self.seed = seed

    def generate(self, n, max_tries=100):
        rng = random.Random(self.seed)
        preps, seen = [], set()
        tries = 0
        while len(preps) < n and tries < max_tries:
            tries += 1
            bits = [rng.randrange(2) for _ in range(self.n_qubits)]
            ops = [{"gate": "X", "qubits": [i]} for i, b in enumerate(bits) if b == 1]
            prep = {"operations": ops}
            sig = tuple(bits)
            if sig in seen:
                continue
            seen.add(sig)
            preps.append(prep)
        return preps
