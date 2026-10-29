"""Original greedy and novelty ordering, including fixed tie handling."""
import time
import numpy as np

def order(scores, states, indices, mode, rng=None):
    start=time.perf_counter();scores=np.asarray(scores);indices=np.asarray(indices)
    overlaps=np.minimum(1,np.abs(states.conj()@states.T)**2)
    remaining=list(range(len(indices)));chosen=[];current=np.zeros(scores.shape[1]);trace=[]
    permutation=list(rng.permutation(sorted(indices.tolist()))) if mode=='random' else None
    for step in range(len(indices)):
        options=[]
        for j in remaining:
            gain=float((np.minimum(1,np.maximum(current,scores[j])/.8)-np.minimum(1,current/.8)).sum())
            novelty=1. if not chosen else float(1-overlaps[j,chosen].max())
            key=(round(gain,12),round(novelty,12),-int(indices[j])) if mode=='qcbc' else (round(novelty,12),-int(indices[j]))
            options.append((key,j,gain,novelty))
        if mode=='random':pick=next(x for x in options if indices[x[1]]==permutation[step])
        else:pick=max(options,key=lambda x:x[0])
        _,j,gain,novelty=pick;chosen.append(j);remaining.remove(j);current=np.maximum(current,scores[j])
        trace.append({'step':step+1,'canonical_index':int(indices[j]),'gain':gain,'novelty':novelty,'structural_coverage':float(np.mean(current>=.8)) if len(current) else 0.,'normalized_coverage':float(np.minimum(1,current/.8).mean()) if len(current) else 0.})
    return indices[chosen].tolist(),trace,time.perf_counter()-start

def rank_at_tau(sc, states, tau):
    overlap=np.minimum(1,np.abs(states.conj()@states.T)**2)
    chosen=[];remaining=list(range(len(states)));current=np.zeros(sc.shape[1])
    while remaining:
        def key(j):
            gain=(np.minimum(1,np.maximum(current,sc[j])/tau)-np.minimum(1,current/tau)).sum()
            novelty=1. if not chosen else 1-overlap[j,chosen].max()
            return round(float(gain),12),round(float(novelty),12),-j
        j=max(remaining,key=key);chosen.append(j);remaining.remove(j);current=np.maximum(current,sc[j])
    return np.asarray(chosen)
