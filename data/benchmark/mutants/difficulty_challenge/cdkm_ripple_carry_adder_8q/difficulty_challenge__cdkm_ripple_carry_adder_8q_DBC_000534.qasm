OPENQASM 2.0;
include "qelib1.inc";
gate c7rx(param0) q0,q1,q2,q3,q4,q5,q6,q7 { h q7; h q7; cx q5,q7; tdg q7; cx q3,q7; t q7; cx q5,q7; tdg q7; cx q3,q7; t q5; t q7; h q7; cx q3,q5; t q3; tdg q5; cx q3,q5; h q5; t q5; cx q2,q5; tdg q5; cx q4,q5; h q4; t q4; cx q1,q4; tdg q4; cx q0,q4; t q4; cx q1,q4; tdg q4; h q4; cx q4,q5; t q5; cx q2,q5; tdg q5; h q5; h q7; cx q5,q7; tdg q7; cx q3,q7; t q7; cx q5,q7; tdg q7; cx q3,q7; t q5; t q7; h q7; cx q3,q5; t q3; tdg q5; cx q3,q5; h q5; t q5; cx q2,q5; tdg q5; cx q4,q5; h q4; t q4; cx q1,q4; tdg q4; cx q0,q4; t q4; cx q1,q4; tdg q4; h q4; cx q4,q5; t q5; cx q2,q5; tdg q5; h q5; rz(-pi/16) q7; h q7; p(pi/8) q4; p(pi/8) q5; p(pi/8) q6; p(pi/8) q7; cx q4,q5; p(-pi/8) q5; cx q4,q5; cx q5,q6; p(-pi/8) q6; cx q4,q6; p(pi/8) q6; cx q5,q6; p(-pi/8) q6; cx q4,q6; cx q6,q7; p(-pi/8) q7; cx q5,q7; p(pi/8) q7; cx q6,q7; p(-pi/8) q7; cx q4,q7; p(pi/8) q7; cx q6,q7; p(-pi/8) q7; cx q5,q7; p(pi/8) q7; cx q6,q7; p(-pi/8) q7; cx q4,q7; h q7; rz(pi/16) q7; h q7; cx q5,q7; tdg q7; cx q3,q7; t q7; cx q5,q7; tdg q7; cx q3,q7; t q5; t q7; h q7; cx q3,q5; t q3; tdg q5; cx q3,q5; h q5; t q5; cx q2,q5; tdg q5; cx q4,q5; h q4; t q4; cx q1,q4; tdg q4; cx q0,q4; t q4; cx q1,q4; tdg q4; h q4; cx q4,q5; t q5; cx q2,q5; tdg q5; h q5; h q7; cx q5,q7; tdg q7; cx q3,q7; t q7; cx q5,q7; tdg q7; cx q3,q7; t q5; t q7; h q7; cx q3,q5; t q3; tdg q5; cx q3,q5; h q5; t q5; cx q2,q5; tdg q5; cx q4,q5; h q4; t q4; cx q1,q4; tdg q4; cx q0,q4; t q4; cx q1,q4; tdg q4; h q4; cx q4,q5; t q5; cx q2,q5; tdg q5; h q5; rz(-pi/16) q7; h q7; p(pi/8) q4; p(pi/8) q5; p(pi/8) q6; p(pi/8) q7; cx q4,q5; p(-pi/8) q5; cx q4,q5; cx q5,q6; p(-pi/8) q6; cx q4,q6; p(pi/8) q6; cx q5,q6; p(-pi/8) q6; cx q4,q6; cx q6,q7; p(-pi/8) q7; cx q5,q7; p(pi/8) q7; cx q6,q7; p(-pi/8) q7; cx q4,q7; p(pi/8) q7; cx q6,q7; p(-pi/8) q7; cx q5,q7; p(pi/8) q7; cx q6,q7; p(-pi/8) q7; cx q4,q7; h q7; rz(pi/16) q7; h q7; }
gate c7rx_o7(param0) q0,q1,q2,q3,q4,q5,q6,q7 { x q3; x q4; x q5; x q6; c7rx(pi/4) q0,q1,q2,q3,q4,q5,q6,q7; x q3; x q4; x q5; x q6; }
qreg q[8];
cx q[1],q[4];
cx q[1],q[0];
ccx q[0],q[4],q[1];
c7rx_o7(pi/4) q[0],q[4],q[2],q[5],q[6],q[3],q[7],q[1];
cx q[2],q[5];
cx q[2],q[1];
ccx q[1],q[5],q[2];
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