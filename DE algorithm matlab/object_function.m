function object_function_result = object_function(params, position)
    % T error
    boundary_score = 0;
    joint_value = position.joints;
    T_estimated = Homogeneous(params.dh_parameter, joint_value);
    position_error = params.desired_pose(1:3)' - T_estimated(1:3,4);
    orientation_error = params.desired_pose(4:7) - rotm2quat(T_estimated(1:3,1:3));
    T_error = params.alpha * sum(sum(position_error.^2)+ sum(orientation_error.^2));

    % q error
    q_error = sum((params.initial_joints - joint_value).^2);

    % joint_boundary 패널티 함수 
    for i = 1:length(joint_value)
        if or(joint_value(i) > params.joint_limit.max, joint_value(i) < params.joint_limit.min) 
            boundary_score = boundary_score + 1;
        else
            boundary_score = boundary_score + 0;
        end
    end

    total_error_MSE = (params.alpha .* T_error) + (params.beta .* q_error) + params.gamma .*boundary_score;
    object_function_result = total_error_MSE;

end
