import rclpy
from rclpy.node import Node
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
import math
import time

class ToiletBowlTrajectoryPublisher(Node):
    def __init__(self):
        super().__init__('toilet_bowl_trajectory_publisher')

        # Use sim time if set
        self.use_sim_time = self.get_parameter_or('use_sim_time', True).get_parameter_value().bool_value

        # Publisher for joint trajectories
        self.publisher_ = self.create_publisher(JointTrajectory, '/set_joint_trajectory', 10)

        # Timer for periodic publishing
        self.timer_period = 0.1  # 10 Hz
        self.timer = self.create_timer(self.timer_period, self.publish_trajectory)

        self.counter = 0
        self.joint_names = ['joint_base', 'joint_1', 'joint_2', 'joint_3', 'joint_4']
        self.get_logger().info(f'Toilet bowl trajectory publisher started (use_sim_time={self.use_sim_time})')

        # Wait for /clock if sim time is active
        if self.use_sim_time:
            while self.get_clock().now().nanoseconds == 0:
                self.get_logger().info("Waiting for /clock...")
                time.sleep(0.1)

    def publish_trajectory(self):
        msg = JointTrajectory()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.joint_names = self.joint_names

        # Simulate a circular "bowl rim" trajectory using sinusoidal joint motion
        t = self.counter * 0.1
        r = 0.8  # bowl radius scaling
        pitch_amplitude = 0.5  # up-down movement amplitude

        # Conceptual motion: base joint sweeps in a circle, others make it dip slightly
        joint_positions = [
            math.sin(t) * r,                 # base rotates in circular path
            0.4 * math.cos(t * 2),           # arm oscillates for dipping
            -0.6 * math.sin(t * 2),          # elbow follows inverse motion
            0.3 * math.sin(t + math.pi / 4), # wrist pitch to simulate bowl curve
            0.2 * math.cos(t)                # wrist rotate slightly
        ]

        point = JointTrajectoryPoint()
        point.positions = joint_positions
        point.time_from_start.sec = 0
        point.time_from_start.nanosec = int(self.timer_period * 1e9)

        msg.points.append(point)
        self.publisher_.publish(msg)
        self.counter += 1

        sim_time = self.get_clock().now().nanoseconds / 1e9
        self.get_logger().info(
            f"Toilet bowl trajectory step {self.counter}: {joint_positions} | sim_time={sim_time:.3f}"
        )

def main(args=None):
    rclpy.init(args=args)
    node = ToiletBowlTrajectoryPublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.get_logger().info("Shutting down toilet bowl trajectory publisher...")
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
