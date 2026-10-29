OPENQASM 2.0;
include "qelib1.inc";
gate ccz q0,q1,q2 { h q2; ccx q0,q1,q2; h q2; }
qreg q[3];
t q[0];
cu1(5.485206474600126) q[1],q[2];
rccx q[1],q[2],q[0];
ccz q[2],q[0],q[1];
sxdg q[0];
cu1(2.026167409578137) q[1],q[0];
cswap q[1],q[2],q[0];