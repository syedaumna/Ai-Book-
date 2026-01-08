import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    # Get the package share directory for your code examples
    code_examples_pkg_dir = get_package_share_directory('ros2_fundamentals_examples')

    # Define nodes for the integrated system
    task_dispatcher_node = Node(
        package='ros2_fundamentals_examples',
        executable='task_dispatcher',
        name='task_dispatcher',
        output='screen',
        emulate_tty=True,
    )

    motion_planner_node = Node(
        package='ros2_fundamentals_examples',
        executable='motion_planner',
        name='motion_planner',
        output='screen',
        emulate_tty=True,
    )

    state_estimator_node = Node(
        package='ros2_fundamentals_examples',
        executable='state_estimator',
        name='state_estimator',
        output='screen',
        emulate_tty=True,
    )

    motor_controller_node = Node(
        package='ros2_fundamentals_examples',
        executable='motor_controller',
        name='motor_controller',
        output='screen',
        emulate_tty=True,
    )

    monitor_node = Node(
        package='ros2_fundamentals_examples',
        executable='monitor',
        name='system_monitor',
        output='screen',
        emulate_tty=True,
    )

    # We also need the sensor_simulator from module1/lab to provide input
    sensor_simulator_node = Node(
        package='ros2_fundamentals_examples',
        executable='sensor_simulator',
        name='sensor_simulator',
        output='screen',
        emulate_tty=True,
    )

    return LaunchDescription([
        sensor_simulator_node, # Provides sensor_data topic
        motion_planner_node,   # Provides plan_trajectory service
        state_estimator_node,  # Subscribes to sensor_data, publishes odometry
        motor_controller_node, # Subscribes to trajectories, publishes motor_commands
        task_dispatcher_node,  # Calls plan_trajectory service, publishes robot_commands
        monitor_node,          # Subscribes to various topics for monitoring
    ])
