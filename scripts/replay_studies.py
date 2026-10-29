"""Recover controlled-study suite scores from per-input outcomes and frozen ranks."""
import os
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:os.environ[k]='1'
from pathlib import Path
import sys,json
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import numpy as np,pandas as pd
from qucotest.workflow import ROOT,metadata
from qucotest.statistics import metrics,PRIMARY
from qucotest.ordering import order
from reproduce import check

def main():
    d=ROOT/'data';rows={k:[] for k in ['ordering','external_ordering','component','factorial']}
    def append(name,subject,rep,method,values):
        rows[name].append(dict(subject=subject,replicate=rep,method=method,**values))
    for subject in pd.read_csv(d/'benchmark/subjects.csv').subject:
        published=metadata(subject)['seed_namespace']!=10082026
        folder=d/'outcomes'/('pool_extensions' if published else 'pools')/subject
        entries=json.loads((folder/'entries.json').read_text());offset=0;mat={}
        with np.load(folder/'detection.npz') as z:
            for e in entries:
                rep=e.get('replicate',e.get('rep'));method=e['method']
                mat[rep,method]=z['killed'][offset:offset+e['size']];offset+=e['size']
            assert offset==len(z['killed'])
        if not published:
            comp=pd.read_csv(d/'outcomes/components'/f'{subject}.csv.gz')
            for (rep,method),g in comp.groupby(['replicate','method']):
                matrix=g.pivot(index='test_index',columns='unified_mutant_id',values='killed').sort_index().to_numpy(bool)
                append('component',subject,int(rep),method,metrics(matrix))
            with np.load(d/'outcomes/locations'/f'{subject}.npz') as z:
                for rep,method,matrix in zip(z['replicates'],z['methods'],z['killed']):
                    append('factorial',subject,int(rep),str(method),metrics(matrix))
        for rep in [1,2,3]:
            pools=d/'pools'/subject/f'seed{rep}';ranks=json.loads((pools/'rankings.json').read_text())
            pool=mat[rep,'pool' if published else 'qcbc']
            for method in ['qcbc','novelty']+[f'tau_{t:g}' for t in [.6,.7,.8,.9,1.]]:
                append('ordering',subject,rep,method,metrics(pool[np.asarray(ranks[method])[:30]]))
            vals=pd.DataFrame([metrics(pool[np.asarray(rank)[:30]]) for rank in ranks['random']]).mean().to_dict()
            append('ordering',subject,rep,'random',vals)
            if published:
                for method in ['qcbc_bc','condition_only_bc','condition_restart_bc','probability_pair_bc']:
                    append('component',subject,rep,method,metrics(mat[rep,method][np.asarray(ranks[method])[:30]]))
                for method in ['checkpoint_checkpoint','checkpoint_entry','entry_checkpoint','entry_entry']:
                    matrix=mat[rep,'entry' if method.startswith('entry') else 'pool']
                    append('factorial',subject,rep,method,metrics(matrix[np.asarray(ranks[method])[:30]]))
            for method in ['brick_circuit','quratest_iqft','quratest_ucnot']:
                if published:
                    matrix=mat[rep,method];semantic=ranks[method+'_qcbc'];random=ranks[method+'_random']
                else:
                    with np.load(d/'outcomes/main'/subject/f'{method}__seed{rep}.npz') as z:matrix=z['killed'].copy()
                    with np.load(pools/f'{method}_ordering.npz') as z:semantic=z['qcbc'].copy();random=z['random'].copy()
                with np.load(pools/f'{method}.npz') as z:states=z['states'].copy()
                novelty=order(np.empty((len(states),0)),states,np.arange(len(states)),'novelty')[0]
                for policy,rank in [('original',np.arange(len(matrix))),('qcbc',semantic),('novelty',novelty)]:
                    append('external_ordering',subject,rep,method+'_'+policy,metrics(matrix[np.asarray(rank)[:30]]))
                vals=pd.DataFrame([metrics(matrix[np.asarray(rank)[:30]]) for rank in random]).mean().to_dict()
                append('external_ordering',subject,rep,method+'_random',vals)
    (ROOT/'outputs').mkdir(exist_ok=True)
    for name,values in rows.items():
        frame=pd.DataFrame(values);reference=pd.read_csv(d/'analysis'/f'{name}_suite_metrics.csv')
        error=check(frame,reference,['subject','method','replicate'],PRIMARY)
        frame.to_csv(ROOT/'outputs'/f'{name}_suite_metrics_replayed.csv',index=False)
        print(name,len(frame),'suite rows; maximum error',error,flush=True)
    print('PASS: controlled-study suite scores reproduced from frozen per-input outcomes.',flush=True)

if __name__=='__main__':main()
