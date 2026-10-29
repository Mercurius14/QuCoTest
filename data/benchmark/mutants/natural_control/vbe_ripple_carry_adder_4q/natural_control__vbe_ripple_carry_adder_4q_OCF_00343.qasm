OPENQASM 2.0;
include "qelib1.inc";
gate mcphase(param0) q0,q1,q2 { cx q0,q2; rz(-pi/16) q2; cx q1,q2; rz(pi/16) q2; cx q0,q2; rz(-pi/16) q2; cx q1,q2; rz(pi/16) q2; crz(pi/8) q0,q1; p(pi/16) q0; }
qreg q[4];
ccx q[1],q[2],q[3];
mcphase(pi/4) q[1],q[2],q[3];
cx q[1],q[2];
ccx q[0],q[2],q[3];
cx q[1],q[2];
cx q[1],q[2];
cx q[0],q[2];