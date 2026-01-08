import rclpy
from rclpy.node import Node
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from code_examples.ros2_fundamentals.module1.lab.msg import MotorCommand # Custom MotorCommand message
from std_msgs.msg import Header

class CapstoneMotorController(Node):
    def __init__(self):
        super().__init__('capstone_motor_controller')
        self.trajectory_subscription = self.create_subscription(
            JointTrajectory,
            'robot_trajectory', # Topic where MotionPlanner might publish full trajectories
            self.trajectory_callback,
            10)
        self.trajectory_subscription # prevent unused variable warning

        self.motor_command_publisher = self.create_publisher(MotorCommand, 'motor_commands', 10)
        self.get_logger().info('CapstoneMotorController Node started.')

        self.current_trajectory = None
        self.trajectory_point_index = 0
        self.trajectory_timer = None

    def trajectory_callback(self, msg: JointTrajectory):
        self.get_logger().info(f'Received new trajectory with {len(msg.points)} points.')
        self.current_trajectory = msg
        self.trajectory_point_index = 0

        # Cancel any existing timer to start a new trajectory
        if self.trajectory_timer:
            self.trajectory_timer.cancel()
        
        # Start timer to execute trajectory points
        self.trajectory_timer = self.create_timer(0.1, self.execute_trajectory_point) # Execute every 100ms

    def execute_trajectory_point(self):
        if not self.current_trajectory or self.trajectory_point_index >= len(self.current_trajectory.points):
            self.get_logger().info('Trajectory execution complete.')
            if self.trajectory_timer:
                self.trajectory_timer.cancel()
            self.current_trajectory = None # Clear trajectory
            return

        point = self.current_trajectory.points[self.trajectory_point_index]
        
        # Publish motor commands for each joint in the current point
        for i, joint_name in enumerate(self.current_trajectory.joint_names):
            motor_cmd_msg = MotorCommand()
            motor_cmd_msg.header.stamp = self.get_clock().now().to_msg()
            motor_cmd_msg.joint_name = joint_name
            
            if i < len(point.positions):
                motor_cmd_msg.position = point.positions[i]
            if i < len(point.velocities):
                motor_cmd_msg.velocity = point.velocities[i]
            if i < len(point.efforts):
                motor_cmd_msg.effort = point.efforts[i]
            
            self.motor_command_publisher.publish(motor_cmd_msg)
            self.get_logger().debug(f'Published MotorCommand for {joint_name}: pos={motor_cmd_msg.position:.2f}, vel={motor_cmd_msg.velocity:.2f}')
        
        self.trajectory_point_index += 1


def main(args=None):
    rclpy.init(args=args)
    motor_controller = CapstoneMotorController()
    rclpy.spin(motor_controller)
    motor_controller.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
