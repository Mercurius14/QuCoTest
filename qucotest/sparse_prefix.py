"""Original sparse prefix isometries for auxiliary-zero MutTG inputs."""
import numpy as np
from scipy.sparse import csr_matrix,eye
from qiskit.quantum_info import Operator

def gate_matrix(qc,item):
    n=qc.num_qubits;dim=1<<n;idx=np.arange(dim);args=[qc.find_bit(q).index for q in item.qubits];op=item.operation
    nc=getattr(op,'num_ctrl_qubits',0);controls=args[:nc];targets=args[nc:];active=np.ones(dim,bool)
    if nc:
        ctrl_state=getattr(op,'ctrl_state',(1<<nc)-1)
        for j,q in enumerate(controls):active&=((idx>>q)&1)==((ctrl_state>>j)&1)
        op=op.base_gate
    if op.name=='swap':
        assert len(targets)==2
        flip=active & (((idx>>targets[0])^(idx>>targets[1]))&1).astype(bool)
        cols=idx.copy();cols[flip]^=(1<<targets[0])|(1<<targets[1])
        return csr_matrix((np.ones(dim),(idx,cols)),shape=(dim,dim))
    assert len(targets)==1,(op.name,targets)
    mat=Operator(op).data;q=targets[0];bits=(idx>>q)&1
    diagonal=np.ones(dim,complex);diagonal[active]=mat[bits[active],bits[active]]
    off=np.zeros(dim,complex);off[active]=mat[bits[active],1-bits[active]]
    g=csr_matrix((np.r_[diagonal,off],(np.r_[idx,idx],np.r_[idx,idx^(1<<q)])),shape=(dim,dim));g.eliminate_zeros();return g

def sparse_unitary(qc,positions=(),input_indices=None):
    u=eye(1<<qc.num_qubits,dtype=complex,format='csr')*np.exp(1j*float(qc.global_phase));prefixes={}
    for pos,item in enumerate(qc.data):
        if pos in positions:prefixes[pos]=u[:,input_indices]
        u=gate_matrix(qc,item)@u;u.eliminate_zeros()
    return u,prefixes
