OPENQASM 2.0;
include "qelib1.inc";
gate mcphase(param0) q0,q1 { cp(-pi/4) q0,q1; }
gate mcphase_custom_001(param0) q0,q1 { cp(pi/4) q0,q1; }
gate mcphase_custom_002(param0) q0,q1 { cp(pi/4) q0,q1; }
gate mcphase_custom_003(param0) q0,q1 { cp(pi/4) q0,q1; }
gate mcphase_custom_004(param0) q0,q1 { cp(pi/4) q0,q1; }
gate mcphase_custom_005(param0) q0,q1 { cp(pi/4) q0,q1; }
gate mcphase_custom_006(param0) q0,q1 { cp(pi/4) q0,q1; }
gate mcphase_custom_007(param0) q0,q1 { cp(pi/4) q0,q1; }
gate ccrx(param0) q0,q1,q2 { cu(pi/8,-pi/2,pi/2,0) q1,q2; cx q1,q0; cu(-pi/8,-pi/2,pi/2,0) q0,q2; cx q1,q0; cu(pi/8,-pi/2,pi/2,0) q0,q2; }
gate mcphase_custom_008(param0) q0,q1 { cp(pi/4) q0,q1; }
gate mcphase_custom_009(param0) q0,q1 { cp(pi/4) q0,q1; }
gate mcphase_custom_010(param0) q0,q1 { cp(pi/4) q0,q1; }
gate mcphase_custom_011(param0) q0,q1 { cp(pi/4) q0,q1; }
gate mcphase_custom_012(param0) q0,q1 { cp(pi/4) q0,q1; }
gate mcphase_custom_013(param0) q0,q1 { cp(pi/4) q0,q1; }
gate mcphase_custom_014(param0) q0,q1 { cp(pi/4) q0,q1; }
gate mcphase_custom_015(param0) q0,q1 { cp(pi/4) q0,q1; }
gate mcphase_custom_016(param0) q0,q1 { cp(pi/4) q0,q1; }
gate mcphase_custom_017(param0) q0,q1 { cp(pi/4) q0,q1; }
gate mcphase_custom_018(param0) q0,q1 { cp(pi/4) q0,q1; }
gate mcphase_custom_019(param0) q0,q1 { cp(pi/4) q0,q1; }
gate mcphase_custom_020(param0) q0,q1 { cp(pi/4) q0,q1; }
gate mcphase_custom_021(param0) q0,q1 { cp(pi/4) q0,q1; }
gate mcphase_custom_022(param0) q0,q1 { cp(pi/4) q0,q1; }
gate mcphase_custom_023(param0) q0,q1 { cp(pi/4) q0,q1; }
gate mcphase_custom_024(param0) q0,q1 { cp(pi/4) q0,q1; }
gate mcphase_custom_025(param0) q0,q1 { cp(pi/4) q0,q1; }
gate mcphase_custom_026(param0) q0,q1 { cp(pi/4) q0,q1; }
gate mcphase_custom_027(param0) q0,q1 { cp(pi/4) q0,q1; }
gate mcphase_custom_028(param0) q0,q1 { cp(pi/4) q0,q1; }
gate mcphase_custom_029(param0) q0,q1 { cp(pi/4) q0,q1; }
gate mcphase_custom_030(param0) q0,q1 { cp(pi/4) q0,q1; }
gate mcphase_custom_031(param0) q0,q1 { cp(pi/4) q0,q1; }
gate mcphase_custom_032(param0) q0,q1 { cp(pi/4) q0,q1; }
qreg q[9];
ccx q[0],q[2],q[4];
ccx q[0],q[3],q[5];
ccx q[0],q[2],q[8];
s q[2];
h q[2];
t q[2];
cx q[0],q[2];
tdg q[2];
h q[2];
sdg q[2];
ccx q[0],q[4],q[2];
mcphase(-pi/4) q[0],q[2];
ccx q[0],q[8],q[2];
mcphase_custom_001(pi/4) q[0],q[2];
ccx q[0],q[4],q[2];
mcphase(-pi/4) q[0],q[2];
mcphase_custom_002(pi/4) q[0],q[4];
ccx q[0],q[8],q[2];
mcphase_custom_003(pi/4) q[0],q[2];
s q[2];
h q[2];
t q[2];
cx q[0],q[2];
tdg q[2];
h q[2];
sdg q[2];
ccx q[0],q[3],q[2];
s q[3];
h q[3];
t q[3];
cx q[0],q[3];
tdg q[3];
h q[3];
sdg q[3];
ccx q[0],q[5],q[3];
mcphase(-pi/4) q[0],q[3];
ccx q[0],q[2],q[3];
mcphase_custom_004(pi/4) q[0],q[3];
ccx q[0],q[5],q[3];
mcphase(-pi/4) q[0],q[3];
ccx q[0],q[2],q[3];
mcphase_custom_005(pi/4) q[0],q[3];
s q[3];
h q[3];
t q[3];
cx q[0],q[3];
tdg q[3];
h q[3];
sdg q[3];
ccx q[0],q[3],q[6];
s q[3];
h q[3];
t q[3];
cx q[0],q[3];
mcphase_custom_006(pi/4) q[0],q[5];
ccx q[0],q[2],q[5];
mcphase_custom_007(pi/4) q[0],q[2];
mcphase(-pi/4) q[0],q[5];
ccx q[0],q[2],q[5];
tdg q[3];
h q[3];
sdg q[3];
ccx q[0],q[5],q[3];
mcphase(-pi/4) q[0],q[3];
ccx q[0],q[2],q[3];
ccrx(pi/4) q[0],q[2],q[3];
mcphase_custom_008(pi/4) q[0],q[3];
ccx q[0],q[5],q[3];
mcphase(-pi/4) q[0],q[3];
ccx q[0],q[2],q[3];
mcphase_custom_009(pi/4) q[0],q[3];
s q[3];
h q[3];
t q[3];
cx q[0],q[3];
mcphase_custom_010(pi/4) q[0],q[5];
ccx q[0],q[2],q[5];
mcphase_custom_011(pi/4) q[0],q[2];
mcphase(-pi/4) q[0],q[5];
ccx q[0],q[2],q[5];
tdg q[3];
h q[3];
sdg q[3];
ccx q[0],q[3],q[2];
ccx q[0],q[2],q[5];
s q[2];
h q[2];
t q[2];
cx q[0],q[2];
ccx q[0],q[8],q[4];
mcphase(-pi/4) q[0],q[4];
mcphase_custom_012(pi/4) q[0],q[8];
ccx q[0],q[8],q[4];
tdg q[2];
h q[2];
sdg q[2];
ccx q[0],q[4],q[2];
mcphase(-pi/4) q[0],q[2];
ccx q[0],q[8],q[2];
mcphase_custom_013(pi/4) q[0],q[2];
ccx q[0],q[4],q[2];
mcphase(-pi/4) q[0],q[2];
mcphase_custom_014(pi/4) q[0],q[4];
ccx q[0],q[8],q[2];
mcphase_custom_015(pi/4) q[0],q[2];
s q[2];
h q[2];
t q[2];
cx q[0],q[2];
ccx q[0],q[8],q[4];
mcphase(-pi/4) q[0],q[4];
mcphase_custom_016(pi/4) q[0],q[8];
ccx q[0],q[8],q[4];
tdg q[2];
h q[2];
sdg q[2];
ccx q[0],q[2],q[8];
ccx q[0],q[8],q[4];
ccx q[1],q[2],q[5];
ccx q[1],q[3],q[6];
ccx q[1],q[2],q[8];
s q[2];
h q[2];
t q[2];
cx q[1],q[2];
tdg q[2];
h q[2];
sdg q[2];
ccx q[1],q[5],q[2];
mcphase(-pi/4) q[1],q[2];
ccx q[1],q[8],q[2];
mcphase_custom_017(pi/4) q[1],q[2];
ccx q[1],q[5],q[2];
mcphase(-pi/4) q[1],q[2];
mcphase_custom_018(pi/4) q[1],q[5];
ccx q[1],q[8],q[2];
mcphase_custom_019(pi/4) q[1],q[2];
s q[2];
h q[2];
t q[2];
cx q[1],q[2];
tdg q[2];
h q[2];
sdg q[2];
ccx q[1],q[3],q[2];
s q[3];
h q[3];
t q[3];
cx q[1],q[3];
tdg q[3];
h q[3];
sdg q[3];
ccx q[1],q[6],q[3];
mcphase(-pi/4) q[1],q[3];
ccx q[1],q[2],q[3];
mcphase_custom_020(pi/4) q[1],q[3];
ccx q[1],q[6],q[3];
mcphase(-pi/4) q[1],q[3];
ccx q[1],q[2],q[3];
mcphase_custom_021(pi/4) q[1],q[3];
s q[3];
h q[3];
t q[3];
cx q[1],q[3];
tdg q[3];
h q[3];
sdg q[3];
ccx q[1],q[3],q[7];
s q[3];
h q[3];
t q[3];
cx q[1],q[3];
mcphase_custom_022(pi/4) q[1],q[6];
ccx q[1],q[2],q[6];
mcphase_custom_023(pi/4) q[1],q[2];
mcphase(-pi/4) q[1],q[6];
ccx q[1],q[2],q[6];
tdg q[3];
h q[3];
sdg q[3];
ccx q[1],q[6],q[3];
mcphase(-pi/4) q[1],q[3];
ccx q[1],q[2],q[3];
mcphase_custom_024(pi/4) q[1],q[3];
ccx q[1],q[6],q[3];
mcphase(-pi/4) q[1],q[3];
ccx q[1],q[2],q[3];
mcphase_custom_025(pi/4) q[1],q[3];
s q[3];
h q[3];
t q[3];
cx q[1],q[3];
mcphase_custom_026(pi/4) q[1],q[6];
ccx q[1],q[2],q[6];
mcphase_custom_027(pi/4) q[1],q[2];
mcphase(-pi/4) q[1],q[6];
ccx q[1],q[2],q[6];
tdg q[3];
h q[3];
sdg q[3];
ccx q[1],q[3],q[2];
ccx q[1],q[2],q[6];
s q[2];
h q[2];
t q[2];
cx q[1],q[2];
ccx q[1],q[8],q[5];
mcphase(-pi/4) q[1],q[5];
mcphase_custom_028(pi/4) q[1],q[8];
ccx q[1],q[8],q[5];
tdg q[2];
h q[2];
sdg q[2];
ccx q[1],q[5],q[2];
mcphase(-pi/4) q[1],q[2];
ccx q[1],q[8],q[2];
mcphase_custom_029(pi/4) q[1],q[2];
ccx q[1],q[5],q[2];
mcphase(-pi/4) q[1],q[2];
mcphase_custom_030(pi/4) q[1],q[5];
ccx q[1],q[8],q[2];
mcphase_custom_031(pi/4) q[1],q[2];
s q[2];
h q[2];
t q[2];
cx q[1],q[2];
ccx q[1],q[8],q[5];
mcphase(-pi/4) q[1],q[5];
mcphase_custom_032(pi/4) q[1],q[8];
ccx q[1],q[8],q[5];
tdg q[2];
h q[2];
sdg q[2];
ccx q[1],q[2],q[8];
ccx q[1],q[8],q[5];