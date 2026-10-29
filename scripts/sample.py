"""Recompute one archived calibrated finite-shot observation from its circuits."""
import os
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:os.environ[k]='1'
from pathlib import Path
import argparse,json,sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import numpy as np,pandas as pd
from qucotest.workflow import ROOT,frozen_inputs,original_circuit,metadata
from qucotest.oracle import probabilities,load_circuit,null_threshold,sampled_statistic,seed_for

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--subject',default='cdkm_ripple_carry_adder_4q')
    ap.add_argument('--method',choices=['condition_coherence','brick_circuit','quratest_iqft'],default='condition_coherence')
    ap.add_argument('--seed',type=int,default=1);ap.add_argument('--shots',type=int,choices=[1024,4096,16384],default=1024)
    ap.add_argument('--test-index',type=int,default=1);ap.add_argument('--sampling-seed',type=int,default=0);args=ap.parse_args()
    raw=pd.read_csv(ROOT/'data/finite_shots/raw'/f'{args.subject}__{args.method}__r{args.seed}.csv.gz')
    record=raw[(raw.shots==args.shots)&(raw.test_index==args.test_index)&(raw.sampling_seed==args.sampling_seed)].iloc[0]
    mutants=pd.read_csv(ROOT/'data/benchmark/mutants.csv')
    ids=mutants.unified_mutant_id.fillna(mutants.mutant_id);m=mutants[ids==record.mutant_id].iloc[0]
    state=frozen_inputs(args.subject,args.method,args.seed)[args.test_index-1:args.test_index]
    op=probabilities(state,original_circuit(args.subject))[0]
    mp=probabilities(state,load_circuit(ROOT/'data/benchmark'/m.bundled_mutant_qasm,metadata(args.subject)['flatten_program']))[0]
    threshold=null_threshold(op,args.shots,seed_for('QGT-E4-NULL-CAL-v1',args.subject,args.method,args.seed,args.test_index,args.shots,'finite_ideal'),2000)
    rng=np.random.default_rng(seed_for('QGT-E4-SAMPLE-v1',args.subject,args.method,args.seed,record.mutant_id,args.test_index,args.shots,'finite_ideal',args.sampling_seed))
    value=sampled_statistic(op,mp,args.shots,rng)
    assert abs(value-record.sampled_statistic)<1e-10
    assert abs(threshold-record.null_threshold)<1e-10
    assert int(value>=threshold)==int(record.sampled_detected)
    print(json.dumps(dict(subject=args.subject,mutant=record.mutant_id,shots=args.shots,
                          threshold=threshold,sampled_statistic=value,detected=bool(value>=threshold),matches_archive=True),indent=2))

if __name__=='__main__':main()
