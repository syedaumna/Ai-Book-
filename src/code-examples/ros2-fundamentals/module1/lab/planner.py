import rclpy
from rclpy.node import Node
from code_examples.ros2_fundamentals.module1.lab.srv import PlanTrajectory # Custom service
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from geometry_msgs.msg import Pose # Assuming start_pose and end_pose are geometry_msgs/Pose

class Planner(Node):
    def __init__(self):
        super().__init__('planner')
        self.srv = self.create_service(PlanTrajectory, 'plan_trajectory', self.plan_trajectory_callback)
        self.get_logger().info('Planner Node started, providing service /plan_trajectory.')

    def plan_trajectory_callback(self, request, response):
        self.get_logger().info(f'Received planning request from {request.start_pose} to {request.end_pose}')

        # --- Dummy Planning Logic ---
        # In a real scenario, this would involve complex algorithms (e.g., A*, RRT, sampling-based planners)
        # For this lab, we'll create a simple, straight-line trajectory.

        trajectory = JointTrajectory()
        trajectory.joint_names = ['joint1', 'joint2', 'joint3'] # Example joint names

        # Start point
        point1 = JointTrajectoryPoint()
        point1.positions = [0.0, 0.0, 0.0]
        point1.time_from_start = rclpy.duration.Duration(seconds=0.0).to_msg()
        trajectory.points.append(point1)

        # Mid point (e.g., based on simple interpolation)
        point2 = JointTrajectoryPoint()
        point2.positions = [0.1, 0.2, 0.3] # Example intermediate positions
        point2.time_from_start = rclpy.duration.Duration(seconds=1.0).to_msg()
        trajectory.points.append(point2)

        # End point (simplified, not directly using request.end_pose's values for joint positions)
        point3 = JointTrajectoryPoint()
        point3.positions = [0.2, 0.4, 0.6] # Example final positions
        point3.time_from_start = rclpy.duration.Duration(seconds=2.0).to_msg()
        trajectory.points.append(point3)
        # --- End Dummy Planning Logic ---

        response.trajectory = trajectory
        self.get_logger().info('Generated dummy trajectory and sending response.')
        return response

def main(args=None):
    rclpy.init(args=args)
    planner_node = Planner()
    rclpy.spin(planner_node)
    planner_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
