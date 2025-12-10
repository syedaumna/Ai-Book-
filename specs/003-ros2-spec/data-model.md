# Data Model for ROS 2 Fundamentals

This document defines the data structures for the ROS 2 Fundamentals chapter. In the context of ROS 2, the "data model" is primarily defined by the custom message, service, and action definitions that are used for communication between nodes.

## Custom Message Definitions

### HumanoidState.msg

This message is used to represent the current state of the humanoid robot.

```
# HumanoidState.msg

std_msgs/Header header

# Joint states
string[] joint_names
float64[] joint_positions
float64[] joint_velocities
float64[] joint_efforts

# End-effector poses
geometry_msgs/Pose[] end_effector_poses
```

### HumanoidJointCommand.msg

This message is used to send commands to the joints of the humanoid robot.

```
# HumanoidJointCommand.msg

string joint_name
float64 position
float64 velocity
float64 effort
```

## Custom Service Definitions

### PlanTrajectory.srv

This service is used to request a trajectory plan from the planner.

```
# PlanTrajectory.srv

geometry_msgs/Pose start_pose
geometry_msgs/Pose end_pose
---
trajectory_msgs/JointTrajectory trajectory
```

## Custom Action Definitions

### Navigate.action

This action is used to command the robot to navigate to a specific goal.

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