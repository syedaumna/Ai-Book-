# Services: Request-Response Communication

While topics are excellent for streaming, asynchronous data, many robotic tasks require a direct **request-response** interaction. This is where **ROS 2 services** come in. Services are ideal for situations where a client needs to make a specific request to a server and wait for a single, direct response.

## When Topics Are Not Enough (Request-Response Patterns)

Consider scenarios where you need:

-   **Immediate Confirmation**: A client needs to know immediately if its request was processed successfully.
-   **Specific Computation**: A client asks a server to perform a computation and return the result (e.g., "calculate inverse kinematics," "localize robot").
-   **Parameter Retrieval/Setting**: A client queries a node for its current configuration or sends a command to change it (though ROS 2 parameters offer a more specialized mechanism for this).
-   **One-Shot Interactions**: The client initiates an interaction that has a clear beginning and end, and expects a single reply.

Topics, being asynchronous and stream-based, are not well-suited for these types of interactions because they don't provide a direct way to associate a response with a specific request.

## Services vs. Topics Comparison

Here's a comparison to help you decide when to use a service versus a topic:

| Feature           | Topics (Publish-Subscribe)                               | Services (Request-Response)                                |
| :---------------- | :------------------------------------------------------- | :--------------------------------------------------------- |
| **Communication** | Asynchronous, one-to-many, streaming                   | Synchronous, one-to-one, one-shot interaction              |
| **Data Flow**     | Continuous stream of messages                            | Single request message, single response message            |
| **Use Case**      | Sensor data, odometry, video streams, joint states       | Querying data, triggering actions, configuration changes   |
| **Feedback**      | No direct feedback for individual messages             | Direct response confirms success/failure, returns data     |
| **Latency**       | Optimized for low latency, high throughput (best-effort) | Can have higher latency due to synchronous blocking nature |

## Service Definition Syntax (`.srv` files)

Just like messages, services require a definition that specifies the structure of the request and response parts. Service definitions are stored in `.srv` files within the `srv/` directory of a ROS 2 package.

A `.srv` file is divided into two parts by a `---` separator:

-   **Above `---`**: Defines the request message fields.
-   **Below `---`**: Defines the response message fields.

Example: `AddTwoInts.srv`

```
# AddTwoInts.srv
int64 a
int64 b
---
int64 sum
```

This service takes two `int64` values (`a` and `b`) as a request and returns a single `int64` value (`sum`) as a response.

## Service Server Implementation (rclpy)

A **service server** is a node that "advertises" a service. It listens for incoming requests, performs the requested operation, and sends back a response.

```python
import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts # Replace with your custom service

class MinimalService(Node):
    def __init__(self):
        super().__init__('minimal_service')
        # Create a service server
        # arguments: service type, service name, callback function
        self.srv = self.create_service(AddTwoInts, 'add_two_ints', self.add_two_ints_callback)
        self.get_logger().info('Service server ready.')

    def add_two_ints_callback(self, request, response):
        # Process the request
        response.sum = request.a + request.b
        self.get_logger().info(f'Incoming request: a={request.a}, b={request.b}')
        self.get_logger().info(f'Sending response: sum={response.sum}')
        return response

def main(args=None):
    rclpy.init(args=args)
    minimal_service = MinimalService()
    rclpy.spin(minimal_service)
    minimal_service.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## Service Client Implementation (rclpy)

A **service client** is a node that "calls" a service. It sends a request to a service server and blocks (or uses asynchronous calls) until it receives a response.

```python
import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts # Replace with your custom service

class MinimalClientAsync(Node):
    def __init__(self):
        super().__init__('minimal_client_async')
        # Create a service client
        # arguments: service type, service name
        self.cli = self.create_client(AddTwoInts, 'add_two_ints')
        
        # Wait until the service is available
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting again...')
        
        self.req = AddTwoInts.Request()

    def send_request(self, a, b):
        self.req.a = a
        self.req.b = b
        # Call the service asynchronously
        self.future = self.cli.call_async(self.req)
        rclpy.spin_until_future_complete(self, self.future) # Blocks until response is received
        return self.future.result()

def main(args=None):
    rclpy.init(args=args)
    minimal_client = MinimalClientAsync()
    response = minimal_client.send_request(int(sys.argv[1]), int(sys.argv[2]))
    minimal_client.get_logger().info(
        f'Result of add_two_ints: for {sys.argv[1]} + {sys.argv[2]} = {response.sum}'
    )
    minimal_client.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 3:
        print('Usage: minimal_client_async <int> <int>')
    else:
        main()
```

## Synchronous and Asynchronous Service Calls

-   **Synchronous Calls**: The client sends a request and immediately waits (blocks) for the response. This is simpler to program but can halt other operations of the node.
-   **Asynchronous Calls**: The client sends a request and continues with other tasks. When the response arrives, a callback function is triggered. This is more complex but allows for more responsive and parallel processing within a single node. The `rclpy.spin_until_future_complete` call in the client example above effectively makes the asynchronous call behave synchronously for demonstration purposes.

## Error Handling and Timeouts

-   **Timeouts**: Clients should always implement timeouts when calling services. If a server is down or unresponsive, the client shouldn't block indefinitely.
-   **Error Responses**: Service definitions can include fields in the response to indicate errors or specific outcomes.
-   **Service Not Available**: Clients should check if a service server is available before attempting to call it (e.g., `wait_for_service`).

## Use Case: Motion Planning Service

For a humanoid robot, a common use case for services is a **motion planning service**.

-   A client (e.g., a high-level task manager) sends a request to the `motion_planner` service.
-   The request might include the robot's current pose, a desired target pose, and constraints.
-   The `motion_planner` server computes a safe and collision-free trajectory for the robot to move from the current pose to the target pose.
-   The server then returns the computed trajectory as the response to the client.

This allows the planning logic to be encapsulated in a separate, dedicated node, which can be swapped out or updated independently without affecting the rest of the system.
