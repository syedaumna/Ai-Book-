# Data Model for Implement ROS 2 Fundamentals Feature

This document outlines the key "data" entities relevant to the ROS 2 Fundamentals chapter. While not a traditional application data model, it describes the structured information that will be conveyed and manipulated throughout the course content and code examples.

## Key Entities

### 1. ROS 2 Concepts

These represent the fundamental building blocks and communication primitives within ROS 2.

-   **Node**: An executable process that performs computation.
    -   Attributes: Name, lifecycle state (e.g., uninitialized, active), associated topics, services, actions, parameters.
-   **Topic**: A named bus over which nodes exchange messages using a publish-subscribe mechanism.
    -   Attributes: Name, message type, Quality of Service (QoS) profile (e.g., reliability, history, durability).
-   **Service**: A request-response communication mechanism between nodes.
    -   Attributes: Name, request message type, response message type.
-   **Action**: A long-running, goal-oriented communication mechanism with feedback.
    -   Attributes: Name, goal message type, result message type, feedback message type.
-   **Parameter**: Configuration values that can be dynamically set and retrieved by nodes.
    -   Attributes: Name, type (e.g., int, float, string, bool), value.
-   **Launch File**: An XML or Python-based file for orchestrating the startup of multiple ROS 2 nodes and configurations.
    -   Attributes: Nodes to launch, parameters to set, remappings, conditionals.
-   **URDF (Unified Robot Description Format)**: An XML format for describing a robot's kinematic and dynamic properties.
    -   Attributes: Links, Joints, Inertia, Visuals, Collisions.

### 2. Code Examples

These represent the Python scripts and related files provided to illustrate ROS 2 concepts.

-   **Python Script**: A runnable program demonstrating a specific ROS 2 concept (e.g., publisher node, service client).
    -   Attributes: File path, associated ROS 2 concept, dependencies (ROS 2 packages, custom messages).
-   **Custom Message/Service/Action Definition File**: `.msg`, `.srv`, `.action` files that define custom data structures for communication.
    -   Attributes: File path, fields (name, type), usage context.

### 3. Hands-on Labs

These represent guided projects where students apply learned concepts.

-   **Lab Project**: A collection of ROS 2 nodes, launch files, and configuration demonstrating an integrated system.
    -   Attributes: Directory path, learning objectives, required components (nodes, interfaces).
-   **Deliverables**: Expected outputs from a lab (e.g., URDF file, screenshot of visualization, analysis document).
