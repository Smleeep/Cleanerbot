import launch
import launch_ros
import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
import xacro  # Add this import

def generate_launch_description():
    # Get package paths
    pkg_path = FindPackageShare('gazebo_simulation').find('gazebo_simulation')
    urdf_xacro_path = os.path.join(pkg_path, 'urdf/robot.xacro')

    # Process Xacro file to URDF
    robot_desc = xacro.process_file(urdf_xacro_path).toxml()

    # Robot State Publisher Node
    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': robot_desc}]
    )

    # RViz Node
    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
    )

    return LaunchDescription([
        DeclareLaunchArgument('model', default_value=urdf_xacro_path, description='Path to robot Xacro'),
        robot_state_publisher_node,
        rviz_node,
    ])
