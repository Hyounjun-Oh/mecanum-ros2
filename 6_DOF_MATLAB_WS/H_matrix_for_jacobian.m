function array = H_matrix_for_jacobian(theta_array)
%% DH파라미터 기입
d = [90 0 0 0 0 190 0 65 0 125];
a = [0 240 30 70 25 0 0 0 35 0];
al = [90 0 0 0 90 -90 90 0 0 0].*(pi/180);
q = [theta_array(1) theta_array(2) -pi/2 theta_array(3) pi/2 theta_array(4) theta_array(5) 0 theta_array(6) 0]; %
%% 동차변환
% T01 = DHmatrix(q(1),d(1),a(1),al(1));
% T12 = DHmatrix(q(2),d(2),a(2),al(2));
% T23 = DHmatrix(q(3),d(3),a(3),al(3));
% T34 = DHmatrix(q(4),d(4),a(4),al(4));
% T45 = DHmatrix(q(5),d(5),a(5),al(5));
% T56 = DHmatrix(q(6),d(6),a(6),al(6));
% T67 = DHmatrix(q(7),d(7),a(7),al(7));
% T78 = DHmatrix(q(8),d(8),a(8),al(8));

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

array = [T01, T12, T34, T56, T67, T89];
end