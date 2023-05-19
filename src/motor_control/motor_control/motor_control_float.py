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

# Editor : Hyoujun Oh

#Arduino Mega - 1 : /dev/ttyACM0 2 : /dev/ttyACM1
import rclpy
from rclpy.node import Node
import numpy as np
import serial
from geometry_msgs.msg import Twist
from std_msgs.msg import Float32MultiArray # 각 바퀴의 각속도 퍼블리쉬용
import time
import struct
#from rcl_interfaces.msg import Parameter
from rclpy.parameter import Parameter
#from rclpy.parameter import ParameterType
#from rcl_interfaces.msg import ParameterValue
#from rcl_interfaces.srv import SetParameters

class CmdVelSubscriber(Node):

    def __init__(self):
        super().__init__('motor_control')
        self.w1 = 0.0
        self.w2 = 0.0
        self.w3 = 0.0
        self.w4 = 0.0
        self.declare_parameter('mobile_robot_length', 0.30)
        self.length = self.get_parameter('mobile_robot_length').value # 중심점으로부터 모터의 세로 위치
        self.declare_parameter('qos_depth', 10)
        qos_depth = self.get_parameter('qos_depth').value #qos파라미터 셋팅
        self.declare_parameter('mobile_robot_width', 0.40)
        self.width = self.get_parameter('mobile_robot_width').value # 중심점으로부터 모터의 가로 위치
        self.declare_parameter('mobile_robot_radius', 0.0625)
        self.radius = self.get_parameter('mobile_robot_radius').value # 메카넘휠 반지름
        self.declare_parameter('baudrate', 1000000)
        self.baudrate = self.get_parameter('baudrate').get_parameter_value().integer_value #시리얼 보드레이트
        self.declare_parameter('arduino_port', "/dev/ttyACM0")
        self.port= self.get_parameter('arduino_port').get_parameter_value().string_value #시리얼 포트
        self.declare_parameter('arduino_num', 0)
        self.arduino_num= Parameter('arduino_num', Parameter.Type.INTEGER,1).value #시리얼 포트
        self.timeout = 10
        self.subscription = self.create_subscription(
            Twist,
            'cmd_vel',
            self.get_cmd_vel,
            qos_depth)
        self.motor_vel_publisher_1 = self.create_publisher(
            Float32MultiArray,
            'motor_vel/front',
            qos_depth
        )
        self.motor_vel_publisher_2 = self.create_publisher(
            Float32MultiArray,
            'motor_vel/rear',
            qos_depth
        )
        self.subscription  # prevent unused variable warning
        self.ser = serial.Serial(self.port, self.baudrate) #OpenCR Port COM3, MEGE Port COM4
        self.get_logger().info("포트 : {0}, 보드레이트 : {1}".format(self.port, self.baudrate, timeout = self.timeout))
        self.ser.flush()
        time.sleep(5)

    def get_cmd_vel(self, msg):
        self.time = self.get_clock().now()
        msg_motor_vel = Float32MultiArray()
        msg_motor_vel.data = [0.0,0.0,0.0]
        self.arduino_num= self.get_parameter('arduino_num').get_parameter_value().integer_value
        self.Vx = msg.linear.x #m/s
        self.Vy = msg.linear.y #m/s
        self.Rz = msg.angular.z #rad/s
        self.cmd_vel2rad()
        if self.ser.readable():
            if self.arduino_num == 0:
                data = str(self.w1) + "," + str(self.w2)
                self.ser.write(data.encode())
                try:
                    motor_vel_arr = list(map(float,(self.ser.readline().decode().rstrip()).split(',')))
                except ValueError: # 시리얼 통신이 처음 초기화 될 때 결측치 발생.
                    motor_vel_arr = [0.0,0.0,0.0]
                else:
                    if motor_vel_arr[0] == 1:
                        if (len(motor_vel_arr) == 3): #데이터가 정상적이지 않으면 거름.
                            msg_motor_vel.layout.data_offset = 1 #모터 드라이버 구분용으로 사용함.
                            msg_motor_vel.data[0] = motor_vel_arr[1]
                            msg_motor_vel.data[1] = motor_vel_arr[2]
                            self.motor_vel_publisher_1.publish(msg_motor_vel)
                        else:
                            pass
                    else:
                        pass
            else:
            
                data = str(self.w3) + "," + str(self.w4)
                self.ser.write(data.encode())
                try:
                    motor_vel_arr = list(map(float,(self.ser.readline().decode().rstrip()).split(',')))
                except ValueError:
                    motor_vel_arr = [0.0, 0.0, 0,0]
                else:
                    if motor_vel_arr[0] == 2:
                        if (len(motor_vel_arr) == 3):
                            msg_motor_vel.layout.data_offset = 2 #모터 드라이버 구분용으로 사용함.
                            msg_motor_vel.data[0] = motor_vel_arr[1]
                            msg_motor_vel.data[1] = motor_vel_arr[2]
                            self.motor_vel_publisher_2.publish(msg_motor_vel)
                        else:
                            pass
                    else:
                        pass

    def cmd_vel2rad(self):
        if self.arduino_num == 0:
            self.w1 = round((((self.Vx - self.Vy - self.Rz*((self.length + self.width)/2))/self.radius)/2*9.5492968),2)
            self.w2 = round((((self.Vx + self.Vy + self.Rz*((self.length + self.width)/2))/self.radius)/2*9.5492968),2)
        else:          
            self.w3 = round((((self.Vx + self.Vy - self.Rz*((self.length + self.width)/2))/self.radius)/2*9.5492968),2)
            self.w4 = round((((self.Vx - self.Vy + self.Rz*((self.length + self.width)/2))/self.radius)/2*9.5492968),2)

def main(args=None):
    rclpy.init(args=args)

    cmd_vel_sub = CmdVelSubscriber()

    rclpy.spin(cmd_vel_sub)
    cmd_vel_sub.clear_serial()
    cmd_vel_sub.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
