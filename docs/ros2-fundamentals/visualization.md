# Visualizing Robots and Sensor Data

Visualization is a critical aspect of robotics development. It allows developers to understand the robot's state, verify sensor readings, debug algorithms, and interpret complex data flows in an intuitive graphical interface. In the ROS 2 ecosystem, **RViz** is the primary 3D visualization tool, complemented by other tools like `rqt_plot` for 2D data.

## What is RViz?

**RViz (ROS Visualization)** is a powerful 3D visualization tool for ROS. It's not a simulator itself, but rather a tool that displays data from a running ROS system. RViz can visualize:

-   **Robot Models**: Displaying the robot's URDF model, showing its current joint positions.
-   **Sensor Data**: Point clouds from LiDAR/depth cameras, camera images, IMU data, range sensors.
-   **Maps**: Occupancy grids, point maps.
-   **Trajectories and Paths**: Planned robot movements.
-   **Transformations (TF Frames)**: Shows the hierarchical relationship of coordinate frames.
-   **Markers**: Arbitrary geometric shapes (spheres, arrows, lines) published by nodes to highlight important features or debugging information.

RViz operates by subscribing to ROS 2 topics. For example, to visualize a robot model, RViz subscribes to the `/joint_states` topic (published by the robot's joint state publisher) and the `/robot_description` topic (published by the robot state publisher).

## Loading and Displaying URDF Models

To display your robot in RViz:

1.  **Robot Description**: Your robot's URDF (or XACRO) model needs to be made available to RViz. This is typically done by launching a `robot_state_publisher` node that reads the URDF and publishes it to the `/robot_description` topic.
2.  **Joint States**: A `joint_state_publisher` (or a hardware interface) needs to publish the current angles of the robot's joints to the `/joint_states` topic.
3.  **RViz Display**: In RViz, you add a "RobotModel" display type and ensure it's subscribed to the correct topics.

## Viewing TF Frames and Coordinate Transformations

The `tf2` system is fundamental to ROS 2, managing the relationships between all coordinate frames in a robot system. RViz can visualize these frames:

-   Add a "TF" display type in RViz.
-   You can see axes representing each frame and lines connecting parent-child frames.
-   This helps verify that your sensor frames, robot base, and world frames are correctly defined and transformed.

## Subscribing to Sensor Data Streams

RViz can display data from various sensor topics:

-   **`PointCloud2` (LiDAR/Depth Sensors)**: Add a "PointCloud2" display type, subscribe to the LiDAR topic (e.g., `/lidar/points`). You can color points by intensity, height, or custom properties.
-   **`Image` (Camera)**: Add an "Image" display type, subscribe to camera topics (e.g., `/camera/image_raw`).
-   **`LaserScan` (2D LiDAR)**: Add a "LaserScan" display type.

RViz allows you to adjust parameters for each display (e.g., color, size, history) to optimize visualization.

## Markers: Visualizing Computed Results

ROS 2 provides a `visualization_msgs/msg/Marker` message type that allows any node to publish simple geometric primitives (spheres, cubes, arrows, lines, text) to RViz. This is incredibly useful for:

-   **Path/Trajectory Visualization**: Show planned paths for the robot.
-   **Object Detection Results**: Display bounding boxes around detected objects.
-   **Debug Information**: Indicate points of interest, force vectors, or text labels.

```python
import rclpy
from rclpy.node import Node
from visualization_msgs.msg import Marker
from geometry_msgs.msg import Point
import random

class MarkerPublisher(Node):
    def __init__(self):
        super().__init__('marker_publisher')
        self.publisher_ = self.create_publisher(Marker, 'visualization_marker', 10)
        self.timer = self.create_timer(1.0, self.timer_callback)
        self.marker_id = 0

    def timer_callback(self):
        marker = Marker()
        marker.header.frame_id = "base_link" # Make sure this frame exists in your TF tree
        marker.header.stamp = self.get_clock().now().to_msg()
        
        marker.ns = "my_markers"
        marker.id = self.marker_id
        marker.type = Marker.SPHERE
        marker.action = Marker.ADD

        marker.pose.position.x = random.uniform(-1.0, 1.0)
        marker.pose.position.y = random.uniform(-1.0, 1.0)
        marker.pose.position.z = random.uniform(0.1, 1.0)
        marker.pose.orientation.w = 1.0

        marker.scale.x = 0.1
        marker.scale.y = 0.1
        marker.scale.z = 0.1
        
        marker.color.a = 1.0 # Alpha
        marker.color.r = random.uniform(0.0, 1.0)
        marker.color.g = random.uniform(0.0, 1.0)
        marker.color.b = random.uniform(0.0, 1.0)

        self.publisher_.publish(marker)
        self.get_logger().info(f'Publishing marker {self.marker_id}')
        self.marker_id += 1

def main(args=None):
    rclpy.init(args=args)
    marker_publisher = MarkerPublisher()
    rclpy.spin(marker_publisher)
    marker_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## RViz Configuration Files (`.rviz`)

When you set up RViz with various display types, topics, and layout, you can save your configuration to an `.rviz` file. This allows you to quickly load the same visualization setup later, ensuring consistent debugging and demonstration environments. You can also pass an `.rviz` file to a launch file to start RViz with a predefined configuration.

## Interactive Controls

RViz can also be used interactively. For example, plugins allow you to:

-   **Move Robot Joints**: Manually manipulate a robot model to check kinematics.
-   **Click to Set Goals**: Publish navigation goals to a robot by clicking in the 3D view.

## Debugging: Checking if Sensors are Aligned Correctly

A common task in RViz is to verify sensor alignment (calibration). By displaying both the robot model and sensor data (e.g., a point cloud), you can visually confirm if:

-   The sensor data appears in the correct location relative to the robot.
-   The coordinate frames (TF) are correctly published.
-   The robot's self-perception aligns with its physical structure.

RViz is an indispensable tool for nearly every stage of ROS 2 robot development, turning abstract data into actionable visual insights.
