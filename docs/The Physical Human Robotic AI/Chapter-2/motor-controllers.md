# Motor Controllers: Actuating Robots

For a robot to move and interact with its environment, it needs **actuators**, primarily motors. **Motor controllers** are the crucial link between high-level commands from the robot's control system and the low-level electrical signals required to drive the motors. In the context of ROS 2, motor controllers are typically implemented as nodes that receive desired motion commands (e.g., joint positions, velocities, or torques) and translate them into physical actions.

## Typical Robot Motor Hardware

Robots employ various types of electric motors, each suited for different applications:

-   **DC Motors**: Simple, widely used for basic movement. Often paired with gearboxes for higher torque.
-   **Brushless DC (BLDC) Motors**: More efficient, longer lifespan, and provide better control than brushed DC motors. Commonly used in drones and high-performance robots.
-   **Stepper Motors**: Provide precise incremental motion, ideal for open-loop positioning applications (e.g., 3D printers, some robotic arms).
-   **Servo Motors**: Often DC or BLDC motors integrated with a gearbox, encoder, and control electronics to provide precise position control. Commonly found in smaller robotic arms and hobby robots.

## Motor Driver Boards: PWM Controllers, CAN Bus Interfaces

Motors are rarely connected directly to the robot's main computer. Instead, they interface through **motor driver boards** (also called motor controllers). These boards are responsible for:

-   **Power Management**: Providing the necessary voltage and current to the motors.
-   **Signal Conversion**: Translating high-level digital commands (e.g., PWM signals, serial commands) into analog power to drive the motors.
-   **Feedback Reading**: Reading data from encoders (for position/velocity feedback) or current sensors.

Common interfaces between the robot's computer and motor driver boards include:

-   **PWM (Pulse Width Modulation)**: Simple, widely used for speed control of DC motors.
-   **UART/Serial**: For communicating with smart servo motors or dedicated motor controller microcontrollers.
-   **CAN Bus (Controller Area Network)**: A robust, multi-master serial bus often used in industrial and automotive applications for connecting multiple motor controllers and other peripherals.
-   **Ethernet**: For high-performance, real-time control systems, especially with advanced industrial drives.

## ROS 2 Abstraction: `MotorCommand` Message

In ROS 2, a motor controller node typically subscribes to a topic publishing **`MotorCommand`** messages (or standard types like `geometry_msgs/msg/Twist` for mobile bases, `trajectory_msgs/msg/JointTrajectory` for arms). This abstraction allows the higher-level control logic to remain independent of the specific motor hardware.

A `MotorCommand` message (or similar) would specify:

-   **Target Joint/Motor**: Which motor or joint is being commanded.
-   **Command Type**: Position, velocity, or effort (torque).
-   **Value**: The desired position, velocity, or effort.

## Feedback Loops: Reading Encoder Values for Odometry

For closed-loop control, motor controllers must provide feedback on the motor's actual state. This usually comes from:

-   **Encoders**: Sensors attached to the motor shaft (or joint) that measure rotation, providing precise position and velocity feedback.
-   **Current/Torque Sensors**: Measure the current flowing to the motor or the torque being exerted.

This feedback is critical for:

-   **Odometry**: For mobile robots, integrating wheel encoder data over time provides an estimate of the robot's position and orientation (`nav_msgs/msg/Odometry`).
-   **Joint State Publishing**: For robotic arms, encoder data is used to publish `sensor_msgs/msg/JointState` messages, which report the current position, velocity, and effort of each joint.
-   **Closed-Loop Control**: Enabling PID controllers to minimize the error between desired and actual motor states.

## Safety Considerations

Motor control involves powerful electromechanical systems, so safety is paramount:

-   **Max Velocity Limits**: Prevent motors from spinning too fast, which can cause instability or damage.
-   **Torque Limits**: Restrict the force a motor can exert to prevent damage to the robot or injury to humans.
-   **Joint Position Limits**: Ensure joints do not move beyond their physical range of motion.
-   **Emergency Stop (E-Stop)**: A critical safety mechanism that immediately cuts power to all motors.
-   **Temperature Monitoring**: Prevent motors from overheating.
-   **Fault Detection**: Monitor for motor stalls, overcurrent, or other abnormal conditions.

## Example Controller Node Structure

A ROS 2 motor controller node (e.g., for a single joint) typically:

1.  **Subscribes** to a topic for `MotorCommand` messages (or `trajectory_msgs/msg/JointTrajectory` for a multi-joint controller).
2.  **Reads** the desired command (position, velocity, or effort).
3.  **Applies Safety Bounds**: Ensures the command is within safe operating limits.
4.  **Translates Command**: Converts the ROS 2 command into low-level signals for the specific motor driver.
5.  **Sends to Hardware**: Communicates with the motor driver board.
6.  **Reads Feedback**: Acquires encoder, current, or other feedback data from the motor driver.
7.  **Publishes Joint States**: Publishes `sensor_msgs/msg/JointState` messages reflecting the robot's current state.

```python
import rclpy
from rclpy.node import Node
from code_examples.ros2_fundamentals.module1.lab.msg import MotorCommand # Custom MotorCommand
from sensor_msgs.msg import JointState
from std_msgs.msg import Header
import time

# --- Conceptual Motor Hardware Interface ---
# In a real scenario, this would be an actual library for talking to motor drivers.
class DummyMotorHardware:
    def __init__(self, joint_name, initial_position=0.0):
        self.joint_name = joint_name
        self._position = initial_position
        self._velocity = 0.0
        self._effort = 0.0
        print(f"[{joint_name}] Dummy motor hardware initialized.")

    def set_target_velocity(self, velocity):
        self._velocity = velocity
        # Simulate movement
        self._position += self._velocity * 0.01 # Assume 100 Hz update
        self._effort = self._velocity * 0.5 # Dummy effort calculation

    def get_joint_state(self):
        return self._position, self._velocity, self._effort

# --- ROS 2 Motor Controller Node ---
class SimpleMotorController(Node):
    def __init__(self):
        super().__init__('simple_motor_controller')
        self.declare_parameter('joint_name', 'robot_joint_1')
        self.joint_name = self.get_parameter('joint_name').value
        self.declare_parameter('max_velocity', 2.0) # rad/s
        self.max_velocity = self.get_parameter('max_velocity').value

        self.motor_hardware = DummyMotorHardware(self.joint_name)

        # Subscriber for motor commands
        self.command_subscription = self.create_subscription(
            MotorCommand,
            'motor_commands',
            self.motor_command_callback,
            10
        )
        self.command_subscription # prevent unused variable warning

        # Publisher for joint states
        self.joint_state_publisher = self.create_publisher(JointState, 'joint_states', 10)
        self.joint_state_timer = self.create_timer(0.01, self.publish_joint_state) # 100 Hz

        self.get_logger().info(f'Motor controller for joint "{self.joint_name}" started.')

    def motor_command_callback(self, msg: MotorCommand):
        if msg.joint_name == self.joint_name:
            target_velocity = msg.velocity
            
            # Apply safety bounds
            if abs(target_velocity) > self.max_velocity:
                self.get_logger().warn(f"[{self.joint_name}] Requested velocity {target_velocity:.2f} exceeds max {self.max_velocity:.2f}. Clamping.")
                target_velocity = self.max_velocity if target_velocity > 0 else -self.max_velocity
            
            self.motor_hardware.set_target_velocity(target_velocity)
            self.get_logger().info(f"[{self.joint_name}] Received command: vel={target_velocity:.2f}")
        else:
            self.get_logger().debug(f"[{self.joint_name}] Ignoring command for {msg.joint_name}")

    def publish_joint_state(self):
        position, velocity, effort = self.motor_hardware.get_joint_state()
        joint_state_msg = JointState()
        joint_state_msg.header.stamp = self.get_clock().now().to_msg()
        joint_state_msg.name = [self.joint_name]
        joint_state_msg.position = [position]
        joint_state_msg.velocity = [velocity]
        joint_state_msg.effort = [effort]
        self.joint_state_publisher.publish(joint_state_msg)
        self.get_logger().debug(f"[{self.joint_name}] Published joint state: pos={position:.2f}")

def main(args=None):
    rclpy.init(args=args)
    controller = SimpleMotorController()
    rclpy.spin(controller)
    controller.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## Sim-to-Real: Consistency Across Environments

A crucial goal in robotics is to ensure that control algorithms developed in simulation behave similarly on the real robot. This is the **sim-to-real** problem. A well-designed motor controller can facilitate this by maintaining consistent interfaces:

-   **Same ROS 2 Topics**: The motor controller node subscribes to the same `MotorCommand` (or `Twist`/`JointTrajectory`) topics in both simulation and real-world.
-   **Abstraction Layer**: The low-level hardware communication logic is encapsulated within the driver, presenting a unified interface to the higher-level controllers.
-   **Gazebo Integration**: In Gazebo, a Gazebo plugin might directly integrate with the physics engine to apply joint forces/torques based on ROS 2 commands, mimicking the behavior of a physical motor controller.

By carefully designing and implementing motor controllers, you can bridge the gap between abstract motion commands and the physical actuation of your humanoid robot, enabling complex and dynamic behaviors.
