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
gate mcphase_custom_008(param0) q0,q1 { cp(pi/4) q0,q1; }
qreg q[5];
ccx q[0],q[1],q[2];
ccx q[0],q[1],q[4];
s q[1];
h q[1];
t q[1];
cx q[0],q[1];
tdg q[1];
h q[1];
sdg q[1];
ccx q[0],q[2],q[1];
mcphase(-pi/4) q[0],q[1];
ccx q[0],q[4],q[1];
mcphase_custom_001(pi/4) q[0],q[1];
ccx q[0],q[2],q[1];
mcphase(-pi/4) q[0],q[1];
mcphase_custom_002(pi/4) q[0],q[2];
ccx q[0],q[4],q[1];
mcphase_custom_003(pi/4) q[0],q[1];
s q[1];
h q[1];
t q[1];
cx q[0],q[1];
tdg q[1];
h q[1];
sdg q[1];
ccx q[0],q[1],q[3];
s q[1];
h q[1];
t q[1];
cx q[0],q[1];
ccx q[0],q[4],q[2];
mcphase(-pi/4) q[0],q[2];
mcphase_custom_004(pi/4) q[0],q[4];
ccx q[0],q[4],q[2];
tdg q[1];
h q[1];
sdg q[1];
ccx q[0],q[2],q[1];
mcphase(-pi/4) q[0],q[1];
ccx q[0],q[4],q[1];
mcphase_custom_005(pi/4) q[0],q[1];
ccx q[0],q[2],q[1];
mcphase(-pi/4) q[0],q[1];
mcphase_custom_006(pi/4) q[0],q[2];
ccx q[0],q[4],q[1];
mcphase_custom_007(pi/4) q[0],q[1];
s q[1];
h q[1];
t q[1];
cx q[0],q[1];
ccx q[0],q[4],q[2];
mcphase(-pi/4) q[0],q[2];
mcphase_custom_008(pi/4) q[0],q[4];
ccx q[0],q[4],q[2];
tdg q[1];
h q[1];
sdg q[1];
ccx q[0],q[1],q[4];
rz(pi/16) q[1];
ccx q[0],q[4],q[2];