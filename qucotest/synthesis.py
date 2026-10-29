"""Original primary search, with 48 screening points and a 1048-call cap."""
import time
import numpy as np
from scipy.optimize import minimize
from .semantics import product_state,compiled_objectives,scores
from . import semantics as base

def search(n,objective,prefix,rng):
    calls=0;best=-1.;bestx=None
    compiled=compiled_objectives(n,[objective])
    def score(x):
        nonlocal calls,best,bestx
        if calls>=1048:raise StopIteration
        state=product_state(x,n)
        if prefix is not None:state=prefix@state
        y=float(scores(state,compiled)[0,0]);calls+=1
        if y>best:best=y;bestx=x.copy()
        return y
    started=time.perf_counter();xs=rng.uniform(0,2*np.pi,(48,2*n));ys=[score(x) for x in xs]
    try:
        minimize(lambda x:-score(x),xs[int(np.argmax(ys))],method='L-BFGS-B',bounds=[(0,2*np.pi)]*(2*n),options={'maxiter':40,'ftol':1e-10})
    except StopIteration:pass
    return np.mod(bestx,2*np.pi),dict(calls=calls,best_score=best,seconds=time.perf_counter()-started)
def logical(params,ni):return np.asarray([base.product_state(x,ni) for x in params])

def scoremat(states,objs,pre,n):
 out=np.empty((len(states),len(objs)))
 for pos in {o['gate_position'] for o in objs}:
  ids=[i for i,o in enumerate(objs) if o['gate_position']==pos];oo=[objs[i] for i in ids]
  transformed=pre[pos].dot(states.T).T
  for j,o in zip(ids,oo):
   if o['kind']=='P_sqrt':
    pp=base.scores(transformed,base.compiled_objectives(n,[o|dict(kind='C',bits=o['active']),o|dict(kind='C')]))
    out[:,j]=np.minimum(1,2*np.sqrt(pp[:,0]*pp[:,1]))
   else:out[:,j]=base.scores(transformed,base.compiled_objectives(n,[o]))[:,0]
 return out

def search_restricted(c,o,pre,rng,maxiter=40,cap=1048,return_last=False):
 ni=c['input_qubits'];n=c['qubits'];calls=0;best=-1;bx=None;start=time.perf_counter()
 def f(x):
  nonlocal calls,best,bx
  if cap and calls>=cap:raise StopIteration
  y=scoremat(logical([x],ni),[o],pre,n)[0,0];calls+=1
  if y>best:best=y;bx=x.copy()
  return -y
 xs=rng.uniform(0,2*np.pi,(48,2*ni));ys=[f(x) for x in xs];last=xs[np.argmin(ys)]
 try:
  rr=minimize(f,last,method='L-BFGS-B',bounds=[(0,2*np.pi)]*(2*ni),options=dict(maxiter=maxiter,ftol=1e-10));last=rr.x
 except StopIteration:pass
 return np.mod(last if return_last else bx,2*np.pi),dict(calls=calls,seconds=time.perf_counter()-start,best_score=best)
