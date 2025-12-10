# Physical AI & Humanoid Robotics - Chapter 2 Specification File

# The Robotic Nervous System (ROS 2)

---

- chapter:
    number: 2
    title: "The Robotic Nervous System: ROS 2 Fundamentals"
    duration: "Weeks 3-5"
    focus: "Middleware for robot control and inter-process communication"
    overview: |
      Chapter 2 introduces Robot Operating System 2 (ROS 2) as the middleware layer that connects sensors, perception algorithms, planners, and motor controllers. Students will learn ROS 2 architecture, core concepts (nodes, topics, services, actions), and practical implementation. By the end, students will design and build a multi-node ROS 2 system that simulates a humanoid robot's control pipeline.
- learning_outcomes:
    conceptual:
    - "Understand ROS 2 architecture and why middleware is essential for robotics"
    - "Grasp the difference between topics (streams), services (RPC), and actions (goals)"
    - "Understand the publish-subscribe pattern and its advantages for distributed systems"
    - "Learn why ROS 2 is superior to ROS 1 for real-time and deterministic systems"
    - "Understand URDF (Unified Robot Description Format) and kinematic chains"
    - "Learn how to describe humanoid robot morphology in machine-readable format"
    practical:
    - "Install and configure a ROS 2 environment"
    - "Create ROS 2 packages with proper structure and dependencies"
    - "Write ROS 2 nodes"
    - "Create custom message and service definitions"
    - "Implement publish-subscribe communication between nodes"
    - "Implement request-response (service) communication"
    - "Use launch files to orchestrate multi-node systems"
    - "Use parameter servers and dynamic parameter reconfiguration"
    - "Parse and validate URDF files for humanoid robots"
    - "Visualize robot morphology using a visualization tool"
    - "Debug ROS 2 systems using command-line tools"
    capstone_relevance:
    - "Students will use ROS 2 nodes to coordinate their capstone system"
    - "Perception pipeline (sensors → fusion) will run as ROS 2 nodes"
    - "Motion planning will be a ROS 2 service"
    - "Motor commands will be published as ROS 2 topics"
- module_1:
    title: "Module 1: ROS 2 Architecture & Core Concepts"
    duration: "Weeks 3-4 (First Half)"
    subsections:
    - title: "1.1 What is ROS 2? The Middleware Problem"
      description: |
        - Why robots need middleware (vs. monolithic code)
        - The distributed architecture problem: sensors on one computer, perception on another, planning on another, control on the robot itself
        - ROS 2 as a publish-subscribe message bus
        - Comparison: ROS 1 vs ROS 2 (real-time, type safety, modularity)
        - The underlying data distribution service foundation
      content_type: "conceptual + technical"
      visuals_needed:
      - Diagram: Monolithic vs. Distributed Robot Architecture
      - Diagram: ROS 2 computation graph with multiple nodes
      - Table: ROS 1 vs ROS 2 comparison matrix
      estimated_length: "8-10 pages"
    - title: "1.2 Nodes: The Building Blocks"
      description: |
        - What is a ROS 2 node? (Independent process, single responsibility)
        - Lifecycle of a node (uninitialized → configured → activated → deactivated → finalized)
        - Node executors
        - Node naming conventions and namespacing
        - Creating a minimal ROS 2 node
        - Best practices: node design, error handling, shutdown procedures
      content_type: "conceptual + code"
      visuals_needed:
      - Diagram: Node lifecycle state machine
      - Diagram: Node execution models
      - Code walkthrough: Minimal publisher node
      estimated_length: "12-15 pages"
    - title: "1.3 Topics: Publish-Subscribe Communication"
      description: |
        - The publish-subscribe pattern explained
        - Topics as named data streams (e.g., /camera/rgb, /lidar/scan, /joint_commands)
        - Message types: built-in vs. custom
        - Quality of Service (QoS): reliability, durability, history policies
        - Topic remapping and composition
        - Latency considerations: best-effort vs. reliable
        - Use case: sensor fusion (multiple sources publishing to single topic)
      content_type: "conceptual + code"
      visuals_needed:
      - Diagram: Topic graph for humanoid robot
      - Table: Common message types for robotics
      - Table: QoS profiles
      - Timing diagram: publisher → topic → subscriber flow
      estimated_length: "15-18 pages"
    - title: "1.4 Services: Request-Response Communication"
      description: |
        - When topics are not enough (request-response patterns)
        - Services vs. Topics comparison
        - Service definition syntax
        - Service server implementation
        - Service client implementation
        - Synchronous and asynchronous service calls
        - Error handling and timeouts
        - Use case: motion planning service (robot queries planner, gets path back)
      content_type: "conceptual + code"
      visuals_needed:
      - Diagram: Service call flow
      - Table: Services vs. Topics
      - Code walkthrough: Service definition and implementation
      estimated_length: "12-14 pages"
    - title: "1.5 Actions: Goal-Oriented Communication"
      description: |
        - The action pattern: client sends goal, server works toward it, reports progress
        - Actions vs. Services (long-running tasks, feedback, cancellation)
        - Action definition syntax
        - Action server implementation
        - Action client implementation
        - Feedback and result handling
        - Cancellation and preemption
        - Use case: navigate_to_goal (robot navigates while reporting progress)
      content_type: "conceptual + code"
      visuals_needed:
      - Diagram: Action lifecycle
      - Diagram: Action vs. Service timeline
      - Code walkthrough: Action definition and implementation
      estimated_length: "12-14 pages"
    - title: "1.6 Parameter Server: Configuration Management"
      description: |
        - Why parameter servers? (Configuration without recompilation)
        - Global parameters vs. node-specific parameters
        - Parameter types: int, double, string, bool, arrays
        - Setting parameters via launch files, command-line, or code
        - Reading and writing parameters from nodes
        - Dynamic parameter reconfiguration
        - Parameter validation and constraints
        - Use case: tuning PID gains for motor controllers without restart
      content_type: "conceptual + code"
      visuals_needed:
      - Table: ROS parameter types
      - Code walkthrough: Parameter server interaction
      estimated_length: "10-12 pages"
    - title: "1.7 Hands-On Lab: Build Your First ROS 2 System"
      description: |
        - Guided project: simulate a humanoid robot's sensor-to-control pipeline
        - Tasks:
          * Create 3 nodes: SensorSimulator, Planner, MotorController
          * SensorSimulator publishes fake sensor data
          * Planner provides trajectory as a service
          * MotorController requests plan and publishes motor commands
          * All nodes communicate via topics and services
        - Testing: verify data flow using command-line tools
        - Debugging: identify bottlenecks, latency issues
      content_type: "hands-on project"
      deliverables:
      - Working 3-node ROS 2 system
      - Launch file that starts all nodes
      - Explanation of data flow and design choices
      visuals_needed:
      - Diagram: Node graph for this system
      - Screenshots: command-line tool output
      estimated_length: "10-12 pages"
- module_2:
    title: "Module 2: Practical ROS 2 Development"
    duration: "Weeks 4-5"
    subsections:
    - title: "2.1 Launch Files: Orchestrating Multi-Node Systems"
      description: |
        - Why launch files? (Starting multiple nodes by hand is error-prone)
        - Launch file syntax
        - Node declarations, remapping, parameter passing
        - Conditional logic for different robot configs
        - Include files for modular system design
        - Event handlers
        - Best practices: organizing launch files
        - Use case: launch entire humanoid robot stack with one command
      content_type: "conceptual + code"
      visuals_needed:
      - Code walkthrough: Simple launch file
      - Code walkthrough: Complex launch file with conditionals
      - Diagram: Launch file hierarchy for humanoid system
      estimated_length: "10-12 pages"
    - title: "2.2 Message and Service Definitions"
      description: |
        - Built-in ROS message types
        - When to create custom messages
        - Custom message, service, and action syntax
        - Type safety and code generation
        - Including messages in custom packages
        - Practical examples for humanoid robotics:
          * HumanoidState message (joint angles, velocities, forces)
          * PlanTrajectory service (query planner)
          * Navigate action (goal-oriented navigation)
      content_type: "conceptual + code"
      visuals_needed:
      - Table: Common message types
      - Code examples: Message definitions
      estimated_length: "12-14 pages"
    - title: "2.3 Debugging ROS 2 Systems"
      description: |
        - ROS 2 command-line tools for nodes, topics, services, actions
        - Topic introspection (listing, echoing, frequency, bandwidth)
        - Service introspection (listing, calling)
        - Action introspection (listing, sending goals)
        - Graph visualization
        - Message inspection
        - Data recording and playback
        - Logging and log inspection
        - Common issues and troubleshooting
      content_type: "technical + hands-on"
      visuals_needed:
      - Screenshots: command-line tool output
      - Screenshots: graph visualization
      - Troubleshooting flowchart
      estimated_length: "10-12 pages"
    - title: "2.4 ROS 2 Logging and Node Lifecycle"
      description: |
        - Logging with the client library
        - Log levels
        - Node lifecycle management (managed nodes)
        - Lifecycle states and transitions
        - Use case: graceful startup/shutdown for humanoid robots
        - Error handling and exception propagation
      content_type: "conceptual + code"
      visuals_needed:
      - Diagram: Node lifecycle state machine
      - Code walkthrough: Managed node
      estimated_length: "8-10 pages"
    - title: "2.5 URDF: Describing Robot Morphology"
      description: |
        - What is URDF? (XML format for robot structure)
        - Why URDF matters: kinematic chains, inertia, collision geometry
        - URDF structure: root link, joints, links, frames
        - Joint types
        - Link properties: visual, collision, inertia
        - Coordinate frames and transformations
        - Forward kinematics
        - URDF validators and best practices
        - Example: Simple 2-DOF arm URDF
      content_type: "technical + reference"
      visuals_needed:
      - Diagram: URDF structure tree
      - Diagram: Coordinate frames in humanoid
      - Code walkthrough: URDF example
      - Screenshots: Visualization of URDF
      estimated_length: "12-14 pages"
    - title: "2.6 Visualizing Robots and Sensor Data"
      description: |
        - What is the standard 3D visualization tool for ROS?
        - Loading and displaying URDF models
        - Viewing TF frames and coordinate transformations
        - Subscribing to sensor data streams
        - Markers: visualizing computed results
        - Configuration files for the visualizer
        - Interactive controls
        - Debugging: checking sensor alignment
      content_type: "technical + hands-on"
      visuals_needed:
      - Screenshots: Visualizer displaying humanoid robot and sensor data
      - Code walkthrough: Publishing markers
      estimated_length: "8-10 pages"
    - title: "2.7 Hands-On Lab: Design a Humanoid URDF"
      description: |
        - Guided project: create a simplified humanoid URDF
        - Tasks:
          * Design kinematic chain
          * Add visual and collision geometry
          * Add inertia properties
          * Validate URDF syntax
          * Visualize in the 3D visualizer
          * Compute forward kinematics
        - Deliverables:
          * Valid URDF file
          * Visualization (screenshot)
          * Forward kinematics analysis
      content_type: "hands-on project"
      deliverables:
      - humanoid_simplified.urdf
      - Visualizer config
      - Screenshots showing visualization
      - Analysis document
      estimated_length: "10-12 pages"
    - title: "2.8 Time in ROS 2: Clocks and Timing"
      description: |
        - System time vs. simulation time
        - ROS 2 clocks
        - Using consistent time sources for reproducible experiments
        - Timing utilities
        - Measuring execution time
        - Scheduling periodic tasks
        - Why timing matters for robots
        - Use case: tuning control loop frequency
      content_type: "conceptual + code"
      visuals_needed:
      - Diagram: Clock hierarchy in ROS 2
      estimated_length: "8-10 pages"
- module_3:
    title: "Module 3: Integration & Capstone Preparation"
    duration: "Week 5 (Latter Half)"
    subsections:
    - title: "3.1 Building a Humanoid Control Architecture"
      description: |
        - Design exercise: how should a humanoid robot's software be organized?
        - Typical architecture layers: Perception, Fusion, Planning, Control, Task
        - Communication patterns between layers
        - Real-time vs. non-real-time constraints
        - Separation of concerns
      content_type: "architectural design"
      visuals_needed:
      - Diagram: Humanoid software architecture layers
      - Diagram: Node graph for full humanoid system
      - Table: Real-time vs. non-real-time tasks
      estimated_length: "8-10 pages"
    - title: "3.2 Sensor Drivers: Integrating Hardware"
      description: |
        - What is a ROS 2 sensor driver? (Hardware interface → ROS topics)
        - Using existing drivers vs. writing custom drivers
        - Wrapping hardware libraries in ROS nodes
        - Example driver structure
        - Common driver types for cameras, LiDAR, IMUs
        - Configuration and calibration
      content_type: "technical + reference"
      visuals_needed:
      - Diagram: Sensor driver architecture
      - Code walkthrough: Simple sensor driver
      estimated_length: "10-12 pages"
    - title: "3.3 Motor Controllers: Actuating Robots"
      description: |
        - Typical robot motor hardware and driver boards
        - ROS 2 abstraction for motor commands
        - Feedback loops and odometry
        - Safety considerations
        - Example controller node structure
        - Sim-to-real considerations
      content_type: "technical"
      visuals_needed:
      - Diagram: Motor feedback control loop
      - Hardware schematic example
      estimated_length: "10-12 pages"
    - title: "3.4 Capstone Preview: The Autonomous Humanoid System"
      description: |
        - Overview of the final capstone project
        - System architecture and data flow
        - Components built in this chapter vs. future chapters
        - Integration checklist
      content_type: "overview + planning"
      visuals_needed:
      - Diagram: Full capstone system architecture
      - Timeline: which chapters contribute which components
      estimated_length: "6-8 pages"
    - title: "3.5 Hands-On Lab: Integration Challenge"
      description: |
        - Comprehensive project integrating Modules 1-2 content
        - Scenario: Humanoid robot receives commands to execute tasks
        - Tasks:
          * Create a full ROS 2 system with 5+ nodes
          * Use custom messages, services, and parameters
          * Integrate a humanoid URDF for visualization
          * Create a launch file
          * Implement logging and error handling
          * Test with the 3D visualizer
        - Success criteria:
          * All nodes start cleanly
          * Task flows through system correctly
          * Visualizer shows robot executing trajectory
          * No crashes or deadlocks
      content_type: "capstone integration project"
      deliverables:
      - 5+ ROS 2 nodes
      - Custom message and service definitions
      - Launch file
      - Humanoid URDF
      - System description document
      - Screenshots of visualization
      - Test results
      estimated_length: "12-15 pages"
- assessments:
    formative:
    - title: "Weekly Quizzes (Weeks 3-5)"
      description: "Short conceptual quizzes on ROS 2 concepts"
      topics:
      - ROS 2 architecture and core concepts
      - Nodes, topics, services, actions
      - URDF structure
      format: "Multiple choice + short answer"
      weight: "10%"
    - title: "Lab Checkpoint 1: First ROS 2 System (Week 3-4)"
      description: "Hands-on lab from section 1.7"
      deliverables:
      - Working 3-node ROS 2 system
      - Launch file
      - Explanation document
      format: "Code submission + demonstration"
      weight: "15%"
    - title: "Lab Checkpoint 2: Humanoid URDF Design (Week 4-5)"
      description: "Hands-on lab from section 2.7"
      deliverables:
      - Valid URDF file
      - Visualization
      - Forward kinematics analysis
      format: "Code submission + screenshots"
      weight: "15%"
    summative:
    - title: "Chapter 2 Integration Challenge (Week 5)"
      description: "Comprehensive project from section 3.5"
      deliverables:
      - Complete 5+ node ROS 2 system
      - All configuration files
      - System documentation
      - Working demonstration
      format: "Code + documentation + presentation"
      weight: "40%"
    - title: "System Design Report"
      description: "Design document for ROS 2 architecture used in capstone"
      content:
      - Node list with responsibilities
      - Topic and service specifications
      - Data flow diagrams
      - Timing and real-time constraints
      - Error handling strategy
      format: "Written report (5-10 pages)"
      weight: "20%"
- technical_requirements:
    software_stack:
    - "A supported ROS 2 distribution"
    - "A supported Python version"
    - "A 3D visualization tool"
    - "Debugging tools"
    - "A code editor"
    hardware:
    - "A Linux-based operating system (dual-boot or VM acceptable)"
    - "Sufficient RAM and disk space"
    - "No specialized hardware needed for Chapter 2 (simulation only)"
    external_dependencies:
    - "A ROS 2 client library"
    - "Standard message types"
    - "A coordinate transformation library"
- reading_materials:
    primary:
    - "ROS 2 Official Documentation"
    - "ROS 2 Design documents"
    - "ROS 2 client library documentation"
    - "URDF Format Specification"
    secondary:
    - "Research papers on real-time robotics"
    - "Best practices for message design"
    - "Books on robot architecture"
    reference:
    - "ROS 2 Command Cheat Sheet"
    - "URDF and visualization tools documentation"
- common_mistakes_to_avoid:
    - "Ignoring QoS settings, leading to data loss or latency."
    - "Creating monolithic nodes, which are hard to debug and reuse."
    - "Not handling dynamic reconnection, causing system hangs."
    - "Using incorrect inertia in URDF, causing simulation divergence."
    - "Mixing real-time and non-real-time code in the same node, causing instability."
    - "Assuming simulated time equals real time, causing failures on hardware."
- chapter_summary:
    duration: "3 weeks (Weeks 3-5)"
    modules: 3
    subsections: 16
    hands_on_projects: 3
    key_takeaways:
    - "ROS 2 is a distributed middleware for complex robot software."
    - "Nodes communicate via topics, services, and actions."
    - "System architecture should separate perception, planning, and control."
    - "URDF describes robot morphology; a 3D visualizer displays it."
    - "Launch files orchestrate multi-node systems."
    - "Debugging tools are essential for system integration."
    - "Real-time constraints are critical for robot stability."
    - "Sim-to-real requires careful time management and hardware abstraction."
    next_chapter_prerequisites:
    - "Working ROS 2 installation"
    - "Ability to write, launch, and debug multi-node systems"
    - "Understanding of URDF and robot kinematics"
    - "Comfort with publish-subscribe and request-response patterns"
    - "Capstone system architecture designed in Chapter 2"
---
end_of_specification: true
