import rclpy
from rclpy.node import Node
from dynamixel_sdk_custom_interfaces.msg import SetPosition
from std_msgs.msg import Float32MultiArray

class ManipulatorMove(Node):
    def __init__(self):
        super().__init__('manipulator_move')
        self.QoS=10
        self.home_position = [2048,2048,2048,2048,2048,2048] #초기 각도값 반영
        # self.man_joint_publisher = self.create_publisher(
        #     SetPosition,
        #     'set_position',
        #     self.QoS
        # )
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
        
    # def publish_joint_value(self, dxl_id, joint_value):
    #     joint_msg = SetPosition()
    #     joint_msg.position = 0 #값 초기화
    #     if dxl_id == 1:
    #         joint_msg.id = dxl_id
    #         joint_msg.position = joint_value
    #         self.man_joint_publisher.publish(joint_msg)
    #     elif dxl_id == 2:
    #         joint_msg.id = dxl_id
    #         joint_msg.position = joint_value
    #         self.man_joint_publisher.publish(joint_msg)
    #     elif dxl_id == 3:
    #         joint_msg.id = dxl_id
    #         joint_msg.position = joint_value
    #         self.man_joint_publisher.publish(joint_msg)
    #     elif dxl_id == 4:
    #         joint_msg.id = dxl_id
    #         joint_msg.position = joint_value
    #         self.man_joint_publisher.publish(joint_msg)
    #     elif dxl_id == 5:
    #         joint_msg.id = dxl_id
    #         joint_msg.position = joint_value
    #         self.man_joint_publisher.publish(joint_msg)
    #     elif dxl_id == 6:
    #         joint_msg.id = dxl_id
    #         joint_msg.position = joint_value
    #         self.man_joint_publisher.publish(joint_msg)
            
    # def manipulator_joints_calculator(self):
    #     input_v = input('조인트 값 네 개를 스페이스바로 구분하여 입력하시오.').split(' ')
    #     input_value = list(map(int,input_v))
    #     return input_value
            
def main(args=None):
    rclpy.init(args=args)
    dxl_id = [1,2,5,6,3,4]
    move = ManipulatorMove()
    while 1:
        input_v = input('원하는 포즈를 스페이스바로 구분하여 입력하시오.').split(' ')
        desired_pose = list(map(float,input_v))
        if sum(desired_pose) == 0:
            flag = 0
        else:
            flag = 1
        print(flag)
        if flag == 1:
            move.publish_desired_pose(desired_pose)
            flag = 0
            desired_pose = [0.0,0.0,0.0]
        else:
            print("Not published")
            pass
            
        # mode = input('MODE 를 설정하시오.')
        # if mode == 'h':
        #     print("Home Pose로 이동합니다.")
        #     joint_value = [2048, 2048, 2048, 2048, 2048, 2048]
        #     for id in dxl_id:
        #             move.publish_joint_value(id, joint_value[id-1])
        # else:
        #     joint_value = move.manipulator_joints_calculator()
        #     print(joint_value)
        #     if mode == 'g':
        #         for id in dxl_id:
        #             move.publish_joint_value(id, joint_value[id-1]) #id가 1~4까지 일경우 id-1임. 아닐경우 변경 요망
        #     elif mode == 'q':
        #         break
    move.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()