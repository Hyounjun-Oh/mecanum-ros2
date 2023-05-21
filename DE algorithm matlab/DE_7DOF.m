% DE 알고리즘을 이용한 매니퓰레이터 해 구하기
% 1. 랜덤 조인트 값들 초기화
% 2. 랜덤 조인트 값들 목적함수로 평가
% Iteration시작
% 3. 초기화한 랜덤조인트
clc
clear
close all
%% Input Parameter

params.desired_pose = [0 -187 1300 0 0 0 0]; % [X, Y, Z, w, x, y, z] 쿼터니언
params.initial_joints = [0 0 0 0 0 0 0];
params.dh_parameter.d = [300 194 449.5 -190 360 183 228];
params.dh_parameter.a = [0 0 0 0 0 0 0];
params.dh_parameter.al = [pi/2 -pi/2 pi/2 -pi/2 pi/2 -pi/2 pi/2];

%% Parameter 

params.F = 0.6;
params.CR = 1.0;
params.alpha = 1;
params.beta = 0.1;
params.population = 50;
params.iteration = 350;
params.tolerance = 0.001;
params.gamma = 1000;

params.joint_limit.max = [175 175 175 175 175 175 175].*pi/180;
params.joint_limit.min = -1*[175 175 175 175 175 175 175].*pi/180;

%% Initialization
best.cost = inf;
for i = 1:params.population
    for j = 1:length(params.joint_limit.max)
        % 1 ~ 7번 Joint까지 랜덤 변수 초기화
        position(i).joints(j) = params.joint_limit.min(j) + (params.joint_limit.max(j) - params.joint_limit.min(j)).*rand();
    end
    position(i).cost = object_function(params,position(i));
    if position(i).cost < best.cost
        best.cost = position(i).cost;
        best.joints = position(i).joints;
    end
end












