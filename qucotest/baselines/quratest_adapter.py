"""QuraTest baseline adapter (Phase 6).

Runs the *public* QuraTest input generators (Random / IQFT / UCNOT) from
`external/quratest-mutators` WITHOUT modifying their generation logic, and
adapts their output (a Qiskit preparation circuit) into the unified QGT test
representation so it flows through the exact same execution / mutation oracle
/ metrics pipeline as every other method.

This is a re-run of the public QuraTest generators on a unified benchmark —
NOT a full reproduction of the QuraTest paper's 47 subjects.

Notes:
  * QuraTest's `line.py` imports `qiskit.execute`/`Aer` (removed in Qiskit 2.x);
    we inject lightweight shims first (generation never calls them).
  * The generators use the global `random` module; we seed it per test so the
    experiment is reproducible (seeds are recorded).
  * QuraTest prep circuits are used as-is (no truncation); their actual depth /
    gate count / CX count are recorded for the cost analysis.
"""

import random
import sys
from copy import deepcopy
from pathlib import Path

import qiskit

QURATEST_DIR = Path(__file__).resolve().parents[2] / "vendor" / "quratest"

# ---- shims so `from qiskit import execute, Aer` succeeds on Qiskit 2.x ----
if not hasattr(qiskit, "Aer"):
    from qiskit_aer import Aer  # noqa: F401
    qiskit.Aer = Aer
if not hasattr(qiskit, "execute"):

    def _quratest_execute(*args, **kwargs):  # pragma: no cover - never called in generation
        raise NotImplementedError("qiskit.execute shim: not used by QuraTest generation")
    qiskit.execute = _quratest_execute


def _load_modules():
    if str(QURATEST_DIR) not in sys.path:
        sys.path.insert(0, str(QURATEST_DIR))
    import line  # noqa: F401  (gates + Circuit)
    from mutators import RandomMutator, QFTMutator, UCNOTMutator  # noqa: F401
    return line, RandomMutator, QFTMutator, UCNOTMutator


_LINE, _RANDOM, _QFT, _UCNOT = None, None, None, None


def _ensure():
    global _LINE, _RANDOM, _QFT, _UCNOT
    if _LINE is None:
        _LINE, _RANDOM, _QFT, _UCNOT = _load_modules()
    return _LINE, _RANDOM, _QFT, _UCNOT


GENERATORS = {
    "quratest_random": "random",
    "quratest_iqft": "qft",
    "quratest_ucnot": "ucnot",
}


def _signature(qc):
    return tuple((inst.operation.name, tuple(qc.find_bit(q).index for q in inst.qubits),
                  tuple(float(p) for p in inst.operation.params))
                 for inst in qc.data)


class QuraTestGenerator:
    """Generates N distinct prep circuits using one public QuraTest mutator."""

    def __init__(self, n_qubits, mutator_name, seed):
        self.n_qubits = int(n_qubits)
        self.mutator_name = mutator_name
        self.seed = int(seed)
        _line, _R, _Q, _U = _ensure()
        self._line = _line
        self._mutator = {"random": _R, "qft": _Q, "ucnot": _U}[mutator_name]()

    # ------------------------------------------------------------------
    def _generate_one(self, salt):
        random.seed(self.seed * 100000 + salt)
        c = self._line.Circuit(self.n_qubits)
        nc = self._mutator.generate_circuit(c)
        qc = deepcopy(nc.code)
        # strip any stray measurements (shouldn't exist, but be safe)
        qc.remove_final_measurements(inplace=False)
        return qc

    def generate(self, n, max_tries=300):
        out, seen = [], set()
        tries = 0
        while len(out) < n and tries < max_tries:
            tries += 1
            qc = self._generate_one(tries)
            sig = _signature(qc)
            if sig in seen:
                continue
            seen.add(sig)
            out.append(qc)
        return out

    @staticmethod
    def cost(qc):
        ops = qc.count_ops()
        return {
            "depth": int(qc.depth()),
            "gate_count": int(sum(ops.values())),
            "cx_count": int(ops.get("cx", 0) + ops.get("cx", 0)),
        }
