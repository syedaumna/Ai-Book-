import rclpy
from rclpy.action import ActionServer
from rclpy.node import Node

from example_interfaces.action import Fibonacci

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
            
            # For demonstration, we just sleep
            import time
            time.sleep(1)

        goal_handle.succeed()
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
