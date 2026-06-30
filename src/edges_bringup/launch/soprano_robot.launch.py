# ============================================================================
# Name        : soprano_robot.launch.py
# Author      : Abubakr Mukhtar
# Description : Launches Soprano robot in Gazebo with RViz, controllers, and teleop
# ROS 2       : Humble
# ============================================================================

from launch import LaunchDescription
from launch.actions import ExecuteProcess, TimerAction
from launch_ros.actions import Node
from launch.substitutions import Command, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():

    ld = LaunchDescription()

    # ------------------- File paths -------------------
    robot_description_pkg = FindPackageShare('robot_description')
    bringup_pkg = FindPackageShare('edges_bringup')

    urdf_file = PathJoinSubstitution(
        [robot_description_pkg, 'urdf', 'soprano.urdf.xacro']
    )

    rviz_config_file = PathJoinSubstitution(
        [robot_description_pkg, 'rviz', 'rviz.rviz']
    )


    world_file = PathJoinSubstitution([
        FindPackageShare('robot_description'),
        'worlds',
        'edges_academy.world'
    ])

    controllers_yaml = PathJoinSubstitution(
        [bringup_pkg, 'config', 'diff_drive.yaml']
    )

    # ------------------- Robot description -------------------
    robot_description = ParameterValue(
        Command(['xacro ', urdf_file]),
        value_type=str
    )

    # ------------------- robot_state_publisher -------------------
    robot_state_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        parameters=[{
            'robot_description': robot_description,
            'use_sim_time': True
        }],
        output='screen'
    )

    # ------------------- Start Gazebo Server -------------------
    start_gzserver = ExecuteProcess(
        cmd=['gzserver', '--verbose', '-s', 'libgazebo_ros_init.so', '-s', 'libgazebo_ros_factory.so', world_file],
        output='screen'
    )
    # ------------------- Gazebo client (GUI) -------------------
    gzclient = ExecuteProcess(
        cmd=['gzclient'],
        output='screen'
    )

    # ------------------- Spawn robot in Gazebo -------------------
    spawn_robot = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=[
            '-topic', 'robot_description',
            '-entity', 'soprano_robot',
            '-x', '0.0',
            '-y', '0.0',
            '-z', '0.1',
            '-reference_frame', 'world'
        ],
        output='screen'
    )

    # ------------------- RViz -------------------
    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        arguments=['-d', rviz_config_file],
        parameters=[{'use_sim_time': True}],
        output='screen'
    )

    # ------------------- Teleop -------------------
    teleop_node = Node(
        package='teleop_twist_keyboard',
        executable='teleop_twist_keyboard',
        name='teleop_twist_keyboard',
        prefix='xterm -e',
        output='screen'
    )

    # ------------------- Add nodes to LaunchDescription -------------------
    ld.add_action(robot_state_node)
    ld.add_action(start_gzserver)
    ld.add_action(TimerAction(period=5.0, actions=[gzclient]))  # wait 5s before GUI
    ld.add_action(spawn_robot)
    ld.add_action(rviz_node)
    ld.add_action(teleop_node)

    return ld


