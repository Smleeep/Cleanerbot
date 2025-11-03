# from moveit_configs_utils import MoveItConfigsBuilder
# from moveit_configs_utils.launches import generate_demo_launch


# def generate_launch_description():
#     moveit_config = MoveItConfigsBuilder("simple_robot", package_name="toilet_moveit_config").to_moveit_configs()
#     return generate_demo_launch(moveit_config)

from moveit_configs_utils import MoveItConfigsBuilder
from moveit_configs_utils.launches import generate_demo_launch

from launch_ros.actions import Node
from launch import LaunchDescription
from launch.actions import TimerAction, OpaqueFunction
from launch.event_handlers import OnProcessStart
from launch.actions import RegisterEventHandler
from launch_ros.substitutions import FindPackageShare
from launch.substitutions import PathJoinSubstitution
from ament_index_python.packages import get_package_share_directory
import os
import subprocess

def generate_launch_description():
    # do NOT call generate_demo_launch(...) immediately
    # create an empty launch description and start controller_manager first
    ld = LaunchDescription()

    # path to ros2_controllers.yaml in your package
    ros2_control_config = PathJoinSubstitution(
        [FindPackageShare("toilet_moveit_config"), "config", "ros2_controllers.yaml"]
    )

    # build absolute path to ros2_controllers.yaml and verify it exists
    ros2_ctrl_yaml = os.path.join(
        get_package_share_directory("toilet_moveit_config"),
        "config",
        "ros2_controllers.yaml",
    )
    if not os.path.exists(ros2_ctrl_yaml):
        raise FileNotFoundError(f"ros2_controllers.yaml not found: {ros2_ctrl_yaml}")
    print("Using ros2_controllers.yaml:", ros2_ctrl_yaml)

    # controller_manager (ros2_control_node)
    controller_manager = Node(
        package="controller_manager",
        executable="ros2_control_node",
        name="controller_manager",
        parameters=[ros2_ctrl_yaml],     # absolute path to YAML
        output="screen",
    )

    ld.add_action(controller_manager)

    # Block until controllers are active, then start MoveIt
    def _wait_for_controllers_and_start_moveit(context):
        import subprocess, time
        desired = {"joint_state_broadcaster", "arm_controller"}
        deadline = time.time() + 15.0
        while time.time() < deadline:
            try:
                r = subprocess.run(
                    ["ros2", "control", "list_controllers", "--controller-manager", "/controller_manager"],
                    capture_output=True, text=True, timeout=5
                )
                out = r.stdout
            except Exception:
                out = ""
            active = set()
            for line in out.splitlines():
                # lines look like: name: <name>, state: <state>, type: ...
                if "name:" in line and "state:" in line:
                    parts = line.split(",")
                    name = parts[0].split("name:")[-1].strip()
                    state = ""
                    for p in parts:
                        if "state:" in p:
                            state = p.split("state:")[-1].strip()
                    if state == "active":
                        active.add(name)
            if desired.issubset(active):
                break
            time.sleep(0.5)
        else:
            # timeout
            print("Timed out waiting for controllers:", desired)
        # start MoveIt launch now
        moveit_config = MoveItConfigsBuilder("simple_robot", package_name="toilet_moveit_config").to_moveit_configs()
        moveit_launch = generate_demo_launch(moveit_config)
        return list(moveit_launch.entities)

    # Start the polling function once controller_manager process starts
    ld.add_action(
        RegisterEventHandler(
            OnProcessStart(
                target_action=controller_manager,
                on_start=[OpaqueFunction(function=_wait_for_controllers_and_start_moveit)],
            )
        )
    )

    return ld
