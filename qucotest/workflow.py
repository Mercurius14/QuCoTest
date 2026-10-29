"""Portable entry point for the paper's unchanged primary configuration."""
from pathlib import Path
import json
import numpy as np
import pandas as pd
from qiskit import qpy
from . import semantics as sem
from .synthesis import search,search_restricted,logical,scoremat
from .sparse_prefix import sparse_unitary
from .ordering import order

ROOT=Path(__file__).resolve().parents[1]

def metadata(subject):
    rows=json.loads((ROOT/'data/benchmark/generation_metadata.json').read_text())
    return next(r for r in rows if r['subject']==subject)

def subject_record(subject):
    frame=pd.read_csv(ROOT/'data/benchmark/subjects.csv').set_index('subject')
    return frame.loc[subject].to_dict()

def original_circuit(subject,generation=False):
    directory='generation_originals' if generation else 'semantic_originals'
    path=ROOT/'data/benchmark'/directory/f'{subject}.qpy'
    if generation and not path.exists():path=ROOT/'data/benchmark/semantic_originals'/f'{subject}.qpy'
    with path.open('rb') as f:
        return qpy.load(f)[0]

def input_indices(record):
    ports=json.loads(record['input_ports_json'])
    logical_indices=np.arange(1<<len(ports));full=np.zeros(len(logical_indices),int)
    for j,q in enumerate(ports):full|=((logical_indices>>j)&1)<<q
    return full

def embed(states,record):
    states=np.asarray(states)
    if states.shape[1]==1<<int(record['qubits']):return states
    full=np.zeros((len(states),1<<int(record['qubits'])),complex)
    full[:,input_indices(record)]=states
    return full

def generate(subject,replicate=1):
    """Full pool, parameters, scores and semantic rank. No mutant access."""
    record=subject_record(subject);meta=metadata(subject)
    qc=original_circuit(subject,generation=True);n=qc.num_qubits;ni=int(record['input_qubits'])
    conditions,pairs=sem.obligations(qc);objectives=conditions+pairs
    assert objectives==meta['objectives']
    positions={o['gate_position'] for o in objectives}
    if meta['sparse_prefix']:
        _,prefixes=sparse_unitary(qc,positions,input_indices(record))
    else:prefixes={p:sem.prefix_unitary(qc,p) for p in positions}
    def rng(j):
        return np.random.default_rng(np.random.SeedSequence([
            meta['seed_namespace'],meta['seed_subject_index'],replicate,j]))
    parameters=[]
    for j,o in enumerate(objectives):
        if meta['sparse_prefix']:
            value,_=search_restricted({'input_qubits':ni,'qubits':n},o,prefixes,rng(j))
        else:value,_=search(n,o,prefixes[o['gate_position']],rng(j))
        parameters.append(value)
    parameters=np.asarray(parameters+list(rng(9999).uniform(0,2*np.pi,(30,2*ni))))
    states=logical(parameters,ni)
    if meta['sparse_prefix']:scores=scoremat(states,objectives,prefixes,n)
    else:scores=sem.checkpoint_scores(states,prefixes,objectives,sem.compiled_objectives(n,objectives))
    rank=order(scores,states,np.arange(len(states)),'qcbc')[0]
    return dict(states=states,parameters=parameters,scores=scores,rank=np.asarray(rank,int))

def frozen_inputs(subject,method='condition_coherence',replicate=1):
    folder=ROOT/'data/pools'/subject/f'seed{replicate}'
    if method=='condition_coherence':
        with np.load(folder/'qucotest.npz') as z:states=z['states'].copy()
        ranks=json.loads((folder/'rankings.json').read_text())
        rank=ranks.get('qcbc',ranks.get('checkpoint_source',{}).get('checkpoint'))
        assert rank is not None
        states=states[np.asarray(rank)[:30]]
    else:
        with np.load(folder/f'{method}.npz') as z:states=z['states'].copy()
    return embed(states,subject_record(subject))
