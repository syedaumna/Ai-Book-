# Quickstart Guide for Implement ROS 2 Fundamentals Feature

This guide provides a quick setup for the ROS 2 environment and demonstrates a minimal "Hello World" ROS 2 node, which will serve as a foundation for the examples in this chapter.

## 1. ROS 2 Environment Setup

It is assumed that you are running a Linux-based operating system (preferably Ubuntu 22.04 LTS) suitable for ROS 2 Humble or Iron distribution.

### 1.1 Install ROS 2

Follow the official ROS 2 documentation for installing either **ROS 2 Humble Hawksbill** or **ROS 2 Iron Irwini**:

-   **ROS 2 Humble**: [https://docs.ros.org/en/humble/Installation/Ubuntu-Install-Debians.html](https://docs.ros.org/en/humble/Installation/Ubuntu-Install-Debians.html)
-   **ROS 2 Iron**: [https://docs.ros.org/en/iron/Installation/Ubuntu-Install-Debians.html](https://docs.ros.org/en/iron/Installation/Ubuntu-Install-Debians.html)

Make sure to install the "Desktop Install" which includes ROS, RViz, and other useful tools.

### 1.2 Source the ROS 2 Environment

After installation, you need to source the ROS 2 setup file in every new terminal you open to use ROS 2 commands:

```bash
source /opt/ros/humble/setup.bash # For Humble
# OR
source /opt/ros/iron/setup.bash   # For Iron
```

For convenience, you can add this line to your `~/.bashrc` file:

```bash
echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
source ~/.bashrc
```

## 2. Create Your First ROS 2 Package

All ROS 2 development is done within packages. Let's create a new package for our "Hello World" example.

```bash
# Navigate to your ROS 2 workspace (e.g., ~/ros2_ws/src)
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws/src

# Create a new Python package
ros2 pkg create --build-type ament_python my_ros2_package
```

## 3. Minimal "Hello World" ROS 2 Node (Python)

Inside your `my_ros2_package`, let's create a simple Python node that prints "Hello World".

### 3.1 Create the Python Script

Create a file named `minimal_publisher.py` inside `~/ros2_ws/src/my_ros2_package/my_ros2_package/` (note the nested directory with the same name as the package).

```python
# minimal_publisher.py
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
        msg.data = 'Hello World: %d' % self.i
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

### 3.2 Make the Script Executable

```bash
chmod +x ~/ros2_ws/src/my_ros2_package/my_ros2_package/minimal_publisher.py
```

### 3.3 Add Entry Point in `setup.py`

Edit `~/ros2_ws/src/my_ros2_package/setup.py` and add the following inside the `entry_points` dictionary:

```python
    entry_points={
        'console_scripts': [
            'minimal_publisher = my_ros2_package.minimal_publisher:main',
        ],
    },
```

### 3.4 Build Your Package

Navigate back to your workspace root and build:

```bash
cd ~/ros2_ws/
colcon build
```

### 3.5 Run Your Node

Source your workspace and run the node:

```bash
source install/setup.bash
ros2 run my_ros2_package minimal_publisher
```

You should see "Publishing: 'Hello World: X'" messages in your terminal.
