import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
import math
import time

class GoalPosePublisher(Node):
    def __init__(self):
        super().__init__('joint_state_publisher')

        # Use simulation time if set in launch file
        self.use_sim_time = self.get_parameter_or('use_sim_time', True).get_parameter_value().bool_value

        # Publisher for joint states
        self.publisher_ = self.create_publisher(JointState, '/joint_states', 10)

        # Timer for periodic publishing
        self.timer_period = 0.1  # seconds (10 Hz)
        self.timer = self.create_timer(self.timer_period, self.publish_pose)

        self.counter = 0
        self.get_logger().info(f'JointState publisher started (use_sim_time={self.use_sim_time})')

        # Optional: wait for /clock if using sim time
        if self.use_sim_time:
            while self.get_clock().now().nanoseconds == 0:
                self.get_logger().info("Waiting for /clock...")
                time.sleep(0.1)

    def publish_pose(self):
        msg = JointState()
        msg.header.stamp = self.get_clock().now().to_msg()  # ROS clock (sim or real)
        msg.header.frame_id = 'base_link'

        # Example: each joint moves differently for demonstration
        joint_positions = [
            math.sin(self.counter * 0.1),
            math.sin(self.counter * 0.1 + 0.5),
            math.sin(self.counter * 0.1 + 1.0),
            math.sin(self.counter * 0.1 + 1.5),
            math.sin(self.counter * 0.1 + 2.0)
        ]

        msg.name = ['joint_base','joint_1', 'joint_2', 'joint_3', 'joint_4']
        msg.position = joint_positions
        self.counter += 1

        self.publisher_.publish(msg)

        # Log sim time and real time for debugging
        sim_time = self.get_clock().now().nanoseconds / 1e9
        real_time = time.time()
        self.get_logger().info(f"Published joints: {joint_positions} | sim_time={sim_time:.3f} | real_time={real_time:.3f}")

def main(args=None):
    rclpy.init(args=args)
    node = GoalPosePublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.get_logger().info("Shutting down joint state publisher...")
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()

#moveit
#rtb jtraj
#dae file
#gazebo - dart
#pybullet 