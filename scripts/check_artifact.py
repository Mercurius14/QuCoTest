"""Validate paper coverage, semantic ranking replay and cost aggregations."""
import os
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:os.environ[k]='1'
from pathlib import Path
import sys,json
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import numpy as np,pandas as pd
from qucotest.workflow import ROOT,metadata,original_circuit
from qucotest.semantics import obligations
from qucotest.ordering import order,rank_at_tau

def main():
    (ROOT/'outputs').mkdir(exist_ok=True)
    data=ROOT/'data';subjects=pd.read_csv(data/'benchmark/subjects.csv');mutants=pd.read_csv(data/'benchmark/mutants.csv')
    assert len(subjects)==46 and len(mutants)==1000
    assert len(list((data/'benchmark/originals').glob('*.qasm')))==46
    assert len(list((data/'benchmark/mutants').rglob('*.qasm')))==1000
    assert mutants.subject.isin(subjects.subject).all()
    for row in mutants.to_dict('records'):assert (data/'benchmark'/row['bundled_mutant_qasm']).is_file()
    pool_count=0;threshold_checks=0;new_outcomes=[];suitechecks=[]
    for subject in subjects.subject:
        qc=original_circuit(subject,generation=True);a,b=obligations(qc)
        assert a+b==metadata(subject)['objectives'],subject
        for rep in [1,2,3]:
            folder=data/'pools'/subject/f'seed{rep}'
            with np.load(folder/'qucotest.npz') as z:
                states=z['states'];scores=z['scores'] if 'scores' in z else z['checkpoint_scores']
                assert np.allclose(np.linalg.norm(states,axis=1),1)
            rankings=json.loads((folder/'rankings.json').read_text())
            actual=order(scores,states,np.arange(len(states)),'qcbc')[0]
            assert actual[:30]==rankings['qcbc'][:30],(subject,rep,'semantic')
            novelty=order(scores,states,np.arange(len(states)),'novelty')[0]
            assert novelty[:30]==rankings['novelty'][:30],(subject,rep,'novelty')
            for tau in [.6,.7,.8,.9,1.]:
                rank=rank_at_tau(scores,states,tau)
                assert np.array_equal(rank[:30],rankings[f'tau_{tau:g}'][:30]),(subject,rep,tau)
                threshold_checks+=1
            pool_count+=1
    # Every finite-shot file covers all mutants of its program, all ten tests,
    # all three shot budgets and30 measurement seeds; read only identity columns.
    units=list((data/'finite_shots/raw').glob('*.csv.gz'));assert len(units)==414
    # Preparation cost uses program-first means, not a pooled average of tests.
    costs=pd.read_csv(data/'analysis/preparation_cost_per_test.csv')
    costs=costs.groupby(['subject','method'])[['prep_depth','prep_cx']].mean().groupby('method').mean()
    reference=pd.read_csv(data/'analysis/preparation_cost_summary.csv').set_index('method')
    assert np.allclose(costs.sort_index(),reference.loc[costs.index].sort_index())
    costs.to_csv(ROOT/'outputs/preparation_cost_summary.csv')
    generation=pd.read_csv(data/'analysis/component_cost.csv')
    means=generation.groupby('method')[['calls','search_seconds','total_seconds']].mean()
    reference=pd.read_csv(data/'analysis/component_cost_summary.csv').set_index('method')
    assert np.allclose(means,reference.loc[means.index])
    # Program-equal control-width strata must recombine to overall main scores.
    control=pd.read_csv(data/'analysis/control_width_scores.csv')
    overall=pd.read_csv(data/'analysis/main_summary.csv').set_index('method')
    for method,g in control.groupby('method'):
        assert g.programs.sum()==46 and g.mutants.sum()==1000
        assert abs(np.average(g.auc1_10,weights=g.programs)-overall.loc[method,'auc1_10'])<1e-12
    report=dict(programs=46,mutants=1000,pools_checked=pool_count,threshold_orders_checked=threshold_checks,
                original_semantic_gate_selection_replayed=True,semantic_and_novelty_rankings_match=True,
                finite_shot_units=len(units),preparation_costs_match=True,component_costs_match=True,
                control_width_strata_recombine=True,
                scope='Packaged benchmark and experimental observations')
    (ROOT/'outputs').mkdir(exist_ok=True)
    (ROOT/'outputs/validation.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
