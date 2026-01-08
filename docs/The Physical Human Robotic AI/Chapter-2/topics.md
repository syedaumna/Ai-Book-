# Topics: Publish-Subscribe Communication

The **publish-subscribe (pub-sub)** communication pattern is the most common way for nodes to exchange asynchronous, streaming data in ROS 2. It's ideal for data that is continuously generated, such as sensor readings, robot odometry, or video streams.

## The Publish-Subscribe Pattern Explained

In the pub-sub model:

-   **Publishers**: Nodes that generate data send ("publish") messages to a designated **topic**. They don't know or care if any other node is listening.
-   **Subscribers**: Nodes that need specific data "subscribe" to a topic. They receive all messages published to that topic. They don't know or care who is publishing.
-   **Topic**: A named channel through which messages flow. The name of the topic acts as an identifier (e.g., `/camera/image_raw`, `/odom`, `/joint_states`).
-   **Message Type**: Each topic has a defined **message type**, which specifies the structure and data types of the information being exchanged. This ensures that all data sent and received on a topic is consistent.

This decoupled architecture allows for great flexibility and modularity. You can add or remove publishers and subscribers dynamically without reconfiguring the entire system.

## Topics as Named Data Streams

Think of topics as continuous streams of data. For a humanoid robot, typical topics might include:

-   `/camera/rgb`: Publishing RGB image frames from a camera.
-   `/lidar/scan`: Publishing 2D or 3D laser scan data from a LiDAR sensor.
-   `/joint_commands`: Subscribing to commands to control individual robot joints.
-   `/odom`: Publishing odometry data (robot's position and orientation over time).

## Message Types: Built-in vs. Custom

ROS 2 provides a rich set of **built-in message types** for common data structures:

-   `std_msgs`: Contains primitive data types like `String`, `Int32`, `Float64`, and the essential `Header` message (for timestamps and frame IDs).
-   `geometry_msgs`: Defines messages for common geometric primitives, such as `Point`, `Pose` (position + orientation), `Quaternion`, `Twist` (linear + angular velocity), and `Transform`.
-   `sensor_msgs`: Contains messages for various sensor data, like `Image`, `LaserScan`, `PointCloud2`, `Imu`, `JointState`.

For more complex or application-specific data, you can define **custom message types**. This allows you to create structured data that perfectly fits your robot's needs. We will cover custom message definitions in a later module.

## Quality of Service (QoS)

**Quality of Service (QoS)** settings in ROS 2 are powerful features inherited from DDS that allow you to fine-tune the communication behavior of publishers and subscribers. QoS policies define how messages are delivered, stored, and managed. Key QoS policies include:

-   **Reliability**:
    -   `best_effort`: Messages are sent as quickly as possible; some might be lost. Suitable for high-frequency, non-critical data (e.g., sensor streams where losing a few frames is acceptable).
    -   `reliable`: Ensures every message is received; retransmissions occur if needed. Suitable for critical data (e.g., control commands, important state information).
-   **Durability**:
    -   `volatile`: Only new subscribers receive messages published while they are active.
    -   `transient_local`: Publishers retain a history of messages and send them to new subscribers upon connection. Useful for sharing initial state.
-   **History**:
    -   `keep_last`: Only a certain number of the most recent messages are kept in the buffer.
    -   `keep_all`: All messages are kept (up to system resource limits).
-   **Depth**: The size of the message queue for `keep_last` history.

Choosing the right QoS profile is crucial for optimizing network usage and ensuring the appropriate level of data integrity for different types of communication.

## Topic Remapping and Composition

-   **Topic Remapping**: You can change the name of a topic that a node publishes to or subscribes from without modifying the node's source code. This is often done in launch files and is extremely useful for reusing nodes in different contexts (e.g., having two camera drivers, one publishing to `/camera1/image_raw` and another to `/camera2/image_raw`).
-   **Composition**: A technique where multiple nodes are run within a single process. This can reduce overhead, especially for high-frequency topics, by allowing direct memory access instead of inter-process communication.

## Latency Considerations: Best-Effort vs. Reliable

Understanding the trade-offs between `best_effort` and `reliable` QoS is important for performance:

-   **`best_effort`**: Lower latency, higher throughput potential, but no guarantee of delivery.
-   **`reliable`**: Higher latency (due to retransmissions), lower throughput, but guaranteed delivery.

For real-time control loops, low latency is often more critical than guaranteed delivery of every single data point, especially if subsequent data points will quickly override the lost one. For commands, reliability is often paramount.

## Use Case: Sensor Fusion

A classic use case for topics is **sensor fusion**. Imagine a robot trying to get a robust estimate of its environment using multiple sensors (e.g., a camera, a LiDAR, and an ultrasonic sensor).

-   Each sensor driver node publishes its readings to its own specific topic (e.g., `/camera/image`, `/lidar/points`, `/ultrasonic/range`).
-   A separate `sensor_fusion` node subscribes to all these topics.
-   When messages arrive on any of these topics, the `sensor_fusion` node processes them, combines the data, and publishes a more accurate or complete representation of the environment to another topic (e.g., `/fused_perception`).

This demonstrates the power of topics in building modular, distributed systems where data flows seamlessly between specialized components.
