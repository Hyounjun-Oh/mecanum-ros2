#!/usr/bin/env python3
import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    param_dir = LaunchConfiguration(
        'param_dir',
        default=os.path.join(
            get_package_share_directory('motor_control'),
            'param',
            'motor_config.yaml'))
    
    return LaunchDescription([
        DeclareLaunchArgument(
            'param_dir',
            default_value=param_dir,
            description='front path of parameter file'),

        Node(
            package='motor_control',
            executable='motor_control_float',
            name='front_motor_control',
            parameters=[param_dir],
            output='screen'),

        Node(
            package='motor_control',
            executable='motor_control_float',
            name='rear_motor_control',
            parameters=[param_dir],
            output='screen'),
    ])