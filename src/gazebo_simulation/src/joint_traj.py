import rclpy
from rclpy.node import Node
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
import math
import time

class GoalTrajectoryPublisher(Node):
    def __init__(self):
        super().__init__('joint_trajectory_publisher')

        # Use simulation time if set in launch file
        self.use_sim_time = self.get_parameter_or('use_sim_time', True).get_parameter_value().bool_value

        # Publisher for joint trajectories
        self.publisher_ = self.create_publisher(JointTrajectory, '/set_joint_trajectory', 10)

        # Timer for periodic publishing
        self.timer_period = 0.1  # seconds (10 Hz)
        self.timer = self.create_timer(self.timer_period, self.publish_trajectory)

        self.counter = 0
        self.joint_names = ['joint_base','joint_1','joint_2','joint_3','joint_4']
        self.get_logger().info(f'JointTrajectory publisher started (use_sim_time={self.use_sim_time})')

        # Optional: wait for /clock if using sim time
        if self.use_sim_time:
            while self.get_clock().now().nanoseconds == 0:
                self.get_logger().info("Waiting for /clock...")
                time.sleep(0.1)

    def publish_trajectory(self):
        msg = JointTrajectory()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.joint_names = self.joint_names

        # Example: each joint moves differently for demonstration
        joint_positions = [
            math.sin(self.counter * 0.1),
            math.sin(self.counter * 0.1 + 0.5),
            math.sin(self.counter * 0.1 + 1.0),
            math.sin(self.counter * 0.1 + 1.5),
            math.sin(self.counter * 0.1 + 2.0)
        ]

        point = JointTrajectoryPoint()
        point.positions = joint_positions
        point.time_from_start.sec = 0
        point.time_from_start.nanosec = int(self.timer_period * 1e9)  # 0.1s later

        msg.points.append(point)
        self.counter += 1

        self.publisher_.publish(msg)

        # Log for debugging
        sim_time = self.get_clock().now().nanoseconds / 1e9
        real_time = time.time()
        self.get_logger().info(f"Published trajectory: {joint_positions} | sim_time={sim_time:.3f} | real_time={real_time:.3f}")

def main(args=None):
    rclpy.init(args=args)
    node = GoalTrajectoryPublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.get_logger().info("Shutting down trajectory publisher...")
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
