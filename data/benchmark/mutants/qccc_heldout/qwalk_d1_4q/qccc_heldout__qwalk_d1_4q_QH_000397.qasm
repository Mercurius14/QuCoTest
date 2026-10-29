OPENQASM 2.0;
include "qelib1.inc";
gate mcx q0,q1,q2,q3 { h q3; p(pi/8) q0; p(pi/8) q1; p(pi/8) q2; p(pi/8) q3; cx q0,q1; p(-pi/8) q1; cx q0,q1; cx q1,q2; p(-pi/8) q2; cx q0,q2; p(pi/8) q2; cx q1,q2; p(-pi/8) q2; cx q0,q2; cx q2,q3; p(-pi/8) q3; cx q1,q3; p(pi/8) q3; cx q2,q3; p(-pi/8) q3; cx q0,q3; p(pi/8) q3; cx q2,q3; p(-pi/8) q3; cx q1,q3; p(pi/8) q3; cx q2,q3; p(-pi/8) q3; cx q0,q3; h q3; }
gate mcphase(param0) q0,q1,q2,q3 { h q3; cx q1,q3; tdg q3; cx q0,q3; t q3; cx q1,q3; tdg q3; cx q0,q3; t q1; t q3; h q3; cx q0,q1; t q0; tdg q1; cx q0,q1; rz(-pi/32) q3; cx q2,q3; rz(pi/32) q3; h q3; cx q1,q3; tdg q3; cx q0,q3; t q3; cx q1,q3; tdg q3; cx q0,q3; t q1; t q3; h q3; cx q0,q1; t q0; tdg q1; cx q0,q1; rz(-pi/32) q3; cx q2,q3; rz(pi/32) q3; cx q0,q2; rz(-pi/64) q2; cx q1,q2; rz(pi/64) q2; cx q0,q2; rz(-pi/64) q2; cx q1,q2; rz(pi/64) q2; crz(pi/32) q0,q1; p(pi/64) q0; }
qreg q[4];
h q[3];
mcx q[3],q[1],q[2],q[0];
mcphase(pi/8) q[3],q[1],q[2],q[0];
ccx q[3],q[2],q[1];
cx q[3],q[2];
x q[3];
x q[1];
x q[2];
mcx q[3],q[1],q[2],q[0];
ccx q[3],q[2],q[1];
cx q[3],q[2];
x q[1];
x q[2];
x q[3];