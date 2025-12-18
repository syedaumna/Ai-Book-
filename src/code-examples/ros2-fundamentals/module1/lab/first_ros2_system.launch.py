import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    # Get the package share directory for your code examples
    # Assuming 'code_examples' is the name of the package
    code_examples_pkg_dir = get_package_share_directory('code_examples')

    # Define nodes
    sensor_simulator_node = Node(
        package='code_examples', # Assuming code_examples is the package where this node resides
        executable='sensor_simulator', # The entry point defined in setup.py
        name='sensor_simulator',
        output='screen',
        emulate_tty=True, # Required for logger to display output in terminal
    )

    planner_node = Node(
        package='code_examples', # Assuming code_examples is the package where this node resides
        executable='planner', # The entry point defined in setup.py
        name='planner',
        output='screen',
        emulate_tty=True, # Required for logger to display output in terminal
    )

    motor_controller_node = Node(
        package='code_examples', # Assuming code_examples is the package where this node resides
        executable='motor_controller', # The entry point defined in setup.py
        name='motor_controller',
        output='screen',
        emulate_tty=True, # Required for logger to display output in terminal
    )

    return LaunchDescription([
        sensor_simulator_node,
        planner_node,
        motor_controller_node,
    ])
