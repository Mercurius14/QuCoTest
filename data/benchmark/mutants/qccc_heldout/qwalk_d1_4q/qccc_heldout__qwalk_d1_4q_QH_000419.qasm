OPENQASM 2.0;
include "qelib1.inc";
gate mcx q0,q1,q2,q3 { h q3; p(pi/8) q0; p(pi/8) q1; p(pi/8) q2; p(pi/8) q3; cx q0,q1; p(-pi/8) q1; cx q0,q1; cx q1,q2; p(-pi/8) q2; cx q0,q2; p(pi/8) q2; cx q1,q2; p(-pi/8) q2; cx q0,q2; cx q2,q3; p(-pi/8) q3; cx q1,q3; p(pi/8) q3; cx q2,q3; p(-pi/8) q3; cx q0,q3; p(pi/8) q3; cx q2,q3; p(-pi/8) q3; cx q1,q3; p(pi/8) q3; cx q2,q3; p(-pi/8) q3; cx q0,q3; h q3; }
gate ccry(param0) q0,q1,q2 { cu(pi/16,0,0,0) q1,q2; cx q1,q0; cu(-pi/16,0,0,0) q0,q2; cx q1,q0; cu(pi/16,0,0,0) q0,q2; }
qreg q[4];
h q[3];
mcx q[3],q[1],q[2],q[0];
ccx q[3],q[2],q[1];
ccry(pi/8) q[3],q[2],q[1];
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