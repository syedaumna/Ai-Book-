import rclpy
from rclpy.node import Node
from code_examples.ros2_fundamentals.module1.lab.srv import PlanTrajectory # Reusing PlanTrajectory service
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from geometry_msgs.msg import Pose # Assuming start_pose and end_pose are geometry_msgs/Pose

class MotionPlanner(Node):
    def __init__(self):
        super().__init__('motion_planner')
        self.srv = self.create_service(PlanTrajectory, 'plan_trajectory', self.plan_trajectory_callback)
        self.get_logger().info('MotionPlanner Node started, providing service /plan_trajectory.')

    def plan_trajectory_callback(self, request, response):
        self.get_logger().info(f'Received planning request from {request.start_pose} to {request.end_pose}')

        # --- Advanced Dummy Planning Logic ---
        # This version will simulate a more complex trajectory, perhaps with more points
        # and a slightly more "realistic" interpolation.

        trajectory = JointTrajectory()
        # Assume 3 joints for a simplified humanoid arm
        trajectory.joint_names = ['shoulder_pan_joint', 'shoulder_lift_joint', 'elbow_joint'] 

        # Example: Simple interpolation from start to end (conceptual)
        num_points = 10
        for i in range(num_points):
            point = JointTrajectoryPoint()
            # Linear interpolation of joint positions (very simplified)
            t = i / float(num_points - 1) # Interpolation factor

            # For each joint, interpolate from 0.0 to some target value
            point.positions = [
                0.0 + t * 0.5,  # shoulder_pan moves from 0 to 0.5 rad
                0.0 + t * 0.8,  # shoulder_lift moves from 0 to 0.8 rad
                0.0 + t * 0.3   # elbow moves from 0 to 0.3 rad
            ]
            point.time_from_start = rclpy.duration.Duration(seconds=float(i * 0.2)).to_msg() # Each point 0.2s apart
            trajectory.points.append(point)
        
        response.trajectory = trajectory
        self.get_logger().info('Generated a more advanced dummy trajectory and sending response.')
        return response

def main(args=None):
    rclpy.init(args=args)
    motion_planner_node = MotionPlanner()
    rclpy.spin(motion_planner_node)
    motion_planner_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
