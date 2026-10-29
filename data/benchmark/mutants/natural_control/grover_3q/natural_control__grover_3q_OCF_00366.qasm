OPENQASM 2.0;
include "qelib1.inc";
gate mcphase(param0) q0,q1,q2 { cx q0,q2; rz(-pi/4) q2; cx q1,q2; rz(pi/4) q2; cx q0,q2; rz(-pi/4) q2; cx q1,q2; rz(pi/4) q2; crz(pi/2) q0,q1; p(pi/4) q0; }
gate ccrx(param0) q0,q1,q2 { cu(pi/16,-pi/2,pi/2,0) q1,q2; cx q1,q0; cu(-pi/16,-pi/2,pi/2,0) q0,q2; cx q1,q0; cu(pi/16,-pi/2,pi/2,0) q0,q2; }
qreg q[3];
u(pi/2,0,pi) q[0];
u(pi/2,0,pi) q[1];
u(pi,0,pi) q[2];
mcphase(pi) q[0],q[1],q[2];
ccrx(pi/8) q[0],q[1],q[2];
h q[0];
x q[0];
h q[1];
x q[1];
h q[1];
cx q[0],q[1];
x q[0];
h q[0];
h q[1];
x q[1];
h q[1];