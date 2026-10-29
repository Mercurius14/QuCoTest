OPENQASM 2.0;
include "qelib1.inc";
gate circuit_100 q0,q1 { h q1; cp(pi/2) q1,q0; h q0; }
gate mcphase(param0) q0,q1,q2 { cx q0,q2; rz(-pi/4) q2; cx q1,q2; rz(pi/4) q2; cx q0,q2; rz(-pi/4) q2; cx q1,q2; rz(pi/4) q2; crz(pi/2) q0,q1; p(pi/4) q0; }
gate mcphase_custom_001(param0) q0,q1,q2 { cx q0,q2; rz(-pi/8) q2; cx q1,q2; rz(pi/8) q2; cx q0,q2; rz(-pi/8) q2; cx q1,q2; rz(pi/8) q2; crz(pi/4) q0,q1; p(pi/8) q0; }
gate ccrx(param0) q0,q1,q2 { cu(pi/8,-pi/2,pi/2,0) q1,q2; cx q1,q0; cu(-pi/8,-pi/2,pi/2,0) q0,q2; cx q1,q0; cu(pi/8,-pi/2,pi/2,0) q0,q2; }
gate circuit_100_dg q0,q1 { h q0; cp(-pi/2) q1,q0; h q1; }
qreg q[4];
circuit_100 q[2],q[3];
mcphase(pi) q[0],q[1],q[2];
mcphase_custom_001(pi/2) q[0],q[1],q[3];
ccrx(pi/4) q[0],q[1],q[3];
circuit_100_dg q[2],q[3];