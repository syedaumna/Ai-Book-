import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from code_examples.ros2_fundamentals.module1.lab.srv import PlanTrajectory # Reusing PlanTrajectory service
from geometry_msgs.msg import Pose # For PlanTrajectory service request

class TaskDispatcher(Node):
    def __init__(self):
        super().__init__('task_dispatcher')
        self.command_publisher = self.create_publisher(String, 'robot_commands', 10)
        self.planner_client = self.create_client(PlanTrajectory, 'plan_trajectory')

        self.timer = self.create_timer(5.0, self.timer_callback) # Dispatch a task every 5 seconds
        self.task_count = 0
        self.get_logger().info('TaskDispatcher Node started.')

        while not self.planner_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('PlanTrajectory service not available, waiting for Planner...')

    def timer_callback(self):
        self.task_count += 1
        if self.task_count % 2 == 1:
            self.publish_command()
        else:
            self.request_plan()

    def publish_command(self):
        msg = String()
        msg.data = f'Execute Task {self.task_count}: Navigate to target area'
        self.command_publisher.publish(msg)
        self.get_logger().info(f'Published command: "{msg.data}"')

    def request_plan(self):
        req = PlanTrajectory.Request()
        req.start_pose = Pose()
        req.start_pose.position.x = 0.0
        req.start_pose.position.y = 0.0
        req.start_pose.position.z = 0.0

        req.end_pose = Pose()
        req.end_pose.position.x = float(self.task_count) * 0.5
        req.end_pose.position.y = float(self.task_count) * -0.5
        req.end_pose.position.z = 0.0

        self.get_logger().info(f'Requesting plan for task {self.task_count}...')
        self.future = self.planner_client.call_async(req)
        self.future.add_done_callback(self.plan_response_callback)

    def plan_response_callback(self, future):
        try:
            response = future.result()
            self.get_logger().info(f'Received plan for task {self.task_count}: {len(response.trajectory.points)} points.')
        except Exception as e:
            self.get_logger().error(f'PlanTrajectory service call failed: {e}')

def main(args=None):
    rclpy.init(args=args)
    task_dispatcher = TaskDispatcher()
    rclpy.spin(task_dispatcher)
    task_dispatcher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
