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

#Arduino Mega - Master Port : /dev/ttyACM0
import rclpy
from rclpy.node import Node
import numpy as np
import serial
from geometry_msgs.msg import Twist
import time
#from rcl_interfaces.msg import Parameter
from rclpy.parameter import Parameter
#from rclpy.parameter import ParameterType
#from rcl_interfaces.msg import ParameterValue
#from rcl_interfaces.srv import SetParameters

class CmdVelSubscriber(Node):

    def __init__(self):
        super().__init__('motor_control')
        #self.my_param = Parameter('my_param', Parameter.Type.STRING, 'hello')
        self.declare_parameter('mobile_robot_length', 0.15)
        self.length = self.get_parameter('mobile_robot_length').value # 중심점으로부터 모터의 세로 위치
        self.declare_parameter('qos_depth', 10)
        qos_depth = self.get_parameter('qos_depth').value #qos파라미터 셋팅
        self.declare_parameter('mobile_robot_width', 0.17)
        self.width = self.get_parameter('mobile_robot_width').value # 중심점으로부터 모터의 가로 위치
        self.declare_parameter('mobile_robot_radius', 0.05)
        self.radius = self.get_parameter('mobile_robot_radius').value # 메카넘휠 반지름
        self.declare_parameter('baudrate', 115200)
        self.baudrate = self.get_parameter('baudrate').get_parameter_value().integer_value #시리얼 보드레이트
        self.declare_parameter('arduino_port', "/dev/ttyACM0")
        self.port= self.get_parameter('arduino_port').get_parameter_value().string_value #시리얼 포트
        self.declare_parameter('arduino_num', 0)
        self.arduino_num= Parameter('arduino_num', Parameter.Type.INTEGER,1).value #시리얼 포트
        self.subscription = self.create_subscription(
            Twist,
            'cmd_vel',
            self.get_cmd_vel,
            qos_depth)
        self.subscription  # prevent unused variable warning
        self.ser = serial.Serial(self.port, self.baudrate) #OpenCR Port COM3, MEGE Port COM4
        self.get_logger().info("포트 : {0}, 보드레이트 : {1}".format(self.port, self.baudrate))

    def get_cmd_vel(self, msg):
        self.arduino_num= self.get_parameter('arduino_num').get_parameter_value().integer_value
        self.Vx = msg.linear.x #m/s
        self.Vy = msg.linear.y #m/s
        self.Rz = msg.angular.z #rad/s
        self.cmd_vel2rad()
        if self.ser.readable():
            if self.arduino_num == 0:                
                trans_data = str(round(float(self.rpm_value[0][0]),2)) + "," + str(round(float(self.rpm_value[1][0]),2))
                trans_data = trans_data.encode()
                self.ser.write(trans_data)
                self.get_logger().info("Front motor data transfer is successful!")
                self.get_logger().info(trans_data)
            else:
                trans_data = str(round(float(self.rpm_value[0][0]),2)) + "," + str(round(float(self.rpm_value[1][0]),2))
                trans_data = trans_data.encode()
                self.ser.write(trans_data)
                self.get_logger().info("Rear motor data transfer is successful!")
                self.get_logger().info(trans_data)
        self.ser.flush() # 시리얼 버퍼 초기화
        # 0.001초 딜레이 적용 완료 아두이노는 10ms 간격
        time.sleep(0.001)
       
    def cmd_vel2rad(self):
        if self.arduino_num == 0:
            w1 = (-self.Vx/self.radius) + (self.Vy/self.radius) + self.Rz*(self.length + self.width)
            w2 = (self.Vx/self.radius) + (self.Vy/self.radius) - self.Rz*(self.length + self.width)
            self.rpm_value = np.array([[w1*9.5492968],[w2*9.5492968]]) # rad/s -> rpm
        else:          
            w3 = -(self.Vx/self.radius) + (self.Vy/self.radius) - self.Rz*(self.length + self.width)
            w4 = (self.Vx/self.radius) + (self.Vy/self.radius) + self.Rz*(self.length + self.width)
            self.rpm_value = np.array([[w3*9.5492968],[w4*9.5492968]]) # rad/s -> rpm
            
def main(args=None):
    rclpy.init(args=args)

    cmd_vel_sub = CmdVelSubscriber()

    rclpy.spin(cmd_vel_sub)

    cmd_vel_sub.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
