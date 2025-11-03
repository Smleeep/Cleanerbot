#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
import serial

class JointStatePublisher(Node):
    def __init__(self, port='/dev/ttyUSB0', baudrate=115200):
        super().__init__('joint_state_publisher')
        self.subscription = self.create_subscription(
            JointState,
            '/joint_states',
            self.joint_state_callback,
            10
        )
        self.ser = serial.Serial(port, baudrate)
        self.subscription  # prevent unused warning

    def joint_state_callback(self, msg: JointState):
        # Convert joint positions to a list of 4 decimal places
        joint_positions = [round(pos, 4) for pos in msg.position]
        # Convert to string format expected by ESP32: [-1.0472, 0.9774, ...]
        msg_str = str(joint_positions) + '\n'
        # Send over serial
        self.ser.write(msg_str.encode('ascii'))
        # Optional: print for debugging
        print(msg_str.strip())

def main(args=None):
    rclpy.init(args=args)
    node = JointStatePublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        print("Shutting down...")
    finally:
        node.ser.close()
        node.destroy_node()
        rclpy.shutdown()

if __name__ == "__main__":
    main()
