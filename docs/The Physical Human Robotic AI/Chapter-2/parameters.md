# Parameter Server: Configuration Management

In any complex robot system, there are numerous configuration values that need to be managed. These might include PID gains for motor controllers, camera exposure settings, navigation thresholds, or object detection confidence scores. **ROS 2 parameters** provide a robust, dynamic mechanism for storing and managing these configuration values, making your robot software more flexible and easier to tune without needing to recompile code.

## Why Parameter Servers? (Configuration without Recompilation)

Hardcoding configuration values directly into your source code has several drawbacks:

-   **Requires Recompilation**: Any change to a parameter necessitates modifying the code, recompiling, and redeploying the node, which is time-consuming.
-   **Lack of Flexibility**: It's difficult to experiment with different values or adapt the robot's behavior in different environments without code changes.
-   **Poor Debuggability**: Identifying the impact of a parameter change on system behavior can be challenging.

ROS 2 parameters solve this by providing a centralized, dynamic, and introspectable way to manage configuration. Parameters are associated with nodes, allowing each node to have its own set of configurable values.

## Global Parameters vs. Node-Specific Parameters

-   **Node-Specific Parameters**: The most common use case. Each node declares and manages its own parameters (e.g., a `camera_node` might have `exposure_time` and `gain` parameters). These parameters are scoped to the node that declares them.
-   **"Global" Parameters**: While ROS 2 doesn't have a strict "global parameter server" like ROS 1, parameters can be set for all nodes or a group of nodes via launch files, providing a similar effect for initial configuration. Parameters for a node are uniquely identified by `/node_name/parameter_name`.

## Parameter Types

ROS 2 parameters support several basic data types:

-   `int` (integer)
-   `double` (floating-point number)
-   `string` (text)
-   `bool` (boolean)
-   `byte_array` (list of bytes)
-   `bool_array` (list of booleans)
-   `int_array` (list of integers)
-   `double_array` (list of floating-point numbers)
-   `string_array` (list of strings)

## Setting Parameters: Launch Files, Command-Line, Code

Parameters can be set in several ways:

1.  **Launch Files**: The most common way to initialize parameters when launching a system. This allows for clear, reproducible configurations.
    ```python
    # Example in a Python launch file
    from launch import LaunchDescription
    from launch_ros.actions import Node

    def generate_launch_description():
        return LaunchDescription([
            Node(
                package='my_robot_package',
                executable='motor_controller',
                name='motor_controller',
                parameters=[
                    {'pid_gain_p': 0.5},
                    {'max_velocity': 1.2}
                ]
            ),
        ])
    ```
2.  **Command-Line**: For quick testing or overriding default values.
    ```bash
    ros2 run my_robot_package motor_controller --ros-args -p pid_gain_p:=0.7 -p max_velocity:=1.5
    ```
3.  **From Code**: Nodes can set their own parameters programmatically, typically as default values.

## Reading and Writing Parameters from Nodes

Nodes can declare, get, and set their own parameters using the `rclpy.node.Node` API.

```python
import rclpy
from rclpy.node import Node

class ParameterNode(Node):
    def __init__(self):
        super().__init__('parameter_node')

        # Declare a parameter with a default value
        self.declare_parameter('my_int_param', 10)
        self.declare_parameter('my_string_param', 'hello')
        self.declare_parameter('pid_gain_p', 0.5)

        # Get parameter values
        int_param = self.get_parameter('my_int_param').get_parameter_value().integer_value
        string_param = self.get_parameter('my_string_param').get_parameter_value().string_value
        pid_gain_p = self.get_parameter('pid_gain_p').get_parameter_value().double_value

        self.get_logger().info(f'my_int_param: {int_param}')
        self.get_logger().info(f'my_string_param: {string_param}')
        self.get_logger().info(f'pid_gain_p: {pid_gain_p}')

        # Set a parameter (this can be done dynamically)
        self.set_parameters([rclpy.Parameter('my_int_param', rclpy.Parameter.Type.INTEGER, 20)])
        self.get_logger().info(f'Updated my_int_param: {self.get_parameter("my_int_param").get_parameter_value().integer_value}')

def main(args=None):
    rclpy.init(args=args)
    parameter_node = ParameterNode()
    rclpy.spin(parameter_node)
    parameter_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## Dynamic Parameter Reconfiguration

One of the most powerful features of ROS 2 parameters is the ability to change them dynamically at runtime without restarting the node. This is achieved through the `ros2 param set` command-line tool or programmatically.

```bash
# In one terminal, run the parameter_node
ros2 run my_robot_package parameter_node

# In another terminal, change a parameter
ros2 param set /parameter_node my_int_param 30
```

To react to parameter changes within a node, you can register a callback function that is triggered whenever a parameter changes.

```python
import rclpy
from rclpy.node import Node
from rcl_interfaces.msg import SetParametersResult

class DynamicParameterNode(Node):
    def __init__(self):
        super().__init__('dynamic_parameter_node')
        self.declare_parameter('some_value', 100)
        self.add_on_set_parameters_callback(self.parameter_callback)

    def parameter_callback(self, params):
        for param in params:
            if param.name == 'some_value':
                self.get_logger().info(f'Parameter "some_value" changed to: {param.value}')
                # You can add validation logic here
                if param.value < 0:
                    self.get_logger().warn('Negative value for some_value not allowed!')
                    return SetParametersResult(successful=False)
        return SetParametersResult(successful=True)

def main(args=None):
    rclpy.init(args=args)
    dynamic_parameter_node = DynamicParameterNode()
    rclpy.spin(dynamic_parameter_node)
    dynamic_parameter_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## Parameter Validation and Constraints

You can implement custom validation logic within your parameter callback functions (as shown in `parameter_callback`) to ensure that parameters are set to valid values. This helps maintain the integrity and safety of your robot system.

## Use Case: Tuning PID Gains for Motor Controllers

A prime example for dynamic parameter reconfiguration is tuning PID (Proportional-Integral-Derivative) gains for motor controllers.

-   A `motor_controller` node uses PID gains (P, I, D) as parameters.
-   During development or operation, an engineer can dynamically adjust these gains using `ros2 param set` or a GUI tool.
-   The `motor_controller` node's parameter callback instantly updates the PID controller with the new gains.
-   This allows for real-time tuning and optimization of motor performance without interrupting the robot's operation or requiring code changes and recompilation.

This significantly speeds up the development and calibration process for robotic systems.
