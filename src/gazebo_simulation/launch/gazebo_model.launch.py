import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

from launch_ros.actions import Node
import xacro

def generate_launch_description():
    robotXacroName='simple_robot'
    namePackage='gazebo_simulation'
    modelFileRelativePath='urdf/robot.xacro'
    worldFileRelativePath='worlds/empty_world.world'
    rvizConfigFileRelativePath='config/config.rviz'
    pathModelFile=os.path.join(get_package_share_directory(namePackage),modelFileRelativePath)
    pathWorldFile=os.path.join(get_package_share_directory(namePackage),worldFileRelativePath)
    pathRvizConfigFile=os.path.join(get_package_share_directory(namePackage),rvizConfigFileRelativePath)
    robotDescription = xacro.process_file(pathModelFile).toxml()

    gazebo_rosPackageLaunch=PythonLaunchDescriptionSource(
        os.path.join(get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py')
    )  
    gazeboLaunch=IncludeLaunchDescription(
        gazebo_rosPackageLaunch,
        launch_arguments={'world': pathWorldFile}.items(),
    )
    spawnModelNode=Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=['-entity', robotXacroName, '-topic', 'robot_description'],
        output='screen'
    )

    nodeRobotStatePublisher=Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': robotDescription, 'use_sim_time': True}]
    )

    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', pathRvizConfigFile],
        parameters=[{'use_sim_time': True}]
    )

    LaunchDescriptionObject=LaunchDescription()
    LaunchDescriptionObject.add_action(gazeboLaunch)
    LaunchDescriptionObject.add_action(spawnModelNode)
    LaunchDescriptionObject.add_action(nodeRobotStatePublisher)
    LaunchDescriptionObject.add_action(rviz_node)

    return LaunchDescriptionObject