import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
import math
import numpy as np
import time
import roboticstoolbox as rtb
from roboticstoolbox.tools.trajectory import trapezoidal
from spatialmath import SE3
import swift


class GoalPosePublisher(Node):
    def __init__(self):
        super().__init__('joint_state_publisher')
        self.publisher_ = self.create_publisher(JointState, '/joint_states', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.publish_pose)
        self.counter = 0

    def publish_pose(self):
        msg = JointState()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'joint_base'

        # Update joint state
        msg.name = ['joint_base','joint_1', 'joint_2', 'joint_3', 'joint_4']
        msg.position = [math.sin(self.counter * 0.1)] * 5
        self.counter += 1

        self.publisher_.publish(msg)
        self.get_logger().info(f'Published joint state: {msg.position}')
    

def main(args=None):
    rclpy.init(args=args)
    node = GoalPosePublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

#moveit
#rtb jtraj
#dae file
#gazebo - dart
#pybullet 