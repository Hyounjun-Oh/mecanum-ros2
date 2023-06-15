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
%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%% FOR 7 DOF MODEL %%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%

function object_function_result = object_function(dh_parameter, desired_position, x, mode)
     if mode == 1
        object_function_result.best_cost = inf;
        for iter = 1:length(x.Position.J1)
            joint_position = [x.Position.J1(iter), x.Position.J2(iter), -pi/2, x.Position.J3(iter), pi/2, x.Position.J4(iter), x.Position.J5(iter), 0, x.Position.J6(iter), 0];
            joint_error = (desired_position' - T_position(dh_parameter, joint_position)).^2;
            if sum(joint_error) < object_function_result.best_cost
                object_function_result.best_cost = sum(joint_error);
                object_function_result.best_position = [x.Position.J1(iter), x.Position.J2(iter), x.Position.J3(iter), x.Position.J4(iter), x.Position.J5(iter), x.Position.J6(iter)];
            end
        end
     else
        joint_position = [x.Position(1), x.Position(2), -pi/2, x.Position(3), pi/2, x.Position(4), x.Position(5), 0, x.Position(6), 0];
        joint_error = (desired_position' - T_position(dh_parameter, joint_position)).^2;
        object_function_result.best_cost = sum(joint_error);
     end
end
