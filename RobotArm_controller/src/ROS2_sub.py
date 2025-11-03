#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
import serial
import time

class Ros2SerialPublisher(Node):
    def __init__(self, port='/dev/ttyUSB0', baudrate=115200):
        super().__init__('ros2_serial_publisher')
        self.subscription = self.create_subscription(
            JointState,
            '/joint_states',
            self.joint_state_callback,
            10
        )
        self.subscription  # prevent unused warning

        # Setup serial
        try:
            self.ser = serial.Serial(port, baudrate, timeout=0.1)
            time.sleep(2)  # wait for ESP32 reset
            self.get_logger().info(f"Opened serial port {port} at {baudrate} baud")
        except Exception as e:
            self.get_logger().error(f"Failed to open serial port: {e}")
            self.ser = None

    def joint_state_callback(self, msg: JointState):
        if self.ser is None:
            return

        # Convert joint positions to CSV string in radians
        joint_str = ','.join([f"{angle:.6f}" for angle in msg.position])
        joint_str += '\n'

        # Send to ESP32
        try:
            self.ser.write(joint_str.encode('utf-8'))
        except Exception as e:
            self.get_logger().error(f"Serial write failed: {e}")


def main(args=None):
    rclpy.init(args=args)
    node = Ros2SerialPublisher(port='/dev/ttyUSB0', baudrate=115200)
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("Shutting down cleanly")
    finally:
        if node.ser and node.ser.is_open:
            node.ser.close()
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
