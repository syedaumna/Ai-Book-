# Data Model for The Digital Twin: Physics Simulation and Environment Building

This document outlines the key data entities relevant to the "Digital Twin" chapter, focusing on the structured information used within physics simulations and environment building.

## Key Entities

### 1. Simulation Description Formats

-   **SDF (Simulation Description Format)**: XML format primarily used by Gazebo for describing robots, environments, and their physical properties.
    -   Attributes: `world` (gravity, physics engine settings), `model` (links, joints, visuals, collisions, inertia), `sensor` (camera, LiDAR, IMU parameters), `plugin` (custom simulation logic).
-   **USD (Universal Scene Description)**: NVIDIA's framework for composing, simulating, and collaborating on 3D scenes, used by Isaac Sim.
    -   Attributes: `Stage` (scene composition), `Prim` (geometric objects, actors), `Schema` (physics, materials, properties), `Material` (PBR properties), `Mesh` (geometry).

### 2. Robot Description Formats

-   **URDF (Unified Robot Description Format)**: XML format for describing a robot's kinematic and dynamic properties, often converted to or integrated with SDF/USD for simulation.
    -   Attributes: `Link` (rigid body), `Joint` (connection between links), `Inertial` (mass, inertia tensor), `Visual` (visual representation), `Collision` (collision geometry).

### 3. Sensor Models

-   **Camera Model**: Defines parameters for simulating cameras (RGB, Depth, Segmentation).
    -   Attributes: `intrinsics` (focal length, principal point, distortion), `noise_model` (Gaussian, shot noise), `resolution`, `frame_rate`.
-   **LiDAR Model**: Defines parameters for simulating LiDAR sensors.
    -   Attributes: `FOV` (field of view), `angular_resolution`, `range_accuracy`, `noise_model`, `min_range`, `max_range`.
-   **IMU Model**: Defines parameters for simulating Inertial Measurement Units (accelerometers, gyroscopes).
    -   Attributes: `noise_model` (bias, drift, white noise), `resolution`, `update_rate`.

### 4. Physics Parameters

-   **World Physics**: Global settings for the simulation environment.
    -   Attributes: `gravity` (vector), `timestep`, `solver_type` (ODE, PhysX), `solver_iterations`.
-   **Body/Link Physics**: Properties applied to individual rigid bodies in the simulation.
    -   Attributes: `mass`, `inertia_tensor`, `friction` (static, dynamic), `damping` (linear, angular), `restitution` (bounciness).
-   **Joint Physics**: Properties applied to connections between rigid bodies.
    -   Attributes: `type` (revolute, prismatic, fixed), `axis`, `limit` (upper, lower, velocity, effort), `dynamics` (damping, friction).

### 5. Synthetic Data

-   **Annotated Image**: An image generated in simulation with associated ground truth labels for perception training.
    -   Attributes: `RGB_image`, `depth_map`, `semantic_segmentation_mask`, `instance_segmentation_mask`, `bounding_boxes` (2D, 3D), `object_6d_pose`.
-   **Randomization Parameters**: Parameters used to vary simulation environments for domain randomization.
    -   Attributes: `lighting_intensity`, `material_color_range`, `texture_set`, `object_position_range`, `sensor_noise_level`.
