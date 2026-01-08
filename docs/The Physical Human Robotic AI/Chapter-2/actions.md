# Actions: Goal-Oriented Communication

ROS 2 **actions** provide a powerful mechanism for long-running, goal-oriented tasks that require continuous feedback and the ability to be canceled or preempted. They combine aspects of both topics and services to offer a more sophisticated form of communication suitable for complex robot behaviors.

## The Action Pattern: Client Sends Goal, Server Works Toward It

The action pattern involves three main parties:

-   **Action Client**: Sends a goal to an action server, can request cancellation, and receives continuous feedback and a final result.
-   **Action Server**: Receives a goal from an action client, performs the long-running task, sends periodic feedback to the client, and eventually sends a final result (or indicates preemption/failure).
-   **Action Goal, Feedback, Result Topics**: Behind the scenes, actions use several topics to manage the communication of goals, feedback, and results.

This pattern is ideal for tasks that:

-   Take a significant amount of time to complete.
-   Benefit from providing progress updates during execution.
-   Need to be interruptible (cancellable or preemptible).

## Actions vs. Services (Long-Running Tasks, Feedback, Cancellation)

Here's how actions compare to services and topics:

| Feature           | Topics (Streaming)                        | Services (Request-Response)                   | Actions (Goal-Oriented)                               |
| :---------------- | :---------------------------------------- | :-------------------------------------------- | :---------------------------------------------------- |
| **Communication** | Asynchronous, one-to-many, streaming     | Synchronous, one-to-one, one-shot              | Asynchronous, one-to-one (logical), long-running      |
| **Data Flow**     | Continuous stream                         | Single request, single response               | Single goal, continuous feedback, single result       |
| **Feedback**      | No direct feedback                        | No direct feedback                            | **Continuous progress feedback**                      |
| **Cancellation**  | Not applicable                            | Not applicable                                | **Cancellable/Preemptible**                           |
| **Use Case**      | Sensor data, odometry                     | Querying data, simple commands                | Navigation, complex manipulation, long-duration tasks |

## Action Definition Syntax (`.action` files)

Action definitions are similar to service definitions but have three sections, separated by `---`:

1.  **Goal**: Defines the structure of the message sent by the client to the server (the desired state or command).
2.  **Result**: Defines the structure of the final message sent by the server back to the client upon completion.
3.  **Feedback**: Defines the structure of the periodic progress updates sent by the server to the client.

Action definitions are stored in `.action` files within the `action/` directory of a ROS 2 package.

Example: `NavigateToPose.action`

```
# NavigateToPose.action
# Goal
geometry_msgs/PoseStamped pose
---
# Result
bool succeeded
---
# Feedback
float32 distance_remaining
geometry_msgs/PoseStamped current_pose
```

## Action Server Implementation (rclpy)

An **action server** accepts goals, executes the requested task, sends feedback, and eventually returns a result.

```python
import rclpy
from rclpy.action import ActionServer
from rclpy.node import Node

from example_interfaces.action import Fibonacci # Replace with your custom action

class MinimalActionServer(Node):
    def __init__(self):
        super().__init__('minimal_action_server')
        self._action_server = ActionServer(
            self,
            Fibonacci,
            'fibonacci',
            self.execute_callback)
        self.get_logger().info('Action server ready.')

    def execute_callback(self, goal_handle):
        self.get_logger().info('Executing goal...')

        feedback_msg = Fibonacci.Feedback()
        feedback_msg.sequence = [0, 1]

        for i in range(1, goal_handle.request.order):
            feedback_msg.sequence.append(
                feedback_msg.sequence[i] + feedback_msg.sequence[i-1])
            self.get_logger().info(f'Feedback: {feedback_msg.sequence}')
            goal_handle.publish_feedback(feedback_msg)
            # You would typically perform your long-running task here
            # For demonstration, we just sleep
            import time
            time.sleep(1)

        goal_handle.succeed() # Mark goal as successful
        result = Fibonacci.Result()
        result.sequence = feedback_msg.sequence
        self.get_logger().info('Goal succeeded.')
        return result

def main(args=None):
    rclpy.init(args=args)
    minimal_action_server = MinimalActionServer()
    rclpy.spin(minimal_action_server)

if __name__ == '__main__':
    main()
```

## Action Client Implementation (rclpy)

An **action client** sends goals to an action server, handles feedback, and processes the final result.

```python
import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node

from example_interfaces.action import Fibonacci # Replace with your custom action

class MinimalActionClient(Node):
    def __init__(self):
        super().__init__('minimal_action_client')
        self._action_client = ActionClient(self, Fibonacci, 'fibonacci')
        self.get_logger().info('Action client ready.')

    def send_goal(self, order):
        self.get_logger().info('Waiting for action server...')
        self._action_client.wait_for_server()

        goal_msg = Fibonacci.Goal()
        goal_msg.order = order

        self.get_logger().info('Sending goal request...')
        self._send_goal_future = self._action_client.send_goal_async(goal_msg, feedback_callback=self.feedback_callback)
        self._send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected :(')
            return

        self.get_logger().info('Goal accepted :)')
        self._get_result_future = goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.get_result_callback)

    def get_result_callback(self, future):
        result = future.result().result
        self.get_logger().info(f'Result: {result.sequence}')
        rclpy.shutdown()

    def feedback_callback(self, feedback_msg):
        self.get_logger().info(f'Received feedback: {feedback_msg.feedback.sequence}')

def main(args=None):
    rclpy.init(args=args)
    action_client = MinimalActionClient()
    action_client.send_goal(10) # Request Fibonacci sequence of order 10
    rclpy.spin(action_client)

if __name__ == '__main__':
    main()
```

## Feedback and Result Handling

-   **Feedback**: The action server can publish progress updates at regular intervals, allowing the client to monitor the task's execution. This is essential for tasks like "navigate to a target" where the client might want to display the robot's current position along the path.
-   **Result**: Once the action server completes its task (or is preempted/canceled), it sends a single result message back to the client.

## Cancellation and Preemption

-   **Cancellation**: An action client can request the action server to stop its current goal execution. The server can then either gracefully abort the goal or acknowledge the cancellation.
-   **Preemption**: A new goal from a client might implicitly preempt an ongoing goal if the action server is configured to handle only one goal at a time.

## Use Case: `navigate_to_goal`

A perfect use case for actions is a navigation task, like `navigate_to_goal`.

-   An action client (e.g., a high-level autonomy system) sends a goal to the `navigation` action server, specifying a target pose.
-   The `navigation` action server begins planning and executing a path.
-   As the robot moves, the action server sends continuous **feedback** to the client, indicating the robot's current position, distance remaining, and any obstacles encountered.
-   If the robot reaches the goal, the server sends a **result** indicating success.
-   If the autonomy system decides to change the target or an emergency occurs, it can send a **cancellation request** to the action server.

This pattern provides a robust and flexible way to manage complex, long-duration robotic behaviors.
