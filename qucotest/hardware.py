"""Original public-snapshot compilation/scheduling model; no noise simulation."""
import os
os.environ["QISKIT_NUM_PROCS"]="1"
os.environ["RAYON_NUM_THREADS"]="1"
import time,json
import numpy as np
from pathlib import Path
from qiskit import QuantumCircuit,transpile
from qiskit.circuit import Parameter,Measure,Reset
from qiskit.circuit.library import IGate,RZGate,SXGate,XGate,ECRGate,QFT
from qiskit.transpiler import Target,InstructionProperties
from .workflow import ROOT,original_circuit,subject_record
CONF=json.loads((ROOT/"data/time_model/backend/conf_brisbane.json").read_text())
PROPS=json.loads((ROOT/"data/time_model/backend/props_brisbane.json").read_text())
METHODS=["condition_coherence","brick_circuit","quratest_iqft"]
OUT=ROOT/"outputs/hardware"
def target():
    t=Target(num_qubits=CONF['n_qubits'],dt=CONF['dt']*1e-9)
    gates={name:{} for name in CONF['basis_gates']+['reset']}
    for g in PROPS['gates']:
        p={x['name']:x for x in g['parameters']}
        duration=p['gate_length']['value']*{'ns':1e-9,'us':1e-6,'s':1}[p['gate_length']['unit']]
        gates[g['gate']][tuple(g['qubits'])]=InstructionProperties(duration=duration,error=p.get('gate_error',{}).get('value',0))
    operations={'id':IGate(),'rz':RZGate(Parameter('theta')),'sx':SXGate(),'x':XGate(),'ecr':ECRGate(),'reset':Reset()}
    for name,props in gates.items():t.add_instruction(operations[name],props)
    measurements={}
    for q,items in enumerate(PROPS['qubits']):
        d={x['name']:x for x in items};v=d['readout_length']
        measurements[(q,)]=InstructionProperties(duration=v['value']*{'ns':1e-9,'us':1e-6,'s':1}[v['unit']],error=d['readout_error']['value'])
    t.add_instruction(Measure(),measurements)
    return t

def template(n,ports,method):
    q=QuantumCircuit(n);ni=len(ports)
    if method=='condition_coherence':
        for j,p in enumerate(ports):q.u(Parameter(f't{j}'),Parameter(f'p{j}'),0,p)
    elif method=='brick_circuit':
        for layer in range(2):
            for j,p in enumerate(ports):q.ry(Parameter(f'a{layer}_{j}'),p)
            for j in range(layer%2,ni-1,2):q.cx(ports[j],ports[j+1])
        for j,p in enumerate(ports):q.ry(Parameter(f'f{j}'),p)
    else:
        for j,p in enumerate(ports):q.u(Parameter(f't{j}'),Parameter(f'p{j}'),Parameter(f'l{j}'),p)
        q.compose(QFT(ni,inverse=True,do_swaps=True),qubits=ports,inplace=True)
    return q

def duration(qc,t):
    ready=np.zeros(qc.num_qubits)
    for item in qc.data:
        ids=[qc.find_bit(q).index for q in item.qubits]
        if not ids:continue
        start=ready[ids].max()
        if item.operation.name=='barrier':d=0
        else:
            prop=t[item.operation.name][tuple(ids)]
            assert prop.duration is not None,(item.operation.name,ids)
            d=prop.duration
        ready[ids]=start+d
    return float(ready.max())

def hardware_unit(subject):
    path=OUT/f'hardware_{subject}.json';path.parent.mkdir(parents=True,exist_ok=True)
    if path.exists():return
    original=original_circuit(subject);n=original.num_qubits
    # QASM-defined ECR has the native name but lacks Qiskit's standard-gate tag.
    # Canonicalize only after verifying operator equivalence (up to global phase).
    from qiskit.quantum_info import Operator
    for j,item in enumerate(original.data):
        if item.operation.name=='ecr' and item.operation.base_class is not ECRGate:
            assert Operator(item.operation).equiv(Operator(ECRGate()))
            original.data[j]=item.replace(operation=ECRGate())
    ports=json.loads(subject_record(subject)['input_ports_json'])
    t=target();result=[];start=time.perf_counter()
    reset=max(t['reset'][(q,)].duration for q in range(CONF['n_qubits']))
    rep_delay=CONF['default_rep_delay']*1e-6
    for method in METHODS:
        prep=template(n,ports,method)
        q=QuantumCircuit(n);q.compose(prep,inplace=True);q.compose(original,inplace=True)
        compiled=transpile(q,basis_gates=CONF['basis_gates'],coupling_map=CONF['coupling_map'],
                           initial_layout=list(range(n)),optimization_level=0,
                           routing_method='sabre',seed_transpiler=916,num_processes=1)
        unitary_duration=duration(compiled,t)
        physical=compiled.layout.final_index_layout(filter_ancillas=True)
        assert len(physical)==n
        readout=max(t['measure'][(p,)].duration for p in physical)
        for basis in ['X','Y','Z']:
            # RZ is virtual; H is RZ-SX-RZ and Sdg adds only a virtual RZ.
            # Basis rotation/readout follows the complete routed unitary stage.
            rotation=max(t['sx'][(p,)].duration for p in physical) if basis!='Z' else 0.
            circuit=unitary_duration+rotation+readout
            result.append(dict(subject=subject,method=method,basis=basis,
                scheduled_circuit_seconds=circuit,reset_seconds=reset,repetition_delay_seconds=rep_delay,
                unitary_seconds=unitary_duration,basis_rotation_seconds=rotation,measurement_seconds=readout,
                per_shot_seconds=circuit+reset+rep_delay,ecr=int(compiled.count_ops().get('ecr',0)),
                native_depth=compiled.depth()))
    path.write_text(json.dumps(dict(rows=result,model_compilation_wall_seconds=time.perf_counter()-start),indent=2)+'\n')
