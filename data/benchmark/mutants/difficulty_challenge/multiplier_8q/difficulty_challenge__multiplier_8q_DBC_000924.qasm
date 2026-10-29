OPENQASM 2.0;
include "qelib1.inc";
gate qft q0,q1,q2,q3 { h q3; cp(pi/2) q3,q2; cp(pi/4) q3,q1; cp(pi/8) q3,q0; h q2; cp(pi/2) q2,q1; cp(pi/4) q2,q0; h q1; cp(pi/2) q1,q0; h q0; swap q0,q3; swap q1,q2; }
gate mcphase(param0) q0,q1,q2 { cx q0,q2; rz(-pi) q2; cx q1,q2; rz(pi) q2; cx q0,q2; rz(-pi) q2; cx q1,q2; rz(pi) q2; crz(2*pi) q0,q1; p(pi) q0; }
gate mcphase_custom_001(param0) q0,q1,q2 { cx q0,q2; rz(-pi/2) q2; cx q1,q2; rz(pi/2) q2; cx q0,q2; rz(-pi/2) q2; cx q1,q2; rz(pi/2) q2; crz(pi) q0,q1; p(pi/2) q0; }
gate mcphase_custom_002(param0) q0,q1,q2 { cx q0,q2; rz(-pi/4) q2; cx q1,q2; rz(pi/4) q2; cx q0,q2; rz(-pi/4) q2; cx q1,q2; rz(pi/4) q2; crz(pi/2) q0,q1; p(pi/4) q0; }
gate mcphase_custom_003(param0) q0,q1,q2 { cx q0,q2; rz(-pi/8) q2; cx q1,q2; rz(pi/8) q2; cx q0,q2; rz(-pi/8) q2; cx q1,q2; rz(pi/8) q2; crz(pi/4) q0,q1; p(pi/8) q0; }
gate mcphase_custom_004(param0) q0,q1,q2 { cx q0,q2; rz(-pi/2) q2; cx q1,q2; rz(pi/2) q2; cx q0,q2; rz(-pi/2) q2; cx q1,q2; rz(pi/2) q2; crz(pi) q0,q1; p(pi/2) q0; }
gate mcphase_custom_005(param0) q0,q1,q2 { cx q0,q2; rz(-pi/2) q2; cx q1,q2; rz(pi/2) q2; cx q0,q2; rz(-pi/2) q2; cx q1,q2; rz(pi/2) q2; crz(pi) q0,q1; p(pi/2) q0; }
gate mcphase_custom_006(param0) q0,q1,q2 { cx q0,q2; rz(-pi/4) q2; cx q1,q2; rz(pi/4) q2; cx q0,q2; rz(-pi/4) q2; cx q1,q2; rz(pi/4) q2; crz(pi/2) q0,q1; p(pi/4) q0; }
gate mcphase_custom_007(param0) q0,q1,q2 { cx q0,q2; rz(-pi/4) q2; cx q1,q2; rz(pi/4) q2; cx q0,q2; rz(-pi/4) q2; cx q1,q2; rz(pi/4) q2; crz(pi/2) q0,q1; p(pi/4) q0; }
gate mcphase_custom_008(param0) q0,q1,q2 { cx q0,q2; rz(-pi/8) q2; cx q1,q2; rz(pi/8) q2; cx q0,q2; rz(-pi/8) q2; cx q1,q2; rz(pi/8) q2; crz(pi/4) q0,q1; p(pi/8) q0; }
gate mcphase_custom_009(param0) q0,q1,q2 { cx q0,q2; rz(-pi/8) q2; cx q1,q2; rz(pi/8) q2; cx q0,q2; rz(-pi/8) q2; cx q1,q2; rz(pi/8) q2; crz(pi/4) q0,q1; p(pi/8) q0; }
gate mcphase_custom_010(param0) q0,q1,q2 { cx q0,q2; rz(-pi/16) q2; cx q1,q2; rz(pi/16) q2; cx q0,q2; rz(-pi/16) q2; cx q1,q2; rz(pi/16) q2; crz(pi/8) q0,q1; p(pi/16) q0; }
gate c7rx(param0) q0,q1,q2,q3,q4,q5,q6,q7 { h q7; h q7; cx q5,q7; tdg q7; cx q3,q7; t q7; cx q5,q7; tdg q7; cx q3,q7; t q5; t q7; h q7; cx q3,q5; t q3; tdg q5; cx q3,q5; h q5; t q5; cx q2,q5; tdg q5; cx q4,q5; h q4; t q4; cx q1,q4; tdg q4; cx q0,q4; t q4; cx q1,q4; tdg q4; h q4; cx q4,q5; t q5; cx q2,q5; tdg q5; h q5; h q7; cx q5,q7; tdg q7; cx q3,q7; t q7; cx q5,q7; tdg q7; cx q3,q7; t q5; t q7; h q7; cx q3,q5; t q3; tdg q5; cx q3,q5; h q5; t q5; cx q2,q5; tdg q5; cx q4,q5; h q4; t q4; cx q1,q4; tdg q4; cx q0,q4; t q4; cx q1,q4; tdg q4; h q4; cx q4,q5; t q5; cx q2,q5; tdg q5; h q5; rz(-pi/16) q7; h q7; p(pi/8) q4; p(pi/8) q5; p(pi/8) q6; p(pi/8) q7; cx q4,q5; p(-pi/8) q5; cx q4,q5; cx q5,q6; p(-pi/8) q6; cx q4,q6; p(pi/8) q6; cx q5,q6; p(-pi/8) q6; cx q4,q6; cx q6,q7; p(-pi/8) q7; cx q5,q7; p(pi/8) q7; cx q6,q7; p(-pi/8) q7; cx q4,q7; p(pi/8) q7; cx q6,q7; p(-pi/8) q7; cx q5,q7; p(pi/8) q7; cx q6,q7; p(-pi/8) q7; cx q4,q7; h q7; rz(pi/16) q7; h q7; cx q5,q7; tdg q7; cx q3,q7; t q7; cx q5,q7; tdg q7; cx q3,q7; t q5; t q7; h q7; cx q3,q5; t q3; tdg q5; cx q3,q5; h q5; t q5; cx q2,q5; tdg q5; cx q4,q5; h q4; t q4; cx q1,q4; tdg q4; cx q0,q4; t q4; cx q1,q4; tdg q4; h q4; cx q4,q5; t q5; cx q2,q5; tdg q5; h q5; h q7; cx q5,q7; tdg q7; cx q3,q7; t q7; cx q5,q7; tdg q7; cx q3,q7; t q5; t q7; h q7; cx q3,q5; t q3; tdg q5; cx q3,q5; h q5; t q5; cx q2,q5; tdg q5; cx q4,q5; h q4; t q4; cx q1,q4; tdg q4; cx q0,q4; t q4; cx q1,q4; tdg q4; h q4; cx q4,q5; t q5; cx q2,q5; tdg q5; h q5; rz(-pi/16) q7; h q7; p(pi/8) q4; p(pi/8) q5; p(pi/8) q6; p(pi/8) q7; cx q4,q5; p(-pi/8) q5; cx q4,q5; cx q5,q6; p(-pi/8) q6; cx q4,q6; p(pi/8) q6; cx q5,q6; p(-pi/8) q6; cx q4,q6; cx q6,q7; p(-pi/8) q7; cx q5,q7; p(pi/8) q7; cx q6,q7; p(-pi/8) q7; cx q4,q7; p(pi/8) q7; cx q6,q7; p(-pi/8) q7; cx q5,q7; p(pi/8) q7; cx q6,q7; p(-pi/8) q7; cx q4,q7; h q7; rz(pi/16) q7; h q7; }
gate c7rx_o15(param0) q0,q1,q2,q3,q4,q5,q6,q7 { x q4; x q5; x q6; c7rx(pi/4) q0,q1,q2,q3,q4,q5,q6,q7; x q4; x q5; x q6; }
gate mcphase_custom_011(param0) q0,q1,q2 { cx q0,q2; rz(-pi/16) q2; cx q1,q2; rz(pi/16) q2; cx q0,q2; rz(-pi/16) q2; cx q1,q2; rz(pi/16) q2; crz(pi/8) q0,q1; p(pi/16) q0; }
gate mcphase_custom_012(param0) q0,q1,q2 { cx q0,q2; rz(-pi/4) q2; cx q1,q2; rz(pi/4) q2; cx q0,q2; rz(-pi/4) q2; cx q1,q2; rz(pi/4) q2; crz(pi/2) q0,q1; p(pi/4) q0; }
gate mcphase_custom_013(param0) q0,q1,q2 { cx q0,q2; rz(-pi/8) q2; cx q1,q2; rz(pi/8) q2; cx q0,q2; rz(-pi/8) q2; cx q1,q2; rz(pi/8) q2; crz(pi/4) q0,q1; p(pi/8) q0; }
gate mcphase_custom_014(param0) q0,q1,q2 { cx q0,q2; rz(-pi/16) q2; cx q1,q2; rz(pi/16) q2; cx q0,q2; rz(-pi/16) q2; cx q1,q2; rz(pi/16) q2; crz(pi/8) q0,q1; p(pi/16) q0; }
gate mcphase_custom_015(param0) q0,q1,q2 { cx q0,q2; rz(-pi/32) q2; cx q1,q2; rz(pi/32) q2; cx q0,q2; rz(-pi/32) q2; cx q1,q2; rz(pi/32) q2; crz(pi/16) q0,q1; p(pi/32) q0; }
gate qft_dg q0,q1,q2,q3 { swap q1,q2; swap q0,q3; h q0; cp(-pi/2) q1,q0; h q1; cp(-pi/4) q2,q0; cp(-pi/2) q2,q1; h q2; cp(-pi/8) q3,q0; cp(-pi/4) q3,q1; cp(-pi/2) q3,q2; h q3; }
qreg q[8];
qft q[4],q[5],q[6],q[7];
mcphase(4*pi) q[1],q[3],q[7];
mcphase_custom_001(2*pi) q[1],q[3],q[6];
mcphase_custom_002(pi) q[1],q[3],q[5];
mcphase_custom_003(pi/2) q[1],q[3],q[4];
mcphase_custom_004(2*pi) q[1],q[2],q[7];
mcphase_custom_005(2*pi) q[0],q[3],q[7];
mcphase_custom_006(pi) q[1],q[2],q[6];
mcphase_custom_007(pi) q[0],q[3],q[6];
mcphase_custom_008(pi/2) q[1],q[2],q[5];
mcphase_custom_009(pi/2) q[0],q[3],q[5];
mcphase_custom_010(pi/4) q[1],q[2],q[4];
c7rx_o15(pi/4) q[1],q[2],q[0],q[3],q[5],q[6],q[7],q[4];
mcphase_custom_011(pi/4) q[0],q[3],q[4];
mcphase_custom_012(pi) q[0],q[2],q[7];
mcphase_custom_013(pi/2) q[0],q[2],q[6];
mcphase_custom_014(pi/4) q[0],q[2],q[5];
mcphase_custom_015(pi/8) q[0],q[2],q[4];
qft_dg q[4],q[5],q[6],q[7];