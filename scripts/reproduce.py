"""Reaggregate paper evidence from archived observations; never change inputs."""
import os
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:os.environ[k]='1'
from pathlib import Path
import sys,json,argparse
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import numpy as np,pandas as pd
from scipy.stats import wilcoxon
from qucotest.workflow import ROOT
from qucotest.statistics import metrics,paired,holm,bootstrap,PRIMARY,METRICS

DATA=ROOT/'data';OUT=ROOT/'outputs';METHODS=['condition_coherence','brick_circuit','quratest_iqft','quratest_ucnot','random_circuit','qucat_pairwise']

def check(actual,reference,keys,columns,tolerance=1e-10):
    if 'seconds' in keys:
        # The601-point grid is stored as decimal CSV text in the archive.
        actual=actual.assign(seconds=actual.seconds.round(10))
        reference=reference.assign(seconds=reference.seconds.round(10))
    actual=actual.set_index(keys).sort_index();reference=reference.set_index(keys).sort_index()
    assert actual.index.equals(reference.index),(keys,len(actual),len(reference))
    error=float(np.nanmax(abs(actual[columns].to_numpy(float)-reference[columns].to_numpy(float))))
    assert error<tolerance,('reference difference',error,columns)
    return error

def exact():
    rows=[]
    family=pd.read_csv(DATA/'benchmark/subjects.csv').set_index('subject').family
    for p in sorted((DATA/'outcomes/main').glob('*/*.npz')):
        method,rep=p.stem.split('__seed');subject=p.parent.name
        with np.load(p) as z:
            # The original kill flags precede CSV float serialization. A stored
            # TVD immediately below0.05 can round to0.05 on CSV round-trip.
            # Some legacy baseline records contain flags without archived TVD.
            different=np.isfinite(z['tvd']) & (z['killed']!=(z['tvd']>=.05))
            assert np.all(abs(z['tvd'][different]-.05)<1e-12)
            rows.append(dict(subject=subject,method=method,replicate=int(rep),family=family[subject],**metrics(z['killed'])))
    raw=pd.DataFrame(rows)
    recorded=pd.read_csv(DATA/'analysis/main_suite_metrics.csv')
    # Six auxiliary configurations remain in the main11-comparison correction family.
    # Some additions archive their suite metrics, without duplicate per-test matrices.
    present=raw[['subject','method','replicate']].assign(present=True)
    missing=recorded.merge(present,on=['subject','method','replicate'],how='left')
    missing=missing[missing.present.isna()].drop(columns='present')
    assert not missing.method.isin(METHODS).any()
    combined=pd.concat([raw,missing],ignore_index=True)
    check(combined,recorded,['subject','method','replicate'],METRICS)
    combined.to_csv(OUT/'main_suite_metrics.csv',index=False)
    summary=combined.groupby(['subject','method'])[METRICS].mean().groupby('method').mean().reset_index()
    summary.to_csv(OUT/'main_summary.csv',index=False)
    check(summary,pd.read_csv(DATA/'analysis/main_summary.csv'),['method'],METRICS)
    print('EXACT: archived test outcomes reproduce all six main generators.',flush=True)

def studies():
    for name in ['ordering','external_ordering','factorial','component']:
        raw=pd.read_csv(DATA/'analysis'/f'{name}_suite_metrics.csv')
        program=raw.groupby(['subject','method'],as_index=False)[METRICS].mean()
        summary=program.groupby('method',as_index=False)[METRICS].mean()
        check(summary,pd.read_csv(DATA/'analysis'/f'{name}_summary.csv'),['method'],PRIMARY)
        summary.to_csv(OUT/f'{name}_summary.csv',index=False)
    # The archived family sizes and bootstrap order are part of the protocol.
    configurations={
        'main':([('condition_coherence',m) for m in sorted(set(pd.read_csv(DATA/'analysis/main_suite_metrics.csv').method)-{'condition_coherence'})],'metric'),
        'ordering':([('qcbc','random'),('qcbc','novelty')],None),
        'factorial':([('checkpoint_checkpoint','entry_entry'),('checkpoint_checkpoint','entry_checkpoint'),('checkpoint_entry','entry_entry'),('entry_checkpoint','entry_entry')],None),
        'threshold':([(f'tau_{t:g}',m) for t in [.6,.7,.8,.9,1.] for m in ['random','novelty']],None),
    }
    for name,(contrasts,groups) in configurations.items():
        source='ordering' if name=='threshold' else name
        raw=pd.read_csv(DATA/'analysis'/f'{source}_suite_metrics.csv')
        result=paired(raw,contrasts,groups=groups)
        ref=pd.read_csv(DATA/'analysis'/f'{name}_statistics.csv')
        check(result,ref,['target','alternative','metric'],['mean_delta_pp','ci_low_pp','ci_high_pp','p','holm_p'])
        result.to_csv(OUT/f'{name}_statistics.csv',index=False)
    raw=pd.read_csv(DATA/'analysis/external_ordering_suite_metrics.csv')
    generators=['brick_circuit','quratest_iqft','quratest_ucnot']
    original=paired(raw,[(m+'_qcbc',m+'_'+o) for m in generators for o in ['original','random']])
    novelty=paired(raw,[(m+'_qcbc',m+'_novelty') for m in generators])
    result=pd.concat([original,novelty],ignore_index=True);result['holm_p']=holm(result.p)
    check(result,pd.read_csv(DATA/'analysis/external_ordering_statistics.csv'),['target','alternative','metric'],['mean_delta_pp','ci_low_pp','ci_high_pp','p','holm_p'])
    result.to_csv(OUT/'external_ordering_statistics.csv',index=False)
    mean=pd.read_csv(DATA/'analysis/component_inference_program_metrics.csv')
    rng=np.random.default_rng(9162026);rows=[]
    for metric in ['auc1_10','ms1','ms5']:
        pivot=mean.pivot(index='subject',columns='method',values=metric)
        for alternative in ['condition_only_bc','condition_restart_bc','probability_pair_bc']:
            d=(pivot.qcbc_bc-pivot[alternative]).to_numpy()
            draws=d[rng.integers(0,len(d),(5000,len(d)))].mean(axis=1)
            rows.append(dict(target='qcbc_bc',alternative=alternative,metric=metric,
                             mean_delta_pp=d.mean()*100,ci_low_pp=np.quantile(draws,.025)*100,
                             ci_high_pp=np.quantile(draws,.975)*100,p=float(wilcoxon(d).pvalue) if np.any(abs(d)>1e-12) else 1.))
    result=pd.DataFrame(rows);result['holm_p']=holm(result.p)
    check(result,pd.read_csv(DATA/'analysis/component_statistics.csv'),['target','alternative','metric'],['mean_delta_pp','ci_low_pp','ci_high_pp','p','holm_p'])
    result.to_csv(OUT/'component_statistics.csv',index=False)
    print('STUDIES: unchanged main11/metric, ordering6, threshold30, location12, transfer27, component9 families.',flush=True)

def finite():
    rows=[]
    for i,p in enumerate(sorted((DATA/'finite_shots/raw').glob('*.csv.gz'))):
        raw=pd.read_csv(p,usecols=['subject','method','replicate','mutant_id','sampling_seed','test_index','shots','sampled_detected','exact_detected'])
        subject,method,rep=raw[['subject','method','replicate']].iloc[0].tolist()
        for shots,g in raw.groupby('shots'):
            matrix=g.pivot(index=['mutant_id','sampling_seed'],columns='test_index',values='sampled_detected').reindex(columns=range(1,11))
            assert not matrix.isna().any().any()
            curve=np.maximum.accumulate(matrix.to_numpy(float),axis=1).mean(axis=0)
            rows.append(dict(subject=subject,method=method,replicate=rep,shots=shots,
                             MS1=curve[0],MS5=curve[4],MS10=curve[9],AUC1_10=(curve.sum()-.5*curve[0]-.5*curve[-1])/9))
        matrix=raw.drop_duplicates(['mutant_id','test_index']).pivot(index='mutant_id',columns='test_index',values='exact_detected').reindex(columns=range(1,11))
        curve=np.maximum.accumulate(matrix.to_numpy(float),axis=1).mean(axis=0)
        rows.append(dict(subject=subject,method=method,replicate=rep,shots=0,MS1=curve[0],MS5=curve[4],MS10=curve[9],AUC1_10=(curve.sum()-.5*curve[0]-.5*curve[-1])/9))
        if (i+1)%100==0:print('FINITE:',i+1,'/414 units',flush=True)
    suite=pd.DataFrame(rows);cols=['MS1','MS5','MS10','AUC1_10']
    check(suite,pd.read_csv(DATA/'finite_shots/reference/suite_metrics.csv'),['subject','method','replicate','shots'],cols)
    program=suite.groupby(['subject','method','shots'],as_index=False)[cols].mean()
    summary=program.groupby(['method','shots'],as_index=False)[cols].mean()
    check(summary,pd.read_csv(DATA/'finite_shots/reference/overall_equal_program_summary.csv'),['method','shots'],cols)
    suite.to_csv(OUT/'finite_suite_metrics.csv',index=False);summary.to_csv(OUT/'finite_summary.csv',index=False)
    rows=[]
    for shots in [1024,4096,16384]:
        part=program[program.shots==shots];family=[]
        for baseline in ['brick_circuit','quratest_iqft']:
            for metric in ['AUC1_10','MS1','MS5']:
                pivot=part.pivot(index='subject',columns='method',values=metric)
                d=(pivot.condition_coherence-pivot[baseline]).to_numpy()
                lo,hi=bootstrap(d,seed=9162026+shots+len(rows))
                family.append(dict(shots=shots,baseline=baseline,metric=metric,paired_difference=d.mean(),ci_low=lo,ci_high=hi,p_raw=float(wilcoxon(d).pvalue) if np.any(d) else 1.))
        for row,p in zip(family,holm([x['p_raw'] for x in family])):row['p_holm']=p;rows.append(row)
    result=pd.DataFrame(rows)
    check(result,pd.read_csv(DATA/'finite_shots/reference/statistical_comparisons.csv'),['shots','baseline','metric'],['paired_difference','ci_low','ci_high','p_raw','p_holm'])
    result.to_csv(OUT/'finite_statistics.csv',index=False)
    print('FINITE: exact references and all three shot budgets reproduced.',flush=True)

def time_curve():
    # Time AUC uses cumulative MS after completed tests, not the input-index AUC.
    costs=pd.read_csv(DATA/'time_model/complete_circuit_costs.csv')
    generation=pd.read_csv(DATA/'time_model/generation_costs.csv').set_index(['subject','method','replicate'])
    grid=np.linspace(0,15,601);rows=[]
    for (subject,method,rep),gr in generation.iterrows():
        path=DATA/'finite_shots/raw'/f'{subject}__{method}__r{rep}.csv.gz'
        raw=pd.read_csv(path,usecols=['shots','mutant_id','sampling_seed','test_index','sampled_detected'])
        matrix=raw[raw.shots==1024].pivot(index=['mutant_id','sampling_seed'],columns='test_index',values='sampled_detected').reindex(columns=range(1,11))
        curve=np.maximum.accumulate(matrix.to_numpy(float),axis=1).mean(axis=0)
        period=2048*costs[(costs.subject==subject)&(costs.method==method)].per_shot_seconds.sum()
        assert period*10>15
        front=float(gr.generation_seconds)+2 if gr.status=='complete' else np.inf
        completion=front+period*np.arange(1,11);increments=np.diff(np.r_[0,curve])
        area=(increments[:,None]*np.maximum(grid-completion[:,None],0)).sum(axis=0)
        auc=np.divide(area,grid,out=np.zeros_like(area),where=grid>0)
        ms=(increments[:,None]*(completion[:,None]<=grid)).sum(axis=0)
        rows.extend(dict(subject=subject,method=method,replicate=rep,seconds=t,MS=m,time_AUC=a) for t,m,a in zip(grid,ms,auc))
    frame=pd.DataFrame(rows).groupby(['subject','method','seconds'],as_index=False)[['MS','time_AUC']].mean()
    overall=frame.groupby(['method','seconds'],as_index=False)[['MS','time_AUC']].mean()
    check(overall,pd.read_csv(DATA/'time_model/reference_curve.csv'),['method','seconds'],['MS','time_AUC'])
    overall.to_csv(OUT/'time_curve.csv',index=False)
    print('TIME: original maxiter40, measured generation plus estimated QPU, 1024shots and15s reproduced.',flush=True)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--stage',choices=['exact','studies','finite','time','all'],default='all');a=ap.parse_args()
    OUT.mkdir(exist_ok=True)
    actions={'exact':exact,'studies':studies,'finite':finite,'time':time_curve}
    for name,run in actions.items():
        if a.stage in [name,'all']:run()
    print('PASS: requested numerical checks completed against archived references.',flush=True)

if __name__=='__main__':main()
