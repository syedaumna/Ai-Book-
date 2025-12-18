# Launch Files: Orchestrating Multi-Node Systems

As ROS 2 applications grow in complexity, manually starting each node and setting its parameters becomes tedious, error-prone, and difficult to reproduce. **ROS 2 Launch Files** provide a declarative way to define and orchestrate the startup of multiple nodes, set their configurations, manage remapping, and even handle conditional logic. They are indispensable for managing complex robotic systems.

## Why Launch Files?

-   **Automation**: Start all necessary nodes with a single command.
-   **Reproducibility**: Ensure the system always starts in a consistent, defined state.
-   **Configuration Management**: Centralize parameter settings and topic remappings.
-   **Modularity**: Combine smaller, reusable launch files to build larger systems.
-   **Conditional Logic**: Adapt system startup based on arguments (e.g., simulation vs. real robot).
-   **Debugging**: Provide structured output and easy access to logs.

## Launch File Syntax (Python)

ROS 2 primarily uses Python-based launch files (though XML is still supported for compatibility). Python launch files offer much greater flexibility, allowing for programmatic generation of nodes, dynamic parameter setting, and complex conditional logic.

A basic Python launch file typically contains:

-   `LaunchDescription`: The root element that describes the system to be launched.
-   `Node`: Represents a single ROS 2 node to be started.
-   `IncludeLaunchDescription`: Allows embedding other launch files, promoting modularity.
-   `DeclareLaunchArgument`: Defines command-line arguments for the launch file.
-   `LaunchConfiguration`: Accesses the values of declared launch arguments.

```python
import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration

def generate_launch_description():
    # Declare a launch argument for verbosity
    verbose_arg = DeclareLaunchArgument(
        'verbose',
        default_value='false',
        description='Set to true to print verbose messages.'
    )

    # Example node 1: minimal_publisher
    minimal_publisher_node = Node(
        package='my_ros2_package', # Replace with your package name
        executable='minimal_publisher',
        name='my_publisher',
        output='screen',
        emulate_tty=True, # Essential for seeing logs in terminal
        parameters=[
            {'some_param': 'default_value'},
            {'another_param': 1.0}
        ],
        remappings=[
            ('/topic', '/custom_topic_name') # Remap /topic to /custom_topic_name
        ]
    )

    # Example node 2: minimal_subscriber
    minimal_subscriber_node = Node(
        package='my_ros2_package', # Replace with your package name
        executable='minimal_subscriber',
        name='my_subscriber',
        output='screen',
        emulate_tty=True, # Essential for seeing logs in terminal
    )

    # Example of including another launch file
    # This might include a robot description or a sensor driver setup
    # robot_description_launch = IncludeLaunchDescription(
    #     PythonLaunchDescriptionSource([
    #         os.path.join(get_package_share_directory('my_robot_description'), 'launch'),
    #         '/robot_description.launch.py'
    #     ])
    # )

    return LaunchDescription([
        verbose_arg, # Add the argument to the launch description
        minimal_publisher_node,
        minimal_subscriber_node,
        # robot_description_launch,
        # Add other nodes or actions here
    ])
```

## Node Declarations, Remapping, Parameter Passing

-   **Node Declaration**: The `Node` action specifies the package, executable, name, and various configurations for a single ROS 2 node.
    -   `package`: The name of the ROS 2 package containing the executable.
    -   `executable`: The name of the executable (as defined in `setup.py` for Python, or `CMakeLists.txt` for C++).
    -   `name`: The name given to this specific instance of the node (important for uniqueness and namespacing).
    -   `output='screen'`: Directs node logs to the console.
    -   `emulate_tty=True`: Crucial for ensuring that Python nodes correctly display their log messages to the terminal.
-   **Parameter Passing**: Use the `parameters` argument to pass a list of dictionaries (or YAML files) containing parameter key-value pairs. These values can then be retrieved by the node using `self.get_parameter()`.
-   **Remapping**: The `remappings` argument allows you to change the names of topics, services, or actions that a node uses without modifying its source code. This is very powerful for reusing nodes in different contexts.

## Conditional Logic

Python launch files can implement conditional logic using `IfCondition` and `UnlessCondition` actions. This allows parts of the system to be launched only if certain conditions are met (e.g., launching a simulated sensor only if a `use_sim_time` argument is true).

```python
from launch.conditions import IfCondition, UnlessCondition

# ... inside generate_launch_description()

use_sim_time_arg = DeclareLaunchArgument(
    'use_sim_time',
    default_value='true',
    description='Use simulation (Gazebo) clock if true'
)

# Launch a simulated sensor node only if use_sim_time is true
simulated_sensor_node = Node(
    package='my_sim_sensors',
    executable='sim_camera_driver',
    name='sim_camera',
    condition=IfCondition(LaunchConfiguration('use_sim_time'))
)

# Launch a real sensor node only if use_sim_time is false
real_sensor_node = Node(
    package='my_real_sensors',
    executable='real_camera_driver',
    name='real_camera',
    condition=UnlessCondition(LaunchConfiguration('use_sim_time'))
)

return LaunchDescription([
    use_sim_time_arg,
    simulated_sensor_node,
    real_sensor_node,
])
```

## Include Files for Modular System Design

The `IncludeLaunchDescription` action allows you to embed one launch file within another. This promotes modularity, allowing you to create small, reusable launch files for specific components (e.g., a launch file for a robot arm, another for a navigation stack) and combine them into a larger system launch file.

## Event Handlers

Launch files can also define event handlers (e.g., `OnProcessExit`, `OnShutdown`) to react to events during the system's runtime, allowing for more robust system management.

## Best Practices: Organizing Launch Files for Large Systems

-   **Modularize**: Break down complex systems into smaller, logical launch files.
-   **Namespaces**: Use namespaces to avoid name collisions, especially when including multiple instances of the same node or complex sub-systems.
-   **Arguments**: Use `DeclareLaunchArgument` for configurable parameters, making launch files flexible.
-   **Comments**: Document your launch files thoroughly.
-   **Testing**: Test individual launch files and then the combined system.

## Use Case: Launch Entire Humanoid Robot Stack

For a complex humanoid robot, a single top-level launch file might:

1.  Start the Gazebo or Isaac Sim simulation environment.
2.  Load the robot's URDF/SDF/USD description.
3.  Launch all sensor drivers (real or simulated).
4.  Launch the perception stack (e.g., object detection, SLAM).
5.  Launch the motion planning nodes.
6.  Launch the motor controllers.
7.  Start visualization tools like RViz.

All with a single `ros2 launch <package> <main_launch_file>` command, dramatically simplifying system bring-up.
