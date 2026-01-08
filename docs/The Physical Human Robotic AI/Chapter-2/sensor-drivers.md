# Sensor Drivers: Integrating Hardware

For a robot to perceive its environment and itself, it needs sensors. Integrating physical sensors with a ROS 2 system involves writing **sensor drivers**. A sensor driver is a software component that acts as an interface between the low-level hardware communication protocols of a sensor and the standardized ROS 2 message types and communication mechanisms.

## What is a ROS 2 Sensor Driver?

A ROS 2 sensor driver is typically a node (or a set of nodes) responsible for:

1.  **Communicating with the physical sensor hardware**: This often involves low-level interfaces like serial ports, USB, Ethernet, I2C, SPI, or manufacturer-specific SDKs.
2.  **Reading raw sensor data**: Acquiring data from the hardware in its native format.
3.  **Processing and formatting data**: Converting the raw data into standardized ROS 2 message types (e.g., `sensor_msgs/msg/Image`, `sensor_msgs/msg/PointCloud2`, `sensor_msgs/msg/Imu`). This may include calibration, filtering, or coordinate transformations.
4.  **Publishing data to ROS 2 topics**: Making the formatted sensor data available to other nodes in the ROS 2 graph.
5.  **Handling errors and disconnections**: Gracefully managing hardware communication failures, sensor malfunctions, or unexpected disconnections.

The core principle is to abstract away the sensor-specific details, providing a consistent ROS 2 interface for higher-level perception, planning, and control algorithms.

## Using Existing Drivers vs. Writing Custom Drivers

-   **Existing Drivers**: Whenever possible, it is highly recommended to use existing, well-maintained ROS 2 drivers for your sensors.
    -   **Advantages**: Saves development time, often more robust, supported by a community, may include features like calibration tools.
    -   **Where to Find**: ROS 2 repositories (e.g., `ros-humble-desktop` often includes common sensor drivers), manufacturer-provided ROS 2 packages, community repositories (GitHub).
-   **Writing Custom Drivers**: You might need to write a custom driver if:
    -   Your sensor is new or esoteric and no existing driver exists.
    -   You need specific performance optimizations not offered by existing drivers.
    -   You need to integrate non-standard functionality from the sensor.

## Wrapping Hardware Libraries in ROS Nodes

When writing a custom driver, a common pattern is to "wrap" an existing non-ROS hardware SDK or library within a ROS 2 node.

-   **Node Initialization**: The ROS 2 node initializes the sensor using the manufacturer's SDK.
-   **Data Acquisition Loop**: The node runs a continuous loop (often driven by a timer or a dedicated thread) to poll data from the sensor.
-   **ROS 2 Message Conversion**: Raw sensor data is converted into appropriate `sensor_msgs` types.
-   **Publishing**: The ROS 2 message is published to a designated topic.
-   **Parameter Management**: Sensor configuration parameters (e.g., exposure, gain, LiDAR resolution) are exposed as ROS 2 parameters.

## Example Driver Structure (Conceptual)

```python
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image, PointCloud2, Imu
from std_msgs.msg import Header

# Assume a non-ROS sensor SDK or hardware interface
# import MySensorHardwareSDK as SensorSDK

class CustomSensorDriver(Node):
    def __init__(self):
        super().__init__('custom_sensor_driver')
        self.declare_parameter('sensor_id', 'my_camera_01')
        self.sensor_id = self.get_parameter('sensor_id').value
        
        # Initialize hardware using external SDK
        # self.sensor = SensorSDK.initialize(self.sensor_id)
        # self.sensor.configure(resolution='640x480', framerate=30)
        
        # Create publishers for sensor data
        self.image_publisher = self.create_publisher(Image, 'image_raw', 10)
        self.imu_publisher = self.create_publisher(Imu, 'imu_data', 10)
        
        # Create a timer to read and publish data periodically
        self.timer = self.create_timer(1.0/30.0, self.read_and_publish_data) # 30 Hz
        self.get_logger().info(f'CustomSensorDriver ({self.sensor_id}) started.')

    def read_and_publish_data(self):
        # 1. Read raw data from hardware (conceptual)
        # raw_image_data = self.sensor.getImage()
        # raw_imu_data = self.sensor.getImuData()
        
        # 2. Convert to ROS 2 messages
        image_msg = Image()
        imu_msg = Imu()

        # Fill image_msg (conceptual)
        image_msg.header.stamp = self.get_clock().now().to_msg()
        image_msg.header.frame_id = f'{self.sensor_id}_link'
        image_msg.width = 640
        image_msg.height = 480
        # ... (fill other image fields like encoding, data)

        # Fill imu_msg (conceptual)
        imu_msg.header.stamp = self.get_clock().now().to_msg()
        imu_msg.header.frame_id = f'{self.sensor_id}_imu_link'
        # ... (fill orientation, angular_velocity, linear_acceleration)

        # 3. Publish messages
        self.image_publisher.publish(image_msg)
        self.imu_publisher.publish(imu_msg)
        
        self.get_logger().debug('Published sensor data.')

    def __del__(self):
        # Clean up hardware resources on shutdown
        # SensorSDK.shutdown(self.sensor)
        pass

def main(args=None):
    rclpy.init(args=args)
    driver = CustomSensorDriver()
    rclpy.spin(driver)
    driver.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## Common Drivers for This Course

For humanoid robotics, you'll frequently encounter drivers for:

-   **USB Cameras**: General-purpose webcams. Drivers like `usb_cam` or integrating with OpenCV often provide `sensor_msgs/Image` output.
-   **Depth Cameras**: Such as Intel RealSense or Azure Kinect. Drivers like `realsense2_camera` provide `Image` (RGB, depth) and `PointCloud2` data.
-   **LiDAR Sensors**: For 2D or 3D mapping and navigation. Drivers vary by manufacturer (e.g., `ldlidar_stl_ros2` for specific models).
-   **IMU Sensors**: For orientation and acceleration data. Often integrated directly or via manufacturer SDKs.

## Configuration: Intrinsics, Extrinsics, Calibration

Proper sensor integration often requires:

-   **Intrinsic Calibration**: For cameras, this involves finding parameters like focal length, principal point, and distortion coefficients. This is crucial for accurate 3D reconstruction.
-   **Extrinsic Calibration**: Determining the 6D pose (position and orientation) of a sensor relative to the robot's base frame or another sensor. This defines the sensor's `tf` frame.
-   **Time Synchronization**: Ensuring sensor timestamps are synchronized across the system for accurate data fusion.

These calibration parameters are typically loaded via ROS 2 parameters or YAML files and used within the driver or downstream processing nodes.
