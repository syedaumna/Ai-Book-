import rclpy
from rclpy.node import Node
from rcl_interfaces.msg import SetParametersResult

class ParameterExamplesNode(Node):
    def __init__(self):
        super().__init__('parameter_examples_node')

        self.get_logger().info('--- Parameter Declaration and Initial Get ---')
        # Declare parameters with default values
        self.declare_parameter('my_int_param', 10)
        self.declare_parameter('my_string_param', 'hello')
        self.declare_parameter('pid_gain_p', 0.5)
        self.declare_parameter('is_enabled', True)

        # Get initial parameter values
        initial_int = self.get_parameter('my_int_param').value
        initial_string = self.get_parameter('my_string_param').value
        initial_pid_gain = self.get_parameter('pid_gain_p').value
        initial_enabled = self.get_parameter('is_enabled').value

        self.get_logger().info(f'Initial my_int_param: {initial_int}')
        self.get_logger().info(f'Initial my_string_param: "{initial_string}"')
        self.get_logger().info(f'Initial pid_gain_p: {initial_pid_gain}')
        self.get_logger().info(f'Initial is_enabled: {initial_enabled}')

        self.get_logger().info('--- Setting Parameters Programmatically ---')
        # Set a parameter programmatically
        self.set_parameters([
            rclpy.Parameter('my_int_param', rclpy.Parameter.Type.INTEGER, 20),
            rclpy.Parameter('my_string_param', rclpy.Parameter.Type.STRING, 'world')
        ])
        updated_int = self.get_parameter('my_int_param').value
        updated_string = self.get_parameter('my_string_param').value
        self.get_logger().info(f'Updated my_int_param: {updated_int}')
        self.get_logger().info(f'Updated my_string_param: "{updated_string}"')

        self.get_logger().info('--- Dynamic Parameter Reconfiguration Setup ---')
        # Add a callback for dynamic parameter changes
        self.add_on_set_parameters_callback(self.dynamic_parameter_callback)
        self.get_logger().info('Dynamic parameter callback registered. Try changing parameters with `ros2 param set /parameter_examples_node <param_name> <value>`')

        # Example: Timer to periodically check a parameter, simulating active usage
        self.timer = self.create_timer(1.0, self.timer_callback)

    def dynamic_parameter_callback(self, params):
        """Callback for when parameters are set dynamically."""
        for param in params:
            self.get_logger().info(f'Received dynamic parameter change for: {param.name} to {param.value}')
            if param.name == 'pid_gain_p':
                if param.type_ == rclpy.Parameter.Type.DOUBLE and 0.0 <= param.value <= 1.0:
                    self.get_logger().info(f'PID gain P updated to: {param.value}')
                    # Here you would typically update the PID controller
                    return SetParametersResult(successful=True, reason='Valid PID gain P')
                else:
                    self.get_logger().warn(f'Invalid value for pid_gain_p: {param.value}. Must be between 0.0 and 1.0.')
                    return SetParametersResult(successful=False, reason='Invalid PID gain P value')
            # Handle other parameters
        return SetParametersResult(successful=True, reason='Parameters set')

    def timer_callback(self):
        # Example of continuously using a parameter
        is_enabled = self.get_parameter('is_enabled').value
        if is_enabled:
            self.get_logger().info(f'Node is currently enabled. Current my_int_param: {self.get_parameter("my_int_param").value}')
        else:
            self.get_logger().info('Node is currently disabled.')

def main(args=None):
    rclpy.init(args=args)
    node = ParameterExamplesNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
