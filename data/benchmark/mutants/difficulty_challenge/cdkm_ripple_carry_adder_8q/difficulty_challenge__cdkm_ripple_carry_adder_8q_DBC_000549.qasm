OPENQASM 2.0;
include "qelib1.inc";
gate c5ry(param0) q0,q1,q2,q3,q4,q5 { h q5; p(pi/8) q0; p(pi/8) q1; p(pi/8) q2; p(pi/8) q5; cx q0,q1; p(-pi/8) q1; cx q0,q1; cx q1,q2; p(-pi/8) q2; cx q0,q2; p(pi/8) q2; cx q1,q2; p(-pi/8) q2; cx q0,q2; cx q2,q5; p(-pi/8) q5; cx q1,q5; p(pi/8) q5; cx q2,q5; p(-pi/8) q5; cx q0,q5; p(pi/8) q5; cx q2,q5; p(-pi/8) q5; cx q1,q5; p(pi/8) q5; cx q2,q5; p(-pi/8) q5; cx q0,q5; h q5; ry(-pi/8) q5; h q5; cx q4,q5; tdg q5; cx q3,q5; t q5; cx q4,q5; tdg q5; cx q3,q5; t q4; t q5; h q5; cx q3,q4; t q3; tdg q4; cx q3,q4; ry(pi/8) q5; h q5; p(pi/8) q0; p(pi/8) q1; p(pi/8) q2; p(pi/8) q5; cx q0,q1; p(-pi/8) q1; cx q0,q1; cx q1,q2; p(-pi/8) q2; cx q0,q2; p(pi/8) q2; cx q1,q2; p(-pi/8) q2; cx q0,q2; cx q2,q5; p(-pi/8) q5; cx q1,q5; p(pi/8) q5; cx q2,q5; p(-pi/8) q5; cx q0,q5; p(pi/8) q5; cx q2,q5; p(-pi/8) q5; cx q1,q5; p(pi/8) q5; cx q2,q5; p(-pi/8) q5; cx q0,q5; h q5; ry(-pi/8) q5; h q5; cx q4,q5; tdg q5; cx q3,q5; t q5; cx q4,q5; tdg q5; cx q3,q5; t q4; t q5; h q5; cx q3,q4; t q3; tdg q4; cx q3,q4; ry(pi/8) q5; }
gate c5ry_o7(param0) q0,q1,q2,q3,q4,q5 { x q3; x q4; c5ry(pi/2) q0,q1,q2,q3,q4,q5; x q3; x q4; }
qreg q[8];
cx q[1],q[4];
cx q[1],q[0];
ccx q[0],q[4],q[1];
cx q[2],q[5];
cx q[2],q[1];
ccx q[1],q[5],q[2];
c5ry_o7(pi/2) q[1],q[5],q[0],q[4],q[6],q[2];
cx q[3],q[6];
cx q[3],q[2];
ccx q[2],q[6],q[3];
cx q[3],q[7];
ccx q[2],q[6],q[3];
cx q[3],q[2];
cx q[2],q[6];
ccx q[1],q[5],q[2];
cx q[2],q[1];
cx q[1],q[5];
ccx q[0],q[4],q[1];
cx q[1],q[0];
cx q[0],q[4];