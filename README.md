# QuCoTest

QuCoTest generates and prioritizes quantum test inputs using control-boundary semantics. This repository contains the implementation, benchmark circuits, frozen inputs, experimental observations, and scripts for replay and analysis.

## Setup

The recorded environment uses Python 3.11 and the versions pinned in `requirements.txt`. From the repository root:

```bash
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

On Windows, activate the environment with `.venv\Scripts\Activate.ps1` instead. No cloud account or quantum hardware is required. Generated files are written to `outputs/` by default.

## Quick start

```bash
# Regenerate one QuCoTest pool and compare it with the frozen pool.
python scripts/generate.py --subject cdkm_ripple_carry_adder_4q --seed 1

# Simulate the original circuit and its mutants using frozen inputs.
python scripts/evaluate.py --subject cdkm_ripple_carry_adder_4q --seed 1

# Check benchmark coverage, rankings, and archived costs.
python scripts/check_artifact.py

# Reaggregate archived outcomes and statistical comparisons.
python scripts/reproduce.py --stage studies
```

`generate.py` and `evaluate.py` accept subject names from `data/benchmark/subjects.csv` and seeds 1, 2, or 3. `evaluate.py --method` selects `condition_coherence` (QuCoTest), `brick_circuit` (BWC), `quratest_iqft`, `quratest_ucnot`, `random_circuit` (RQC), or `qucat_pairwise`. Both scripts perform computation and compare their output with frozen data; numerical optimization and timing can vary across environments.

Additional commands:

```bash
python scripts/replay_studies.py         # Recompute metrics from frozen ranks and outcomes
python scripts/reproduce_strata.py       # Recompute subgroup summaries
python scripts/sample.py                 # Recompute one finite-shot observation and threshold
python scripts/reproduce.py --stage all  # Reaggregate all archived numerical evidence
python scripts/plot_figures.py           # Generate plots from archived summaries
python scripts/estimate_hardware.py      # Recompile a small program against the backend snapshot
```

The reproduction stages can also run individually with `--stage exact`, `studies`, `finite`, or `time`. The finite stage reads 414 compressed files and may take several minutes. These stages reaggregate saved observations; they do not rerun the complete circuit simulation campaign. `outputs/` is ignored by Git.

## Repository contents

| Path | Contents |
| --- | --- |
| `qucotest/` | Control semantics, input synthesis, ordering, oracle, baseline adapters, and hardware cost model |
| `scripts/` | Generation, evaluation, sampling, replay, validation, and plotting commands |
| `data/benchmark/` | Metadata, 46 original circuits, 1,000 mutant circuits, and QPY originals used by generation and simulation |
| `data/pools/` | Frozen candidate inputs, scores, and rankings for three seeds per subject, including component and baseline pools |
| `data/outcomes/` | Per-test detection records for the main and controlled studies |
| `data/analysis/` | Suite-level, program-level, summary, and statistical results |
| `data/finite_shots/` | Finite-shot observations and reference aggregates for 46 programs, three methods, and three input seeds |
| `data/time_model/` | Backend snapshot, measured classical costs, modeled circuit costs, and reference time curve |
| `vendor/` | Included baseline dependencies and their accompanying notices where supplied |

## Data and experiment conventions

- `subjects.csv` describes qubit counts and variable input ports; `mutants.csv` maps mutants to bundled QASM files. QPY files preserve gate structure used by the implementation.
- Pool `.npz` files contain states and, where applicable, parameters and semantic scores. `rankings.json` stores frozen orderings. Component-study pools are separate from the main QuCoTest pools.
- Main outcome arrays store per-input mutant kill flags, TVD values, and mutant IDs. Some legacy baseline TVD values are unavailable and stored as NaN; their recorded kill flags are retained. QuCAT's shorter native suites are extended at their terminal score when comparing larger budgets.
- The exact oracle uses the maximum TVD across global X, Y, and Z measurements with a threshold of 0.05. Finite-shot records instead use calibrated two-sample thresholds and 1,024, 4,096, or 16,384 shots per basis. Results average seeds within each program before taking an equal-program mean.
- The primary search uses 48 screening candidates, L-BFGS-B with `maxiter=40`, and a 1,048-objective-call cap. The separate matched-budget component search uses `maxiter=10000` and the same call cap. Fixed seeds and settings preserve the archived experimental protocol.
- The time model combines archived classical timings with estimated execution costs from a public IBM Brisbane snapshot. Its detection observations include finite-shot sampling but no simulated backend noise. It is not a measurement on quantum hardware; compilation, calibration, queueing, and network overheads are excluded.
- The component statistics in `data/analysis/component_statistics.csv` preserve the archived observations. For the QuCoTest versus Probability pair AUC comparison, the recorded difference is 0.21 percentage points and the Holm-adjusted p-value is 1.0.
- Some controlled-study summary CSVs contain intermediate budget columns with inconsistent values. Replay scripts check the primary reported metrics; use the underlying per-test outcomes and frozen rankings when recomputing other budgets.

## Sources and reuse

The benchmark draws on MQTBench, published MutTG programs, and QMutBench option-pricing mutants. QuraTest baseline code includes its original MIT license in `vendor/quratest/`. Other third-party material may have its own terms; check upstream sources before redistribution. A project-wide license has not been specified.
