OPENQASM 2.0;
include "qelib1.inc";
gate mcx q0,q1,q2,q3,q4 { h q4; cp(pi/2) q3,q4; h q4; h q3; t q3; cx q2,q3; tdg q3; h q3; cx q0,q3; t q3; cx q1,q3; tdg q3; cx q0,q3; t q3; cx q1,q3; tdg q3; h q3; t q3; cx q2,q3; tdg q3; h q3; h q4; cp(-pi/2) q3,q4; h q4; h q3; t q3; cx q2,q3; tdg q3; h q3; t q3; cx q1,q3; tdg q3; cx q0,q3; t q3; cx q1,q3; tdg q3; cx q0,q3; h q3; t q3; cx q2,q3; tdg q3; h q3; h q4; cp(pi/8) q0,q4; h q4; cx q0,q1; h q4; cp(-pi/8) q1,q4; h q4; cx q0,q1; h q4; cp(pi/8) q1,q4; h q4; cx q1,q2; h q4; cp(-pi/8) q2,q4; h q4; cx q0,q2; h q4; cp(pi/8) q2,q4; h q4; cx q1,q2; h q4; cp(-pi/8) q2,q4; h q4; cx q0,q2; h q4; cp(pi/8) q2,q4; h q4; }
gate mcx_custom_001 q0,q1,q2,q3 { h q3; p(pi/8) q0; p(pi/8) q1; p(pi/8) q2; p(pi/8) q3; cx q0,q1; p(-pi/8) q1; cx q0,q1; cx q1,q2; p(-pi/8) q2; cx q0,q2; p(pi/8) q2; cx q1,q2; p(-pi/8) q2; cx q0,q2; cx q2,q3; p(-pi/8) q3; cx q1,q3; p(pi/8) q3; cx q2,q3; p(-pi/8) q3; cx q0,q3; p(pi/8) q3; cx q2,q3; p(-pi/8) q3; cx q1,q3; p(pi/8) q3; cx q2,q3; p(-pi/8) q3; cx q0,q3; h q3; }
gate c3rx(param0) q0,q1,q2,q3 { cu(pi/16,-pi/2,pi/2,0) q2,q3; cx q2,q1; cu(-pi/16,-pi/2,pi/2,0) q1,q3; cx q2,q1; cu(pi/16,-pi/2,pi/2,0) q1,q3; cx q1,q0; cu(-pi/16,-pi/2,pi/2,0) q0,q3; cx q2,q0; cu(pi/16,-pi/2,pi/2,0) q0,q3; cx q1,q0; cu(-pi/16,-pi/2,pi/2,0) q0,q3; cx q2,q0; cu(pi/16,-pi/2,pi/2,0) q0,q3; }
gate mcx_custom_002 q0,q1,q2,q3 { h q3; p(pi/8) q0; p(pi/8) q1; p(pi/8) q2; p(pi/8) q3; cx q0,q1; p(-pi/8) q1; cx q0,q1; cx q1,q2; p(-pi/8) q2; cx q0,q2; p(pi/8) q2; cx q1,q2; p(-pi/8) q2; cx q0,q2; cx q2,q3; p(-pi/8) q3; cx q1,q3; p(pi/8) q3; cx q2,q3; p(-pi/8) q3; cx q0,q3; p(pi/8) q3; cx q2,q3; p(-pi/8) q3; cx q1,q3; p(pi/8) q3; cx q2,q3; p(-pi/8) q3; cx q0,q3; h q3; }
qreg q[5];
h q[4];
mcx q[4],q[1],q[2],q[3],q[0];
mcx_custom_001 q[4],q[2],q[3],q[1];
c3rx(pi/4) q[4],q[2],q[3],q[1];
ccx q[4],q[3],q[2];
cx q[4],q[3];
x q[4];
x q[1];
x q[2];
x q[3];
mcx q[4],q[1],q[2],q[3],q[0];
mcx_custom_002 q[4],q[2],q[3],q[1];
ccx q[4],q[3],q[2];
cx q[4],q[3];
x q[1];
x q[2];
x q[3];
x q[4];