% Foward_Kinematics Using Homogeneous Transformation
% Jeonbuk National University
% Hyounjun Oh

function tool_position = T_position(dh_parameter, theta_array)
    dh_parameter.theta = theta_array;
    for iter = 1:length(theta_array)
        T(iter).transform_matrix = DHmatrix(dh_parameter.theta(iter),dh_parameter.d(iter),dh_parameter.a(iter),dh_parameter.al(iter));
        if iter == 1
            T(iter).multiple_transform = T(iter).transform_matrix;
        else
            T(iter).multiple_transform = T(iter-1).multiple_transform * T(iter).transform_matrix;
        end
    end
    tool_position = T(iter).multiple_transform(1:3,4);
end