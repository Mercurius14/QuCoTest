"""Preserve the original subgroup aggregation used by the paper's scope table."""
import os
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:os.environ[k]='1'
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import numpy as np,pandas as pd
from qucotest.workflow import ROOT
from qucotest.statistics import metrics
from reproduce import check,METHODS

def main():
    d=ROOT/'data';mutants=pd.read_csv(d/'benchmark/mutants.csv')
    mutants['id']=mutants.unified_mutant_id.fillna(mutants.mutant_id)
    mutants['construction_group']=mutants.provenance.replace({'published_muttg':'difficulty_challenge','published_qmutbench':'difficulty_challenge'})
    meta=mutants.set_index('id');raw=[]
    for p in sorted((d/'outcomes/main').glob('*/*.npz')):
        method,rep=p.stem.split('__seed')
        if method not in METHODS:continue
        with np.load(p) as z:
            subset=meta.loc[z['mutant_ids']].reset_index(drop=True)
            # Difficulty uses the original subject-by-provenance cells, rather
            # than silently replacing the published weighting policy.
            for (track,band),g in subset.groupby(['provenance','difficulty']):
                raw.append(dict(subject=p.parent.name,method=method,replicate=int(rep),track=track,
                                view='Calibration difficulty',group=band,auc1_10=metrics(z['killed'][:,g.index])['auc1_10']))
            for band,g in subset.groupby('construction_group'):
                raw.append(dict(subject=p.parent.name,method=method,replicate=int(rep),track=band,
                                view='Fault construction groups',group=band,auc1_10=metrics(z['killed'][:,g.index])['auc1_10']))
    cells=pd.DataFrame(raw).groupby(['subject','method','track','view','group'],as_index=False).auc1_10.mean()
    result=cells.groupby(['view','group','method'],as_index=False).auc1_10.mean()
    pm=pd.read_csv(d/'analysis/main_program_metrics.csv');pm=pm[pm.method.isin(METHODS)]
    structure=pd.read_csv(d/'analysis/program_structure.csv')
    pm=pm.merge(structure[['subject','qubit_band','gate_band']],on='subject',validate='many_to_one')
    extra=[]
    for col,view in [('qubit_band','Total qubits'),('gate_band','Logical gates')]:
        for (band,method),g in pm.groupby([col,'method']):extra.append(dict(view=view,group=band,method=method,auc1_10=g.auc1_10.mean()))
    result=pd.concat([result,pd.DataFrame(extra)],ignore_index=True)
    error=check(result,pd.read_csv(d/'analysis/stratified_auc.csv'),['view','group','method'],['auc1_10'])
    (ROOT/'outputs').mkdir(exist_ok=True);result.to_csv(ROOT/'outputs/stratified_auc_replayed.csv',index=False)
    print('PASS: all difficulty, construction, qubit and gate strata reproduced; maximum error',error)

if __name__=='__main__':main()
