%
% Copyright (c) 2016, Yarpiz (www.yarpiz.com)
% All rights reserved. Please read the "license.txt" for license terms.
%
% Project Code: YTEA101
% Project Title: Particle Swarm Optimization Video Tutorial
% Publisher: Yarpiz (www.yarpiz.com)
% 
% Developer and Instructor: S. Mostapha Kalami Heris (Member of Yarpiz Team)
% 
% Contact Info: sm.kalami@gmail.com, info@yarpiz.com
%

clc;
clear;  
close all;

global desired_pose
global desired_pose_old
global params
global BesrSol
global BestCosts
global problem
global pub

node = ros2node("joint_calculator");
pub = ros2publisher(node,"joint_variables","std_msgs/Float32MultiArray");
sub = ros2subscriber(node,"/desired_pose", @callback_desired_pose);
%% DH parameter

params.dh_parameter.d = [300 194 449.5 -190 360 183 228];
params.dh_parameter.a = [0 0 0 0 0 0 0];
params.dh_parameter.al = [pi/2 -pi/2 pi/2 -pi/2 pi/2 -pi/2 pi/2];
%% Problem Definiton

problem.nVar = 6;       % Number of Unknown (Decision) Variables
% 조인트 리밋 
problem.VarMin = [-1.570796326794897 -1.570796326794897 -1.570796326794897 -1.570796326794897 -1.570796326794897 -1.570796326794897 -1.570796326794897];  % Lower Bound of Decision Variables
problem.VarMax = [1.570796326794897 1.570796326794897 1.570796326794897 1.570796326794897 1.570796326794897 1.570796326794897 1.570796326794897];   % Upper Bound of Decision Variables

%% Parameters of PSO
 
params.MaxIt = 1000;        % Maximum Number of Iterations
params.nPop = 100;           % Population Size (Swarm Size)
params.w = 1;               % Intertia Coefficient
params.wdamp = 0.99;        % Damping Ratio of Inertia Coefficient
params.c1 = 2;              % Personal Acceleration Coefficient
params.c2 = 2;              % Social Acceleration Coefficient
params.ShowIterInfo = true; % Flag for Showing Iteration Informatin

%% Calling PSO
desired_pose_old = [0.0 0.0 0.0];
desired_pose = [0.0 0.0 0.0];
% %% Results
% 
% figure;
% % plot(BestCosts, 'LineWidth', 2);
% semilogy(BestCosts, 'LineWidth', 2);
% xlabel('Iteration');
% ylabel('Best Cost');
% grid on;
% clear manipulator_node

function callback_desired_pose(msg)
    global desired_pose
    global desired_pose_old
    global params
    global BesrSol
    global BestCosts
    global problem
    global pub
    desired_pose = [msg.data(1), msg.data(2), msg.data(3)];
    disp(desired_pose)
    if sum(desired_pose) ~= sum(desired_pose_old)
        disp('published')
        msg = ros2message("std_msgs/Float32MultiArray");
        params.desired_position = [desired_pose(1),desired_pose(2),desired_pose(3)]; %0 -187 1324
        out = PSO_MANIPULATOR(problem, params);
        BestSol = out.BestSol;
        BestCosts = out.BestCosts;
        if BestSol.Cost < 0.0001
            msg.data = single([BestSol.Position(1),BestSol.Position(2),BestSol.Position(3),BestSol.Position(4),BestSol.Position(5),BestSol.Position(6),BestSol.Position(7)]);
            send(pub,msg);
            disp("Publish Joint Variables")
            params.desired_position = [0,0,0];
        end
    end
    desired_pose_old = desired_pose;
end

