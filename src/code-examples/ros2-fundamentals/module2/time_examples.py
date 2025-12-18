import rclpy
from rclpy.node import Node
from rclpy.time import Time
from rclpy.duration import Duration
import time as py_time

class TimeManagementExamplesNode(Node):
    def __init__(self):
        super().__init__('time_management_examples_node')
        self.get_logger().info('TimeManagementExamplesNode started.')

        # 1. Getting current time (ROS time, or system time if use_sim_time is false)
        current_ros_time = self.get_clock().now()
        self.get_logger().info(f'Current ROS time: {current_ros_time.nanoseconds / 1e9:.3f} seconds')

        # 2. Getting system time (always wall clock)
        current_system_time = self.get_clock().get_clock_type().to_system_time(self.get_clock().now())
        self.get_logger().info(f'Current System time (wall clock): {current_system_time.nanoseconds / 1e9:.3f} seconds')

        # 3. Using rclpy.Rate for fixed-frequency looping
        self.timer_rate = self.create_timer(1.0 / 2.0, self.rate_callback) # 2 Hz
        self.rate_count = 0

        # 4. Measuring elapsed time with Duration
        self.start_time = self.get_clock().now()
        self.timer_measure = self.create_timer(3.0, self.measure_elapsed_time)

        # 5. One-shot timer demonstration
        self.create_timer(5.0, self.one_shot_timer_callback)

        self.get_logger().info("Note: For simulation time ('use_sim_time'), make sure to set the '/use_sim_time' parameter to true and have a simulation publishing to '/clock'.")
        self.get_logger().info("You can toggle '/use_sim_time' by: `ros2 param set /ros_control_node use_sim_time true`") # Example, replace node name if needed.

    def rate_callback(self):
        self.rate_count += 1
        self.get_logger().info(f'Rate callback executed. Count: {self.rate_count}. Current time: {self.get_clock().now().nanoseconds / 1e9:.3f}')

    def measure_elapsed_time(self):
        elapsed = self.get_clock().now() - self.start_time
        self.get_logger().info(f'Elapsed time since start: {elapsed.nanoseconds / 1e9:.3f} seconds')

    def one_shot_timer_callback(self):
        self.get_logger().info('One-shot timer fired after 5 seconds.')
        self.destroy_timer(self.get_timer_names()[0]) # Destroy this timer

def main(args=None):
    rclpy.init(args=args)
    node = TimeManagementExamplesNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
