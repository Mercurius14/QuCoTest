OPENQASM 2.0;
include "qelib1.inc";
gate qft q0,q1 { h q1; cp(pi/2) q1,q0; h q0; swap q0,q1; }
gate mcphase(param0) q0,q1,q2 { cx q0,q2; rz(-pi/4) q2; cx q1,q2; rz(pi/4) q2; cx q0,q2; rz(-pi/4) q2; cx q1,q2; rz(pi/4) q2; crz(pi/2) q0,q1; p(pi/4) q0; }
gate mcphase_custom_002(param0) q0,q1,q2 { cx q0,q2; rz(-pi/16) q2; cx q1,q2; rz(pi/16) q2; cx q0,q2; rz(-pi/16) q2; cx q1,q2; rz(pi/16) q2; crz(pi/8) q0,q1; p(pi/16) q0; }
gate mcphase_custom_001(param0) q0,q1,q2 { cx q0,q2; rz(-pi/8) q2; cx q1,q2; rz(pi/8) q2; cx q0,q2; rz(-pi/8) q2; cx q1,q2; rz(pi/8) q2; crz(pi/4) q0,q1; p(pi/8) q0; }
gate qft_dg q0,q1 { swap q0,q1; h q0; cp(-pi/2) q1,q0; h q1; }
qreg q[4];
qft q[2],q[3];
mcphase(pi) q[0],q[1],q[3];
mcphase_custom_002(pi/4) q[0],q[1],q[3];
mcphase_custom_001(pi/2) q[0],q[1],q[2];
qft_dg q[2],q[3];