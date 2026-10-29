OPENQASM 2.0;
include "qelib1.inc";
gate ccrx(param0) q0,q1,q2 { cu(pi/8,-pi/2,pi/2,0) q1,q2; cx q1,q0; cu(-pi/8,-pi/2,pi/2,0) q0,q2; cx q1,q0; cu(pi/8,-pi/2,pi/2,0) q0,q2; }
qreg q[4];
ccx q[1],q[2],q[3];
cx q[1],q[2];
ccx q[0],q[2],q[3];
ccrx(pi/4) q[0],q[2],q[3];
cx q[1],q[2];
cx q[1],q[2];
cx q[0],q[2];