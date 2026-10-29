OPENQASM 2.0;
include "qelib1.inc";
gate r(param0,param1) q0 { u(2.026167409578137,0.2037857985092717,-0.2037857985092717) q0; }
gate mcx q0,q1,q2,q3 { h q3; p(pi/8) q0; p(pi/8) q1; p(pi/8) q2; p(pi/8) q3; cx q0,q1; p(-pi/8) q1; cx q0,q1; cx q1,q2; p(-pi/8) q2; cx q0,q2; p(pi/8) q2; cx q1,q2; p(-pi/8) q2; cx q0,q2; cx q2,q3; p(-pi/8) q3; cx q1,q3; p(pi/8) q3; cx q2,q3; p(-pi/8) q3; cx q0,q3; p(pi/8) q3; cx q2,q3; p(-pi/8) q3; cx q1,q3; p(pi/8) q3; cx q2,q3; p(-pi/8) q3; cx q0,q3; h q3; }
gate c3z q0,q1,q2,q3 { h q3; mcx q0,q1,q2,q3; h q3; }
gate ccz q0,q1,q2 { h q2; ccx q0,q1,q2; h q2; }
qreg q[4];
cswap q[1],q[2],q[0];
t q[3];
rccx q[1],q[3],q[0];
c3sqrtx q[2],q[3],q[1],q[0];
r(2.026167409578137,1.7745821253041683) q[1];
rccx q[3],q[2],q[0];
u(3.772222268266399,1.6460880880040647,0.9388015080041642) q[0];
c3z q[3],q[2],q[0],q[1];
ccz q[2],q[1],q[3];
ccx q[3],q[1],q[0];
ch q[0],q[1];
ch q[3],q[2];