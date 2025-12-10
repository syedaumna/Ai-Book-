# Quickstart Guide for The Digital Twin Feature

This guide provides a quick setup for a basic Gazebo simulation integrated with ROS 2, allowing you to run your first digital twin experiment.

## 1. Gazebo & `gazebo_ros` Installation

It is assumed that you have a ROS 2 Humble or Iron environment set up on Ubuntu 22.04 LTS.

### 1.1 Install Gazebo

Gazebo Garden (or Fortress if you prefer) is recommended for ROS 2. Follow the official instructions:

```bash
# Add Gazebo repository
sudo sh -c 'echo "deb http://packages.osrfoundation.org/gazebo/ubuntu-stable `lsb_release -cs` main" > /etc/apt/sources.list.d/gazebo-stable.list'
wget http://packages.osrfoundation.org/gazebo.key -O - | sudo apt-key add -

# Update and install Gazebo Garden
sudo apt update
sudo apt install gazebo-garden
```

Verify installation: `gazebo --version`

### 1.2 Install `gazebo_ros` Bridge

The `gazebo_ros` package provides the necessary bridge to integrate Gazebo with ROS 2.

```bash
sudo apt install ros-<ros2-distro>-gazebo-ros # Replace <ros2-distro> with humble or iron
```

## 2. Create a Simple Gazebo World

Let's create a minimal world with just a floor. Save this as `my_first_world.world` in a new package (e.g., `~/ros2_ws/src/my_gazebo_pkg/worlds/`).

```xml
<?xml version="1.0" ?>
<sdf version="1.6">
  <world name="default">
    <include>
      <uri>model://sun</uri>
    </include>
    <include>
      <uri>model://ground_plane</uri>
    </include>
  </world>
</sdf>
```

## 3. Launch Gazebo with a Basic Robot

For this quickstart, we'll use a simple robot model (e.g., `box_bot`) and launch Gazebo.

### 3.1 Create a Robot Description Package

Create a ROS 2 package for your robot description (e.g., `my_robot_description`).

```bash
cd ~/ros2_ws/src
ros2 pkg create --build-type ament_python my_robot_description
```

### 3.2 Add a Simple URDF

Inside `~/ros2_ws/src/my_robot_description/urdf/`, create `simple_box.urdf`:

```xml
<?xml version="1.0"?>
<robot name="simple_box_robot">
  <link name="base_link">
    <visual>
      <geometry>
        <box size="0.1 0.1 0.1"/>
      </geometry>
    </visual>
    <collision>
      <geometry>
        <box size="0.1 0.1 0.1"/>
      </geometry>
    </collision>
    <inertial>
      <origin xyz="0 0 0" rpy="0 0 0"/>
      <mass value="0.1"/>
      <inertia ixx="0.0001" ixy="0" ixz="0" iyy="0.0001" iyz="0" izz="0.0001"/>
    </inertial>
  </link>
</robot>
```

### 3.3 Create a Launch File

Create `launch_sim.launch.py` inside `~/ros2_ws/src/my_robot_description/launch/`:

```python
import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

def generate_launch_description():
    pkg_gazebo_ros = get_package_share_directory('gazebo_ros')
    pkg_my_robot_description = get_package_share_directory('my_robot_description')

    # Start Gazebo server and client
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_gazebo_ros, 'launch', 'gazebo.launch.py')
        ),
        launch_arguments={'world': os.path.join(pkg_my_gazebo_pkg, 'worlds', 'my_first_world.world')}.items(),
    )

    # Spawn robot entity
    spawn_entity = Node(package='gazebo_ros', executable='spawn_entity.py',
                        arguments=['-entity', 'simple_box_robot',
                                   '-topic', 'robot_description',
                                   '-x', '0.0', '-y', '0.0', '-z', '0.5'],
                        output='screen')

    # Publish robot description
    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description': open(os.path.join(pkg_my_robot_description, 'urdf', 'simple_box.urdf')).read()}],
        output='screen'
    )

    return LaunchDescription([
        gazebo,
        robot_state_publisher_node,
        spawn_entity,
    ])
```

**Note**: You will need to add `pkg_my_gazebo_pkg` (the name of your world package) to the imports and adjust the world path.

### 3.4 Build and Launch

```bash
cd ~/ros2_ws
colcon build --packages-select my_robot_description # Also build my_gazebo_pkg
source install/setup.bash
ros2 launch my_robot_description launch_sim.launch.py
```

Gazebo should start, and you should see a simple red box (your robot) floating above a ground plane.

## 4. Verify ROS 2 Connection

In a new terminal, source your ROS 2 environment and run:

```bash
ros2 topic list
```

You should see topics like `/clock`, `/joint_states`, `/robot_description`, `/tf`, `/tf_static`, and potentially others from Gazebo. This confirms that Gazebo is communicating with ROS 2.
