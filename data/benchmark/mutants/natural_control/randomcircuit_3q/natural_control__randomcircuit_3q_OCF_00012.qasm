OPENQASM 2.0;
include "qelib1.inc";
gate ccz q0,q1,q2 { h q2; ccx q0,q1,q2; h q2; }
gate ccry(param0) q0,q1,q2 { cu(pi/16,0,0,0) q1,q2; cx q1,q0; cu(-pi/16,0,0,0) q0,q2; cx q1,q0; cu(pi/16,0,0,0) q0,q2; }
qreg q[3];
t q[0];
cu1(5.288856933750764) q[1],q[2];
rccx q[1],q[2],q[0];
ccz q[2],q[0],q[1];
ccry(pi/8) q[2],q[0],q[1];
sxdg q[0];
cu1(2.026167409578137) q[1],q[0];
cswap q[1],q[2],q[0];