import rclpy
from rclpy.node import Node
from visualization_msgs.msg import Marker
from geometry_msgs.msg import Point
import random
import math

class VisualizationExamplesNode(Node):
    def __init__(self):
        super().__init__('visualization_examples_node')
        self.marker_publisher = self.create_publisher(Marker, 'visualization_marker', 10)
        self.timer = self.create_timer(1.0, self.timer_callback) # Publish every 1 second
        self.marker_id_counter = 0
        self.get_logger().info('VisualizationExamplesNode started.')

    def timer_callback(self):
        # Publish a sphere marker that moves in a circle
        self.publish_moving_sphere_marker()

        # Publish a static text marker
        if self.marker_id_counter == 0: # Publish text only once
            self.publish_static_text_marker()
        
        self.marker_id_counter += 1

    def publish_moving_sphere_marker(self):
        marker = Marker()
        marker.header.frame_id = "map" # Assuming a 'map' frame exists
        marker.header.stamp = self.get_clock().now().to_msg()
        
        marker.ns = "moving_sphere"
        marker.id = 0 # Use a fixed ID for the moving marker so it gets updated
        marker.type = Marker.SPHERE
        marker.action = Marker.ADD

        # Calculate position for circular motion
        radius = 2.0
        angle = self.get_clock().now().nanoseconds * 1e-9 * 0.5 # Rotate at 0.5 rad/s
        marker.pose.position.x = radius * math.cos(angle)
        marker.pose.position.y = radius * math.sin(angle)
        marker.pose.position.z = 0.5
        marker.pose.orientation.w = 1.0 # No rotation

        marker.scale.x = 0.3
        marker.scale.y = 0.3
        marker.scale.z = 0.3
        
        marker.color.a = 1.0 # Alpha
        marker.color.r = 1.0
        marker.color.g = 0.0
        marker.color.b = 0.0

        self.marker_publisher.publish(marker)
        self.get_logger().info(f'Published moving sphere marker at ({marker.pose.position.x:.2f}, {marker.pose.position.y:.2f})')

    def publish_static_text_marker(self):
        marker = Marker()
        marker.header.frame_id = "map"
        marker.header.stamp = self.get_clock().now().to_msg()

        marker.ns = "static_text"
        marker.id = 1 # Unique ID for the text marker
        marker.type = Marker.TEXT_VIEW_FACING
        marker.action = Marker.ADD

        marker.pose.position.x = 0.0
        marker.pose.position.y = 0.0
        marker.pose.position.z = 1.0
        marker.pose.orientation.w = 1.0

        marker.scale.z = 0.5 # Text height
        
        marker.color.a = 1.0
        marker.color.r = 0.0
        marker.color.g = 0.0
        marker.color.b = 1.0

        marker.text = "Hello RViz!"
        self.marker_publisher.publish(marker)
        self.get_logger().info('Published static text marker.')

def main(args=None):
    rclpy.init(args=args)
    node = VisualizationExamplesNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
