OPENQASM 2.0;
include "qelib1.inc";
gate mcphase(param0) q0,q1,q2 { cx q0,q2; rz(-pi/32) q2; cx q1,q2; rz(pi/32) q2; cx q0,q2; rz(-pi/32) q2; cx q1,q2; rz(pi/32) q2; crz(pi/16) q0,q1; p(pi/32) q0; }
qreg q[5];
cx q[1],q[3];
cx q[1],q[4];
ccx q[0],q[2],q[1];
mcphase(pi/8) q[0],q[2],q[1];
ccx q[1],q[3],q[4];
cx q[1],q[3];
ccx q[0],q[2],q[1];
cx q[0],q[2];
x q[3];
x q[3];
cx q[1],q[3];