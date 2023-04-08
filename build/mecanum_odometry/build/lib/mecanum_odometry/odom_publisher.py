import rclpy
import numpy as np
import math
from rclpy.node import Node
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist
from sensor_msgs.msg import JointState
from geometry_msgs.msg import TransformStamped
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
        self.vel_x = 0
        self.vel_y = 0
        self.rot_z = 0
        self.odom_pos_y, self.odom_pos_x, self.odom_ori_z = 0,0,0
        self.old_time = self.get_clock().now().nanoseconds
        self.odom_publisher = self.create_publisher(Odometry, 'odom', self.QoS_)
        self.vel_subscription = self.create_subscription(
            Twist,
            'cmd_vel',
            self.cmd_vel_callback,
            self.QoS_)
        # self.imu_subscription = self.create_subscription(
        #     Float64,
        #     'imu/yaw',
        #     self.imu_callback,
        #     self.QoS_
        # )
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
        self.get_logger().info("조인트 콜백 완료")

        
    def update_joint_state(self):
        self.diff_joint_positions_[0] = self.joint_msg.position[0] - self.last_joint_positions_[0]
        self.diff_joint_positions_[1] = self.joint_msg.position[1] - self.last_joint_positions_[1]
        self.diff_joint_positions_[2] = self.joint_msg.position[2] - self.last_joint_positions_[2]
        self.diff_joint_positions_[3] = self.joint_msg.position[3] - self.last_joint_positions_[3]

        self.last_joint_positions_[0] = self.joint_msg.position[0]
        self.last_joint_positions_[1] = self.joint_msg.position[1]
        self.last_joint_positions_[2] = self.joint_msg.position[2]
        self.last_joint_positions_[3] = self.joint_msg.position[3]
        self.get_logger().info("조인트 스테이트 완료")

    def cmd_vel_callback(self, msg): #속도값 받아오기
        self.vel_msg = msg
        self.vel_x = self.vel_msg.linear.x
        self.vel_y = self.vel_msg.linear.y
        self.rot_z = self.vel_msg.angular.z
        self.get_logger().info("속도값 받아오기 완료")

    def imu_callback(self, msg): #IMU값 받아오기
        self.imu_msg = msg
        self.yaw = self.imu_msg

    def odom_calaulator(self): #Odometry값 계산하기
        self.time = self.get_clock().now().nanoseconds
        duration = (int(self.time) - int(self.old_time))/1000000000
        
        pos_x = self.vel_x * duration
        pos_y = self.vel_y * duration
        ori_z = self.rot_z * duration

        self.odom_pos_x = self.odom_pos_x + pos_x
        self.odom_pos_y = self.odom_pos_y + pos_y
        self.odom_ori_z = self.odom_ori_z + ori_z

        self.old_time = self.time
        self.get_logger().info("odom 계산완료")

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
        self.get_logger().info("publish완료")
        

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
