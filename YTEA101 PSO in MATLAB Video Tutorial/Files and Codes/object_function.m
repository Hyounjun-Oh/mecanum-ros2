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

function object_function_result = object_function(dh_parameter, initial_joints, x, iter)
    joint_position = [x(iter).joint_1, x(iter).joint_2, x(iter).joint_3, x(iter).joint_4, x(iter).joint_5, x(iter).joint_6, x(iter).joint_7];
    object_function_result = abs(T_position(dh_parameter, initial_joints) - T_position(dh_parameter, joint_position));

end
