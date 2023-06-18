import rclpy
from rclpy.node import Node
from dynamixel_sdk_custom_interfaces.msg import SetPosition
from std_msgs.msg import Float32MultiArray
from std_msgs.msg import Float64MultiArray
from std_msgs.msg import Int16
import numpy as np

class PublishPose(Node):
    def __init__(self):
        super().__init__('publish_pose')
        self.QoS=10
        self.desired_joint_publisher = self.create_publisher(
            Float32MultiArray,
            'desired_pose',
            self.QoS
        )
        self.timer = self.create_timer(1.0, self.publish_desired_pose)
        self.man_joint_publisher = self.create_publisher(
                SetPosition,
                'set_position',
                self.QoS
            )
        self.tomato_sub = self.create_subscription(
            Float64MultiArray,
            'tomato_detection',
            self.sub_tomato,
            self.QoS
        )
        self.command_flag = self.create_subscription(
            Int16,
            'manipulator_move_flag',
            self.manipulator_flag,
            self.QoS
        )
        self.tomato_position = []
        self.tomato_pose_arr = np.zeros((50,3))
        self.mani_flag = 0
        
    def publish_desired_pose(self,desired_pose):
        msg = Float32MultiArray()
        msg.data = desired_pose
        self.desired_joint_publisher.publish(msg)
        
    def manipulator_flag(self,msg):
        self.mani_flag = msg.data
    
    def sub_tomato(self,msg):
        self.tomato = msg
        self.tomato_id = self.tomato.layout.data_offset
        self.tomato_position = self.tomato.data
        if self.tomato_id:
            if self.tomato_position[0] < 500:
                self.tomato_pose_arr[self.tomato_id-1][0] = self.tomato_position[0]
                self.tomato_pose_arr[self.tomato_id-1][1] = self.tomato_position[1]
                self.tomato_pose_arr[self.tomato_id-1][2] = self.tomato_position[2]

    def publish_joint_value(self, dxl_id, joint_value):
        joint_msg = SetPosition()
        joint_msg.position = 0 #값 초기화
        if dxl_id == 1:
            joint_msg.id = dxl_id
            joint_msg.position = joint_value
            self.man_joint_publisher.publish(joint_msg)
        elif dxl_id == 2:
            joint_msg.id = dxl_id
            joint_msg.position = joint_value
            self.man_joint_publisher.publish(joint_msg)
        elif dxl_id == 3:
            joint_msg.id = dxl_id
            joint_msg.position = joint_value
            self.man_joint_publisher.publish(joint_msg)
        elif dxl_id == 4:
            joint_msg.id = dxl_id
            joint_msg.position = joint_value
            self.man_joint_publisher.publish(joint_msg)
        elif dxl_id == 5:
            joint_msg.id = dxl_id
            joint_msg.position = joint_value
            self.man_joint_publisher.publish(joint_msg)
        elif dxl_id == 6:
            joint_msg.id = dxl_id
            joint_msg.position = joint_value
            self.man_joint_publisher.publish(joint_msg)
        elif dxl_id == 7:
            joint_msg.id = dxl_id
            joint_msg.position = joint_value
            self.man_joint_publisher.publish(joint_msg)
            
def main(args=None):
    rclpy.init(args=args)
    move = PublishPose()
    while 1:
        input_v = input('원하는 포즈를 스페이스바로 구분하여 입력하시오.\n1 : zero\n2 : home\n3 : gripper open\n4 : gripper close\n5 : gripper twist\n6 : aproach bin\n7 : driving mode\n').split(' ')
        desired_pose = list(map(float,input_v))
        if abs(desired_pose[0]) + abs(desired_pose[1]) + abs(desired_pose[2]) == 1:
            dxl_id = [1,2,3,4,5,6]
            joint = [2048,2048,2048,2048,2048,2048]
            for id in dxl_id:
                move.publish_joint_value(id, round(joint[id-1]))
        elif abs(desired_pose[0]) + abs(desired_pose[1]) + abs(desired_pose[2]) == 2:
            dxl_id = [1,2,3,4,5,6]
            joint = [2048,2400,1450,2048,2400,2048]
            for id in dxl_id:
                move.publish_joint_value(id, round(joint[id-1]))
        elif abs(desired_pose[0]) + abs(desired_pose[1]) + abs(desired_pose[2]) == 3:
            dxl_id = [7]
            joint = [650]
            for id in dxl_id:
                move.publish_joint_value(id, round(joint[0]))
        elif abs(desired_pose[0]) + abs(desired_pose[1]) + abs(desired_pose[2]) == 4:
            dxl_id = [7]
            joint = [440]
            for id in dxl_id:
                move.publish_joint_value(id, round(joint[0]))
        elif abs(desired_pose[0]) + abs(desired_pose[1]) + abs(desired_pose[2]) == 5:
            dxl_id = [6]
            joint = [3500]
            for id in dxl_id:
                move.publish_joint_value(id, round(joint[0]))
        elif abs(desired_pose[0]) + abs(desired_pose[1]) + abs(desired_pose[2]) == 6:
            dxl_id = [1,2,3,4,5,6]
            joint = [10,2400,1450,2048,1500,2048]
            for id in dxl_id:
                move.publish_joint_value(id, round(joint[id-1]))
        elif abs(desired_pose[0]) + abs(desired_pose[1]) + abs(desired_pose[2]) == 7:
            dxl_id = [1,2,3,4,5,6]
            joint = [2048,3400,1015,2048,1800,2048]
            for id in dxl_id:
                move.publish_joint_value(id, round(joint[id-1]))
        else:
            if abs(desired_pose[0]) + abs(desired_pose[1]) + abs(desired_pose[2]) == 0:
                flag = 0
            else:
                flag = 1
            if flag == 1:
                move.publish_desired_pose(desired_pose)
                flag = 0
            else:
                print("Not published")
                pass

    move.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()