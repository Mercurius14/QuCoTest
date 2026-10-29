"""Original estimands, inference rounding and bootstrap seeds."""
import numpy as np,pandas as pd
from scipy.stats import wilcoxon
METRICS=[f"ms{k}" for k in range(1,31)]+["auc1_10"]
PRIMARY=["ms1","ms5","auc1_10"]

def metrics(kills):
    curve = np.maximum.accumulate(kills,axis=0).mean(axis=1)
    curve = np.pad(curve,(0,max(0,30-len(curve))),mode='edge')
    return dict(zip(METRICS, [*curve[:30],float(np.trapezoid(curve[:10])/9)]))

def paired(frame,pairs,groups=None):
    mean=frame.groupby(['subject','method'])[METRICS].mean()
    rng=np.random.default_rng(10082026);rows=[]
    for a,b in pairs:
        for metric in PRIMARY:
            aa=mean.xs(a,level='method')[metric];bb=mean.xs(b,level='method')[metric]
            assert set(aa.index)==set(bb.index)
            d=(aa-bb.reindex(aa.index)).to_numpy();rounded=np.round(d,12)
            boots=d[rng.integers(0,len(d),(5000,len(d)))].mean(axis=1)
            rows.append(dict(target=a,alternative=b,metric=metric,programs=len(d),
                mean_delta_pp=100*d.mean(),ci_low_pp=100*np.quantile(boots,.025),
                ci_high_pp=100*np.quantile(boots,.975),p=float(wilcoxon(rounded).pvalue) if np.any(rounded) else 1.,
                wins=int((rounded>0).sum()),ties=int((rounded==0).sum()),losses=int((rounded<0).sum())))
    df=pd.DataFrame(rows)
    families=[df] if groups is None else [g for _,g in df.groupby(groups)]
    for family in families:
        ix=family.sort_values('p',kind='stable').index
        df.loc[ix,'holm_p']=np.minimum(1,np.maximum.accumulate(df.loc[ix,'p'].to_numpy()*np.arange(len(ix),0,-1)))
    return df
def holm(pvalues):
    p=np.asarray(pvalues,float);order=np.argsort(p);out=np.empty(len(p));running=0
    for rank,index in enumerate(order):
        running=max(running,(len(p)-rank)*p[index]);out[index]=min(1,running)
    return out

def bootstrap(values,seed=9162026,repeats=5000):
    a=np.asarray(values,float);rng=np.random.default_rng(seed)
    means=np.mean(rng.choice(a,(repeats,len(a)),replace=True),axis=1)
    return float(np.quantile(means,.025)),float(np.quantile(means,.975))
