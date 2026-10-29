"""Recompile a small program using the packaged public backend snapshot."""
import os
os.environ['QISKIT_NUM_PROCS']='1';os.environ['RAYON_NUM_THREADS']='1'
from pathlib import Path
import sys,argparse,json
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from qucotest.hardware import hardware_unit,OUT

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--subject',default='cdkm_ripple_carry_adder_4q');a=ap.parse_args()
    if a.subject=='grover_10q':
        ap.error('The archived Grover10q record is a lower bound, not a completed routed compile. Use the supplied bound only within its proven15s window.')
    hardware_unit(a.subject)
    print(json.dumps(json.loads((OUT/f'hardware_{a.subject}.json').read_text()),indent=2))

if __name__=='__main__':main()
