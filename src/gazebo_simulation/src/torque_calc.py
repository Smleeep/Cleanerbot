import numpy as np
import matplotlib.pyplot as plt

# ---------- Robot Parameters from URDF ----------

# Link masses (kg)
masses = [0.25, 0.18, 0.18, 0.13, 0.016, 0.016]  # base_link + 5 links

# COM positions in local link frames (meters)
com_positions = [
    np.array([0, 0, 0]),        # base_link (fixed, can ignore)
    np.array([0, 0, 0.045]),     # link_1
    np.array([-0.002, 0, 0.151]),     # link_2
    np.array([0, 0, 0.153]),     # link_3
    np.array([0, 0, 0.14]),     # link_4
    np.array([0, 0, 0.026])     # link_5
]

# Joint axes (unit vectors in parent frame)
joint_axes = [
    np.array([0, 0, 1]),  # joint_base
    np.array([0, 1, 0]),  # joint_1
    np.array([0, 1, 0]),  # joint_2
    np.array([0, 1, 0]),  # joint_3
    np.array([0, 0, 1])   # joint_4
]

# Joint positions (relative to parent link frame)
joint_positions = [
    np.array([0, 0, 0.0485]),    # joint_base
    np.array([0, 0, 0.08086]),   # joint_1
    np.array([0, 0, 0.21676113]),# joint_2
    np.array([0, 0, 0.280488]),  # joint_3
    np.array([0, 0, 0])          # joint_4
]

# Joint limits from URDF (radians)
joint_limits = [
    [-np.pi, np.pi],
    [-np.pi, np.pi],
    [-np.pi, np.pi],
    [-np.pi/2, np.pi/2],
    [-np.pi/2, np.pi/2]
]

# Number of joints
n = len(joint_axes)

# ---------- Forward Kinematics ----------
def forward_kinematics(q):
    transforms = [np.eye(4)]
    for i in range(n):
        T_parent = transforms[i]
        axis = joint_axes[i]
        theta = q[i]
        pos = joint_positions[i]

        # Rotation matrix
        if np.allclose(axis, [1,0,0]):
            R = np.array([[1,0,0],
                          [0,np.cos(theta),-np.sin(theta)],
                          [0,np.sin(theta), np.cos(theta)]])
        elif np.allclose(axis, [0,1,0]):
            R = np.array([[np.cos(theta),0,np.sin(theta)],
                          [0,1,0],
                          [-np.sin(theta),0,np.cos(theta)]])
        else:  # z-axis
            R = np.array([[np.cos(theta),-np.sin(theta),0],
                          [np.sin(theta), np.cos(theta),0],
                          [0,0,1]])
        # Homogeneous transform
        T = np.eye(4)
        T[:3,:3] = R
        T[:3,3] = pos
        transforms.append(T_parent @ T)
    return transforms

# ---------- Gravity Torque Calculation ----------
def gravity_torques(q, g=np.array([0,0,-9.81])):
    tau = np.zeros(n)
    transforms = forward_kinematics(q)
    for i in range(n):
        axis = joint_axes[i]
        torque = 0.0
        for j in range(i+1, n+1):
            m = masses[j]
            com_local = com_positions[j]
            T = transforms[j]
            com_world = T[:3,3] + T[:3,:3] @ com_local
            r = com_world - transforms[i][:3,3]
            torque += np.dot(np.cross(r, m*g), axis)
        tau[i] = torque
    return tau

# ---------- Sweep Each Joint and Plot ----------
steps = 100  # steps per joint
plt.figure(figsize=(10,6))

for joint_idx in range(n):
    joint_range = np.linspace(joint_limits[joint_idx][0], joint_limits[joint_idx][1], steps)
    torques = []
    for angle in joint_range:
        q = np.zeros(n)
        q[joint_idx] = angle
        tau = gravity_torques(q)
        torques.append(tau[joint_idx])
    plt.plot(np.rad2deg(joint_range), torques, label=f'Joint {joint_idx+1}')

plt.xlabel('Joint Angle (degrees)')
plt.ylabel('Torque (Nm)')
plt.title('Gravity Torque vs Joint Angle for Each Joint')
plt.legend()
plt.grid(True)
plt.show()
