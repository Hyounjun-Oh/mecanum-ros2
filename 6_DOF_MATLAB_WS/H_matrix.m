function array = H_matrix(theta_array)
%% DH파라미터 기입
d = [90 0 0 0 0 190 0 65 0 125];
a = [0 240 30 70 25 0 0 0 35 0];
al = [90 0 0 0 90 -90 90 0 0 0].*(pi/180);
q = [theta_array(1) theta_array(2) -pi/2 theta_array(3) pi/2 theta_array(4) theta_array(5) 0 theta_array(6) 0]; %
%% 동차변환
T01 = DHmatrix(q(1),d(1),a(1),al(1));
T12 = DHmatrix(q(2),d(2),a(2),al(2));
T23 = DHmatrix(q(3),d(3),a(3),al(3));
T34 = DHmatrix(q(4),d(4),a(4),al(4));
T45 = DHmatrix(q(5),d(5),a(5),al(5));
T56 = DHmatrix(q(6),d(6),a(6),al(6));
T67 = DHmatrix(q(7),d(7),a(7),al(7));
T78 = DHmatrix(q(8),d(8),a(8),al(8));
T89 = DHmatrix(q(9),d(9),a(9),al(9));
T910 = DHmatrix(q(10),d(10),a(10),al(10));

T02 = T01 * T12;
T03 = T02 * T23;
T04 = T03 * T34;
T05 = T04 * T45;
T06 = T05 * T56;
T07 = T06 * T67;
T08 = T07 * T78;
T09 = T08 * T89;
T010 = T09 * T910;

P1 = T01(1:3,4);
P2 = T02(1:3,4);
P3 = T03(1:3,4);
P4 = T04(1:3,4);
P5 = T05(1:3,4);
P6 = T06(1:3,4);
P7 = T07(1:3,4);
P8 = T08(1:3,4);
P9 = T09(1:3,4);
P10 = T010(1:3,4);
%% plot array

To1 = T67.*[260;-20;280-20;0];
To2 = T67.*[260;-20;280;0];
To3 = T67.*[260;20;280;0];
To4 = T67.*[260;20;280-20;0];

Px = [0 P1(1) P2(1) P3(1) P4(1) P5(1) P6(1) P7(1) P8(1) P9(1) P10(1)];
Py = [0 P1(2) P2(2) P3(2) P4(2) P5(2) P6(2) P7(2) P8(2) P9(2) P10(2)];
Pz = [0 P1(3) P2(3) P3(3) P4(3) P5(3) P6(3) P7(3) P8(3) P9(3) P10(3)];

array = [Px;Py;Pz];
end