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
% 쿼터니언으로 에러 계산시 오차 큼. 가중치 100 주어도 마찬가지
% rotation 행렬 자체로 계산?
function object_function_result = object_function(dh_parameter, desired_value, x, mode)
    alpha = 0; 
    if mode == 1
        object_function_result.best_cost = inf;
        for iter = 1:length(x.Position.J1)
            joint_value = [x.Position.J1(iter), x.Position.J2(iter), x.Position.J3(iter), x.Position.J4(iter), x.Position.J5(iter), x.Position.J6(iter), x.Position.J7(iter)];
            T_estimated = Homogeneous(dh_parameter, joint_value);
            position_error = desired_value(1:3)' - T_estimated(1:3,4);
            %orientation_error = desired_value(4:7) - rotm2quat(T_estimated(1:3,1:3));
            total_error_MSE = sum(position_error.^2) ;%+ alpha * sum(orientation_error.^2));
            if sum(position_error) < object_function_result.best_cost
                object_function_result.best_cost = total_error_MSE;
                object_function_result.best_position = joint_value;
            end
        end
     else
        joint_value = x.Position;
        T_estimated = Homogeneous(dh_parameter, joint_value);
        position_error = desired_value(1:3)' - T_estimated(1:3,4);
        %orientation_error = desired_value(4:7) - rotm2quat(T_estimated(1:3,1:3));
        total_error_MSE = sum(position_error.^2); %+ alpha*sum(orientation_error.^2));
        object_function_result.best_cost = total_error_MSE;
     end
end
