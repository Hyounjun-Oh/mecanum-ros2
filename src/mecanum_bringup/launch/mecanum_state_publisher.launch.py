#!/usr/bin/env python3

import os
import xacro
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch.conditions import IfCondition, UnlessCondition

def generate_launch_description():

    use_sim_time = LaunchConfiguration('use_sim_time', default='false')
    share_dir = get_package_share_directory('mobile_description')
    urdf = os.path.join(share_dir, 'urdf', 'mobile.urdf')
    #robot_description_config = xacro.process_file(xacro_file)
    #robot_urdf = robot_description_config.toxml()

    with open(urdf, 'r') as infp:
        robot_desc = infp.read()

    rsp_params = {'robot_description': robot_desc}

    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='false', # 노드간 시간 동기화
            description='Use simulation (Gazebo) clock if true'), 
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            output='screen',
            parameters=[rsp_params, {'use_sim_time': use_sim_time}])
    ])