import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from nav_msgs.msg import Odometry
from code_examples.ros2_fundamentals.module1.lab.msg import SensorData, MotorCommand # Custom messages
from trajectory_msgs.msg import JointTrajectory # From Planner

class SystemMonitor(Node):
    def __init__(self):
        super().__init__('system_monitor')

        self.sensor_sub = self.create_subscription(SensorData, 'sensor_data', self.sensor_callback, 10)
        self.odometry_sub = self.create_subscription(Odometry, 'odometry/filtered', self.odometry_callback, 10)
        self.robot_commands_sub = self.create_subscription(String, 'robot_commands', self.robot_commands_callback, 10)
        self.motor_commands_sub = self.create_subscription(MotorCommand, 'motor_commands', self.motor_commands_callback, 10)
        self.trajectory_sub = self.create_subscription(JointTrajectory, 'robot_trajectory', self.trajectory_callback, 10)


        self.get_logger().info('SystemMonitor Node started. Subscribing to various topics.')

    def sensor_callback(self, msg: SensorData):
        self.get_logger().info(f'[Sensor] Temp: {msg.temperature:.2f}, Hum: {msg.humidity:.2f}, Pos: {msg.position[0]:.2f}')

    def odometry_callback(self, msg: Odometry):
        self.get_logger().info(f'[Odometry] x: {msg.pose.pose.position.x:.2f}, y: {msg.pose.pose.position.y:.2f}')

    def robot_commands_callback(self, msg: String):
        self.get_logger().info(f'[RobotCmd] Received: "{msg.data}"')

    def motor_commands_callback(self, msg: MotorCommand):
        self.get_logger().info(f'[MotorCmd] Joint: {msg.joint_name}, Pos: {msg.position:.2f}, Vel: {msg.velocity:.2f}')

    def trajectory_callback(self, msg: JointTrajectory):
        self.get_logger().info(f'[Trajectory] Received trajectory with {len(msg.points)} points. First point time: {msg.points[0].time_from_start.sec}s')


def main(args=None):
    rclpy.init(args=args)
    monitor = SystemMonitor()
    rclpy.spin(monitor)
    monitor.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
