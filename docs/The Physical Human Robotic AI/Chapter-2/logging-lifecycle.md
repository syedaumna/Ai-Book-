# ROS 2 Logging and Node Lifecycle

Understanding how to effectively log messages and manage the operational states of your ROS 2 nodes is crucial for developing robust and maintainable robotic systems. **Logging** provides insights into a node's behavior and helps with debugging, while a well-defined **node lifecycle** allows for predictable and controlled startup, shutdown, and error recovery.

## Python Logging with `rclpy.logging`

ROS 2 integrates a sophisticated logging system, built on top of the standard Python `logging` module for `rclpy` (the Python client library). This system allows you to categorize messages by severity and direct them to various outputs (console, file, `rosout` topic).

### Log Levels

Log levels provide a way to filter messages based on their importance. Common levels, in increasing order of severity, include:

-   **`DEBUG`**: Detailed information, typically only of interest to developers diagnosing problems.
-   **`INFO`**: Confirmation that things are working as expected. This is the default log level.
-   **`WARN`**: An indication that something unexpected happened, or a problem might occur soon (e.g., 'disk space running low'). The software is still running.
-   **`ERROR`**: A more serious problem has occurred; the software has not been able to perform some function.
-   **`FATAL`**: A severe error that has caused the application to abort.

You can set the log level for a node or globally using ROS 2 parameters or command-line arguments.

### Using the Logger in a Node

Every `rclpy.node.Node` instance comes with its own logger.

```python
import rclpy
from rclpy.node import Node

class LoggingExampleNode(Node):
    def __init__(self):
        super().__init__('logging_example_node')
        self.timer = self.create_timer(1.0, self.timer_callback)
        self.count = 0
        self.get_logger().info('LoggingExampleNode started. Default log level is INFO.')

    def timer_callback(self):
        self.count += 1
        if self.count % 5 == 0:
            self.get_logger().warn(f'Count is {self.count}. This is a warning message!')
        elif self.count % 10 == 0:
            self.get_logger().error(f'Count is {self.count}. This is an error message!')
        else:
            self.get_logger().info(f'Count is {self.count}. This is an info message.')
        self.get_logger().debug(f'Detailed debug information for count {self.count}.') # Will not show by default

def main(args=None):
    rclpy.init(args=args)
    node = LoggingExampleNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

To see `DEBUG` messages, you would launch the node and then set its log level:

```bash
# In one terminal:
ros2 run my_package logging_example_node

# In another terminal:
ros2 param set /logging_example_node logger_level DEBUG
```

### `rosout` Topic

All log messages from ROS 2 nodes are published to the `/rosout` topic. This allows for centralized collection and analysis of logs, which is especially useful in multi-node systems. You can view these logs using `ros2 topic echo /rosout`.

## Node Lifecycle Management (Managed Nodes)

Traditional ROS nodes have an implicit lifecycle: they start, run, and then shut down. For critical applications, this "all or nothing" approach isn't always sufficient. **Managed nodes** in ROS 2 introduce a more explicit lifecycle, allowing nodes to transition through well-defined states. This enables predictable behavior, facilitates system bring-up and tear-down, and improves robustness.

### Lifecycle States

Managed nodes can be in one of several primary states:

-   **`Unconfigured`**: The initial state after being created. The node is not yet ready to perform its main functions.
-   **`Inactive`**: The node has been configured and is ready to be activated, but is not yet actively processing data or controlling hardware.
-   **`Active`**: The node is fully operational, performing its main functions (publishing, subscribing, processing data, controlling hardware).
-   **`Finalized`**: The node is shutting down.

### Lifecycle Transitions

Nodes move between these states via specific transition commands:

-   **`configure`**: From `Unconfigured` to `Inactive`. The node loads parameters, allocates resources (e.g., opens serial ports, connects to hardware), and gets ready.
-   **`activate`**: From `Inactive` to `Active`. The node starts its main operations (e.g., publishing data, enabling actuators).
-   **`deactivate`**: From `Active` to `Inactive`. The node stops its main operations but retains allocated resources.
-   **`cleanup`**: From `Inactive` to `Unconfigured`. The node releases resources.
-   **`shutdown`**: Terminates the node from any primary state to `Finalized`.

These transitions can be triggered programmatically or via `ros2 lifecycle` command-line tools.

### Example: Basic Managed Node Structure

Implementing a managed node requires inheriting from `LifecycleNode` and implementing callback functions for each state transition.

```python
import rclpy
from rclpy.lifecycle import LifecycleNode, State, TransitionCallbackReturn
from std_msgs.msg import String

class ManagedTalker(LifecycleNode):
    def __init__(self):
        super().__init__('managed_talker')
        self.publisher_ = None
        self.timer_ = None
        self.count = 0
        self.get_logger().info('Node created in unconfigured state.')

    def on_configure(self, state: State) -> TransitionCallbackReturn:
        self.get_logger().info('Transitioning to "configuring"')
        self.publisher_ = self.create_publisher(String, 'lifecycle_topic', 10)
        self.timer_ = self.create_timer(1.0, self.publish_message)
        self.get_logger().info('Publisher and timer created. Now in inactive state.')
        return TransitionCallbackReturn.SUCCESS

    def on_activate(self, state: State) -> TransitionCallbackReturn:
        self.get_logger().info('Transitioning to "activating"')
        # Start publishers and timers, enable hardware
        super().on_activate(state) # Required to activate components
        self.get_logger().info('Node activated. Now in active state.')
        return TransitionCallbackReturn.SUCCESS

    def on_deactivate(self, state: State) -> TransitionCallbackReturn:
        self.get_logger().info('Transitioning to "deactivating"')
        # Stop publishers and timers, disable hardware
        self.get_logger().info('Node deactivated. Now in inactive state.')
        return TransitionCallbackReturn.SUCCESS

    def on_cleanup(self, state: State) -> TransitionCallbackReturn:
        self.get_logger().info('Transitioning to "cleaning up"')
        # Destroy publishers, timers, and release resources
        self.destroy_publisher(self.publisher_)
        self.destroy_timer(self.timer_)
        self.get_logger().info('Resources cleaned up. Now in unconfigured state.')
        return TransitionCallbackReturn.SUCCESS

    def publish_message(self):
        msg = String()
        msg.data = f'Lifecycle Hello World: {self.count}'
        self.publisher_.publish(msg)
        self.get_logger().info(f'Published: "{msg.data}"')
        self.count += 1

def main(args=None):
    rclpy.init(args=args)
    managed_talker = ManagedTalker()
    rclpy.spin(managed_talker)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### Use Case: Graceful Startup/Shutdown for Humanoid Robots

For humanoid robots, managed nodes are incredibly valuable:

-   **Controlled Actuation**: Ensure motors are only enabled when all safety checks are passed (e.g., after `configure` and `activate`).
-   **Resource Management**: Allocate vision system buffers, network connections, or inverse kinematics solvers only when needed.
-   **Error Recovery**: If a sensor fails, the node can `deactivate` and `cleanup` its resources without crashing the entire system, allowing for a controlled restart.
-   **System Bring-up**: Orchestrate a complex robot startup sequence, ensuring dependencies are met at each stage.

## Error Handling and Exception Propagation

Within lifecycle callbacks, it's important to handle exceptions gracefully. If an error occurs during a transition (e.g., hardware initialization fails in `on_configure`), the callback should return `TransitionCallbackReturn.FAILURE`, signaling to the lifecycle manager that the transition was unsuccessful. This prevents the system from entering an inconsistent state.

By combining structured logging with explicit node lifecycle management, you can build ROS 2 systems that are not only functional but also robust, maintainable, and predictable in their behavior.
