# Simulation Interfaces (Contracts) for The Digital Twin

This document defines the formal interfaces and data structures used for communication and description within the digital twin environment, encompassing Gazebo's SDF, NVIDIA Isaac Sim's USD, and general ROS 2 interfaces for simulated sensors and control.

## 1. Simulation Description Formats Contracts

### 1.1 SDF (Simulation Description Format) Contract

SDF specifies the structure for defining entire simulation worlds, including static objects, robots, sensors, and environmental physics.

-   **World Definition (`.world` files)**:
    -   Contract for `<world>` element:
        -   `<name>`: Unique identifier for the world.
        -   `<gravity>`: `Vector3` representing gravitational force (e.g., `0 0 -9.8`).
        -   `<physics>`: Configuration for the physics engine.
            -   `<max_step_size>`: Simulation timestep.
            -   `<real_time_factor>`: Ratio of simulated time to real time.
            -   `<solver>`: Physics solver type (e.g., `ode`, `bullet`).
-   **Model Definition (`.sdf` files or within `.world`)**:
    -   Contract for `<model>` element:
        -   `<name>`: Unique identifier for the model.
        -   `<link>`: Defines a rigid body.
            -   `<inertial>`: Mass, inertia matrix (`ixx iyy izz ixy ixz iyz`).
            -   `<visual>`: Visual properties (geometry, material).
            -   `<collision>`: Collision properties (geometry, friction, restitution).
        -   `<joint>`: Defines a connection between two links.
            -   `<name>`, `<type>` (revolute, prismatic, fixed).
            -   `<parent>`, `<child>`.
            -   `<axis>`: Rotation/translation axis.
            -   `<limit>`: Joint limits (lower, upper, velocity, effort).
-   **Sensor Definition (within `<link>` or `<model>`)**:
    -   Contract for `<sensor>` element (e.g., `camera`, `gpu_lidar`, `imu`).
        -   `<name>`, `<type>`.
        -   `<camera>`: `<horizontal_fov>`, `<image>` (width, height, format), `<clip>` (near, far).
        -   `<ray>` (for LiDAR): `<scan>` (horizontal/vertical samples, resolution, min/max angle, range), `<noise>`.

### 1.2 USD (Universal Scene Description) Contract

USD provides a robust, hierarchical, and composable framework for defining 3D scenes in Isaac Sim.

-   **Stage (`.usd`, `.usdc`, `.usda` files)**:
    -   Contract for `defaultPrim`: Root primitive of the stage.
    -   Layering system for composition.
-   **Primitives (`Prim`)**:
    -   Contract for `Xform` (transformable object): position, orientation, scale.
    -   Contract for `Mesh`: geometry data (vertices, faces, UVs), material binding.
    -   Contract for `PhysicsScene`: global physics settings (gravity).
    -   Contract for `PhysicsRigidBody`: mass, velocity, inertia.
    -   Contract for `PhysicsRevoluteJoint`: axis, limits, drive.
-   **Material (`Material`)**:
    -   Contract for `PBRShader` parameters: baseColor, metallic, roughness, normal map.
-   **Sensors (e.g., `Camera`, `Lidar`)**:
    -   Contract for `IsaacReadCameraParameters`, `IsaacReadLidarParameters` for configuration.

## 2. ROS 2 Interface Contracts for Simulation

These define the standard ROS 2 message, service, and action types used to interact with simulated robots and sensors.

### 2.1 Standard Message Types

-   **`sensor_msgs/msg/Image`**:
    -   Purpose: Transmit camera images (RGB, depth).
    -   Fields: `std_msgs/Header header`, `uint32 height`, `uint32 width`, `string encoding`, `uint8 is_bigendian`, `uint32 step`, `uint8[] data`.
-   **`sensor_msgs/msg/PointCloud2`**:
    -   Purpose: Transmit LiDAR scan data.
    -   Fields: `std_msgs/Header header`, `uint32 height`, `uint32 width`, `sensor_msgs/PointField[] fields`, `bool is_bigendian`, `uint32 point_step`, `uint32 row_step`, `uint8[] data`, `bool is_dense`.
-   **`sensor_msgs/msg/Imu`**:
    -   Purpose: Transmit Inertial Measurement Unit data.
    -   Fields: `std_msgs/Header header`, `geometry_msgs/Quaternion orientation`, `float64[9] orientation_covariance`, `geometry_msgs/Vector3 angular_velocity`, `float64[9] angular_velocity_covariance`, `geometry_msgs/Vector3 linear_acceleration`, `float64[9] linear_acceleration_covariance`.
-   **`sensor_msgs/msg/JointState`**:
    -   Purpose: Transmit joint positions, velocities, and efforts.
    -   Fields: `std_msgs/Header header`, `string[] name`, `float64[] position`, `float64[] velocity`, `float64[] effort`.
-   **`geometry_msgs/msg/Twist`**:
    -   Purpose: Transmit linear and angular velocity commands to robots.
    -   Fields: `geometry_msgs/Vector3 linear`, `geometry_msgs/Vector3 angular`.

### 2.2 Standard Service Types

-   **`gazebo_msgs/srv/SetEntityState`**:
    -   Purpose: Set the pose and twist of an entity in Gazebo.
    -   Request fields: `gazebo_msgs/EntityState entity_state`, `bool teleporter_only`.
    -   Response fields: `bool success`, `string status_message`.
-   **`std_srvs/srv/Empty`**:
    -   Purpose: Generic empty service for simple triggers (e.g., pause/resume simulation).

## 3. Custom Plugin Contracts

Custom plugins extend simulation functionality (e.g., specialized sensors, robot controllers).

-   **Gazebo Plugin Contract (C++)**:
    -   Inherits from `gazebo::sensors::SensorPlugin`, `gazebo::physics::ModelPlugin`, etc.
    -   Exports specific Gazebo entry points.
    -   Communicates with ROS 2 via `gazebo_ros` bridge.
-   **Isaac Sim Extension Contract (Python)**:
    -   Python classes inheriting from `omni.ext.IExt` or similar.
    -   Uses Isaac Sim APIs (`omni.isaac.core`, `omni.isaac.dynamic_control`) for simulation interaction.
    -   Communicates with ROS 2 via `omni.isaac.ros_bridge`.
