import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, ExecuteProcess, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
import xacro

def generate_launch_description():
    robotXacroName = 'simple_robot'
    namePackage = 'gazebo_simulation'
    modelFileRelativePath = 'urdf/robot.xacro'
    worldFileRelativePath = 'worlds/empty_world.world'
    rvizConfigFileRelativePath = 'config/config.rviz'

    pathModelFile = os.path.join(get_package_share_directory(namePackage), modelFileRelativePath)
    pathWorldFile = os.path.join(get_package_share_directory(namePackage), worldFileRelativePath)
    pathRvizConfigFile = os.path.join(get_package_share_directory(namePackage), rvizConfigFileRelativePath)

    # Process URDF/XACRO
    robotDescription = xacro.process_file(pathModelFile).toxml()

    # Gazebo launch
    gazebo_rosPackageLaunch = PythonLaunchDescriptionSource(
        os.path.join(get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py')
    )
    gazeboLaunch = IncludeLaunchDescription(
        gazebo_rosPackageLaunch,
        launch_arguments={'world': pathWorldFile}.items(),
    )

    # Spawn robot in Gazebo
    spawnModelNode = TimerAction(
        period=2.0,  # wait for Gazebo to start
        actions=[Node(
            package='gazebo_ros',
            executable='spawn_entity.py',
            arguments=['-entity', robotXacroName, '-topic', 'robot_description'],
            output='screen'
        )]
    )

    # Robot state publisher
    nodeRobotStatePublisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': robotDescription, 'use_sim_time': True}]
    )

    # ros2_control_node (controller manager)
    ros2ControlNode = Node(
        package='controller_manager',
        executable='ros2_control_node',
        parameters=[{'robot_description': robotDescription},
                    os.path.join(get_package_share_directory(namePackage), 'config', 'ros2_controllers.yaml')],
        output='screen'
    )

    # Load controllers with delay to allow ros2_control_node to start
    jointStateBroadcasterNode = TimerAction(
        period=3.0,  # wait 3 seconds
        actions=[ExecuteProcess(
            cmd=['ros2', 'control', 'load_controller', '--set-state', 'active', 'joint_state_broadcaster'],
            output='screen'
        )]
    )

    jointTrajectoryControllerNode = TimerAction(
        period=5.0,  # wait 5 seconds
        actions=[ExecuteProcess(
            cmd=['ros2', 'control', 'load_controller', '--set-state', 'active', 'joint_trajectory_controller'],
            output='screen'
        )]
    )

    # Launch description
    ld = LaunchDescription()
    ld.add_action(gazeboLaunch)
    ld.add_action(ros2ControlNode)
    ld.add_action(spawnModelNode)
    ld.add_action(nodeRobotStatePublisher)
    ld.add_action(jointStateBroadcasterNode)
    ld.add_action(jointTrajectoryControllerNode)

    return ld
