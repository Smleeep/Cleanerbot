#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from std_msgs.msg import Header
import numpy as np
from roboticstoolbox import DHRobot, RevoluteDH
from spatialmath import SE3

class ToiletCleaning(Node):
    def __init__(self):
        super().__init__('rmrc_base_swing_publisher')

        # ROS publisher setup
        self.pub = self.create_publisher(JointState, '/joint_states', 10)
        self.dt = 0.1  # 0.1s → 10 Hz update
        self.timer = self.create_timer(self.dt, self.timer_callback)
        self.phase_step = 0

        # --- Robot DH parameters ---
        self.robot = DHRobot([
            RevoluteDH(d=0.0485, a=0, alpha=0, qlim=[-np.pi, np.pi]),
            RevoluteDH(d=0.08086, a=0, alpha=-np.pi/2, qlim=[-np.pi, np.pi]),
            RevoluteDH(d=0.216761, a=0, alpha=0, qlim=[-1.57, 1.57]),
            RevoluteDH(d=0.280488, a=0, alpha=0, qlim=[-1.57, 1.57]),
            RevoluteDH(d=0.05274, a=0, alpha=np.pi/2, qlim=[-1.57, 1.57])
        ], name='ToiletArm')

        self.joint_names = ['joint_base', 'joint_1', 'joint_2', 'joint_3', 'joint_4']

        # --- Start at home ---
        self.q_home = np.zeros(5)

        # --- Target joint (degrees -> radians) ---
        q_target_deg = np.array([-120, 56, 73, 22, -17])
        self.q_target = np.deg2rad(q_target_deg)
        self.steps_to_target = 100  # smoother trajectory

        # --- Linear trajectory to target ---
        self.q_traj_to_target = np.zeros((self.steps_to_target, 5))
        for i in range(self.steps_to_target):
            alpha = (i + 1) / self.steps_to_target
            self.q_traj_to_target[i, :] = (1 - alpha) * self.q_home + alpha * self.q_target

        # --- Step 2: base rotates 60° while EE follows semicircle ---
        self.steps_base_swing = 120  # smoother semicircle
        self.q_base_traj = []

        # semicircle parameters
        radius = 0.0  # meters, semicircle radius (adjust if needed)
        base_start = self.q_target[0]
        base_end = base_start + np.deg2rad(60)
        base_angles = np.linspace(base_start, base_end, self.steps_base_swing)

        # compute semicircle center relative to target EE
        T_target = self.robot.fkine(self.q_target)
        center_x = T_target.t[0]
        center_y = T_target.t[1] - radius
        z_fixed = T_target.t[2]

        theta = np.linspace(0, np.pi, self.steps_base_swing)  # semicircle angle

        for i in range(self.steps_base_swing):
            q = self.q_target.copy()
            q[0] = base_angles[i]

            # EE desired position along semicircle
            x = center_x + radius * np.cos(theta[i])
            y = center_y + radius * np.sin(theta[i])
            T_des = SE3(x, y, z_fixed)

            # Solve IK for joints 1-4
            try:
                q_corr = self.robot.ikine_min(T_des, q0=q)
                q[1:] = q_corr.q[1:]
            except:
                pass

            self.q_base_traj.append(q)

        self.q_base_traj = np.array(self.q_base_traj)

        # --- Initialize phase ---
        self.phase = 'to_target'
        self.phase_step = 0

    def timer_callback(self):
        msg = JointState()
        msg.header = Header()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.name = self.joint_names

        if self.phase == 'to_target':
            joint_values = self.q_traj_to_target[self.phase_step, :]
            self.phase_step += 1
            if self.phase_step >= self.steps_to_target:
                self.phase = 'base_swing'
                self.phase_step = 0

        elif self.phase == 'base_swing':
            if self.phase_step < len(self.q_base_traj):
                joint_values = self.q_base_traj[self.phase_step, :]
                self.phase_step += 1
            else:
                # Stop at final EE position
                joint_values = self.q_base_traj[-1, :]

        msg.position = joint_values.tolist()
        self.pub.publish(msg)
        print(f"Step {self.phase_step} | Phase: {self.phase} | Joints (rad): {np.round(joint_values, 3)}")

def main(args=None):
    rclpy.init(args=args)
    node = ToiletCleaning()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("Shutting down cleanly")
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
