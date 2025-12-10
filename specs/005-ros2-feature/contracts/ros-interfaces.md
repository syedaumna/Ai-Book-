# ROS 2 Interfaces (Contracts) for Implement ROS 2 Fundamentals Feature

This document defines the formal interfaces (contracts) for communication within the ROS 2 Fundamentals chapter's examples and labs. These interfaces are primarily composed of custom message, service, and action definitions, which establish the data structures and communication protocols between ROS 2 nodes.

## Custom Message Definitions

### `std_msgs/Header`

-   **Purpose**: Provides timestamp and coordinate frame information for messages.
-   **Fields**:
    -   `std_msgs/msg/Header header`: Standard header containing `stamp` (time) and `frame_id` (coordinate frame).

### Example: `HumanoidState.msg` (Conceptual, if custom messages were defined)

If a custom `HumanoidState` message were defined for a lab, its contract would be:

```
# HumanoidState.msg
std_msgs/Header header
string[] joint_names
float64[] joint_positions
float64[] joint_velocities
float64[] joint_efforts
geometry_msgs/Pose[] end_effector_poses
```

## Custom Service Definitions

### Example: `PlanTrajectory.srv` (Conceptual, if custom services were defined)

If a custom `PlanTrajectory` service were defined for a lab, its contract would be:

```
# PlanTrajectory.srv
geometry_msgs/Pose start_pose
geometry_msgs/Pose end_pose
---
trajectory_msgs/JointTrajectory trajectory
```

## Custom Action Definitions

### Example: `Navigate.action` (Conceptual, if custom actions were defined)

If a custom `Navigate` action were defined for a lab, its contract would be:

```
# Navigate.action
geometry_msgs/PoseStamped goal
---
# Result
bool success
---
# Feedback
geometry_msgs/PoseStamped current_pose
```

## Standard ROS 2 Message Types Used

The following standard ROS 2 message types are expected to be used throughout the chapter's examples and labs:

-   `std_msgs`: Basic data types (e.g., `String`, `Int32`, `Float64`, `Header`).
-   `geometry_msgs`: Geometric primitives (e.g., `Point`, `Pose`, `Quaternion`, `Twist`, `Transform`).
-   `sensor_msgs`: Sensor data types (e.g., `Image`, `LaserScan`, `PointCloud2`, `Imu`, `JointState`).
-   `trajectory_msgs`: Robot trajectory definitions (e.g., `JointTrajectory`).
