from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():

    turtlesim_node = Node(
        package='turtlesim',
        executable='turtlesim_node',
        name='turtlesim'
    )

    bridge_node = Node(
        package='gazebo_turtle_bridge',
        executable='cmd_vel_bridge',
        name='cmd_vel_bridge',
        parameters=[
            {'linear_scale': 1.0},
            {'angular_scale': 1.0}
        ]
    )

    return LaunchDescription([
        turtlesim_node,
        bridge_node
    ])

