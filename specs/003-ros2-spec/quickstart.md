# Quickstart Guide for ROS 2 Fundamentals

This guide provides a quick overview of how to use the custom interfaces defined for the ROS 2 Fundamentals chapter.

## Using the `HumanoidState` Message

To publish the state of the humanoid robot, you can use the following Python code:

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import Header
from geometry_msgs.msg import Pose
from your_package.msg import HumanoidState

class StatePublisher(Node):
    def __init__(self):
        super().__init__('state_publisher')
        self.publisher_ = self.create_publisher(HumanoidState, 'humanoid_state', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)

    def timer_callback(self):
        msg = HumanoidState()
        msg.header = Header(stamp=self.get_clock().now().to_msg())
        msg.joint_names = ['joint1', 'joint2']
        msg.joint_positions = [1.0, 2.0]
        msg.joint_velocities = [0.1, 0.2]
        msg.joint_efforts = [10.0, 20.0]
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: "%s"' % msg)

def main(args=None):
    rclpy.init(args=args)
    state_publisher = StatePublisher()
    rclpy.spin(state_publisher)
    state_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## Using the `PlanTrajectory` Service

To call the `PlanTrajectory` service, you can use the following Python code:

```python
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Pose
from your_package.srv import PlanTrajectory

class TrajectoryClient(Node):
    def __init__(self):
        super().__init__('trajectory_client')
        self.cli = self.create_client(PlanTrajectory, 'plan_trajectory')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting again...')
        self.req = PlanTrajectory.Request()

    def send_request(self):
        self.req.start_pose = Pose()
        self.req.end_pose = Pose()
        self.future = self.cli.call_async(self.req)

def main(args=None):
    rclpy.init(args=args)
    trajectory_client = TrajectoryClient()
    trajectory_client.send_request()

    while rclpy.ok():
        rclpy.spin_once(trajectory_client)
        if trajectory_client.future.done():
            try:
                response = trajectory_client.future.result()
            except Exception as e:
                trajectory_client.get_logger().info(
                    'Service call failed %r' % (e,))
            else:
                trajectory_client.get_logger().info(
                    'Result of plan_trajectory: %s' % (response.trajectory,))
            break

    trajectory_client.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```