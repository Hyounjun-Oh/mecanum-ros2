import rclpy
from rclpy.node import Node
from dynamixel_sdk_custom_interfaces.msg import SetPosition
from std_msgs.msg import Float32MultiArray

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
    def publish_desired_pose(self,desired_pose):
        msg = Float32MultiArray()
        msg.data = desired_pose
        self.desired_joint_publisher.publish(msg)

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
    move = PublishPose()
    desired_pose_old = [0.0, 0.0, 0.0]
    while 1:
        input_v = input('원하는 포즈를 스페이스바로 구분하여 입력하시오.').split(' ')
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
        else:
            if abs(desired_pose[0]) + abs(desired_pose[1]) + abs(desired_pose[2]) == 0:
                flag = 0
            elif desired_pose == desired_pose_old:
                flag = 0
            else:
                flag = 1
            print(flag)
            if flag == 1:
                move.publish_desired_pose(desired_pose)
                flag = 0
                #desired_pose = [0.0,0.0,0.0]
            else:
                print("Not published")
                pass
        
        desired_pose_old = desired_pose

    move.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()