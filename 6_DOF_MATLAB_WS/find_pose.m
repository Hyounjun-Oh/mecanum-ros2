%Homogeneous Transformation 사용한 순기구학
function [pose] = find_pose(joints, d, a, alpha)
    max_iteration = length(joints);
    A_matrix= zeros(4,max_iteration * 4) + find_A_matrix(joints,d,a,alpha);
    end_effector_A_matrix = zeros(4);
    for iteration = 1:max_iteration
        if iteration == 1
            end_effector_A_matrix(:,:) = A_matrix(:,1:4);
        else
            end_effector_A_matrix = end_effector_A_matrix * A_matrix(:,(4*iteration - 3):(4*iteration));
        end
    end
    pose = [end_effector_A_matrix(1:3,4)' 0 0 0];
end