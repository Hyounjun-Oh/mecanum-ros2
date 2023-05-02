import rclpy
from rclpy.node import Node
from dynamixel_sdk_custom_interfaces.msg import SetPosition

class ManipulatorMove(Node):
    def __init__(self):
        super().__init__('manipulator_move')
        self.QoS=10
        self.joint_arr = [500,400,1500,4000] #초기 각도값 반영
        self.man_joint_publisher = self.create_publisher(
            SetPosition,
            'set_position',
            self.QoS
        )
        
    def publish_joint_value(self, dxl_id):
        joint_msg = SetPosition()
        joint_msg.position = 0 #값 초기화
        if dxl_id == 1:
            joint_msg.id = dxl_id
            joint_msg.position = self.joint_arr[0]
            self.man_joint_publisher.publish(joint_msg)
        elif dxl_id == 2:
            joint_msg.id = dxl_id
            joint_msg.position = self.joint_arr[1]
            self.man_joint_publisher.publish(joint_msg)
        elif dxl_id == 3:
            joint_msg.id = dxl_id
            joint_msg.position = self.joint_arr[2]
            self.man_joint_publisher.publish(joint_msg)
        elif dxl_id == 4:
            joint_msg.id = dxl_id
            joint_msg.position = self.joint_arr[3]
            self.man_joint_publisher.publish(joint_msg)
            
def main(args=None):
    rclpy.init(args=args)
    dxl_id = [1,2,3,4]
    move = ManipulatorMove()
    while 1:
        mode = input()
        if mode == 'g':
            for id in dxl_id:
                move.publish_joint_value(id)
        elif mode == 'q':
            break
    move.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()