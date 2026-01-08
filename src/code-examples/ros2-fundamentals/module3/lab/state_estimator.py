import rclpy
from rclpy.node import Node
from code_examples.ros2_fundamentals.module1.lab.msg import SensorData # Custom SensorData message
from nav_msgs.msg import Odometry
from geometry_msgs.msg import PoseWithCovariance, TwistWithCovariance, Pose, Twist
from tf2_ros import TransformBroadcaster
from geometry_msgs.msg import TransformStamped

class StateEstimator(Node):
    def __init__(self):
        super().__init__('state_estimator')
        self.sensor_subscription = self.create_subscription(
            SensorData,
            'sensor_data',
            self.sensor_data_callback,
            10)
        self.sensor_subscription # prevent unused variable warning

        self.odometry_publisher = self.create_publisher(Odometry, 'odometry/filtered', 10)
        self.tf_broadcaster = TransformBroadcaster(self)

        self.last_sensor_data_time = self.get_clock().now()
        self.current_x = 0.0
        self.current_y = 0.0
        self.current_theta = 0.0 # Orientation in radians

        self.get_logger().info('StateEstimator Node started.')

    def sensor_data_callback(self, msg: SensorData):
        current_time = self.get_clock().now()
        dt_ns = (current_time - self.last_sensor_data_time).nanoseconds
        dt = dt_ns / 1e9 # Convert to seconds
        self.last_sensor_data_time = current_time

        if dt == 0:
            return

        # --- Conceptual State Estimation Logic ---
        # For this lab, we'll do a very simplified integration of position/velocity from SensorData.
        # In a real estimator (e.g., Extended Kalman Filter), you'd integrate sensor readings
        # to update a more sophisticated state model.

        # Assume linear.x and angular.z from MotorCommand directly affect Odometry
        # Here we'll just integrate the conceptual velocity from SensorData
        
        # Simplified dead reckoning based on SensorData's position and velocity
        # This is not how a real odometer works but serves as a simple example
        self.current_x += msg.velocity[0] * dt # Assuming velocity[0] is forward velocity
        self.current_y += msg.velocity[1] * dt # Assuming velocity[1] is sideways velocity
        # For orientation, let's just make it randomly drift for demonstration
        self.current_theta += msg.velocity[2] * dt # Assuming velocity[2] is angular velocity around Z

        # Clamp theta to [-pi, pi]
        self.current_theta = (self.current_theta + np.pi) % (2 * np.pi) - np.pi

        # Create and publish Odometry message
        odom_msg = Odometry()
        odom_msg.header.stamp = current_time.to_msg()
        odom_msg.header.frame_id = 'odom' # The world frame for odometry
        odom_msg.child_frame_id = 'base_link' # The robot's base frame

        odom_msg.pose.pose.position.x = self.current_x
        odom_msg.pose.pose.position.y = self.current_y
        odom_msg.pose.pose.position.z = 0.0 # Assuming 2D ground robot
        
        # Convert yaw to quaternion
        q = self.euler_to_quaternion(0, 0, self.current_theta)
        odom_msg.pose.pose.orientation.x = q[0]
        odom_msg.pose.pose.orientation.y = q[1]
        odom_msg.pose.pose.orientation.z = q[2]
        odom_msg.pose.pose.orientation.w = q[3]

        # Simplified velocities from SensorData
        odom_msg.twist.twist.linear.x = msg.velocity[0]
        odom_msg.twist.twist.angular.z = msg.velocity[2]

        self.odometry_publisher.publish(odom_msg)
        self.get_logger().debug(f'Published Odometry: x={self.current_x:.2f}, y={self.current_y:.2f}, theta={self.current_theta:.2f}')

        # Also publish TF transform from odom to base_link
        self.publish_tf(odom_msg)

    def euler_to_quaternion(self, roll, pitch, yaw):
        # From en.wikipedia.org/wiki/Conversion_between_quaternions_and_Euler_angles
        qx = np.sin(roll/2) * np.cos(pitch/2) * np.cos(yaw/2) - np.cos(roll/2) * np.sin(pitch/2) * np.sin(yaw/2)
        qy = np.cos(roll/2) * np.sin(pitch/2) * np.cos(yaw/2) + np.sin(roll/2) * np.cos(pitch/2) * np.sin(yaw/2)
        qz = np.cos(roll/2) * np.cos(pitch/2) * np.sin(yaw/2) - np.sin(roll/2) * np.sin(pitch/2) * np.cos(yaw/2)
        qw = np.cos(roll/2) * np.cos(pitch/2) * np.cos(yaw/2) + np.sin(roll/2) * np.sin(pitch/2) * np.sin(yaw/2)
        return [qx, qy, qz, qw]

    def publish_tf(self, odom_msg: Odometry):
        t = TransformStamped()
        t.header.stamp = odom_msg.header.stamp
        t.header.frame_id = odom_msg.header.frame_id
        t.child_frame_id = odom_msg.child_frame_id
        t.transform.translation.x = odom_msg.pose.pose.position.x
        t.transform.translation.y = odom_msg.pose.pose.position.y
        t.transform.translation.z = odom_msg.pose.pose.position.z
        t.transform.rotation = odom_msg.pose.pose.orientation
        self.tf_broadcaster.sendTransform(t)


def main(args=None):
    rclpy.init(args=args)
    state_estimator = StateEstimator()
    rclpy.spin(state_estimator)
    state_estimator.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    import numpy as np # Import numpy for euler_to_quaternion

    main()
