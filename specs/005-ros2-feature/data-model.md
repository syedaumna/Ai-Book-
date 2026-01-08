# Data Model for Implement ROS 2 Fundamentals Feature

This document defines the key data structures and conceptual entities central to the "ROS 2 Fundamentals" chapter. While not a traditional software data model in terms of database schemas, it outlines the structured information that students will learn to understand, create, and manipulate as they develop ROS 2 applications. This includes ROS 2 communication primitives, custom message types, and components of code examples and labs.

## Key Entities

### 1. ROS 2 Communication Primitives (Conceptual)

These represent the fundamental building blocks for inter-node communication within a ROS 2 system.

-   **Node**: An independent executable process performing specific computations.
    -   Attributes: `name` (string), `lifecycle_state` (enum: e.g., `unconfigured`, `inactive`, `active`), `associated_topics` (list of strings), `associated_services` (list of strings), `associated_actions` (list of strings), `parameters` (map of key-value pairs).
-   **Topic**: A named channel for asynchronous, many-to-many data streaming.
    -   Attributes: `name` (string), `message_type` (string), `qos_profile` (enum: e.g., `reliable`, `best_effort`).
-   **Service**: A named channel for synchronous, one-to-one request-response interactions.
    -   Attributes: `name` (string), `request_message_type` (string), `response_message_type` (string).
-   **Action**: A named channel for asynchronous, goal-oriented tasks with feedback and cancellability.
    -   Attributes: `name` (string), `goal_message_type` (string), `result_message_type` (string), `feedback_message_type` (string).
-   **Parameter**: A configurable value associated with a node, modifiable at runtime.
    -   Attributes: `name` (string), `type` (enum: `integer`, `float`, `string`, `boolean`, `array_of_type`), `value` (any), `default_value` (any).
-   **Launch File**: A script (Python or XML) for orchestrating the startup of multiple ROS 2 nodes and their configurations.
    -   Attributes: `path` (string), `nodes_launched` (list of strings), `parameters_set` (map of key-value pairs), `remappings_applied` (map of old-to-new topic/service names).
-   **URDF (Unified Robot Description Format)**: An XML file describing a robot's physical and kinematic properties.
    -   Attributes: `links` (list of `Link` entities), `joints` (list of `Joint` entities), `materials` (list of `Material` entities).

### 2. Custom Message/Service/Action Types (Defined by Files)

These are user-defined data structures used for specific communication needs.

-   **Custom Message (`.msg`)**: A simple data structure for topics.
    -   Attributes: `file_path` (string), `fields` (list of `Field` entities), `dependencies` (list of standard/custom message types).
-   **Custom Service (`.srv`)**: Defines a request-response pair.
    -   Attributes: `file_path` (string), `request_fields` (list of `Field` entities), `response_fields` (list of `Field` entities), `dependencies`.
-   **Custom Action (`.action`)**: Defines a goal, result, and feedback structure.
    -   Attributes: `file_path` (string), `goal_fields` (list of `Field` entities), `result_fields` (list of `Field` entities), `feedback_fields` (list of `Field` entities), `dependencies`.
-   **Field**: A single data entry within a message, service, or action definition.
    -   Attributes: `type` (string: e.g., `int32`, `float64`, `string`, `geometry_msgs/Pose`), `name` (string), `is_array` (boolean).

### 3. Code Example Components

These are the runnable scripts and configurations provided as part of the chapter's learning material.

-   **Python ROS 2 Node Script**: A Python file implementing a ROS 2 node.
    -   Attributes: `file_path` (string), `ros_node_name` (string), `communication_pattern_used` (enum: `publisher`, `subscriber`, `service_server`, `service_client`, `action_server`, `action_client`), `custom_messages_used` (list of strings).
-   **Launch File Script**: A Python file for launching ROS 2 nodes.
    -   Attributes: `file_path` (string), `nodes_launched` (list of strings), `arguments_declared` (list of strings).

### 4. Hands-on Lab Structure

These represent guided projects designed to apply the concepts learned.

-   **Lab Project**: A collection of related files (nodes, messages, launch files) forming an integrated system.
    -   Attributes: `directory_path` (string), `learning_objectives` (list of strings), `required_components` (list of `ROS 2 Communication Primitives`), `deliverables` (list of expected outputs).