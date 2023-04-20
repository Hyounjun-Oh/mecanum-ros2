#!/usr/bin/env python
#
# Copyright (c) 2011, Willow Garage, Inc.
# All rights reserved.
#
# Software License Agreement (BSD License 2.0)
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above
#    copyright notice, this list of conditions and the following
#    disclaimer in the documentation and/or other materials provided
#    with the distribution.
#  * Neither the name of {copyright_holder} nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
# Author: Darby Lim

import os
import select
import sys
import rclpy
import time

from geometry_msgs.msg import Twist
from rclpy.qos import QoSProfile

if os.name == 'nt':
    import msvcrt
else:
    import termios
    import tty

MAX_LIN = 0.30
#MAX_DIA = 0.6
MAX_ROT = 2.0
LIN_VEL_STEP_SIZE = 0.01
ANG_VEL_STEP_SIZE = 0.2

msg = """
혼자서도 잘해요
[Mecanum wheel Mobile Manipulator]
---------------------------
키배치:
    Q   W   E
    A   S   D
        X

w/x : 증가/감소 Vx [최고속도 : 0.3 m/s]
a/d : 증가/감소 Vy [최고속도 : 0.3 m/s]
q/e : 증가/감소 Rz [최고속도 : 2.0rad/s]
s   : 강제 정지
CTRL-C : 컨트롤러 종료
"""

r = """
Communications Failed
"""


def get_key(settings):
    if os.name == 'nt':
        return msvcrt.getch().decode('utf-8')
    tty.setraw(sys.stdin.fileno())
    rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
    if rlist:
        key = sys.stdin.read(1)
    else:
        key = ''

    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key


def print_vels(target_linear_X_velocity, target_linear_Y_velocity, target_angular_velocity):
    print('currently:\tlinear X velocity {0} \tlinear Y velocity {1}\t angular velocity {2} '.format(
        target_linear_X_velocity,target_linear_Y_velocity,
        target_angular_velocity))


def make_simple_profile(output, input, slop):
    if input > output:
        output = min(input, output + slop)
    elif input < output:
        output = max(input, output - slop)
    else:
        output = input

    return output


def constrain(input_vel, low_bound, high_bound):
    if input_vel < low_bound:
        input_vel = low_bound
    elif input_vel > high_bound:
        input_vel = high_bound
    else:
        input_vel = input_vel

    return input_vel


def check_linear_limit_velocity(velocity):
    return constrain(velocity, -MAX_LIN, MAX_LIN)


def check_angular_limit_velocity(velocity):
    return constrain(velocity, -MAX_ROT, MAX_ROT)


def main():
    settings = None
    if os.name != 'nt':
        settings = termios.tcgetattr(sys.stdin)

    rclpy.init()
    qos = QoSProfile(depth=10)
    node = rclpy.create_node('teleop_keyboard')
    pub = node.create_publisher(Twist, 'cmd_vel', qos)

    status = 0
    target_linear_X_velocity = 0.0
    target_linear_Y_velocity = 0.0    
    target_angular_velocity = 0.0
    control_linear_X_velocity = 0.0
    control_linear_Y_velocity = 0.0
    control_angular_velocity = 0.0
    
    try:
        print(msg)
        while(1):
            key = get_key(settings)
            if key == 'w':
                target_linear_X_velocity =\
                    check_linear_limit_velocity(target_linear_X_velocity + LIN_VEL_STEP_SIZE)
                
                print_vels(target_linear_X_velocity, target_linear_Y_velocity, target_angular_velocity)
            elif key == 'x':
                target_linear_X_velocity =\
                    check_linear_limit_velocity(target_linear_X_velocity - LIN_VEL_STEP_SIZE)
                
                print_vels(target_linear_X_velocity, target_linear_Y_velocity, target_angular_velocity)
            elif key == 'a':
                target_linear_Y_velocity =\
                    check_linear_limit_velocity(target_linear_Y_velocity + LIN_VEL_STEP_SIZE)
                
                print_vels(target_linear_X_velocity, target_linear_Y_velocity, target_angular_velocity)
            elif key == 'd':
                target_linear_Y_velocity =\
                    check_linear_limit_velocity(target_linear_Y_velocity - LIN_VEL_STEP_SIZE)
                
                print_vels(target_linear_X_velocity, target_linear_Y_velocity, target_angular_velocity)                              
            elif key == 'q':
                target_angular_velocity =\
                    check_angular_limit_velocity(target_angular_velocity + ANG_VEL_STEP_SIZE)
               
                print_vels(target_linear_X_velocity, target_linear_Y_velocity, target_angular_velocity)
            elif key == 'e':
                target_angular_velocity =\
                    check_angular_limit_velocity(target_angular_velocity - ANG_VEL_STEP_SIZE)
                
                print_vels(target_linear_X_velocity, target_linear_Y_velocity, target_angular_velocity)
            elif key == ' ' or key == 's':
                target_linear_X_velocity = 0.0
                target_linear_Y_velocity = 0.0    
                target_angular_velocity = 0.0
                control_linear_X_velocity = 0.0
                control_linear_Y_velocity = 0.0
                control_angular_velocity = 0.0
                print_vels(target_linear_X_velocity, target_linear_Y_velocity, target_angular_velocity)
            else:
                if (key == '\x03'):
                    break

            if status == 20:
                print(msg)
                status = 0

            twist = Twist()

            control_linear_X_velocity = make_simple_profile(
                control_linear_X_velocity,
                target_linear_X_velocity,
                (LIN_VEL_STEP_SIZE / 2.0))

            control_linear_Y_velocity = make_simple_profile(
                control_linear_Y_velocity,
                target_linear_Y_velocity,
                (LIN_VEL_STEP_SIZE / 2.0))

            twist.linear.x = control_linear_X_velocity
            twist.linear.y = control_linear_Y_velocity
            twist.linear.z = 0.0

            control_angular_velocity = make_simple_profile(
                control_angular_velocity,
                target_angular_velocity,
                (ANG_VEL_STEP_SIZE / 2.0))

            twist.angular.x = 0.0
            twist.angular.y = 0.0
            twist.angular.z = control_angular_velocity

            pub.publish(twist)

    except Exception as e:
        print(e)

    finally:
        twist = Twist()
        twist.linear.x = 0.0
        twist.linear.y = 0.0
        twist.linear.z = 0.0

        twist.angular.x = 0.0
        twist.angular.y = 0.0
        twist.angular.z = 0.0

        pub.publish(twist)

        if os.name != 'nt':
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)


if __name__ == '__main__':
    main()
