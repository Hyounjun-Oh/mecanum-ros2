#!/usr/bin/env python3
#
# Copyright 2019 ROBOTIS CO., LTD.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Authors: Darby Lim

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch.substitutions import ThisLaunchFileDir
from launch_ros.actions import Node


def generate_launch_description():

    ydlidar_pkg_dir = LaunchConfiguration(
        'ydlidar_pkg_dir',
        default = os.path.join(get_package_share_directory('ydlidar_ros2_driver'),'launch')
    )
    imu_pkg_dir = LaunchConfiguration(
        'imu_pkg_dir',
        default = os.path.join(get_package_share_directory('stella_ahrs'),'launch')
    )
    motor_driver_pkg = LaunchConfiguration(
        'motor_driver_pkg_dir',
        default = os.path.join(get_package_share_directory('motor_control'),'launch')
    )
    use_sim_time = LaunchConfiguration('use_sim_time', default='false')
    
    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time',
            default_value=use_sim_time,
            description='Use simulation (Gazebo) clock if true'),

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                [ThisLaunchFileDir(), '/mecanum_state_publisher.launch.py']),
            launch_arguments={'use_sim_time': use_sim_time}.items(),
        ),

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                [ydlidar_pkg_dir, '/ydlidar_launch.py']),
        ),
        
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                [imu_pkg_dir, '/stella_ahrs_launch.py']),
        ),
        
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                [motor_driver_pkg, '/motor_control.launch.py']),
        ),
        Node(
            package='manipulator',
            executable='manipulater_move',
            name='manipulator_move',
            output='screen'),
        Node(
            package='dynamixel_sdk_examples',
            executable='read_write_node',
            name='dynamixel_sdk',
            output='screen'),
    ])
