OPENQASM 2.0;
include "qelib1.inc";
gate ccry(param0) q0,q1,q2 { cu(pi/8,0,0,0) q1,q2; cx q1,q0; cu(-pi/8,0,0,0) q0,q2; cx q1,q0; cu(pi/8,0,0,0) q0,q2; }
qreg q[5];
cx q[1],q[3];
cx q[1],q[4];
ccx q[0],q[2],q[1];
ccry(pi/4) q[0],q[2],q[1];
ccx q[1],q[3],q[4];
cx q[1],q[3];
ccx q[0],q[2],q[1];
cx q[0],q[2];
x q[3];
x q[3];
cx q[1],q[3];