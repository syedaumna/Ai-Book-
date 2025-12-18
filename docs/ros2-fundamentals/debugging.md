# Debugging ROS 2 Systems

Debugging complex, distributed robotic systems built with ROS 2 can be challenging due to their asynchronous nature and numerous interacting components. Fortunately, ROS 2 provides a rich set of command-line tools and visualization utilities that are invaluable for understanding system behavior, identifying issues, and ensuring everything is working as expected.

## ROS 2 Command-Line Tools

The `ros2` command-line interface (CLI) is your primary interface for interacting with a running ROS 2 system. It offers subcommands for inspecting nodes, topics, services, actions, and more.

### `ros2 node`

Used to inspect ROS 2 nodes.

-   `ros2 node list`: Lists all currently running nodes.
-   `ros2 node info <node_name>`: Shows detailed information about a specific node, including its publishers, subscribers, services, and actions.

### `ros2 topic`

Essential for inspecting data flowing over topics.

-   `ros2 topic list`: Lists all active topics.
-   `ros2 topic info <topic_name>`: Displays information about a topic, including its message type and the nodes publishing/subscribing to it.
-   `ros2 topic echo <topic_name>`: Prints messages being published to a topic to the console in real-time. Invaluable for checking sensor data or command streams.
-   `ros2 topic hz <topic_name>`: Reports the publishing rate (frequency) of a topic. Useful for diagnosing performance issues.
-   `ros2 topic bw <topic_name>`: Reports the bandwidth used by a topic. Helps identify network bottlenecks.

### `ros2 service`

For interacting with services (request-response communication).

-   `ros2 service list`: Lists all available services.
-   `ros2 service info <service_name>`: Shows information about a service, including its type and the node providing it.
-   `ros2 service call <service_name> <service_type> <request_args>`: Calls a service with specified arguments and waits for a response.
    -   Example: `ros2 service call /add_two_ints example_interfaces/srv/AddTwoInts "{a: 1, b: 2}"`

### `ros2 action`

For interacting with actions (goal-oriented, long-running tasks).

-   `ros2 action list`: Lists all active actions.
-   `ros2 action info <action_name>`: Shows information about an action.
-   `ros2 action send_goal <action_name> <action_type> <goal_args>`: Sends a goal to an action server and displays feedback and result.
    -   Example: `ros2 action send_goal /fibonacci example_interfaces/action/Fibonacci "{order: 5}"`

### `ros2 param`

For inspecting and modifying node parameters.

-   `ros2 param list`: Lists all parameters on a node.
-   `ros2 param get <node_name> <param_name>`: Gets the current value of a parameter.
-   `ros2 param set <node_name> <param_name> <value>`: Sets the value of a parameter dynamically.

## Graph Visualization: `rqt_graph`

`rqt_graph` is a graphical tool that visualizes the computation graph of a running ROS 2 system. It shows nodes as circles and topics as rectangles, with arrows indicating the data flow between them. This is incredibly useful for:

-   Understanding the system's architecture at a glance.
-   Verifying that nodes are connected as expected.
-   Identifying disconnected topics or missing nodes.

To run: `rqt_graph` (ensure `ros-<ros2-distro>-rqt` and `ros-<ros2-distro>-rqt-graph` are installed).

## Message Inspection: `rqt_topic`

`rqt_topic` provides a GUI for inspecting topics. You can:

-   List active topics.
-   Select a topic and view incoming messages in a structured format.
-   Plot numerical data from messages over time.
-   Publish messages to a topic manually (useful for testing).

To run: `rqt_topic`

## Bag Recording and Playback: `ros2 bag`

`ros2 bag` is a powerful tool for recording and playing back ROS 2 message data.

-   `ros2 bag record -a`: Records all published topics to a `.db3` file.
-   `ros2 bag record -o <output_filename> <topic1> <topic2>`: Records specific topics to a named file.
-   `ros2 bag play <bag_file.db3>`: Plays back recorded messages, effectively simulating the original sensor data or robot behavior.

This is invaluable for:

-   **Reproducible Testing**: Replay a specific scenario to debug an algorithm repeatedly.
-   **Offline Analysis**: Analyze data without needing the physical robot.
-   **Sensor Data Archiving**: Store real-world sensor data for future development or testing.

## Logging and `rosout`: Capturing Node Output

ROS 2 nodes use a logging system that can direct messages to various destinations, including the console and a central `rosout` topic.

-   `ros2 run rcl_interfaces rosout_aggregator`: Aggregates log messages from all nodes to a single topic.
-   `ros2 topic echo /rosout`: View all aggregated log messages.
-   Log levels (DEBUG, INFO, WARN, ERROR, FATAL) allow filtering messages based on severity.

## Common Issues and Troubleshooting

-   **Node Won't Start**:
    -   **Missing Dependencies**: Check `package.xml` and `CMakeLists.txt` (or `setup.py`).
    -   **Syntax Errors**: Especially in Python launch files or YAML parameter files.
    -   **Resource Conflicts**: Another node already using the desired name.
-   **No Data on Topic**:
    -   **Publisher Not Publishing**: Is the publishing node running and actively publishing? Use `ros2 topic hz`.
    -   **QoS Mismatch**: Publisher and subscriber might have incompatible QoS settings (e.g., one is reliable, the other best-effort).
    -   **Remapping Issues**: Topic name might have been remapped unexpectedly. Use `rqt_graph` to visualize actual connections.
-   **Service Calls Timeout**:
    -   **Server Not Running**: Is the service server node active? Use `ros2 node info`.
    -   **Network Latency**: High latency in a distributed system.
    -   **Server Crashed**: Check server node logs for errors.
-   **Memory Leaks in Long-Running Systems**: Monitor `top` or `htop` for increasing memory usage.
-   **Timing Mismatches**: Especially between simulation and real hardware, or when mixing different time sources. Use `ros2 topic echo /clock` to check if `/clock` is being published.

By systematically using these tools and understanding common pitfalls, you can efficiently diagnose and resolve issues in your ROS 2 robotic applications.
