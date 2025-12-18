# Message and Service Definitions

Effective communication is the cornerstone of any distributed robotic system, and in ROS 2, this communication is built upon precisely defined data structures known as **messages** and **services**. While ROS 2 provides a rich set of built-in types, the ability to create **custom message, service, and action definitions** is crucial for handling application-specific data.

## Built-in ROS Message Types

ROS 2 comes with a comprehensive collection of standard message types, categorized by their domain. These cover most common use cases in robotics:

-   **`std_msgs`**: Contains basic, primitive data types.
    -   `String`: Simple text.
    -   `Int32`, `Float64`, `Bool`: Numeric and boolean values.
    -   `Header`: Essential for timestamping and associating data with coordinate frames (`frame_id`).
-   **`geometry_msgs`**: Defines messages for common geometric primitives, essential for describing positions, orientations, and velocities.
    -   `Point`: A 3D point (`x`, `y`, `z`).
    -   `Quaternion`: Represents orientation using quaternions (`x`, `y`, `z`, `w`).
    -   `Pose`: Combines `Point` and `Quaternion` for position and orientation.
    -   `Twist`: Linear and angular velocity in 3D (`linear`, `angular`).
    -   `Transform`: A translation and rotation.
-   **`sensor_msgs`**: Contains messages for various sensor data.
    -   `Image`: Raw camera image data.
    -   `LaserScan`: 2D LiDAR scan data.
    -   `PointCloud2`: 3D point cloud data.
    -   `Imu`: Inertial Measurement Unit (accelerometer, gyroscope, magnetometer) data.
    -   `JointState`: Positions, velocities, and efforts of robot joints.
-   **`nav_msgs`**: Messages related to navigation.
    -   `Odometry`: Robot's position and velocity in a free-space frame.
    -   `Path`: A sequence of poses for a robot to follow.
-   **`trajectory_msgs`**: Messages for robot trajectories.
    -   `JointTrajectory`: A sequence of desired joint positions, velocities, and accelerations over time.

It's always recommended to use built-in message types when possible, as they ensure compatibility with other ROS 2 tools and packages.

## When to Create Custom Messages

You should create custom message types when:

-   None of the built-in message types adequately represent your data.
-   You need to combine multiple pieces of information into a single, cohesive structure.
-   Your data has a specific meaning within your application that warrants its own type.

For a humanoid robot, examples might include a message describing the state of its emotional display, or a service to initiate a complex multi-robot interaction.

## Custom Message, Service, and Action Syntax

Custom definitions are typically created in `.msg`, `.srv`, and `.action` files, respectively, within specific subdirectories (`msg/`, `srv/`, `action/`) of a ROS 2 package.

### Message (`.msg` files)

A `.msg` file is a plain text file that defines the fields and their types. Each field has a type (built-in or other custom messages) and a name.

```
# MyCustomMessage.msg
std_msgs/Header header
string name
float32 value
geometry_msgs/Point position
int32[] ids # Array of integers
```

### Service (`.srv` files)

A `.srv` file has two parts, separated by `---`: the request fields and the response fields.

```
# MyCustomService.srv
string request_message
float64 request_value
---
string response_message
bool success
```

### Action (`.action` files)

An `.action` file has three parts, separated by `---`: the goal, result, and feedback fields.

```
# MyCustomAction.action
# Goal
string target_pose_name
float32 speed_factor
---
# Result
bool success
string status_message
---
# Feedback
float32 percent_complete
string current_state
```

## Type Safety and Code Generation

One of the strengths of ROS 2 is its **type safety**. When you define custom messages, services, or actions, ROS 2's build system automatically generates source code (e.g., Python classes, C++ structs) for these types. This generated code ensures:

-   **Compile-time Checks**: For C++, errors are caught during compilation if you try to use an incorrect type.
-   **Runtime Type Checking**: For Python, the generated classes enforce the defined structure, catching type mismatches at runtime.
-   **Serialization/Deserialization**: Handles the conversion of your data to and from bytes for network transmission.

## Including Messages in Custom Packages

To make your custom messages available to other ROS 2 packages:

1.  **Place `.msg`/`.srv`/`.action` files**: In the `msg/`, `srv/`, or `action/` directories of your package.
2.  **Update `package.xml`**: Add `build_depend` and `exec_depend` tags for `rosidl_default_generators` and `rosidl_default_runtime`. Also, declare any custom message dependencies.
    ```xml
    <build_depend>rosidl_default_generators</build_depend>
    <exec_depend>rosidl_default_runtime</exec_depend>
    <member_of_group>rosidl_interface_packages</member_of_group>
    ```
3.  **Update `CMakeLists.txt`**: Use `rosidl_generate_interfaces()` to tell the build system to generate code for your custom types.
    ```cmake
    find_package(rosidl_default_generators REQUIRED)
    rosidl_generate_interfaces(${PROJECT_NAME}
      "msg/MyCustomMessage.msg"
      "srv/MyCustomService.srv"
      "action/MyCustomAction.action"
      DEPENDENCIES std_msgs geometry_msgs # Declare any internal/external message dependencies
    )
    ```

After rebuilding your package (`colcon build`), you can then import and use these types in your Python or C++ nodes:

```python
# In Python
from my_package.msg import MyCustomMessage
from my_package.srv import MyCustomService
from my_package.action import MyCustomAction
```

## Practical Examples for Humanoid Robotics

-   **`HumanoidState.msg`**: A message to encapsulate the entire state of a humanoid robot, including joint angles, velocities, efforts, end-effector poses, and potentially contact forces. This provides a single, comprehensive snapshot of the robot.
-   **`PlanTrajectory.srv`**: A service where a client requests a motion planner to compute a path from a start pose to an end pose. The request might include constraints, and the response would be a `trajectory_msgs/JointTrajectory`.
-   **`Navigate.action`**: An action where a client sends a goal to a navigation server (e.g., a target waypoint). The server provides feedback (e.g., current progress, remaining distance) and eventually a result (success/failure of navigation).

By thoughtfully designing your custom messages, services, and actions, you create clear, type-safe interfaces that facilitate robust communication and development within your ROS 2 robotic applications.
