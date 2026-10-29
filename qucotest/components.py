"""Original matched-budget component search; separate RNG from primary."""
from __future__ import annotations
import hashlib,time
import numpy as np
from scipy.optimize import minimize
from .semantics import product_state
def configuration_probability(state,controls,bits):
 idx=np.arange(len(state));mask=np.ones(len(state),bool)
 for q,b in zip(controls,bits):mask&=((idx>>int(q))&1)==int(b)
 return float(np.abs(state[mask])@np.abs(state[mask]))
from .synthesis import base
from .semantics import scores,compiled_objectives
from .semantics import product_state
def boundary_coherence(state, controls, bits_a, bits_b):
    """Return 2|rho[a,b]| of the reduced control-state density matrix."""
    controls = list(map(int, controls)); bits_a = list(map(int, bits_a)); bits_b = list(map(int, bits_b))
    control_mask = sum(1 << q for q in controls)
    value = 0.0j
    for base in range(len(state)):
        if base & control_mask:
            continue
        ia, ib = base, base
        for qubit, a, b in zip(controls, bits_a, bits_b):
            ia |= int(a) << qubit; ib |= int(b) << qubit
        value += state[ia] * np.conj(state[ib])
    return float(min(1.0, 2 * abs(value)))
def rng_for(*parts):
    raw = hashlib.sha256("|".join(map(str, parts)).encode()).digest()
    return np.random.default_rng(np.random.SeedSequence(np.frombuffer(raw, dtype="<u4")))

class CallBudget:
    def __init__(self, cap: int):
        self.cap = cap
        self.calls = 0
        self.best_score = -np.inf
        self.best_parameters = None

    def record(self, parameters, score):
        if self.calls >= self.cap:
            raise StopIteration("objective-call budget exhausted")
        self.calls += 1
        if score > self.best_score:
            self.best_score = float(score)
            self.best_parameters = np.asarray(parameters).copy()
        return score

def raw_score(parameters, n, prefix, objective):
    state = prefix @ product_state(parameters, n)
    pa = configuration_probability(state, objective["controls"], objective["active"])
    if objective["kind"] == "C":
        return configuration_probability(state, objective["controls"], objective["bits"])
    pb = configuration_probability(state, objective["controls"], objective["bits"])
    if objective["kind"] == "B":
        return boundary_coherence(state, objective["controls"], objective["active"], objective["bits"])
    if objective["kind"] == "P_sqrt":
        return float(min(1.0, 2 * np.sqrt(pa * pb)))
    if objective["kind"] == "P_product":
        return float(min(1.0, 2 * pa * pb))
    raise ValueError(objective["kind"])

def search(objective, n, prefix, rng, cap):
    counter = CallBudget(cap)

    def score(parameters):
        value = raw_score(parameters, n, prefix, objective)
        return counter.record(parameters, value)

    start = time.perf_counter()
    samples = rng.uniform(0, 2 * np.pi, (48, 2 * n))
    values = []
    for parameters in samples:
        values.append(score(parameters))
    initial = samples[int(np.argmax(values))]
    converged = False
    message = ""
    try:
        result = minimize(
            lambda x: -score(x),
            initial,
            method="L-BFGS-B",
            bounds=[(0, 2 * np.pi)] * (2 * n),
            options={"maxiter": 10000, "ftol": 1e-10},
        )
        converged = bool(result.success)
        message = str(result.message)
    except StopIteration:
        message = "hard objective-call cap reached"
    return (
        np.mod(counter.best_parameters, 2 * np.pi),
        {
            "actual_calls": counter.calls,
            "unused_calls": cap - counter.calls,
            "checkpoint_state_computations": counter.calls,
            "best_value": counter.best_score,
            "threshold_reached": counter.best_score >= 0.8,
            "converged_before_cap": converged,
            "message": message,
            "seconds": time.perf_counter() - start,
        },
    )
