import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.conditions import IfCondition, UnlessCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, TextSubstitution
from launch_ros.actions import Node

def generate_launch_description():
    # 1. Declare Launch Arguments
    # Argument to switch between simulation and real robot (example)
    use_sim_time_arg = DeclareLaunchArgument(
        'use_sim_time',
        default_value='true',
        description='Use simulation (Gazebo) clock if true'
    )

    # Argument for a configurable parameter
    robot_name_arg = DeclareLaunchArgument(
        'robot_name',
        default_value='my_robot',
        description='Name of the robot'
    )

    # Argument to enable/disable a specific sensor
    enable_lidar_arg = DeclareLaunchArgument(
        'enable_lidar',
        default_value='true',
        description='Enable LiDAR sensor node'
    )

    # 2. Node with Parameter Passing and Remapping
    # This node will use the 'robot_name' argument as its namespace and pass a parameter
    example_node_with_params = Node(
        package='my_ros2_package', # Assuming your example nodes are in 'my_ros2_package'
        executable='minimal_publisher', # Reusing a minimal publisher example
        name='publisher_node',
        namespace=LaunchConfiguration('robot_name'), # Use robot_name as namespace
        output='screen',
        emulate_tty=True,
        parameters=[
            {'robot_id': LaunchConfiguration('robot_name')}, # Pass robot_name as a parameter
            {'update_frequency': 10.0}
        ],
        remappings=[
            ('/robot_name/topic', '/global_topic') # Remap its topic to a global one
        ]
    )

    # 3. Conditional Node Launching
    # Launch a simulated LiDAR driver if 'enable_lidar' is true and 'use_sim_time' is true
    simulated_lidar_node = Node(
        package='my_sim_sensors',
        executable='sim_lidar_driver',
        name='sim_lidar',
        output='screen',
        condition=IfCondition(
            LaunchConfiguration('enable_lidar') and LaunchConfiguration('use_sim_time')
        )
    )

    # Launch a real LiDAR driver if 'enable_lidar' is true and 'use_sim_time' is false
    real_lidar_node = Node(
        package='my_real_sensors',
        executable='real_lidar_driver',
        name='real_lidar',
        output='screen',
        condition=IfCondition(
            LaunchConfiguration('enable_lidar') and UnlessCondition(LaunchConfiguration('use_sim_time'))
        )
    )

    # 4. Including another Launch File
    # This could be a complex robot description launch file
    # For demonstration, let's assume 'robot_description.launch.py' exists in 'my_robot_description' package
    # robot_description_pkg_dir = get_package_share_directory('my_robot_description')
    # robot_description_launch = IncludeLaunchDescription(
    #     PythonLaunchDescriptionSource(
    #         os.path.join(robot_description_pkg_dir, 'launch', 'robot_description.launch.py')
    #     ),
    #     launch_arguments={'use_gazebo': LaunchConfiguration('use_sim_time')}.items()
    # )

    return LaunchDescription([
        use_sim_time_arg,
        robot_name_arg,
        enable_lidar_arg,
        example_node_with_params,
        simulated_lidar_node,
        real_lidar_node,
        # robot_description_launch, # Uncomment to include if you have it
    ])
