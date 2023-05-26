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

function out = PSO_MANIPULATOR(problem, params)
    %% Problem Definiton

    nVar = problem.nVar;        % Number of Unknown (Decision) Variables

    VarSize = [1 nVar];         % Matrix Size of Decision Variables

    VarMin = problem.VarMin;	% Lower Bound of Decision Variables
    VarMax = problem.VarMax;    % Upper Bound of Decision Variables


    %% Parameters of PSO
    MaxIt = params.MaxIt;   % Maximum Number of Iterations
    
    nPop = params.nPop;     % Population Size (Swarm Size)
    
    w = params.w;           % Intertia Coefficient
    wdamp = params.wdamp;   % Damping Ratio of Inertia Coefficient
    c1 = params.c1;         % Personal Acceleration Coefficient
    c2 = params.c2;         % Social Acceleration Coefficient
    % The Flag for Showing Iteration Information
    ShowIterInfo = params.ShowIterInfo;    

    MaxVelocity = 0.2*(VarMax-VarMin);
    MinVelocity = -MaxVelocity;
    desired_position = params.desired_position;
    %% Initialization

    % The Particle Template
    empty_particle.Position.J1 = [];
    empty_particle.Velocity = [];
    empty_particle.Cost = [];
    empty_particle.Best.Position = [];
    empty_particle.Best.Cost = [];

    empty_particle.Position.J2 = [];
    % empty_particle.Velocity.J2 = [];
    % empty_particle.Cost.J2 = [];
    % empty_particle.Best.Position.J2 = [];
    % empty_particle.Best.Cost.J2 = [];

    empty_particle.Position.J3 = [];
    % empty_particle.Velocity.J3 = [];
    % empty_particle.Cost.J3 = [];
    % empty_particle.Best.Position.J3 = [];
    % empty_particle.Best.Cost.J3 = [];

    empty_particle.Position.J4 = [];
    % empty_particle.Velocity.J4 = [];
    % empty_particle.Cost.J4 = [];
    % empty_particle.Best.Position.J4 = [];
    % empty_particle.Best.Cost.J4 = [];

    empty_particle.Position.J5 = [];
    % empty_particle.Velocity.J5 = [];
    % empty_particle.Cost.J5 = [];
    % empty_particle.Best.Position.J5 = [];
    % empty_particle.Best.Cost.J5 = [];

    empty_particle.Position.J6 = [];
    % empty_particle.Velocity.J6 = [];
    % empty_particle.Cost.J6 = [];
    % empty_particle.Best.Position.J6 = [];
    % empty_particle.Best.Cost.J6 = [];

    % empty_particle.Position.J7 = [];
    % % empty_particle.Velocity.J7 = [];
    % % empty_particle.Cost.J7 = [];
    % % empty_particle.Best.Position.J7 = [];
    % % empty_particle.Best.Cost.J7 = [];

    % Create Population Array
    particle = repmat(empty_particle, nPop, 1);

    % Initialize Global Best
    GlobalBest.Cost= inf;

    % Initialize Population Members
    for i=1:nPop

        % Generate Random Solution
        particle(i).Position.J1 = unifrnd(VarMin(1), VarMax(1), VarSize);
        particle(i).Position.J2 = unifrnd(VarMin(2), VarMax(2), VarSize);
        particle(i).Position.J3 = unifrnd(VarMin(3), VarMax(3), VarSize);
        particle(i).Position.J4 = unifrnd(VarMin(4), VarMax(4), VarSize);
        particle(i).Position.J5 = unifrnd(VarMin(5), VarMax(5), VarSize);
        particle(i).Position.J6 = unifrnd(VarMin(6), VarMax(6), VarSize);
        % particle(i).Position.J7 = unifrnd(VarMin(7), VarMax(7), VarSize);

        % Initialize Velocity
        particle(i).Velocity = zeros(1,6);
        % particle(i).Velocity.J2 = zeros(VarSize);
        % particle(i).Velocity.J3 = zeros(VarSize);
        % particle(i).Velocity.J4 = zeros(VarSize);
        % particle(i).Velocity.J5 = zeros(VarSize);
        % particle(i).Velocity.J6 = zeros(VarSize);
        % particle(i).Velocity.J7 = zeros(VarSize);

        % Evaluation
        object_function_result = object_function(params.dh_parameter, desired_position, particle(i),1);
        particle(i).Cost = object_function_result.best_cost;
        particle(i).Best.Cost = object_function_result.best_cost;
        particle(i).Position = object_function_result.best_position;
        particle(i).Best.Position = object_function_result.best_position;

        % Update the Personal Best
        % particle(i).Best.Position = particle(i).Position;
        % particle(i).Best.Cost = particle(i).Cost;

        % Update Global Best
        if particle(i).Best.Cost < GlobalBest.Cost
            GlobalBest = particle(i).Best;
        end

    end

    % Array to Hold Best Cost Value on Each Iteration
    BestCosts = zeros(MaxIt, 1);


    %% Main Loop of PSO

    for it=1:MaxIt

        for i=1:nPop

            % Update Velocity
            particle(i).Velocity = w*particle(i).Velocity ...
                + c1*rand(size(particle(i).Position)).*(particle(i).Best.Position - particle(i).Position) ...
                + c2*rand(size(particle(i).Position)).*(GlobalBest.Position - particle(i).Position);
            

            % Apply Velocity Limits
            particle(i).Velocity = max(particle(i).Velocity, MinVelocity);
            particle(i).Velocity = min(particle(i).Velocity, MaxVelocity);
            
            % Update Position
            particle(i).Position = particle(i).Position + particle(i).Velocity;
            
            % Apply Lower and Upper Bound Limits
            particle(i).Position = max(particle(i).Position, VarMin);
            particle(i).Position = min(particle(i).Position, VarMax);

            % Evaluation
            object_function_result = object_function(params.dh_parameter, desired_position, particle(i),2);

            particle(i).Cost = object_function_result.best_cost;

            % Update Personal Best
            if particle(i).Cost < particle(i).Best.Cost

                particle(i).Best.Position = particle(i).Position;
                particle(i).Best.Cost = particle(i).Cost;

                % Update Global Best
                if particle(i).Best.Cost < GlobalBest.Cost
                    GlobalBest = particle(i).Best;
                end            

            end

        end

        % Store the Best Cost Value
        BestCosts(it) = GlobalBest.Cost;

        % Display Iteration Information
        if ShowIterInfo
            disp(['Iteration ' num2str(it) ': Best Cost = ' num2str(BestCosts(it))]);
        end

        % Damping Inertia Coefficient
        w = w * wdamp;

    end
    
    out.pop = particle;
    out.BestSol = GlobalBest;
    out.BestCosts = BestCosts;
    
end