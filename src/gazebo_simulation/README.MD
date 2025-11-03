colcon build
source install/setup.bash
ros2 launch gazebo_simulation gazebo_model.launch.py

ros2 launch moveit_setup_assistant setup_assistant.launch.py
