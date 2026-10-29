OPENQASM 2.0;
include "qelib1.inc";
gate c3rx(param0) q0,q1,q2,q3 { cu(pi/32,-pi/2,pi/2,0) q2,q3; cx q2,q1; cu(-pi/32,-pi/2,pi/2,0) q1,q3; cx q2,q1; cu(pi/32,-pi/2,pi/2,0) q1,q3; cx q1,q0; cu(-pi/32,-pi/2,pi/2,0) q0,q3; cx q2,q0; cu(pi/32,-pi/2,pi/2,0) q0,q3; cx q1,q0; cu(-pi/32,-pi/2,pi/2,0) q0,q3; cx q2,q0; cu(pi/32,-pi/2,pi/2,0) q0,q3; }
gate ecr q0,q1 { s q0; sx q1; cx q0,q1; x q0; }
gate csdg q0,q1 { tdg q0; cx q0,q1; t q1; cx q0,q1; tdg q1; }
qreg q[5];
t q[1];
cswap q[0],q[3],q[2];
swap q[3],q[2];
cswap q[4],q[0],q[1];
t q[1];
c3sqrtx q[3],q[2],q[4],q[0];
c3rx(pi/8) q[3],q[2],q[4],q[0];
ecr q[0],q[2];
t q[0];
cu(4.07828399178064,5.2625683110417505,4.875952527358193,2.1332392738715247) q[2],q[4];
cz q[3],q[1];
tdg q[1];
ccx q[3],q[1],q[2];
rccx q[2],q[0],q[4];
cu1(2.6610319766865294) q[0],q[3];
rccx q[4],q[2],q[1];
csdg q[0],q[4];
u1(3.981707520827624) q[0];
cy q[2],q[1];
ecr q[1],q[4];
rzz(1.7530182469673898) q[2],q[3];