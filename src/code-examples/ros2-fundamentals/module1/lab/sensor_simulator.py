import rclpy
from rclpy.node import Node
from std_msgs.msg import Header
from code_examples.ros2_fundamentals.module1.lab.msg import SensorData # Custom message

import random

class SensorSimulator(Node):
    def __init__(self):
        super().__init__('sensor_simulator')
        self.publisher_ = self.create_publisher(SensorData, 'sensor_data', 10)
        self.timer = self.create_timer(1.0, self.timer_callback) # Publish every 1 second
        self.get_logger().info('SensorSimulator Node started.')

    def timer_callback(self):
        msg = SensorData()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'sensor_frame'
        
        msg.temperature = random.uniform(20.0, 30.0)
        msg.humidity = random.uniform(40.0, 60.0)
        msg.position = [random.uniform(-1.0, 1.0), random.uniform(-1.0, 1.0), random.uniform(0.0, 2.0)]
        msg.velocity = [random.uniform(-0.1, 0.1), random.uniform(-0.1, 0.1), random.uniform(-0.1, 0.1)]

        self.publisher_.publish(msg)
        self.get_logger().info(f'Publishing sensor data: Temp={msg.temperature:.2f}, Humidity={msg.humidity:.2f}')

def main(args=None):
    rclpy.init(args=args)
    sensor_simulator = SensorSimulator()
    rclpy.spin(sensor_simulator)
    sensor_simulator.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
