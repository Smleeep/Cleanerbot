# Cleanerbot

Cleanerbot is a robotic toilet-cleaning system developed as a university capstone project. The project explores how industrial robotic-arm concepts can be adapted to a small-scale household cleaning application.

The system uses a custom 5-degree-of-freedom robotic arm together with ROS 2, MoveIt 2, RViz, robot kinematics, trajectory planning, and an ESP32-based servo controller.

The software allows the robot to be modelled and visualised in ROS, planned using MoveIt, and controlled physically by transmitting joint commands from ROS to the ESP32.

---

# Project Overview

Cleanerbot consists of two main components:

## ROS 2 Robotic Arm Workspace

- Robot model (URDF/Xacro)
- RViz visualisation
- MoveIt 2 motion planning
- Joint state communication
- Trajectory generation
- Gazebo simulation
- Serial communication

## ESP32 Robot Controller

- Receives joint commands from ROS
- Converts commands into servo movements
- Controls the physical robotic arm

### System Architecture

```text
                  ┌─────────────┐
                  │    RViz     │
                  │ Interactive │
                  │   Marker    │
                  └──────┬──────┘
                         │
                         ▼
                  ┌─────────────┐
                  │   MoveIt 2  │
                  │   Motion    │
                  │   Planner   │
                  └──────┬──────┘
                         │
                         ▼
                 Joint Positions
                         │
                         ▼
                  /joint_states
                         │
                         ▼
               ┌─────────────────┐
               │ ROS Serial Node │
               │     Python      │
               └────────┬────────┘
                        │ USB Serial
                        ▼
                    ┌───────┐
                    │ ESP32 │
                    └───┬───┘
                        │
                        ▼
                     Servos
                        │
                        ▼
                 Physical Robot Arm
```

---

# Robot Design

The robot uses five rotational joints:

| Joint | Function |
|---------|---------|
| joint_base | Base rotation (yaw) |
| joint_1 | Shoulder pitch |
| joint_2 | Elbow pitch |
| joint_3 | Wrist pitch |
| joint_4 | Wrist rotation |

Robot links:

```text
base_link
link_1
link_2
link_3
link_4
link_5
camera_link
```

---

# Repository Structure

```text
Cleanerbot/
│
├── src/
│   ├── Robot description packages
│   ├── URDF/Xacro files
│   ├── MoveIt configuration
│   ├── Gazebo configuration
│   ├── Launch files
│   └── ROS nodes
│
├── RobotArm_controller/
│   └── ESP32 controller code
│
├── README.md
└── LICENSE
```

---

# Software Requirements

The project was developed using:

- Ubuntu 22.04 LTS
- ROS 2 Humble
- MoveIt 2
- RViz 2
- Gazebo
- Python 3
- ESP32
- Arduino IDE / PlatformIO
- Git

---

# ROS 2 Installation

Install ROS 2 Humble Desktop:

```bash
sudo apt update
sudo apt install ros-humble-desktop
```

Source ROS:

```bash
source /opt/ros/humble/setup.bash
```

Add to `.bashrc`:

```bash
echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
source ~/.bashrc
```

---

# Required Packages

## Development Tools

```bash
sudo apt install \
python3-colcon-common-extensions \
python3-rosdep \
python3-pip \
git
```

## MoveIt 2

```bash
sudo apt install ros-humble-moveit
```

## MoveIt Setup Assistant

```bash
sudo apt install ros-humble-moveit-setup-assistant
```

## RViz

```bash
sudo apt install ros-humble-rviz2
```

## Robot State Publisher

```bash
sudo apt install ros-humble-robot-state-publisher
```

## Joint State Publisher

```bash
sudo apt install \
ros-humble-joint-state-publisher \
ros-humble-joint-state-publisher-gui
```

## Xacro

```bash
sudo apt install ros-humble-xacro
```

## ROS 2 Control

```bash
sudo apt install \
ros-humble-ros2-control \
ros-humble-ros2-controllers
```

## Gazebo

```bash
sudo apt install \
ros-humble-gazebo-ros \
ros-humble-gazebo-ros-pkgs \
ros-humble-gazebo-ros2-control
```

## Serial Communication

```bash
pip3 install pyserial
```

or

```bash
sudo apt install python3-serial
```

---

# Installing Dependencies Automatically

Initialize rosdep:

```bash
sudo rosdep init
rosdep update
```

Install dependencies:

```bash
rosdep install --from-paths src --ignore-src -r -y
```

---

# Clone the Repository

```bash
git clone https://github.com/Smleeep/Cleanerbot.git
cd Cleanerbot
```

---

# Build the Workspace

```bash
source /opt/ros/humble/setup.bash
colcon build
```

After building:

```bash
source install/setup.bash
```

Optional:

```bash
echo "source ~/Cleanerbot/install/setup.bash" >> ~/.bashrc
```

---

# How Cleanerbot Works

## 1. Robot Description

The robot is described using a URDF/Xacro model.

The model defines:

- Links
- Joints
- Joint limits
- Collision geometry
- Visual geometry
- Masses
- Inertial properties

Robot kinematic chain:

```text
base_link
    │
joint_base
    │
 link_1
    │
 joint_1
    │
 link_2
    │
 joint_2
    │
 link_3
    │
 joint_3
    │
 link_4
    │
 joint_4
    │
 link_5
```

---

## 2. Robot State Publisher

`robot_state_publisher` reads the robot model and current joint positions and publishes TF transforms used by RViz.

```text
URDF
  +
Joint States
  │
  ▼
robot_state_publisher
  │
  ▼
TF Transforms
  │
  ▼
RViz
```

---

## 3. Joint States

ROS uses the `/joint_states` topic to store current robot positions.

Example:

```text
joint_base = -1.2 rad
joint_1    =  0.8 rad
joint_2    =  1.0 rad
joint_3    =  0.3 rad
joint_4    = -0.2 rad
```

---

## 4. MoveIt 2

MoveIt handles:

- Inverse kinematics
- Motion planning
- Collision checking
- Trajectory generation

```text
Target Pose
      │
      ▼
Inverse Kinematics
      │
      ▼
Joint Angles
      │
      ▼
Trajectory Planning
      │
      ▼
Motion Execution
```

---

## 5. RViz

RViz provides a graphical interface for:

- Viewing the robot
- Planning trajectories
- Visualising collisions
- Manipulating end-effector targets

Interactive markers can be moved to generate robot motions.

---

## 6. Serial Communication

The physical robot receives commands through a Python serial bridge.

Process:

```text
ROS Joint States
       │
       ▼
Python Node
       │
       ▼
Radians → Degrees
       │
       ▼
Serial Message
       │
       ▼
ESP32
```

---

## 7. ESP32 Controller

The ESP32:

1. Receives serial data
2. Parses joint angles
3. Converts angles into servo commands
4. Moves the physical arm

```text
ROS
 │
 ▼
Serial Bridge
 │
 ▼
ESP32
 │
 ├── Servo 1
 ├── Servo 2
 ├── Servo 3
 ├── Servo 4
 └── Servo 5
```

---

# Coordinate Units

ROS uses SI units:

| Quantity | Unit |
|-----------|-----------|
| Distance | metres |
| Rotation | radians |
| Mass | kilograms |
| Time | seconds |

Servo controllers typically use degrees.

Conversion:

```text
degrees = radians × 180 / π
```

---

# Development Workflow

Rebuild after making changes:

```bash
cd ~/Cleanerbot
colcon build
source install/setup.bash
```

For faster Python development:

```bash
colcon build --symlink-install
```

---

# Useful Commands

List nodes:

```bash
ros2 node list
```

List topics:

```bash
ros2 topic list
```

View joint states:

```bash
ros2 topic echo /joint_states
```

View topic information:

```bash
ros2 topic info /joint_states
```

Generate TF tree:

```bash
ros2 run tf2_tools view_frames
```

Validate URDF:

```bash
check_urdf robot.urdf
```

---

# Troubleshooting

## Package Not Found

```bash
source /opt/ros/humble/setup.bash
source install/setup.bash
```

## Missing Dependencies

```bash
rosdep install --from-paths src --ignore-src -r -y
colcon build
```

## Joint States Missing

```bash
ros2 topic list
```

Ensure a joint state publisher or controller is running.

## Serial Port Issues

Find connected device:

```bash
ls /dev/ttyUSB*
```

or

```bash
ls /dev/ttyACM*
```

Add serial permissions:

```bash
sudo usermod -a -G dialout $USER
```

Log out and back in afterwards.

---

# Future Improvements

Potential future developments include:

- Computer vision
- Automatic toilet detection
- Surface recognition
- Camera-based localisation
- Force sensing
- Automated cleaning trajectories
- Improved simulation
- Autonomous cleaning routines

---

# Technologies Used

- ROS 2 Humble
- MoveIt 2
- RViz 2
- Gazebo
- ROS 2 Control
- URDF
- Xacro
- Python
- C++
- ESP32
- Serial Communication
- Robotic Kinematics
- Motion Planning

---

# Project Purpose

Cleanerbot was developed to investigate the integration of:

- Robotics
- Embedded Systems
- Kinematics
- Motion Planning
- Simulation
- Software Development
- Hardware Control
- Autonomous Systems

The project demonstrates how industrial robotic-arm software architectures can be adapted to a household robotic cleaning application.

---

# Author

Developed as a university engineering capstone project.

GitHub:

https://github.com/Smleeep/Cleanerbot
