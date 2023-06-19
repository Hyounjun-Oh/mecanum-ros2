import rclpy
from rclpy.node import Node
from dynamixel_sdk_custom_interfaces.msg import SetPosition
from std_msgs.msg import Float32MultiArray
from std_msgs.msg import Float64MultiArray
from std_msgs.msg import Int16
import numpy as np
import time

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
        # self.command_flag = self.create_subscription(
        #     Int16,
        #     'manipulator_flag',
        #     self.manipulator_flag,
        #     self.QoS
        # )
        # self.get_position = self.create_client(
        #     ,
        #     'get_position',
        #     self.get_position,
            
        # )
        self.tomato_position = []
        self.tomato_pose_arr = np.zeros((10,4),dtype=float) # 맥시멈 50개 4 : id, X, Y, Z
        self.joint_position_arr = np.array([
            [2048,2048,2048,2048,2048,2048], # Zero Pose
            [2048,2400,1450,2048,2400,2048], # Detection Pose
            [10,2400,1450,2048,1500,2048],   # Aproach Bin Pose
            [2048,3400,1015,2048,1800,2048]  # Driving Pose
        ])
        self.gripper_pose = np.array([
            [650],# 열기
            [440] # 닫기
        ])
        self.mani_flag = 1
        self.desired_pose = [0.0,0.0,0.0]
        
    def publish_desired_pose(self):
        msg = Float32MultiArray()
        msg.data = list(self.desired_pose)
        self.desired_joint_publisher.publish(msg)
        
    # def manipulator_flag(self,msg):
    #     self.mani_flag = msg.data
    
    def sub_tomato(self,msg):
        self.tomato = msg
        self.tomato_id = self.tomato.layout.data_offset
        self.tomato_position = self.tomato.data
        if self.tomato_id:
            if self.tomato_position[0] < 400:
                self.tomato_pose_arr[self.tomato_id-1][0] = self.tomato_id
                self.tomato_pose_arr[self.tomato_id-1][1] = (self.tomato_position[0] + 270)
                self.tomato_pose_arr[self.tomato_id-1][2] = self.tomato_position[1]
                self.tomato_pose_arr[self.tomato_id-1][3] = (self.tomato_position[2] + 80 + 300 )#50
        #self.get_logger().info(self.tomato_pose_arr)

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
    input_mode = int(input('모드를 선택하세요.\n1 : 자동 수확모드\n2 : 수동 수확모드'))
    dxl_id = [1,2,3,4,5,6]
    while 1:
        if input_mode == 1:
            ############################토마토 감지 포즈로 초기화#########################
            joint = move.joint_position_arr[1][:]
            for id in dxl_id:
                move.publish_joint_value(id, round(joint[id-1]))
            time.sleep(8)
            #########################################################################
            rclpy.spin_once(move)
            print(move.tomato_pose_arr)
            # if move.mani_flag == 0: #좌표값이 0이 아니며 매니퓰레이터가 정지한 상태
            #     print("플래그 작동 필요!!!!")
            for id in range(0,np.size(move.tomato_pose_arr,0)):
                if move.tomato_pose_arr[id][0] == 0:
                    print("ID{0} 정보 없음.".format(id+1))
                else:
                    print("ID{0} 수확 시작".format(id+1))
                    # 수확 과정 알고리즘 적용
                    if abs(move.tomato_pose_arr[id][1]) + abs(move.tomato_pose_arr[id][2]) + abs(move.tomato_pose_arr[id][3]) != 0: #좌표가 0이 아니어야함
                        move.desired_pose = move.tomato_pose_arr[id][1:]
                        print("Desired Position\n{0}".format(move.desired_pose))
                        move.publish_desired_pose() #move노드에서 Matlab 돌리고 목표점까지 구동
                        time.sleep(8) #계산하는 동안은 매니퓰레이터가 작동을 안하므로 sleep으로 일정 텀을 준다.
                        
                        move.publish_joint_value(7,440) # 그리퍼 클로즈
                        time.sleep(1)
                        
                        move.publish_joint_value(6,3500) # 6번조인트 트위스트
                        time.sleep(4)
                        
                        # joint = move.joint_position_arr[1][:] # 디텍션 자세로 복귀
                        # for id_iter in dxl_id:
                        #     move.publish_joint_value(dxl_id, round(joint[id_iter-1]))
                        joint = move.joint_position_arr[1][:]
                        for id in dxl_id:
                            move.publish_joint_value(id, round(joint[id-1]))

                        time.sleep(4)
                        joint = move.joint_position_arr[2][:] # 바구니로 뒤쪽 회전
                        for id in dxl_id:
                            move.publish_joint_value(id, round(joint[id-1]))
                        time.sleep(4)
                        
                        move.publish_joint_value(7,650) # 그리퍼 오픈
                        time.sleep(1)
                        
                        joint = move.joint_position_arr[1][:] # 디텍션 자세로 복귀
                        for id in dxl_id:
                            move.publish_joint_value(id, round(joint[id-1]))
                        time.sleep(4)
                        # move.tomato_pose_arr = np.zeros((10,4),dtype=float)
            # else:
            #     print("Not published")
            #     pass
        elif input_mode == 2:
            input_v = input('원하는 포즈를 스페이스바로 구분하여 입력하시오.\n1 : zero\n2 : home\n3 : gripper open\n4 : gripper close\n5 : gripper twist\n6 : aproach bin\n7 : driving mode\n').split(' ')
            desired_pose = list(map(float,input_v))
            if abs(desired_pose[0]) + abs(desired_pose[1]) + abs(desired_pose[2]) == 1:
                dxl_id = [1,2,3,4,5,6]
                joint = move.joint_position_arr[0][:]
                for id in dxl_id:
                    move.publish_joint_value(id, round(joint[id-1]))
            elif abs(desired_pose[0]) + abs(desired_pose[1]) + abs(desired_pose[2]) == 2:
                dxl_id = [1,2,3,4,5,6]
                joint = move.joint_position_arr[1][:]
                for id in dxl_id:
                    move.publish_joint_value(id, round(joint[id-1]))
            elif abs(desired_pose[0]) + abs(desired_pose[1]) + abs(desired_pose[2]) == 3:
                dxl_id = [7]
                joint = move.gripper_pose[0][0]
                for id in dxl_id:
                    move.publish_joint_value(id, round(joint))
            elif abs(desired_pose[0]) + abs(desired_pose[1]) + abs(desired_pose[2]) == 4:
                dxl_id = [7]
                joint = move.gripper_pose[1][0]
                for id in dxl_id:
                    move.publish_joint_value(id, round(joint))
            elif abs(desired_pose[0]) + abs(desired_pose[1]) + abs(desired_pose[2]) == 5:
                dxl_id = [6]
                joint = [3500]
                for id in dxl_id:
                    move.publish_joint_value(id, round(joint[0]))
            elif abs(desired_pose[0]) + abs(desired_pose[1]) + abs(desired_pose[2]) == 6:
                dxl_id = [1,2,3,4,5,6]
                joint = move.joint_position_arr[2][:]
                for id in dxl_id:
                    move.publish_joint_value(id, round(joint[id-1]))
            elif abs(desired_pose[0]) + abs(desired_pose[1]) + abs(desired_pose[2]) == 7:
                dxl_id = [1,2,3,4,5,6]
                joint = move.joint_position_arr[3][:]
                for id in dxl_id:
                    move.publish_joint_value(id, round(joint[id-1]))
            else:
                if abs(desired_pose[0]) + abs(desired_pose[1]) + abs(desired_pose[2]) == 0:
                    pass
                else:
                    move.publish_desired_pose(desired_pose)

    move.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()