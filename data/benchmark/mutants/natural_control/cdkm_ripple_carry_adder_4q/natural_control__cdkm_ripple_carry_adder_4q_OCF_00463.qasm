OPENQASM 2.0;
include "qelib1.inc";
gate ccry(param0) q0,q1,q2 { cu(pi/16,0,0,0) q1,q2; cx q1,q0; cu(-pi/16,0,0,0) q0,q2; cx q1,q0; cu(pi/16,0,0,0) q0,q2; }
qreg q[4];
cx q[1],q[2];
cx q[1],q[0];
ccx q[0],q[2],q[1];
cx q[1],q[3];
ccx q[0],q[2],q[1];
ccry(pi/8) q[0],q[2],q[1];
cx q[1],q[0];
cx q[0],q[2];