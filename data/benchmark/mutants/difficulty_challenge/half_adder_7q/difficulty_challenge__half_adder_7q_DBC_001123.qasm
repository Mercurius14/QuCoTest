OPENQASM 2.0;
include "qelib1.inc";
gate mcphase(param0) q0,q1,q2,q3,q4,q5,q6 { h q6; p(pi/8) q0; p(pi/8) q1; p(pi/8) q2; p(pi/8) q6; cx q0,q1; p(-pi/8) q1; cx q0,q1; cx q1,q2; p(-pi/8) q2; cx q0,q2; p(pi/8) q2; cx q1,q2; p(-pi/8) q2; cx q0,q2; cx q2,q6; p(-pi/8) q6; cx q1,q6; p(pi/8) q6; cx q2,q6; p(-pi/8) q6; cx q0,q6; p(pi/8) q6; cx q2,q6; p(-pi/8) q6; cx q1,q6; p(pi/8) q6; cx q2,q6; p(-pi/8) q6; cx q0,q6; h q6; rz(-pi/4) q6; h q6; p(pi/8) q3; p(pi/8) q4; p(pi/8) q5; p(pi/8) q6; cx q3,q4; p(-pi/8) q4; cx q3,q4; cx q4,q5; p(-pi/8) q5; cx q3,q5; p(pi/8) q5; cx q4,q5; p(-pi/8) q5; cx q3,q5; cx q5,q6; p(-pi/8) q6; cx q4,q6; p(pi/8) q6; cx q5,q6; p(-pi/8) q6; cx q3,q6; p(pi/8) q6; cx q5,q6; p(-pi/8) q6; cx q4,q6; p(pi/8) q6; cx q5,q6; p(-pi/8) q6; cx q3,q6; h q6; rz(pi/4) q6; h q6; p(pi/8) q0; p(pi/8) q1; p(pi/8) q2; p(pi/8) q6; cx q0,q1; p(-pi/8) q1; cx q0,q1; cx q1,q2; p(-pi/8) q2; cx q0,q2; p(pi/8) q2; cx q1,q2; p(-pi/8) q2; cx q0,q2; cx q2,q6; p(-pi/8) q6; cx q1,q6; p(pi/8) q6; cx q2,q6; p(-pi/8) q6; cx q0,q6; p(pi/8) q6; cx q2,q6; p(-pi/8) q6; cx q1,q6; p(pi/8) q6; cx q2,q6; p(-pi/8) q6; cx q0,q6; h q6; rz(-pi/4) q6; h q6; p(pi/8) q3; p(pi/8) q4; p(pi/8) q5; p(pi/8) q6; cx q3,q4; p(-pi/8) q4; cx q3,q4; cx q4,q5; p(-pi/8) q5; cx q3,q5; p(pi/8) q5; cx q4,q5; p(-pi/8) q5; cx q3,q5; cx q5,q6; p(-pi/8) q6; cx q4,q6; p(pi/8) q6; cx q5,q6; p(-pi/8) q6; cx q3,q6; p(pi/8) q6; cx q5,q6; p(-pi/8) q6; cx q4,q6; p(pi/8) q6; cx q5,q6; p(-pi/8) q6; cx q3,q6; h q6; rz(pi/4) q6; h q5; p(pi/8) q0; p(pi/8) q1; p(pi/8) q2; p(pi/8) q5; cx q0,q1; p(-pi/8) q1; cx q0,q1; cx q1,q2; p(-pi/8) q2; cx q0,q2; p(pi/8) q2; cx q1,q2; p(-pi/8) q2; cx q0,q2; cx q2,q5; p(-pi/8) q5; cx q1,q5; p(pi/8) q5; cx q2,q5; p(-pi/8) q5; cx q0,q5; p(pi/8) q5; cx q2,q5; p(-pi/8) q5; cx q1,q5; p(pi/8) q5; cx q2,q5; p(-pi/8) q5; cx q0,q5; h q5; rz(-pi/8) q5; h q5; cx q4,q5; tdg q5; cx q3,q5; t q5; cx q4,q5; tdg q5; cx q3,q5; t q4; t q5; h q5; cx q3,q4; t q3; tdg q4; cx q3,q4; rz(pi/8) q5; h q5; p(pi/8) q0; p(pi/8) q1; p(pi/8) q2; p(pi/8) q5; cx q0,q1; p(-pi/8) q1; cx q0,q1; cx q1,q2; p(-pi/8) q2; cx q0,q2; p(pi/8) q2; cx q1,q2; p(-pi/8) q2; cx q0,q2; cx q2,q5; p(-pi/8) q5; cx q1,q5; p(pi/8) q5; cx q2,q5; p(-pi/8) q5; cx q0,q5; p(pi/8) q5; cx q2,q5; p(-pi/8) q5; cx q1,q5; p(pi/8) q5; cx q2,q5; p(-pi/8) q5; cx q0,q5; h q5; rz(-pi/8) q5; h q5; cx q4,q5; tdg q5; cx q3,q5; t q5; cx q4,q5; tdg q5; cx q3,q5; t q4; t q5; h q5; cx q3,q4; t q3; tdg q4; cx q3,q4; rz(pi/8) q5; h q4; cx q1,q4; tdg q4; cx q0,q4; t q4; cx q1,q4; tdg q4; cx q0,q4; t q1; t q4; h q4; cx q0,q1; t q0; tdg q1; cx q0,q1; rz(-pi/16) q4; h q4; cx q3,q4; tdg q4; cx q2,q4; t q4; cx q3,q4; tdg q4; cx q2,q4; t q3; t q4; h q4; cx q2,q3; t q2; tdg q3; cx q2,q3; rz(pi/16) q4; h q4; cx q1,q4; tdg q4; cx q0,q4; t q4; cx q1,q4; tdg q4; cx q0,q4; t q1; t q4; h q4; cx q0,q1; t q0; tdg q1; cx q0,q1; rz(-pi/16) q4; h q4; cx q3,q4; tdg q4; cx q2,q4; t q4; cx q3,q4; tdg q4; cx q2,q4; t q3; t q4; h q4; cx q2,q3; t q2; tdg q3; cx q2,q3; rz(pi/16) q4; h q3; cx q1,q3; tdg q3; cx q0,q3; t q3; cx q1,q3; tdg q3; cx q0,q3; t q1; t q3; h q3; cx q0,q1; t q0; tdg q1; cx q0,q1; rz(-pi/32) q3; cx q2,q3; rz(pi/32) q3; h q3; cx q1,q3; tdg q3; cx q0,q3; t q3; cx q1,q3; tdg q3; cx q0,q3; t q1; t q3; h q3; cx q0,q1; t q0; tdg q1; cx q0,q1; rz(-pi/32) q3; cx q2,q3; rz(pi/32) q3; cx q0,q2; rz(-pi/64) q2; cx q1,q2; rz(pi/64) q2; cx q0,q2; rz(-pi/64) q2; cx q1,q2; rz(pi/64) q2; crz(pi/32) q0,q1; p(pi/64) q0; }
gate mcx q0,q1,q2,q3,q4,q5,q6 { h q6; mcphase(pi) q0,q1,q2,q3,q4,q5,q6; h q6; }
gate mcx_o28 q0,q1,q2,q3,q4,q5,q6 { x q0; x q1; x q5; mcx q0,q1,q2,q3,q4,q5,q6; x q0; x q1; x q5; }
qreg q[7];
cx q[1],q[4];
cx q[2],q[5];
cx q[2],q[6];
cx q[1],q[2];
ccx q[0],q[3],q[1];
ccx q[1],q[4],q[2];
cx q[1],q[4];
ccx q[2],q[5],q[6];
mcx_o28 q[2],q[5],q[0],q[1],q[3],q[4],q[6];
cx q[2],q[5];
x q[4];
ccx q[1],q[4],q[2];
ccx q[0],q[3],q[1];
cx q[0],q[3];
cx q[1],q[2];
cx q[2],q[5];
x q[4];
cx q[1],q[4];