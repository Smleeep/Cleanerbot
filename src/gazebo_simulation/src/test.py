import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
import math
import time


class ToiletBowlRimPublisher(Node):
    def __init__(self):
        super().__init__('toilet_bowl_rim_publisher')

        # Use sim time if available
        self.use_sim_time = self.get_parameter_or('use_sim_time', True).get_parameter_value().bool_value

        # Joint state publisher
        self.publisher_ = self.create_publisher(JointState, '/joint_states', 10)

        # 10 Hz timer
        self.timer_period = 0.1
        self.timer = self.create_timer(self.timer_period, self.publish_pose)

        self.counter = 0
        self.get_logger().info(f'Toilet bowl rim trajectory started (use_sim_time={self.use_sim_time})')

        # Wait for clock if using sim time
        if self.use_sim_time:
            while self.get_clock().now().nanoseconds == 0:
                self.get_logger().info("Waiting for /clock...")
                time.sleep(0.1)

        # Joint names – must match your URDF
        self.joint_names = ['joint_base', 'joint_1', 'joint_2', 'joint_3', 'joint_4']

    def publish_pose(self):
        msg = JointState()
        msg.header.stamp = self.get_clock().now().to_msg()

        # Circular “bowl rim” parameters
        t = self.counter * 0.1
        speed = 0.4           # angular speed of rim traversal
        radius_motion = 0.6   # amplitude of base rotation (circle size)
        lift_amplitude = 0.3  # vertical oscillation (bowl curvature)
        bend = 0.5            # nominal bend angle for shoulder/elbow

        # Joint angles that make the end effector move in a circular rim path
        joint_positions = [
            math.sin(speed * t) * radius_motion,              # base sweeps around rim
            bend + 0.2 * math.sin(speed * t + math.pi / 4),   # shoulder bends slightly
            -bend + 0.2 * math.cos(speed * t + math.pi / 3),  # elbow counter-moves
            lift_amplitude * math.sin(2 * speed * t),         # wrist follows bowl curvature
            0.3 * math.cos(speed * t)                         # wrist orientation
        ]

        msg.name = self.joint_names
        msg.position = joint_positions
        self.counter += 1

        self.publisher_.publish(msg)

        sim_time = self.get_clock().now().nanoseconds / 1e9
        real_time = time.time()
        self.get_logger().info(
            f"Rim motion step {self.counter}: {joint_positions} | sim_time={sim_time:.3f} | real_time={real_time:.3f}"
        )


def main(args=None):
    rclpy.init(args=args)
    node = ToiletBowlRimPublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.get_logger().info("Shutting down toilet bowl rim publisher...")
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
