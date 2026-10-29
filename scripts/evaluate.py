"""Replay frozen inputs against actual original/mutant circuits, not stored scores."""
import os
for key in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:os.environ[key]='1'
from pathlib import Path
import sys,argparse,json
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import numpy as np,pandas as pd
from qucotest.workflow import ROOT,frozen_inputs,original_circuit,metadata
from qucotest.oracle import load_circuit,probabilities
from qucotest.statistics import metrics

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--subject',default='cdkm_ripple_carry_adder_4q')
    ap.add_argument('--method',default='condition_coherence',choices=['condition_coherence','brick_circuit','quratest_iqft','quratest_ucnot','random_circuit','qucat_pairwise'])
    ap.add_argument('--seed',type=int,choices=[1,2,3],default=1)
    ap.add_argument('--output',type=Path,default=ROOT/'outputs/evaluation.npz');args=ap.parse_args()
    mutants=pd.read_csv(ROOT/'data/benchmark/mutants.csv');mutants=mutants[mutants.subject==args.subject]
    states=frozen_inputs(args.subject,args.method,args.seed);ref=probabilities(states,original_circuit(args.subject))
    tvd=[];ids=[]
    for m in mutants.to_dict('records'):
        changed=probabilities(states,load_circuit(ROOT/'data/benchmark'/m['bundled_mutant_qasm'],metadata(args.subject)['flatten_program']))
        tvd.append([max(.5*abs(a[b]-c[b]).sum() for b in ['X','Y','Z']) for a,c in zip(ref,changed)])
        ids.append(m['unified_mutant_id'] if pd.notna(m.get('unified_mutant_id')) else m['mutant_id'])
    tvd=np.asarray(tvd).T;killed=tvd>=.05
    args.output.parent.mkdir(parents=True,exist_ok=True)
    np.savez_compressed(args.output,tvd=tvd,killed=killed,mutant_ids=np.asarray(ids,str))
    archive=ROOT/'data/outcomes/main'/args.subject/f'{args.method}__seed{args.seed}.npz'
    with np.load(archive) as z:
        order=[ids.index(x) for x in z['mutant_ids']]
        assert np.array_equal(killed[:,order],z['killed'])
    print(json.dumps(dict(subject=args.subject,method=args.method,seed=args.seed,mutants=len(ids),
                         inputs=len(states),matches_archived_kills=True,metrics=metrics(killed)),indent=2))

if __name__=='__main__':main()
