import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from example_interfaces.srv import AddTwoInts
import time

class DebuggingExamplesNode(Node):
    def __init__(self):
        super().__init__('debugging_examples_node')

        # Publisher for ros2 topic echo/hz/info example
        self.publisher_ = self.create_publisher(String, 'debug_topic', 10)
        self.timer_publish = self.create_timer(0.5, self.publish_message) # Publish at 2 Hz
        self.get_logger().info('Publishing to /debug_topic at 2 Hz.')

        # Service server for ros2 service call example
        self.srv = self.create_service(AddTwoInts, 'debug_service', self.debug_service_callback)
        self.get_logger().info('Providing /debug_service.')

        # Timer to demonstrate a long-running process (action example or just a delay)
        self.timer_long_process = self.create_timer(10.0, self.long_running_task) # Every 10 seconds
        self.get_logger().info('Long running task scheduled to run every 10 seconds.')

        # Parameter to demonstrate ros2 param get/set
        self.declare_parameter('debug_level', 'INFO')
        self.add_on_set_parameters_callback(self.param_callback)
        self.get_logger().info(f"Current debug_level parameter: {self.get_parameter('debug_level').value}")

    def publish_message(self):
        msg = String()
        msg.data = f'Hello from DebuggingExamplesNode at {self.get_clock().now().nanoseconds / 1e9:.2f}'
        self.publisher_.publish(msg)
        self.get_logger().debug(f'Published: "{msg.data}"') # Will only show if log level is DEBUG

    def debug_service_callback(self, request, response):
        self.get_logger().info(f'Received service request: a={request.a}, b={request.b}')
        response.sum = request.a + request.b
        self.get_logger().info(f'Sending service response: sum={response.sum}')
        return response

    def long_running_task(self):
        self.get_logger().warn('Starting a simulated long running task (e.g. computation or action)...')
        time.sleep(2) # Simulate work
        self.get_logger().warn('Simulated long running task finished.')

    def param_callback(self, params):
        for param in params:
            if param.name == 'debug_level':
                self.get_logger().info(f"debug_level changed to: {param.value}")
        return rclpy.ParameterSetResult(successful=True)


def main(args=None):
    rclpy.init(args=args)
    node = DebuggingExamplesNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
