# Nodes: The Building Blocks

In ROS 2, a **node** is the fundamental unit of computation. Conceptually, a node is an executable program that performs a specific task within the ROS 2 ecosystem. Think of it as a single-purpose process that communicates with other nodes to achieve a larger robotic application.

## What is a ROS 2 Node?

-   **Independent Process**: Each node typically runs as its own executable, allowing for modularity and fault isolation. If one node crashes, it ideally doesn't bring down the entire robot system.
-   **Single Responsibility Principle**: Good ROS 2 node design often adheres to the Single Responsibility Principle. A node should do one thing and do it well. For instance, you might have:
    -   A camera driver node that only publishes camera images.
    -   A perception node that only processes those images to detect objects.
    -   A navigation node that only plans paths.
-   **Communication**: Nodes communicate with each other using various ROS 2 communication mechanisms:
    -   **Topics**: For continuous, asynchronous data streams (publish-subscribe).
    -   **Services**: For synchronous request-response interactions.
    -   **Actions**: For long-running, goal-oriented tasks with feedback and preemption.
    -   **Parameters**: For configuration and dynamic tuning.

## Lifecycle of a Node

Modern ROS 2 nodes, particularly "managed nodes," can have a well-defined lifecycle to enable more robust and predictable system behavior. This is crucial for applications that require high reliability, such as industrial robots or autonomous vehicles, where controlled startup and shutdown sequences are vital.

A typical lifecycle for a managed node includes states like:

-   **Unconfigured**: The initial state.
-   **Inactive**: The node is configured but not actively running its main operations.
-   **Active**: The node is fully operational, publishing, subscribing, and performing its tasks.
-   **Finalized**: The node is shutting down.

Nodes transition between these states via specific commands (e.g., `configure`, `activate`, `deactivate`, `cleanup`). This allows for controlled bring-up and tear-down of complex robot systems.

## Node Executors

Nodes require an **executor** to spin them, which is the mechanism that allows callbacks (e.g., for incoming messages, service requests, timer events) to be triggered. ROS 2 provides different types of executors:

-   **SingleThreadedExecutor**: Processes all callbacks from all nodes it's responsible for in a single thread, sequentially. Simple but can be a bottleneck if one callback takes a long time.
-   **MultiThreadedExecutor**: Uses a pool of threads to process callbacks concurrently. This can improve throughput for systems with many independent callbacks, but introduces complexity related to concurrency and thread safety.

## Node Naming Conventions and Namespacing

-   **Unique Names**: Each active node in a ROS 2 graph should have a unique name (e.g., `/my_robot/camera_driver`, `/my_robot/object_detector`).
-   **Namespacing**: Nodes can be organized into namespaces (e.g., `/my_robot/`). This helps prevent name collisions in large, complex systems and provides a logical grouping of components. Namespaces are typically defined using a leading slash.

## Creating a Minimal ROS 2 Node in Python (rclpy)

Let's look at how to create a very basic ROS 2 node using `rclpy`, the Python client library for ROS 2. This node will simply print a message to the console periodically.

```python
import rclpy
from rclpy.node import Node

class MinimalPublisher(Node):
    def __init__(self):
        # Initialize the Node with a unique name
        super().__init__('minimal_publisher')
        # Create a timer that will call the timer_callback function every 0.5 seconds
        self.timer = self.create_timer(0.5, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        # Log a message to the console
        self.get_logger().info(f'Hello ROS 2: {self.i}')
        self.i += 1

def main(args=None):
    # Initialize the ROS 2 Python client library
    rclpy.init(args=args)
    
    # Create an instance of our MinimalPublisher node
    minimal_publisher = MinimalPublisher()
    
    # Spin the node, keeping it alive and processing callbacks
    rclpy.spin(minimal_publisher)
    
    # Destroy the node and shutdown rclpy once rclpy.spin() returns
    minimal_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

To run this node, you would typically save it as a Python file within a ROS 2 package, make it executable, and then run it using `ros2 run <package_name> minimal_publisher`. More details on creating packages and running nodes will be covered in later sections.

## Best Practices: Node Design, Error Handling, Shutdown Procedures

-   **Modularity**: Keep nodes focused on a single responsibility.
-   **Robustness**: Implement error handling for external dependencies (e.g., sensor failures, network issues) and unexpected input.
-   **Graceful Shutdown**: Ensure nodes can shut down cleanly, releasing resources and notifying other parts of the system if necessary. Use `rclpy.shutdown()` and `destroy_node()`.
-   **Configuration**: Prefer using ROS 2 parameters for configurable values rather than hardcoding them in the source code.
-   **Logging**: Utilize the ROS 2 logging system (`self.get_logger()`) for effective debugging and system monitoring.
