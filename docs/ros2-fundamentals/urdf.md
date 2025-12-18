# URDF: Describing Robot Morphology

To simulate, visualize, and control a robot, its physical structure must be formally defined. The **Unified Robot Description Format (URDF)** is an XML-based file format used in ROS 2 to describe a robot's kinematic and dynamic properties. It's an essential tool for communicating a robot's physical characteristics to various software components within the ROS ecosystem.

## What is URDF?

URDF provides a standardized way to represent:

-   **Kinematics**: The geometric arrangement of a robot's links and joints.
-   **Dynamics**: The physical properties of those links (mass, inertia) and joints (friction, damping).
-   **Visuals**: The appearance of the robot for visualization.
-   **Collisions**: The simplified geometric shapes used for collision detection.

A single URDF file contains a hierarchical description of the robot, allowing tools like RViz (for visualization), Gazebo (for simulation), and motion planners to correctly interpret the robot's structure.

## Why URDF Matters: Kinematic Chains, Inertia, Collision Geometry

-   **Kinematic Chains**: URDF defines a chain of rigid bodies (links) connected by joints. This allows software to calculate the robot's forward kinematics (where each part of the robot is in space given its joint angles) and inverse kinematics (what joint angles are needed to reach a desired position).
-   **Inertia**: The inertial properties (mass and inertia tensor) of each link are crucial for accurate physics simulation. Without correct inertia, a robot in simulation might behave unnaturally, e.g., fall over too easily or resist movement incorrectly.
-   **Collision Geometry**: While visual models can be highly detailed, collision detection typically uses simpler, convex geometric primitives (boxes, spheres, cylinders). This reduces computational overhead for real-time collision checking in simulation and planning.

## URDF Structure: Root Link, Joints, Links, Frames

A URDF file begins with a `<robot>` tag and contains a series of `<link>` and `<joint>` tags that define the robot's structure.

-   **`<robot name="...">`**: The root tag, giving a name to the robot.
-   **`<link name="...">`**: Represents a rigid body segment of the robot. Each link has:
    -   **`<inertial>`**: Defines mass, center of mass (origin), and inertia tensor.
    -   **`<visual>`**: Describes the link's appearance.
        -   **`<geometry>`**: Shape (box, cylinder, sphere, mesh).
        -   **`<material>`**: Color and texture.
    -   **`<collision>`**: Defines the shape used for physical interaction.
        -   **`<geometry>`**: Simpler shape (box, cylinder, sphere, mesh).
-   **`<joint name="..." type="...">`**: Connects two links, defining their relative motion.
    -   **`<parent link="..." />`**: The link closer to the robot's base.
    -   **`<child link="..." />`**: The link further from the robot's base.
    -   **`<origin xyz="..." rpy="..." />`**: Defines the joint's position and orientation relative to the parent link.
    -   **`<axis xyz="..." />`**: Defines the axis of rotation or translation for the joint.
    -   **`<limit lower="..." upper="..." velocity="..." effort="..." />`**: Specifies the joint's range of motion, maximum velocity, and maximum effort.

## Joint Types

URDF supports several joint types:

-   **`revolute`**: A rotating joint with a single axis of rotation and a limited range (e.g., elbow, shoulder).
-   **`continuous`**: A rotating joint with a single axis of rotation and an unlimited range (e.g., spinning wheel).
-   **`prismatic`**: A sliding joint with a single axis of translation and a limited range (e.g., linear actuator).
-   **`fixed`**: A joint that rigidly connects two links (no motion). Useful for attaching sensors or tools.
-   **`floating`**: Represents a base link with 6 degrees of freedom relative to the world (unconstrained).
-   **`planar`**: Allows motion in a plane (2 prismatic, 1 revolute degree of freedom).

## Link Properties: Visual, Collision, Inertia

-   **`visual`**: This describes how the link *looks*. It can be a simple primitive (box, cylinder, sphere) or a complex 3D mesh (e.g., STL, DAE).
-   **`collision`**: This describes the link's *physical interaction* with other objects. It typically uses simpler geometric primitives to reduce the computational cost of collision detection. It's common for the visual and collision geometries to differ.
-   **`inertial`**: This defines the mass properties of the link: its `mass` (in kg), its `origin` (center of mass relative to the link's frame), and its `inertia` tensor. Accurate inertial properties are crucial for realistic physics simulation.

## Coordinate Frames and Transformations (TF2)

Each `<link>` in a URDF inherently defines a **coordinate frame**. The joints define the transformations between these frames. The `tf2` (Transform Frame) system in ROS 2 uses this information to keep track of all coordinate frames in the robot and provides a way to transform data between any two frames at any point in time. This is fundamental for robust robot perception, planning, and control.

## Forward Kinematics

**Forward kinematics** is the computation of the position and orientation of the robot's end-effector (or any link) in 3D space, given the joint angles of the robot. URDF provides all the necessary geometric and joint information for kinematic solvers to perform these calculations.

## URDF Validators and Best Practices

-   **URDF Validation**: Tools exist (e.g., `check_urdf` in ROS 2, or online validators) to check your URDF file for syntax errors and consistency.
-   **Modular URDFs**: For complex robots, it's good practice to split the URDF into smaller, manageable files (e.g., separate files for arm, hand, base) and use XACRO (XML Macros for ROS) to include and parameterize them.
-   **Standard Units**: Always use meters for lengths, kilograms for masses, and radians for angles.
-   **Clear Frame Definitions**: Ensure that all links have clearly defined frames and that their origins and axes are intuitively placed.

## Example: Simple 2-DOF Arm URDF

```xml
<?xml version="1.0"?>
<robot name="simple_2dof_arm">
  <!-- Base Link -->
  <link name="base_link">
    <visual>
      <geometry><box size="0.1 0.1 0.05"/></geometry>
      <material name="green"><color rgba="0 1 0 1"/></material>
    </visual>
    <collision>
      <geometry><box size="0.1 0.1 0.05"/></geometry>
    </collision>
    <inertial>
      <mass value="1.0"/>
      <inertia ixx="0.001" ixy="0" ixz="0" iyy="0.001" iyz="0" izz="0.001"/>
    </inertial>
  </link>

  <!-- Joint 1 -->
  <joint name="joint1" type="revolute">
    <parent link="base_link"/>
    <child link="link1"/>
    <origin xyz="0 0 0.025" rpy="0 0 0"/> <!-- Offset from base_link to top -->
    <axis xyz="0 0 1"/> <!-- Rotate around Z -->
    <limit lower="-1.57" upper="1.57" effort="100" velocity="1"/>
  </joint>

  <!-- Link 1 -->
  <link name="link1">
    <visual>
      <geometry><cylinder radius="0.02" length="0.2"/></geometry>
      <origin xyz="0 0 0.1" rpy="0 0 0"/>
      <material name="blue"><color rgba="0 0 1 1"/></material>
    </visual>
    <collision>
      <geometry><cylinder radius="0.02" length="0.2"/></geometry>
      <origin xyz="0 0 0.1" rpy="0 0 0"/>
    </collision>
    <inertial>
      <mass value="0.1"/>
      <inertia ixx="0.0001" ixy="0" ixz="0" iyy="0.0001" iyz="0" izz="0.00001"/>
    </inertial>
  </link>

  <!-- Joint 2 -->
  <joint name="joint2" type="revolute">
    <parent link="link1"/>
    <child link="link2"/>
    <origin xyz="0 0 0.2" rpy="0 0 0"/> <!-- Offset from link1 end -->
    <axis xyz="0 1 0"/> <!-- Rotate around Y -->
    <limit lower="-1.57" upper="1.57" effort="100" velocity="1"/>
  </joint>

  <!-- Link 2 (End-effector) -->
  <link name="link2">
    <visual>
      <geometry><sphere radius="0.03"/></geometry>
      <origin xyz="0 0 0" rpy="0 0 0"/>
      <material name="red"><color rgba="1 0 0 1"/></material>
    </visual>
    <collision>
      <geometry><sphere radius="0.03"/></geometry>
      <origin xyz="0 0 0" rpy="0 0 0"/>
    </collision>
    <inertial>
      <mass value="0.05"/>
      <inertia ixx="0.00001" ixy="0" ixz="0" iyy="0.00001" iyz="0" izz="0.00001"/>
    </inertial>
  </link>
</robot>
```
This URDF describes a simple robotic arm with two revolute joints, allowing it to move its two links.
