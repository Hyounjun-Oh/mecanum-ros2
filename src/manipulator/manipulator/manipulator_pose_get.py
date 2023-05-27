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
        
    def publish_desired_pose(self,desired_pose):
        msg = Float32MultiArray()
        msg.data = desired_pose
        self.desired_joint_publisher.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    move = PublishPose()
    desired_pose_old = [0.0, 0.0, 0.0]
    while 1:
        input_v = input('원하는 포즈를 스페이스바로 구분하여 입력하시오.').split(' ')
        desired_pose = list(map(float,input_v))
        if sum(desired_pose) == 0:
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