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
import time


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
        self.ser = serial.Serial('/dev/ttyACM0', 115200,timeout=1) #OpenCR Port COM3, MEGE Port COM4

    def get_cmd_vel(self, msg):
        self.Vx = msg.linear.x #m/s
        self.Vy = msg.linear.y #m/s
        self.Rz = msg.angular.z #rad/s
        self.cmd_vel2rad()
        if self.ser.readable():
            for motor_num in range(1,5):
                trans_data = str(motor_num) + "," + str(round(float(self.rpm_value[motor_num -1][0]),2))
                trans_data = trans_data.encode()
                self.ser.write(trans_data)
                self.get_logger().info("Data transfer is successful!")
                self.get_logger().info(trans_data)
            #trans_data = str(round(float(self.rpm_value[0][0]),2)) + "," + str(round(float(self.rpm_value[1][0]),2)) + "," + str(round(float(self.rpm_value[2][0]),2)) + "," + str(round(float(self.rpm_value[3][0]),2))
            #trans_data = trans_data.encode()
            #self.ser.write(trans_data)
            #self.get_logger().info("Data transfer is successful!")
            #self.get_logger().info(trans_data)
            #time.sleep(1)
        motor_num = 1
       
    def cmd_vel2rad(self):
        # convert_matrix = np.array([[1, -1, -(self.width + self.length)], [1, 1, (self.width + self.length)], [1, 1, -(self.width + self.length)], [1, -1, (self.width + self.length)]])
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
    ser.close()


if __name__ == '__main__':
    main()
