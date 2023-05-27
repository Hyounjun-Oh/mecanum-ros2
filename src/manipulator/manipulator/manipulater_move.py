import rclpy
import time
from rclpy.node import Node
from dynamixel_sdk_custom_interfaces.msg import SetPosition
from std_msgs.msg import Float32MultiArray

class ManipulatorMove(Node):
    def __init__(self):
        super().__init__('manipulator_move')
        self.QoS=10
        self.man_joint_publisher = self.create_publisher(
            SetPosition,
            'set_position',
            self.QoS
        )
        self.sub_dxl_vel = self.create_subscription(
            Float32MultiArray,
            'joint_variables',
            self.sub_dxl_vel,
            self.QoS
        )

    def sub_dxl_vel(self,msg):
        self.joint = msg.data
        dxl_id = [1,2,3,4,5,6]
        for id in dxl_id:
            self.publish_joint_value(id, round(self.joint[id]))

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

def main(args=None):
    rclpy.init(args=args)
    move = ManipulatorMove()
    rclpy.spin(move)
    move.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()