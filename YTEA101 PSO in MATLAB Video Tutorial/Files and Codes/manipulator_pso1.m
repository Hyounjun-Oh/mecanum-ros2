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

%% DH parameter

params.dh_parameter.d = [300 194 449.5 -190 360 183 228];
params.dh_parameter.a = [0 0 0 0 0 0 0];
params.dh_parameter.al = [pi/2 -pi/2 pi/2 -pi/2 pi/2 -pi/2 pi/2];

params.desired_value = [0 -187 800 eul2quat([0 0 0])];
%% Problem Definiton

problem.nVar = 10;       % Number of Unknown (Decision) Variables
% 조인트 리밋 
problem.VarMin = [-3.0543 -3.0543 -3.0543 -3.0543 -3.0543 -3.0543 -3.0543];  % Lower Bound of Decision Variables
problem.VarMax = [3.0543 3.0543 3.0543 3.0543 3.0543 3.0543 3.0543];   % Upper Bound of Decision Variables

%% Parameters of PSO
 
params.MaxIt = 10000;        % Maximum Number of Iterations
params.nPop = 50;           % Population Size (Swarm Size)
params.w = 1;               % Intertia Coefficient
params.wdamp = 0.99;        % Damping Ratio of Inertia Coefficient
params.c1 = 2;              % Personal Acceleration Coefficient
params.c2 = 2;              % Social Acceleration Coefficient
params.ShowIterInfo = true; % Flag for Showing Iteration Informatin

%% Calling PSO

out = PSO_MANIPULATOR(problem, params);

BestSol = out.BestSol;
BestCosts = out.BestCosts;

%% Results

% figure;
% % plot(BestCosts, 'LineWidth', 2);
% semilogy(BestCosts, 'LineWidth', 2);
% xlabel('Iteration');
% ylabel('Best Cost');
% grid on;


