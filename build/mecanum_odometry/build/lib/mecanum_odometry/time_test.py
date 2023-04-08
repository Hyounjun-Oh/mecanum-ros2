import rclpy
from rclpy.node import Node
from std_msgs.msg import Int16


class time_test(Node):

    def __init__(self):
        super().__init__("time_test")
        self.old_time = self.get_clock().now().nanoseconds
        self.QOS_ = 10
        self.time_publisher = self.create_publisher(
            Int16,
            'time_test',
            self.QOS_
        )

        timer_period = 0.5
        self.timer = self.create_timer(timer_period, self.time_callback)


    def time_callback(self):
        time = self.get_clock().now().nanoseconds
        duration = (int(time) - int(self.old_time))/1000000000
        print(duration)
        self.old_time = time

def main(args=None):
    rclpy.init()
    tm = time_test()
    rclpy.spin(tm)
    tm.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
