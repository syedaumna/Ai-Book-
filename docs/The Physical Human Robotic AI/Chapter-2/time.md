# Time in ROS 2: Clocks and Timing

Accurate time synchronization and management are critical in robotics. Sensor data needs to be correctly timestamped, control loops must run at precise frequencies, and events across a distributed system must be ordered consistently. ROS 2 provides robust mechanisms for managing time, including different clock sources and utility functions.

## System Time vs. Simulation Time

One of the most important distinctions in ROS 2 time management is between **system time** and **simulation time**.

-   **System Time (Wall Clock Time)**: This is the real-world time as reported by the operating system. It's used when running a physical robot or when working with real-time hardware.
-   **Simulation Time (ROS Time)**: This is a virtual clock used within simulation environments (like Gazebo or Isaac Sim). It allows simulations to be paused, run faster or slower than real-time, and replayed deterministically. When `use_sim_time` is enabled in ROS 2, all nodes subscribe to the `/clock` topic, which publishes the simulation time.

Mixing these two types of time incorrectly can lead to severe debugging headaches and unpredictable robot behavior.

## ROS 2 Clocks

ROS 2 provides an abstraction for different clock sources:

-   **`rclpy.clock.ClockType.ROS_TIME`**: This clock reads time from the `/clock` topic. It's the standard for simulated environments. If `/clock` is not published (or `use_sim_time` is false), it falls back to system time.
-   **`rclpy.clock.ClockType.SYSTEM_TIME`**: This clock always reports the system's wall clock time, ignoring `/clock`. Useful for nodes that must always operate on real time, regardless of simulation.
-   **`rclpy.clock.ClockType.STEADY_TIME`**: Provides a monotonically increasing system time that is not subject to system clock adjustments (like NTP updates). Useful for measuring durations reliably.

Nodes should generally use `ROS_TIME` so they can seamlessly switch between real and simulated environments.

## Using `ros_time` for Reproducible Experiments

When `use_sim_time` is enabled (typically in your launch file or by setting the `/use_sim_time` parameter to `true`), all ROS 2 nodes will automatically use the simulation time published on the `/clock` topic. This is vital for:

-   **Reproducibility**: Running the same simulation multiple times will yield identical results, regardless of how fast or slow your computer is.
-   **Debugging**: You can pause the simulation at a specific moment to inspect the robot's state and data.
-   **Offline Analysis**: Recorded `rosbag` files (which contain `/clock` topic data) can be replayed, allowing nodes to process the data as if they were running live in the simulation.

## Timing Utilities: `Rate`, `Sleep`

`rclpy` provides utilities to help nodes manage their timing and execution frequency.

-   **`self.create_timer(period, callback_function)`**: The most common way to schedule periodic tasks within a node. The timer automatically respects `ROS_TIME` if `use_sim_time` is active.
-   **`rclpy.Rate(frequency)`**: Helps maintain a desired loop frequency. It provides a `sleep()` method that will pause execution until the next desired cycle time, respecting `ROS_TIME`.
    ```python
    import rclpy
    from rclpy.node import Node
    import time

    class TimedNode(Node):
        def __init__(self):
            super().__init__('timed_node')
            self.rate = self.create_rate(1.0) # 1 Hz
            self.get_logger().info('TimedNode started.')

        def run(self):
            while rclpy.ok():
                self.get_logger().info('Running at 1 Hz.')
                self.rate.sleep()

    def main(args=None):
        rclpy.init(args=args)
        node = TimedNode()
        node.run()
        node.destroy_node()
        rclpy.shutdown()

    if __name__ == '__main__':
        main()
    ```
-   **`rclpy.spin_once(node)`**: Processes a single set of pending callbacks. Often used in custom loops with `rclpy.Rate`.
-   **`rclpy.spin(node)`**: Blocks until the node is shut down, continuously processing all pending callbacks.

## Measuring Execution Time: `get_clock().now()`

To accurately measure durations within a node, always use the node's clock:

```python
import rclpy
from rclpy.node import Node
import time

class TimeMeasurementNode(Node):
    def __init__(self):
        super().__init__('time_measurement_node')
        self.start_time = self.get_clock().now()
        self.timer = self.create_timer(1.0, self.measure_time_callback)

    def measure_time_callback(self):
        current_time = self.get_clock().now()
        elapsed_time = current_time - self.start_time
        self.get_logger().info(f'Elapsed time: {elapsed_time.nanoseconds / 1e9:.2f} seconds')

def main(args=None):
    rclpy.init(args=args)
    node = TimeMeasurementNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```
The `rclpy.duration.Duration` object provides convenient methods for working with time differences.

## Scheduling: Timers for Periodic Tasks

`self.create_timer()` is the preferred way to schedule periodic activities in a ROS 2 node. It automatically handles the complexity of `ROS_TIME` and integrates with the executor.

## Why Timing Matters for Robots

-   **Control Loop Frequency**: Robot control systems often require precise, high-frequency execution (e.g., 50 Hz, 100 Hz, 500 Hz). Missed deadlines can lead to unstable control, jerky movements, or even system failure.
-   **Sensor Fusion**: Combining data from multiple sensors requires accurate timestamps to correctly align measurements.
-   **Motion Planning**: Trajectories are often time-parameterized, requiring the robot to follow specific points at specific times.
-   **Sim-to-Real Transfer**: Ensuring that real-time constraints and timing characteristics are consistent between simulation and hardware is crucial for effective transfer.

## Use Case: Tuning Control Loop Frequency for Motor Commands

Imagine a node that sends motor commands based on sensor feedback. The frequency at which these commands are sent (the control loop frequency) directly impacts the robot's performance and stability.

-   A `motor_controller` node uses `self.create_timer(period, callback)` to ensure its control loop runs at a fixed `period`.
-   This `period` can be exposed as a ROS 2 parameter, allowing for dynamic tuning.
-   By monitoring the `/tf` (robot state) and `/joint_states` topics, a developer can observe the impact of different control frequencies on robot smoothness and responsiveness.
-   In a simulated environment, `use_sim_time` ensures that if the simulation slows down due to heavy computation, the control loop also effectively slows down in simulation time, preventing inconsistencies.

Proper time management ensures that your robot operates reliably and deterministically, whether in simulation or the real world.
