import rclpy
from rclpy.node import Node
from rclpy.lifecycle import LifecycleNode, State, TransitionCallbackReturn
from std_msgs.msg import String
import time

class LoggingAndLifecycleNode(LifecycleNode):
    def __init__(self):
        super().__init__('logging_and_lifecycle_node')
        self.publisher_ = None
        self.timer_ = None
        self.count = 0
        self.get_logger().info('Node created in unconfigured state.')

    def on_configure(self, state: State) -> TransitionCallbackReturn:
        self.get_logger().info('Transitioning to "configuring": Loading parameters and setting up resources.')
        # Example: Declare parameters
        self.declare_parameter('message_prefix', 'Hello from Lifecycle Node: ')
        self.message_prefix = self.get_parameter('message_prefix').value

        # Example: Create publisher and timer
        self.publisher_ = self.create_publisher(String, 'lifecycle_topic', 10)
        self.timer_ = self.create_timer(1.0, self.publish_message)
        self.get_logger().info('Publisher and timer created. Now in inactive state.')
        return TransitionCallbackReturn.SUCCESS

    def on_activate(self, state: State) -> TransitionCallbackReturn:
        self.get_logger().info('Transitioning to "activating": Starting data flow and operations.')
        # Activate components (e.g., start hardware, enable timers)
        # It's good practice to call super().on_activate(state) for proper lifecycle management
        super().on_activate(state)
        self.get_logger().info('Node activated. Now in active state.')
        return TransitionCallbackReturn.SUCCESS

    def on_deactivate(self, state: State) -> TransitionCallbackReturn:
        self.get_logger().info('Transitioning to "deactivating": Stopping data flow and operations.')
        # Deactivate components (e.g., stop timers, disable hardware)
        self.get_logger().info('Node deactivated. Now in inactive state.')
        return TransitionCallbackReturn.SUCCESS

    def on_cleanup(self, state: State) -> TransitionCallbackReturn:
        self.get_logger().info('Transitioning to "cleaning up": Releasing resources.')
        # Destroy publishers, timers, and release resources
        if self.publisher_:
            self.destroy_publisher(self.publisher_)
        if self.timer_:
            self.destroy_timer(self.timer_)
        self.get_logger().info('Resources cleaned up. Now in unconfigured state.')
        return TransitionCallbackReturn.SUCCESS

    def on_shutdown(self, state: State) -> TransitionCallbackReturn:
        self.get_logger().fatal('Transitioning to "shutting down": Performing final cleanup.')
        # Final cleanup tasks
        self.get_logger().fatal('Node shut down.')
        return TransitionCallbackReturn.SUCCESS

    def publish_message(self):
        if self.publisher_ and self.get_current_state().label == 'active':
            msg = String()
            msg.data = f'{self.message_prefix}{self.count}'
            self.publisher_.publish(msg)
            self.get_logger().info(f'Published: "{msg.data}"')
            self.count += 1
            if self.count % 5 == 0:
                self.get_logger().warn('This is a warning from the active state.')
            if self.count % 10 == 0:
                self.get_logger().error('This is an error from the active state.')
        else:
            self.get_logger().debug('Not publishing, node not active.')

def main(args=None):
    rclpy.init(args=args)
    node = LoggingAndLifecycleNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
