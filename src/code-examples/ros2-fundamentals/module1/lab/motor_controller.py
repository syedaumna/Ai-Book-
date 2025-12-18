import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from geometry_msgs.msg import Pose, PoseStamped # For service request
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint # For service response
from code_examples.ros2_fundamentals.module1.lab.srv import PlanTrajectory # Custom service
from code_examples.ros2_fundamentals.module1.lab.msg import MotorCommand # Custom message

class MotorController(Node):
    def __init__(self):
        super().__init__('motor_controller')
        self.publisher_ = self.create_publisher(MotorCommand, 'motor_commands', 10)
        self.cli = self.create_client(PlanTrajectory, 'plan_trajectory')

        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('PlanTrajectory service not available, waiting again...')
        
        self.get_logger().info('MotorController Node started.')
        self.timer = self.create_timer(5.0, self.timer_callback) # Request a plan every 5 seconds
        self.current_trajectory = None
        self.trajectory_point_index = 0
        self.execution_timer = None

    def timer_callback(self):
        # Request a new plan periodically
        self.request_trajectory_plan()

    def request_trajectory_plan(self):
        req = PlanTrajectory.Request()
        # Dummy start and end poses
        req.start_pose = Pose()
        req.start_pose.position.x = 0.0
        req.start_pose.position.y = 0.0
        req.start_pose.position.z = 0.0
        
        req.end_pose = Pose()
        req.end_pose.position.x = 1.0
        req.end_pose.position.y = 1.0
        req.end_pose.position.z = 1.0

        self.get_logger().info('Requesting new trajectory plan...')
        self.future = self.cli.call_async(req)
        self.future.add_done_callback(self.response_callback)

    def response_callback(self, future):
        try:
            response = future.result()
            self.current_trajectory = response.trajectory
            self.trajectory_point_index = 0
            self.get_logger().info('Received new trajectory plan. Starting execution.')
            # Start executing the trajectory
            if self.execution_timer:
                self.execution_timer.cancel()
            self.execution_timer = self.create_timer(0.1, self.execute_trajectory) # Execute every 100ms
        except Exception as e:
            self.get_logger().error(f'Service call failed: {e}')

    def execute_trajectory(self):
        if not self.current_trajectory or self.trajectory_point_index >= len(self.current_trajectory.points):
            self.get_logger().info('Trajectory execution complete or no trajectory available.')
            if self.execution_timer:
                self.execution_timer.cancel()
            return

        point = self.current_trajectory.points[self.trajectory_point_index]
        
        for i, joint_name in enumerate(self.current_trajectory.joint_names):
            motor_cmd_msg = MotorCommand()
            motor_cmd_msg.header.stamp = self.get_clock().now().to_msg()
            motor_cmd_msg.joint_name = joint_name
            motor_cmd_msg.position = point.positions[i] if i < len(point.positions) else 0.0
            motor_cmd_msg.velocity = point.velocities[i] if i < len(point.velocities) else 0.0
            motor_cmd_msg.effort = point.efforts[i] if i < len(point.efforts) else 0.0
            
            self.publisher_.publish(motor_cmd_msg)
            self.get_logger().debug(f'Published MotorCommand for {joint_name}: pos={motor_cmd_msg.position:.2f}')
        
        self.trajectory_point_index += 1


def main(args=None):
    rclpy.init(args=args)
    motor_controller = MotorController()
    rclpy.spin(motor_controller)
    motor_controller.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
