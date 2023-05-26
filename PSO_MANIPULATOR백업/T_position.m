% Foward_Kinematics Using Homogeneous Transformation
% Jeonbuk National University
% Hyounjun Oh

function tool_position = T_position(x, theta_array)
    theta = theta_array;
    for iter = 1:length(theta)
        T(iter).transform_matrix = DHmatrix(theta(iter),x.d(iter),x.a(iter),x.al(iter));
        if iter == 1
            T(iter).multiple_transform = T(iter).transform_matrix;
        else
            T(iter).multiple_transform = T(iter-1).multiple_transform * T(iter).transform_matrix;
        end
    end
    tool_position = T(iter).multiple_transform(1:3,4);
end