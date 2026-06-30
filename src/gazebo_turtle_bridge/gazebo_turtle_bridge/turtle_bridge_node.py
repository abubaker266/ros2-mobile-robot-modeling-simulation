#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist


class TurtuleBridgeNode(Node):
    def __init__(self):
        super().__init__('turtule_bridge_node')

        # parameters for scaling
        self.declare_parameter('linear_scale', 1.0)
        self.declare_parameter('angular_scale', 1.0)

        self.linear_scale = self.get_parameter('linear_scale').value
        self.angular_scale = self.get_parameter('angular_scale').value

        # subscribe to robot cmd_vel
        self.subscription = self.create_subscription(
            Twist,
            '/cmd_vel',
            self.cmd_vel_callback,
            10
        )

        # publish to turtlesim
        self.publisher = self.create_publisher(
            Twist,
            '/turtle1/cmd_vel',
            10
        )

        self.get_logger().info(
            'Turtule bridge node started: /cmd_vel → /turtle1/cmd_vel'
        )

    def cmd_vel_callback(self, msg):
        turtle_msg = Twist()
        turtle_msg.linear.x = msg.linear.x * self.linear_scale
        turtle_msg.angular.z = msg.angular.z * self.angular_scale
        self.publisher.publish(turtle_msg)


def main(args=None):
    rclpy.init(args=args)
    node = TurtuleBridgeNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

