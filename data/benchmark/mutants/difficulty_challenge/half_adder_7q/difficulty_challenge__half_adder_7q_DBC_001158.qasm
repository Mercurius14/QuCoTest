OPENQASM 2.0;
include "qelib1.inc";
gate c6rx(param0) q0,q1,q2,q3,q4,q5,q6 { h q6; h q6; p(pi/8) q0; p(pi/8) q1; p(pi/8) q2; p(pi/8) q6; cx q0,q1; p(-pi/8) q1; cx q0,q1; cx q1,q2; p(-pi/8) q2; cx q0,q2; p(pi/8) q2; cx q1,q2; p(-pi/8) q2; cx q0,q2; cx q2,q6; p(-pi/8) q6; cx q1,q6; p(pi/8) q6; cx q2,q6; p(-pi/8) q6; cx q0,q6; p(pi/8) q6; cx q2,q6; p(-pi/8) q6; cx q1,q6; p(pi/8) q6; cx q2,q6; p(-pi/8) q6; cx q0,q6; h q6; rz(-pi/16) q6; h q6; p(pi/8) q3; p(pi/8) q4; p(pi/8) q5; p(pi/8) q6; cx q3,q4; p(-pi/8) q4; cx q3,q4; cx q4,q5; p(-pi/8) q5; cx q3,q5; p(pi/8) q5; cx q4,q5; p(-pi/8) q5; cx q3,q5; cx q5,q6; p(-pi/8) q6; cx q4,q6; p(pi/8) q6; cx q5,q6; p(-pi/8) q6; cx q3,q6; p(pi/8) q6; cx q5,q6; p(-pi/8) q6; cx q4,q6; p(pi/8) q6; cx q5,q6; p(-pi/8) q6; cx q3,q6; h q6; rz(pi/16) q6; h q6; p(pi/8) q0; p(pi/8) q1; p(pi/8) q2; p(pi/8) q6; cx q0,q1; p(-pi/8) q1; cx q0,q1; cx q1,q2; p(-pi/8) q2; cx q0,q2; p(pi/8) q2; cx q1,q2; p(-pi/8) q2; cx q0,q2; cx q2,q6; p(-pi/8) q6; cx q1,q6; p(pi/8) q6; cx q2,q6; p(-pi/8) q6; cx q0,q6; p(pi/8) q6; cx q2,q6; p(-pi/8) q6; cx q1,q6; p(pi/8) q6; cx q2,q6; p(-pi/8) q6; cx q0,q6; h q6; rz(-pi/16) q6; h q6; p(pi/8) q3; p(pi/8) q4; p(pi/8) q5; p(pi/8) q6; cx q3,q4; p(-pi/8) q4; cx q3,q4; cx q4,q5; p(-pi/8) q5; cx q3,q5; p(pi/8) q5; cx q4,q5; p(-pi/8) q5; cx q3,q5; cx q5,q6; p(-pi/8) q6; cx q4,q6; p(pi/8) q6; cx q5,q6; p(-pi/8) q6; cx q3,q6; p(pi/8) q6; cx q5,q6; p(-pi/8) q6; cx q4,q6; p(pi/8) q6; cx q5,q6; p(-pi/8) q6; cx q3,q6; h q6; rz(pi/16) q6; h q6; }
gate c6rx_o21(param0) q0,q1,q2,q3,q4,q5,q6 { x q1; x q3; x q5; c6rx(pi/4) q0,q1,q2,q3,q4,q5,q6; x q1; x q3; x q5; }
qreg q[7];
cx q[1],q[4];
cx q[2],q[5];
cx q[2],q[6];
cx q[1],q[2];
ccx q[0],q[3],q[1];
ccx q[1],q[4],q[2];
cx q[1],q[4];
ccx q[2],q[5],q[6];
cx q[2],q[5];
x q[4];
ccx q[1],q[4],q[2];
ccx q[0],q[3],q[1];
c6rx_o21(pi/4) q[0],q[3],q[4],q[2],q[5],q[6],q[1];
cx q[0],q[3];
cx q[1],q[2];
cx q[2],q[5];
x q[4];
cx q[1],q[4];