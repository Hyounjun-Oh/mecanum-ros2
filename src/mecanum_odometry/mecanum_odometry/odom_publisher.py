import rclpy
import numpy as np
import math
from rclpy.node import Node
from rclpy import parameter
from nav_msgs.msg import Odometry
from sensor_msgs.msg import JointState
from geometry_msgs.msg import TransformStamped
from std_msgs.msg import Float32MultiArray 
#from sensor_msgs.msg import Imu
from std_msgs.msg import Float64
from tf2_ros import TransformBroadcaster # base_footprint publish

class OdometryNode(Node):

    def __init__(self):
        super().__init__('odom_publisher')
        self.QoS_ = 10
        self.QoS_imu = 1
        self.frame_id = 'odom'
        self.child_frame_id = 'base_footprint'
        self.last_joint_positions_ = [0,0,0,0]
        self.diff_joint_positions_ = [0,0,0,0]
        self.declare_parameter('mobile_robot_length', 0.30)
        self.length = self.get_parameter('mobile_robot_length').value # 중심점으로부터 모터의 세로 위치
        self.declare_parameter('mobile_robot_width', 0.40)
        self.width = self.get_parameter('mobile_robot_width').value # 중심점으로부터 모터의 가로 위치
        self.declare_parameter('mobile_robot_radius', 0.0625)
        self.radius = self.get_parameter('mobile_robot_radius').value # 메카넘휠 반지름
        self.vel_x = 0.0
        self.vel_y = 0.0
        self.rot_z = 0.0
        self.ori_z = 0.0
        self.rot_old = 0.0
        self.odom_ori_z = 0.0
        self.w1, self.w2, self.w3, self.w4 = 0,0,0,0
        self.odom_pos_y, self.odom_pos_x, self.odom_ori_z = 0,0,0
        self.old_time = self.get_clock().now().nanoseconds
        self.odom_publisher = self.create_publisher(Odometry, 'wheel/odometry', self.QoS_)
        #wheel/odometry
        # 모터의 실제 각속도를 받아온다.
        self.vel_subscription_1 = self.create_subscription(
            Float32MultiArray,
            'motor_vel/front',
            self.cmd_vel_callback_1,
            self.QoS_)
        self.vel_subscription_2 = self.create_subscription(
            Float32MultiArray,
            'motor_vel/rear',
            self.cmd_vel_callback_2,
            self.QoS_)
        # self.imu_subscription = self.create_subscription(
        #     Float64,
        #     'imu/yaw',
        #     self.imu_callback,
        #     self.QoS_
        #     )
        self.joint_state_subscription = self.create_subscription(
            JointState,
            'joint_states',
            self.joint_statue_callback,
            self.QoS_
        )
        self.tf_broadcaster = TransformBroadcaster(self)

    def joint_statue_callback(self,msg):
        self.time_now = self.get_clock().now().to_msg()
        self.joint_msg = msg
        self.update_joint_state()
        self.odom_calaulator()
        self.publish()
        #self.get_logger().info("조인트 콜백 완료")

        
    def update_joint_state(self):
        self.diff_joint_positions_[0] = self.joint_msg.position[0] - self.last_joint_positions_[0]
        self.diff_joint_positions_[1] = self.joint_msg.position[1] - self.last_joint_positions_[1]
        self.diff_joint_positions_[2] = self.joint_msg.position[2] - self.last_joint_positions_[2]
        self.diff_joint_positions_[3] = self.joint_msg.position[3] - self.last_joint_positions_[3]

        self.last_joint_positions_[0] = self.joint_msg.position[0]
        self.last_joint_positions_[1] = self.joint_msg.position[1]
        self.last_joint_positions_[2] = self.joint_msg.position[2]
        self.last_joint_positions_[3] = self.joint_msg.position[3]

    def cmd_vel_callback_1(self, msg): #속도값 받아오기
        self.vel_msg = msg
        self.w1 = msg.data[0]*0.1047198 # rpm to rad/s
        self.w2 = msg.data[1]*0.1047198
            
    def cmd_vel_callback_2(self, msg): #속도값 받아오기
        self.vel_msg = msg
        self.w3 = msg.data[0]*0.1047198
        self.w4 = msg.data[1]*0.1047198
        #self.get_logger().info(str(self.odom_ori_z))

    # def imu_callback(self, msg): #IMU값 받아오기
    #     self.imu_msg = msg
    #     self.yaw = self.imu_msg

    def odom_calaulator(self): #Odometry값 계산하기
        self.time = self.get_clock().now().nanoseconds
        duration = (int(self.time) - int(self.old_time))/1000000000
        self.vel_x = (self.radius/4)*(self.w1 + self.w2 + self.w3 + self.w4)
        self.vel_y = (self.radius/4)*(-self.w1 + self.w2 + self.w3 - self.w4)
        self.rot_z = (self.radius/4)*(4/(self.length + self.width))*(-self.w1 + self.w2 - self.w3 + self.w4) #2
        del_rot = self.rot_z * duration
        del_x = (self.vel_x * np.cos(del_rot) - self.vel_y * np.sin(del_rot) ) * duration
        del_y = (self.vel_x * np.sin(del_rot) + self.vel_y * np.cos(del_rot) ) * duration
        self.odom_pos_x += del_x
        self.odom_pos_y += del_y 
        self.odom_ori_z += del_rot
        self.get_logger().info(str(self.odom_ori_z))
        self.rot_old = self.rot_z
        self.old_time = self.time

    def publish(self): # Odometry와 tf발행
        msg_odom = Odometry()
        msg_odom.header.frame_id = self.frame_id
        msg_odom.child_frame_id = self.child_frame_id
        msg_odom.header.stamp = self.time_now

        msg_odom.pose.pose.position.x = self.odom_pos_x
        msg_odom.pose.pose.position.y = self.odom_pos_y
        msg_odom.pose.pose.position.z = 0.0

        orientation_quaternion = self.quaternion_from_euler(0,0,self.odom_ori_z)
        msg_odom.pose.pose.orientation.x = orientation_quaternion[0]
        msg_odom.pose.pose.orientation.y = orientation_quaternion[1]
        msg_odom.pose.pose.orientation.z = orientation_quaternion[2]
        msg_odom.pose.pose.orientation.w = orientation_quaternion[3]
        msg_odom.twist.twist.linear.x = self.vel_x
        msg_odom.twist.twist.linear.y = self.vel_y
        msg_odom.twist.twist.angular.z = self.rot_z

        msg_tf = TransformStamped()
        msg_tf.header.frame_id = self.frame_id
        msg_tf.child_frame_id = self.child_frame_id
        msg_tf.header.stamp = self.time_now

        msg_tf.transform.translation.x = msg_odom.pose.pose.position.x
        msg_tf.transform.translation.y = msg_odom.pose.pose.position.y
        msg_tf.transform.translation.z = msg_odom.pose.pose.position.z
        msg_tf.transform.rotation.x = msg_odom.pose.pose.orientation.x
        msg_tf.transform.rotation.y = msg_odom.pose.pose.orientation.y
        msg_tf.transform.rotation.z = msg_odom.pose.pose.orientation.z
        msg_tf.transform.rotation.w = msg_odom.pose.pose.orientation.w

        self.odom_publisher.publish(msg_odom)
        self.tf_broadcaster.sendTransform(msg_tf)
        #self.get_logger().info("현재 x좌표 : {0}, Y좌표 : {1}, 헤딩 : {2}".format(self.odom_pos_x,self.odom_pos_y,self.odom_ori_z))
        

    def quaternion_from_euler(self, ai, aj, ak):
        ai /= 2.0
        aj /= 2.0
        ak /= 2.0
        ci = math.cos(ai)
        si = math.sin(ai)
        cj = math.cos(aj)
        sj = math.sin(aj)
        ck = math.cos(ak)
        sk = math.sin(ak)
        cc = ci*ck
        cs = ci*sk
        sc = si*ck
        ss = si*sk

        q = np.empty((4, ))
        q[0] = cj*sc - sj*cs
        q[1] = cj*ss + sj*cc
        q[2] = cj*cs - sj*sc
        q[3] = cj*cc + sj*ss

        return q
        
        
    


def main(args=None):
    rclpy.init(args=args)
    node = OdometryNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
