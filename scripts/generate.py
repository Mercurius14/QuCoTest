"""Regenerate the primary QuCoTest pool for one benchmark program."""
import os
for key in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:os.environ[key]='1'
from pathlib import Path
import sys,argparse,time,json
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import numpy as np
from qucotest.workflow import generate,ROOT

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--subject',default='cdkm_ripple_carry_adder_4q')
    ap.add_argument('--seed',type=int,choices=[1,2,3],default=1)
    ap.add_argument('--output',type=Path,default=ROOT/'outputs/generated.npz');args=ap.parse_args()
    started=time.perf_counter();result=generate(args.subject,args.seed)
    args.output.parent.mkdir(parents=True,exist_ok=True);np.savez_compressed(args.output,**result)
    with np.load(ROOT/'data/pools'/args.subject/f'seed{args.seed}/qucotest.npz') as z:
        fidelity=abs(np.sum(result['states'].conj()*z['states'],axis=1))**2
    report=dict(subject=args.subject,seed=args.seed,seconds=time.perf_counter()-started,
                pool_size=len(result['states']),minimum_fidelity_to_frozen=float(fidelity.min()),
                output=str(args.output))
    print(json.dumps(report,indent=2));assert fidelity.min()>1-1e-8

if __name__=='__main__':main()
