# Quickstart Guide: Setting Up Your ROS 2 Development Environment

This guide provides essential steps for setting up a ROS 2 development environment and introduces you to creating and running your first ROS 2 nodes. This foundation is crucial for following the examples and labs throughout the "ROS 2 Fundamentals" chapter.

## 1. ROS 2 Environment Setup

This chapter assumes you are working within a **Linux-based operating system**, specifically **Ubuntu 22.04 LTS**, which is the recommended platform for ROS 2 Humble and Iron distributions.

### 1.1 Install ROS 2

If you haven't already, please follow the comprehensive installation instructions provided in the official ROS 2 documentation. It is generally recommended to install the "Desktop Install" which includes the core ROS 2 packages, RViz (for visualization), and other essential development tools.

-   **ROS 2 Humble Hawksbill (LTS)**: [https://docs.ros.org/en/humble/Installation/Ubuntu-Install-Debians.html](https://docs.ros.org/en/humble/Installation/Ubuntu-Install-Debians.html)
-   **ROS 2 Iron Irwini**: [https://docs.ros.org/en/iron/Installation/Ubuntu-Install-Debians.html](https://docs.ros.org/en/iron/Installation/Ubuntu-Install-Debians.html)

### 1.2 Source Your ROS 2 Environment

After installation, you **must** source the ROS 2 setup file in **every new terminal session** before you can use any ROS 2 commands.

```bash
source /opt/ros/humble/setup.bash # If you installed ROS 2 Humble
# OR
source /opt/ros/iron/setup.bash   # If you installed ROS 2 Iron
```

**Tip**: To avoid typing this command every time, you can add it to your `~/.bashrc` file:

```bash
echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc # For Humble
# OR
echo "source /opt/ros/iron/setup.bash" >> ~/.bashrc   # For Iron

source ~/.bashrc # Apply the changes
```

## 2. Create and Build Your First ROS 2 Package

All ROS 2 software components are organized into **packages**. A package is a directory that contains source code, message definitions, launch files, and other resources.

### 2.1 Create a ROS 2 Workspace

A **workspace** is a directory where you develop and build your ROS 2 packages.

```bash
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws/src
```

### 2.2 Create a New Python Package

We'll create a new Python package named `ros2_fundamentals_examples` to house the code examples for this chapter.

```bash
ros2 pkg create --build-type ament_python ros2_fundamentals_examples
```

### 2.3 Add a Minimal Python Node

Navigate into your new package and create a simple "Hello World" publisher node.
Create a file named `minimal_publisher.py` inside `~/ros2_ws/src/ros2_fundamentals_examples/ros2_fundamentals_examples/`.

```python
# ~/ros2_ws/src/ros2_fundamentals_examples/ros2_fundamentals_examples/minimal_publisher.py
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class MinimalPublisher(Node):
    def __init__(self):
        super().__init__('minimal_publisher')
        self.publisher_ = self.create_publisher(String, 'topic', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        msg = String()
        msg.data = 'Hello ROS 2 World: %d' % self.i
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: "%s"' % msg.data)
        self.i += 1

def main(args=None):
    rclpy.init(args=args)
    minimal_publisher = MinimalPublisher()
    rclpy.spin(minimal_publisher)
    minimal_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### 2.4 Make the Script Executable and Define Entry Point

First, make your Python script executable:

```bash
chmod +x ~/ros2_ws/src/ros2_fundamentals_examples/ros2_fundamentals_examples/minimal_publisher.py
```

Next, open the `~/ros2_ws/src/ros2_fundamentals_examples/setup.py` file and add the following entry point to the `entry_points` dictionary. This allows `ros2 run` to find and execute your node.

```python
    entry_points={
        'console_scripts': [
            'minimal_publisher = ros2_fundamentals_examples.minimal_publisher:main',
        ],
    },
```

### 2.5 Build Your ROS 2 Workspace

Navigate back to your workspace root and build your package using `colcon build`:

```bash
cd ~/ros2_ws/
colcon build --packages-select ros2_fundamentals_examples
```

### 2.6 Source and Run Your Node

After building, you must source your workspace's `install/setup.bash` file. This makes your newly built package visible to ROS 2.

```bash
source install/setup.bash # From ~/ros2_ws/
ros2 run ros2_fundamentals_examples minimal_publisher
```

You should now see your node publishing "Hello ROS 2 World" messages to the console. Congratulations, you've created and run your first ROS 2 node!