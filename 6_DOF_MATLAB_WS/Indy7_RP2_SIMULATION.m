%INDY7-RP2 모션 컨트롤 시뮬레이션
%오현준
%% MEMO
% 실제 INDY의 DH파라미터 사용 전 임의 모델로 테스트 진행
%%
%close all
clf
clear
clc
format long
%% INDY7-RP2 CONFIGURATION
% DH PARAMETER
theta = [0 0 0 0 0 0 0].*(pi/180);
d = [300 194 449.5 -190 350 183 228];
a_dh = [0 0 0 0 0 0 0];
alpha = [90.00021 -90.0002 90.00021 -90.0002 90.00021 -90.0002 90.00021].*(pi/180);
%% DATA INITIALIZATION
% Value of each Actuator
vi = [0 0 0 0 0 0];
vf = [0 0 0 0 0 0];
ai = [0 0 0 0 0 0];
af = [0 0 0 0 0 0];
% Sampling Time
ti = 0; tf = 2; t = linspace(ti,tf,100*(tf-ti));
% Desired Pose6
desired_pose_1 = [800 800 800 0 0 0];
%% FIND INITIAL POSE

initial_joints = [-90.0002 0 0 0 0 0 90.00021].*(pi/180);
initial_pose = H_matrix(initial_joints);
%% FIND TRAJECTORIES

% Quintic Polynomial
M = [1 ti ti^2 ti^3 ti^4 ti^5;
     0 1 2*ti 3*(ti^2) 4*(ti^3) 5*(ti^4);
     0 0 2 6*ti 12*(ti^2) 20*(ti^3);
     1 tf tf^2 tf^3 tf^4 tf^5;
     0 1 2*tf 3*(tf^2) 4*(tf^3) 5*(tf^4);
     0 0 2 6*tf 12*(tf^2) 20*(tf^3)];
b = [initial_pose(1:3,8)', 0, 0, 0;vi;ai;desired_pose_1;vf;af];
a = M\b;
c = ones(size(t));

% Desired trajectory
pxd = a(1).*c + a(2).*t +a(3).*t.^2 + a(4).*t.^3 +a(5).*t.^4 + a(6).*t.^5;
vxd = a(2).*c +2*a(3).*t +3*a(4).*t.^2 +4*a(5).*t.^3 +5*a(6).*t.^4;
axd = 2*a(3).*c + 6*a(4).*t +12*a(5).*t.^2 +20*a(6).*t.^3;

pyd = a(1,2).*c + a(2,2).*t +a(3,2).*t.^2 + a(4,2).*t.^3 +a(5,2).*t.^4 + a(6,2).*t.^5;
vyd = a(2,2).*c +2*a(3,2).*t +3*a(4,2).*t.^2 +4*a(5,2).*t.^3 +5*a(6,2).*t.^4;
ayd = 2*a(3,2).*c + 6*a(4,2).*t +12*a(5,2).*t.^2 +20*a(6,2).*t.^3;

pzd = a(1,3).*c + a(2,3).*t +a(3,3).*t.^2 + a(4,3).*t.^3 +a(5,3).*t.^4 + a(6,3).*t.^5;
vzd = a(2,3).*c +2*a(3,3).*t +3*a(4,3).*t.^2 +4*a(5,3).*t.^3 +5*a(6,3).*t.^4;
azd = 2*a(3,3).*c + 6*a(4,3).*t +12*a(5,3).*t.^2 +20*a(6,3).*t.^3;
%% INVERSE KINEMATICS

for k = 1:length(t)-1
    if k == 1
        q_dot_f = pinv(jacobian7(initial_joints)) * ([vxd(k) vyd(k) vzd(k) 0 0 0])';
        qf = initial_joints' + q_dot_f.*(t(k+1)-t(k));
        Plot_Points = H_matrix(qf);
        plot3(Plot_Points(1,:),Plot_Points(2,:),Plot_Points(3,:),'-or','LineWidth',3);
        axis([-1000,1000,-1000,1000,-500,2000]);
        grid on
    else
        Plot_Points = H_matrix(qf);
        vf = [vxd(k);vyd(k);vzd(k);0;0;0];
        p_dot_ref = vf + (0.*([pxd(k);pyd(k);pzd(k);0;0;0] - [Plot_Points(1:3,8);0;0;0]))./(t(k+1)-t(k));
        q_dot_f = pinv(jacobian7(qf)) * p_dot_ref;
        qf = qf + q_dot_f*(t(k+1)-t(k));
        plot3(Plot_Points(1,:),Plot_Points(2,:),Plot_Points(3,:),'-or','LineWidth',3);
        axis([-1000,1000,-1000,1000,-500,2000]);
        grid on
        pause(0.001)
    end
end










