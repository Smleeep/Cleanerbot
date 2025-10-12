import os
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
from moveit_configs_utils import MoveItConfigsBuilder

def generate_launch_description():
    # Paths
    moveit_config = (
        MoveItConfigsBuilder("simple_robot", package_name="arm_moveit2")
        .robot_description(file_path="config/simple_robot.urdf.xacro")
        .robot_description_semantic(file_path="config/simple_robot.srdf")
        .trajectory_execution(file_path="config/moveit_controllers.yaml")
        .planning_pipelines(
            pipelines=["ompl", "chomp", "pilz_industrial_motion_planner"],
            default_planning_pipeline="ompl"
        )
        .to_moveit_configs()
    )

    gazebo_world_path = os.path.join(
        get_package_share_directory("gazebo_simulation"),
        "worlds",
        "empty_world.world"
    )

    # Launch Gazebo
    gazebo_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory("gazebo_ros"), "launch", "gazebo.launch.py")
        ),
        launch_arguments={"world": gazebo_world_path}.items(),
    )

    # ros2_control node
    ros2_control_node = Node(
        package="controller_manager",
        executable="ros2_control_node",
        parameters=[
            moveit_config.robot_description,
            os.path.join(get_package_share_directory("arm_moveit2"), "config", "ros2_controllers.yaml")
        ],
        output="screen",
    )

    # Spawners for joint_state_broadcaster and arm_controller
    joint_state_broadcaster_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_state_broadcaster", "--controller-manager", "/controller_manager"],
        output="screen",
    )
    
    arm_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["arm_controller", "--controller-manager", "/controller_manager"],
        output="screen",
    )

    # Robot State Publisher
    robot_state_publisher_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        output="screen",
        parameters=[moveit_config.robot_description],
    )

    # Spawn the robot in Gazebo (wait a few seconds for Gazebo to start)
    spawn_robot_node = Node(
        package="gazebo_ros",
        executable="spawn_entity.py",
        arguments=["-entity", "simple_robot", "-topic", "robot_description"],
        output="screen",
    )
    spawn_robot_delayed = TimerAction(
        period=3.0,  # wait 3 seconds to ensure Gazebo is ready
        actions=[spawn_robot_node]
    )

    # MoveIt move_group
    move_group_node = Node(
        package="moveit_ros_move_group",
        executable="move_group",
        output="screen",
        parameters=[moveit_config.to_dict()],
        arguments=["--ros-args", "--log-level", "info"],
    )

    # RViz
    rviz_config_file = os.path.join(
        get_package_share_directory("arm_moveit2"),
        "config",
        "moveit.rviz"
    )
    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        output="screen",
        arguments=["-d", rviz_config_file],
        parameters=[
            moveit_config.robot_description,
            moveit_config.robot_description_semantic,
            moveit_config.planning_pipelines,
            moveit_config.robot_description_kinematics,
        ],
    )

    return LaunchDescription([
        gazebo_launch,
        ros2_control_node,
        joint_state_broadcaster_spawner,
        arm_controller_spawner,
        robot_state_publisher_node,
        spawn_robot_delayed,
        move_group_node,
        rviz_node,
    ])
