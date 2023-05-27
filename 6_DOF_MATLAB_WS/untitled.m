% DH 파라미터 설정
a = [0 70 25 0 255 0];
d = [330 0 0 0 0 10];
alpha = [90 0 90 -90 90 0] * pi/180;

% 초기 위치와 방향 설정
initial_joints = [0 0 90 0 -90 0] * pi/180;

% 목표 위치와 방향 설정
desired_pose = [300 0 100 0 0 0];

% 각 관절의 제한값 설정
joint_min = [-pi/2 -pi/2 -pi/2 -pi/2 -pi/2 -pi/2];
joint_max = [pi/2 pi/2 pi/2 pi/2 pi/2 pi/2];

% 시간 설정
ti = 0;
tf = 1;
t = linspace(ti, tf, 100*(tf-ti));

% 초기 관절 상태 계산
initial_pose = forward_kinematics(initial_joints, a, d, alpha);

% 목표 관절 상태 계산
desired_joints = inverse_kinematics(desired_pose, a, d, alpha, joint_min, joint_max, initial_joints);

% 트라젝토리 생성
[q, qd, qdd] = quintic_trajectory(initial_joints, desired_joints, ti, tf, t);

% 최종 위치와 각도 출력
final_pose = forward_kinematics(q(end,:), a, d, alpha);
final_joints = q(end,:);
disp('Final Position:');
disp(final_pose);
disp('Final Joints:');
disp(final_joints);


% 함수: 전역 위치 계산
function pose = forward_kinematics(joints, a, d, alpha)
    pose = eye(4);
    for i = 1:length(joints)
        A = [cos(joints(i)) -sin(joints(i))*cos(alpha(i)) sin(joints(i))*sin(alpha(i)) a(i)*cos(joints(i));
             sin(joints(i)) cos(joints(i))*cos(alpha(i)) -cos(joints(i))*sin(alpha(i)) a(i)*sin(joints(i));
             0 sin(alpha(i)) cos(alpha(i)) d(i);
             0 0 0 1];
        pose = pose * A;
    end
end

% 함수: 역기구학 계산
function joints = inverse_kinematics(pose, a, d, alpha, joint_min, joint_max, initial_joints)
    options = optimoptions('fmincon', 'Display', 'off');
    joints = fmincon(@(x) error_function(x, pose, a, d, alpha), initial_joints, [], [], [], [], joint_min, joint_max, [], options);
end

% 함수: 에러 함수 계산
function err = error_function(joints, pose, a, d, alpha)
    end_pose = forward_kinematics(joints, a, d, alpha);
    err = norm(end_pose - pose);
end

% 함수: Quintic 트라젝토리 생성
function [q, qd, qdd] = quintic_trajectory(q0, qf, ti, tf, t)
    a0 = q0;
    a1 = zeros(size(q0));
    a2 = zeros(size(q0));
    a3 = 10*(qf - q0)/(tf^3);
    a4 = -15*(qf - q0)/(tf^4);
    a5 = 6*(qf - q0)/(tf^5);
    
    q = a0 + a1.*(t-ti) + a2.*(t-ti).^2 + a3.*(t-ti).^3 + a4.*(t-ti).^4 + a5.*(t-ti).^5;
    qd = a1 + 2*a2.*(t-ti) + 3*a3.*(t-ti).^2 + 4*a4.*(t-ti).^3 + 5*a5.*(t-ti).^4;
    qdd = 2*a2 + 6*a3.*(t-ti) + 12*a4.*(t-ti).^2 + 20*a5.*(t-ti).^3;
end
