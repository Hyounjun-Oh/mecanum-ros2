clc;
clear;
close all;

costfunction = @(x) Sphere(x); %cost function

nVar =5;

VarSize = [1 nVar];

VarMin = -10;
VarMax = 10;

%% Parameter of Pso

MaxIt = 100; % maximum iteration
nPop = 50; % swarm size
w = 1; %Inertia Coefficient
c1 = 2; %Personal Acceleration Coefficient
c2 = 2; %Social Acceleration Coefficient

%% Initialization

% The Particle Template
empty_particle.position = [];
empty_particle.velocity = [];
empty_particle.cost = [];
empty_particle.best.position = [];
empty_particle.best.cost = [];

%Create Population Array
particle = repmat(empty_particle, nPop,1); %repmat is fuction helps repeat large matrix

% Initialize Global Best
globalbest.cost = inf; %

% Initialize Population Members
for i=1:nPop
    % Generate Random Solution
    particle(i).position = unifrnd(VarMin,VarMax,VarSize);

    % Initialize Velocity
    particle(i).velocity = zeros(VarSize);

    %Evaluation
    particle(i).cost = costfunction(particle(i).position);

    %update the personal best
    particle(i).best.position = particle(i).position;
    particle(i).best.cost = particle(i).cost;
    
    % update global best
    if particle(i).best.cost < globalbest.cost
        globalbest = particle(i).best;
    end

end
%Array to hold best cost value on each iteration
bestcosts = zeros(MaxIt, 1);

%% Main loop of PSO

for it = 1:MaxIt
    for i=1:nPop
    
        
    
    end
end

%% function

function z = Sphere(x)
    
    z = sum(x.^2);

end
