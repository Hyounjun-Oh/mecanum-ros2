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
global a

node = ros2node("joint_calculator");
pub = ros2publisher(node,"joint_variables","std_msgs/Float32MultiArray");
sub = ros2subscriber(node,"/desired_pose", @callback_desired_pose);
%% DH parameter

params.dh_parameter.d = [330 0 0 190 0 10];
params.dh_parameter.a = [0 70 25 0 65 0];
params.dh_parameter.al = [90 0 90 -90 90 0].*(pi/180);
%% Problem Definiton

problem.nVar = 6;       % Number of Unknown (Decision) Variables
% 조인트 리밋 
problem.VarMin = [-175 -100 -90 -175 -100 -175].*(pi/180);  % Lower Bound of Decision Variables
problem.VarMax = [175 100 90 175 100 175].*(pi/180);   % Upper Bound of Decision Variables

%% Parameters of PSO
 
params.MaxIt = 1000;        % Maximum Number of Iterations
params.nPop = 500;           % Population Size (Swarm Size)
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
    global a
    joint_conv = [0 0 0 0 0 0 0];
    desired_pose = [msg.data(1), msg.data(2), msg.data(3)];
    if sum(desired_pose) ~= sum(desired_pose_old)
        disp('published')
        msg = ros2message("std_msgs/Float32MultiArray");
        params.desired_position = [desired_pose(1),desired_pose(2),desired_pose(3)]; %0 -187 1324
        out = PSO_MANIPULATOR(problem, params);
        BestSol = out.BestSol;
        BestCosts = out.BestCosts;
        if BestSol.Cost < 0.0001
            joint = [BestSol.Position(1),BestSol.Position(2),BestSol.Position(3),BestSol.Position(4),BestSol.Position(5),BestSol.Position(6)];
            for i = 1:length(joint)
                joint_conv(1) = 0;
                if joint(i) < 0
                    proportion = (pi + joint(i))/(2*pi);
                    joint_conv(i+1) = proportion*4096;
                elseif joint(i) > 0
                    proportion = (pi + joint(i))/(2*pi);
                    joint_conv(i+1) = proportion*4096;
                else
                    joint_conv(i+1) = 2048;
                end
            end
            for i = 1:length(joint_conv)
                msg.data(i) = single(joint_conv(i));
            end
            disp(joint)
            % msg.data = single(joint);
            send(pub,msg);
            disp("Publish Joint Variables")
            a = joint;
            params.desired_position = [0,0,0];
        end
    end
    desired_pose_old = desired_pose;
end

