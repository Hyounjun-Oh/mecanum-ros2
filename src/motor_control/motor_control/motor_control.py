# Copyright 2016 Open Source Robotics Foundation, Inc.
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

#Arduino Mega - Master Port : /dev/ttyACM0
import rclpy
from rclpy.node import Node
import numpy as np
import serial
from geometry_msgs.msg import Twist


class CmdVelSubscriber(Node):

    def __init__(self):
        super().__init__('motor_control')
        self.subscription = self.create_subscription(
            Twist,
            'cmd_vel',
            self.get_cmd_vel,
            10)
        self.subscription  # prevent unused variable warning
        self.width = 0.17 # 중심점으로부터 모터의 가로 위치
        self.length = 0.15 # 중심점으로부터 모터의 세로 위치
        self.radius = 0.05 # 메카넘휠 반지름
        # self.ser = serial.Serial('/dev/ttyACM0', 37600) #OpenCR Port COM3, MEGE Port COM4

    def get_cmd_vel(self, msg):
        self.Vx = msg.linear.x #m/s
        self.Vy = msg.linear.y #m/s
        self.Rz = msg.angular.z #rad/s
        self.cmd_vel2rad()
        # if self.ser.readable():
        trans_data = str(float(self.rpm_value[0][0])) + "," + str(float(self.rpm_value[1][0])) + "," + str(float(self.rpm_value[2][0])) + "," + str(float(self.rpm_value[3][0]))
        trans_data = trans_data.encode()
        #     self.ser.write(trans_data)
        self.get_logger().info("Data transfer is successful!")
        self.get_logger().info(trans_data)
       
    def cmd_vel2rad(self):
        # convert_matrix = np.array([[1, -1, -(self.width + self.length)], [1, 1, (self.width + self.length)], [1, 1, -(self.width + self.length)], [1, -1, (self.width + self.length)]])
        # self.rpm_value = (convert_matrix*(1/self.radius))@np.array([[self.Vx], [self.Vy], [0.0]]) #rad/s 4by1 matrix
        # if self.Rz < 0.000001 and self.Rz > -0.000001:
        #     pass
        # elif self.Rz > 0.000001:#CCW
        #     rot_mat = np.array([[0.0],[self.Rz],[-self.Rz],[0.0]])
        #     self.rpm_value = self.rpm_value + rot_mat
        # elif self.Rz < -0.000001: #CW
        #     rot_mat = np.array([[self.Rz],[0.0],[0.0],[-self.Rz]])
        #     self.rpm_value = self.rpm_value + rot_mat
        w1 = (-self.Vx/self.radius) + (self.Vy/self.radius) + self.Rz*(self.length + self.width) # rad/s
        w2 = (self.Vx/self.radius) + (self.Vy/self.radius) - self.Rz*(self.length + self.width)
        w3 = -(self.Vx/self.radius) + (self.Vy/self.radius) - self.Rz*(self.length + self.width)
        w4 = (self.Vx/self.radius) + (self.Vy/self.radius) + self.Rz*(self.length + self.width)
        self.rpm_value = np.array([[w1*9.5492968],[w2*9.5492968],[w3*9.5492968],[w4*9.5492968]]) # rad/s -> rpm
            
            


def main(args=None):
    rclpy.init(args=args)

    cmd_vel_sub = CmdVelSubscriber()

    rclpy.spin(cmd_vel_sub)

    cmd_vel_sub.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()