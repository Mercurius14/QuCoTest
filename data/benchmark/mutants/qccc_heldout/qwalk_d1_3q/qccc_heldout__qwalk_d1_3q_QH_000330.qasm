OPENQASM 2.0;
include "qelib1.inc";
gate mcphase(param0) q0,q1,q2 { cx q0,q2; rz(-pi/32) q2; cx q1,q2; rz(pi/32) q2; cx q0,q2; rz(-pi/32) q2; cx q1,q2; rz(pi/32) q2; crz(pi/16) q0,q1; p(pi/32) q0; }
qreg q[3];
h q[2];
ccx q[2],q[1],q[0];
cx q[2],q[1];
x q[2];
x q[1];
ccx q[2],q[1],q[0];
mcphase(pi/8) q[2],q[1],q[0];
cx q[2],q[1];
x q[1];
x q[2];