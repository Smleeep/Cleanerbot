import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
import numpy as np
from itertools import product
import time

class JointStatePublisher(Node):
    def __init__(self):
        super().__init__('joint_state_publisher')

        # Publisher
        self.publisher_ = self.create_publisher(JointState, 'joint_states', 10)

        # Joint names in order (include curved joint)
        self.joint_names = [
            'joint_curved',
            'joint_base',
            'joint_1',
            'joint_2',
            'joint_3',
            'joint_4'
        ]

        # Joint limits
        self.joint_limits = [
            (0.0, 3.14),          # joint_curved
            (-3.14159, 3.14159),  # joint_base
            (-1.57, 1.57),        # joint_1
            (-1.57, 1.57),        # joint_2
            (-1.57, 1.57),        # joint_3
            (-1.57, 1.57),        # joint_4
        ]

        self.step_size = 0.1  # radians
        self.angle_ranges = [np.arange(low, high + self.step_size, self.step_size) for low, high in self.joint_limits]

        # Precompute all joint configurations
        self.all_joint_configs = list(product(*self.angle_ranges))
        self.get_logger().info(f'Total configurations: {len(self.all_joint_configs)}')

        # Start publishing
        self.timer = self.create_timer(0.05, self.publish_next_config)  # 0.5 s between configs
        self.index = 0

    def publish_next_config(self):
        if self.index >= len(self.all_joint_configs):
            self.index = 0  # loop back to start

        joint_angles = self.all_joint_configs[self.index]

        msg = JointState()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.name = self.joint_names
        msg.position = joint_angles

        self.publisher_.publish(msg)
        self.get_logger().info(f'Published: {joint_angles}')

        self.index += 1


def main(args=None):
    rclpy.init(args=args)
    node = JointStatePublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
