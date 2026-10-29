OPENQASM 2.0;
include "qelib1.inc";
gate ccrx(param0) q0,q1,q2 { cu(pi/16,-pi/2,pi/2,0) q1,q2; cx q1,q0; cu(-pi/16,-pi/2,pi/2,0) q0,q2; cx q1,q0; cu(pi/16,-pi/2,pi/2,0) q0,q2; }
qreg q[3];
ccx q[0],q[1],q[2];
ccrx(pi/8) q[0],q[1],q[2];
cx q[0],q[1];