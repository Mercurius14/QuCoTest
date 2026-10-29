OPENQASM 2.0;
include "qelib1.inc";
gate ccz q0,q1,q2 { h q2; ccx q0,q1,q2; h q2; }
gate mcphase(param0) q0,q1,q2,q3,q4,q5,q6 { h q6; p(pi/8) q0; p(pi/8) q1; p(pi/8) q2; p(pi/8) q6; cx q0,q1; p(-pi/8) q1; cx q0,q1; cx q1,q2; p(-pi/8) q2; cx q0,q2; p(pi/8) q2; cx q1,q2; p(-pi/8) q2; cx q0,q2; cx q2,q6; p(-pi/8) q6; cx q1,q6; p(pi/8) q6; cx q2,q6; p(-pi/8) q6; cx q0,q6; p(pi/8) q6; cx q2,q6; p(-pi/8) q6; cx q1,q6; p(pi/8) q6; cx q2,q6; p(-pi/8) q6; cx q0,q6; h q6; rz(-pi/16) q6; h q6; p(pi/8) q3; p(pi/8) q4; p(pi/8) q5; p(pi/8) q6; cx q3,q4; p(-pi/8) q4; cx q3,q4; cx q4,q5; p(-pi/8) q5; cx q3,q5; p(pi/8) q5; cx q4,q5; p(-pi/8) q5; cx q3,q5; cx q5,q6; p(-pi/8) q6; cx q4,q6; p(pi/8) q6; cx q5,q6; p(-pi/8) q6; cx q3,q6; p(pi/8) q6; cx q5,q6; p(-pi/8) q6; cx q4,q6; p(pi/8) q6; cx q5,q6; p(-pi/8) q6; cx q3,q6; h q6; rz(pi/16) q6; h q6; p(pi/8) q0; p(pi/8) q1; p(pi/8) q2; p(pi/8) q6; cx q0,q1; p(-pi/8) q1; cx q0,q1; cx q1,q2; p(-pi/8) q2; cx q0,q2; p(pi/8) q2; cx q1,q2; p(-pi/8) q2; cx q0,q2; cx q2,q6; p(-pi/8) q6; cx q1,q6; p(pi/8) q6; cx q2,q6; p(-pi/8) q6; cx q0,q6; p(pi/8) q6; cx q2,q6; p(-pi/8) q6; cx q1,q6; p(pi/8) q6; cx q2,q6; p(-pi/8) q6; cx q0,q6; h q6; rz(-pi/16) q6; h q6; p(pi/8) q3; p(pi/8) q4; p(pi/8) q5; p(pi/8) q6; cx q3,q4; p(-pi/8) q4; cx q3,q4; cx q4,q5; p(-pi/8) q5; cx q3,q5; p(pi/8) q5; cx q4,q5; p(-pi/8) q5; cx q3,q5; cx q5,q6; p(-pi/8) q6; cx q4,q6; p(pi/8) q6; cx q5,q6; p(-pi/8) q6; cx q3,q6; p(pi/8) q6; cx q5,q6; p(-pi/8) q6; cx q4,q6; p(pi/8) q6; cx q5,q6; p(-pi/8) q6; cx q3,q6; h q6; rz(pi/16) q6; h q5; p(pi/8) q0; p(pi/8) q1; p(pi/8) q2; p(pi/8) q5; cx q0,q1; p(-pi/8) q1; cx q0,q1; cx q1,q2; p(-pi/8) q2; cx q0,q2; p(pi/8) q2; cx q1,q2; p(-pi/8) q2; cx q0,q2; cx q2,q5; p(-pi/8) q5; cx q1,q5; p(pi/8) q5; cx q2,q5; p(-pi/8) q5; cx q0,q5; p(pi/8) q5; cx q2,q5; p(-pi/8) q5; cx q1,q5; p(pi/8) q5; cx q2,q5; p(-pi/8) q5; cx q0,q5; h q5; rz(-pi/32) q5; h q5; cx q4,q5; tdg q5; cx q3,q5; t q5; cx q4,q5; tdg q5; cx q3,q5; t q4; t q5; h q5; cx q3,q4; t q3; tdg q4; cx q3,q4; rz(pi/32) q5; h q5; p(pi/8) q0; p(pi/8) q1; p(pi/8) q2; p(pi/8) q5; cx q0,q1; p(-pi/8) q1; cx q0,q1; cx q1,q2; p(-pi/8) q2; cx q0,q2; p(pi/8) q2; cx q1,q2; p(-pi/8) q2; cx q0,q2; cx q2,q5; p(-pi/8) q5; cx q1,q5; p(pi/8) q5; cx q2,q5; p(-pi/8) q5; cx q0,q5; p(pi/8) q5; cx q2,q5; p(-pi/8) q5; cx q1,q5; p(pi/8) q5; cx q2,q5; p(-pi/8) q5; cx q0,q5; h q5; rz(-pi/32) q5; h q5; cx q4,q5; tdg q5; cx q3,q5; t q5; cx q4,q5; tdg q5; cx q3,q5; t q4; t q5; h q5; cx q3,q4; t q3; tdg q4; cx q3,q4; rz(pi/32) q5; h q4; cx q1,q4; tdg q4; cx q0,q4; t q4; cx q1,q4; tdg q4; cx q0,q4; t q1; t q4; h q4; cx q0,q1; t q0; tdg q1; cx q0,q1; rz(-pi/64) q4; h q4; cx q3,q4; tdg q4; cx q2,q4; t q4; cx q3,q4; tdg q4; cx q2,q4; t q3; t q4; h q4; cx q2,q3; t q2; tdg q3; cx q2,q3; rz(pi/64) q4; h q4; cx q1,q4; tdg q4; cx q0,q4; t q4; cx q1,q4; tdg q4; cx q0,q4; t q1; t q4; h q4; cx q0,q1; t q0; tdg q1; cx q0,q1; rz(-pi/64) q4; h q4; cx q3,q4; tdg q4; cx q2,q4; t q4; cx q3,q4; tdg q4; cx q2,q4; t q3; t q4; h q4; cx q2,q3; t q2; tdg q3; cx q2,q3; rz(pi/64) q4; h q3; cx q1,q3; tdg q3; cx q0,q3; t q3; cx q1,q3; tdg q3; cx q0,q3; t q1; t q3; h q3; cx q0,q1; t q0; tdg q1; cx q0,q1; rz(-0.02454369260617026) q3; cx q2,q3; rz(0.02454369260617026) q3; h q3; cx q1,q3; tdg q3; cx q0,q3; t q3; cx q1,q3; tdg q3; cx q0,q3; t q1; t q3; h q3; cx q0,q1; t q0; tdg q1; cx q0,q1; rz(-0.02454369260617026) q3; cx q2,q3; rz(0.02454369260617026) q3; cx q0,q2; rz(-0.01227184630308513) q2; cx q1,q2; rz(0.01227184630308513) q2; cx q0,q2; rz(-0.01227184630308513) q2; cx q1,q2; rz(0.01227184630308513) q2; crz(0.02454369260617026) q0,q1; p(0.01227184630308513) q0; }
gate mcphase_o42(param0) q0,q1,q2,q3,q4,q5,q6 { x q0; x q2; x q4; mcphase(pi/4) q0,q1,q2,q3,q4,q5,q6; x q0; x q2; x q4; }
gate ecr q0,q1 { s q0; sx q1; cx q0,q1; x q0; }
gate csdg q0,q1 { tdg q0; cx q0,q1; t q1; cx q0,q1; tdg q1; }
gate r(param0,param1) q0 { u(0.12487864535773079,0.8822725062196755,-0.8822725062196755) q0; }
gate rcccx q0,q1,q2,q3 { h q3; t q3; cx q2,q3; tdg q3; h q3; cx q0,q3; t q3; cx q1,q3; tdg q3; cx q0,q3; t q3; cx q1,q3; tdg q3; h q3; t q3; cx q2,q3; tdg q3; h q3; }
qreg q[7];
t q[3];
ccz q[4],q[2],q[0];
mcphase_o42(pi/4) q[4],q[2],q[1],q[3],q[5],q[6],q[0];
ecr q[3],q[0];
cswap q[1],q[5],q[6];
c3sqrtx q[2],q[4],q[1],q[5];
cswap q[0],q[3],q[1];
csdg q[4],q[5];
t q[5];
sdg q[5];
tdg q[6];
cz q[6],q[2];
cry(0.9334849134188741) q[3],q[2];
ccx q[4],q[6],q[1];
ccz q[0],q[6],q[3];
ch q[2],q[1];
ccx q[4],q[5],q[0];
cy q[1],q[0];
cswap q[6],q[2],q[3];
ccx q[3],q[4],q[2];
h q[2];
ccz q[4],q[3],q[1];
ccz q[1],q[2],q[4];
csdg q[5],q[6];
ccz q[6],q[5],q[0];
r(0.12487864535773079,2.453068833014572) q[0];
crz(5.625348551233995) q[5],q[3];
ccx q[0],q[5],q[4];
rccx q[3],q[1],q[2];
rcccx q[2],q[1],q[4],q[5];
x q[6];
cswap q[6],q[3],q[0];
sdg q[0];
rccx q[2],q[4],q[6];
rccx q[3],q[5],q[1];
rccx q[2],q[3],q[0];
ry(1.2956580914789548) q[2];
rcccx q[6],q[4],q[1],q[5];
cu3(5.698148910708643,0.7232928624012734,2.3386467136971576) q[0],q[6];
ccx q[3],q[1],q[4];
sx q[5];