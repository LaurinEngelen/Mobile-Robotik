__author__ = "Michael Blaich, Florian Drescher, Christopher Gogl"

# default imports
import time
import pytest
import unittest

# required launch imports
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch_ros.actions import Node
from launch_testing.actions import ReadyToTest
from ament_index_python import get_package_share_directory
from launch.launch_description_sources import PythonLaunchDescriptionSource

# ROS imports
import rclpy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry

# additional packages import
import numpy as np
import os.path

robot_velocity = 0.25
robot_target_distance = 1.0


@pytest.mark.rostest
def generate_test_description():
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('turtlebot3_gazebo'), 'launch', 'empty_world.launch.py')])
    )

    straight_drive_node = Node(
        package='my_diffdrive_kinematics',
        executable='straight_drive',
        prefix=['bash -c \'sleep 10; $0 $@\''],
        # parameters=[{"v": str(robot_velocity), "distance": str(robot_target_distance)}]
        arguments=['--ros-args -p v:=0.25 -p distance:=1.0']
    )
    return (
        LaunchDescription([
            gazebo,
            straight_drive_node,
            ReadyToTest(),
        ]),
        {
        }
    )


class TestStraightDriveNode(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Initialize the ROS context for the test node
        rclpy.init()

    @classmethod
    def tearDownClass(cls):
        # Shutdown the ROS context
        rclpy.shutdown()

    def setUp(self):
        # Create a ROS node for tests
        self.node = rclpy.create_node('test_straight_drive')

    def tearDown(self):
        self.node.destroy_node()

    def test_straight_drive(self, launch_service, proc_output):
        twist_msgs_rec_buffer: list[Twist] = []
        odom_msgs_rec_buffer: list[Odometry] = []

        twist_subscriber = self.node.create_subscription(
            Twist,
            'cmd_vel',
            lambda msg: twist_msgs_rec_buffer.append(msg),
            10
        )

        odom_subscriber = self.node.create_subscription(
            Odometry,
            'odom',
            lambda msg: odom_msgs_rec_buffer.append(msg),
            10
        )

        try:
            # Allow test to run for 60 seconds
            robot_move_start = False
            robot_move_start_position = None
            robot_move_stop = False
            robot_move_stop_position = None
            robot_move_stop_twist_msg = None
            end_time = time.time() + 60
            while time.time() < end_time:
                rclpy.spin_once(self.node, timeout_sec=30)
                if not robot_move_start:
                    if len(odom_msgs_rec_buffer) > 0 and len(twist_msgs_rec_buffer) > 0:
                        # wait for node to send drive twist msg
                        if twist_msgs_rec_buffer[-1].linear.x > 0:
                            robot_move_start_position = odom_msgs_rec_buffer[-1].pose.pose.position
                            robot_move_start = True
                    continue

                latest_twist_msg = twist_msgs_rec_buffer[-1]
                if latest_twist_msg.linear.x == 0:
                    # wait for node to send stop twist msg
                    robot_move_stop_position = odom_msgs_rec_buffer[-1].pose.pose.position
                    robot_move_stop_twist_msg = latest_twist_msg
                    robot_move_stop = True
                    break

                # test for correct twist msg content
                self.assertEqual(latest_twist_msg.linear.x, robot_velocity,
                                 "\033[0;31m Robot's target linear x-velocity "
                                 "does not match expected velocity\033[0m")
                self.assertEqual(latest_twist_msg.linear.y, 0,
                                 "\033[0;31m Robot's target linear y-velocity "
                                 "does not match expected velocity\033[0m")
                self.assertEqual(latest_twist_msg.linear.z, 0,
                                 "\033[0;31m Robot's target linear z-velocity "
                                 "does not match expected velocity\033[0m")

                self.assertEqual(latest_twist_msg.angular.x, 0,
                                 "\033[0;31m Robot's target angular x-velocity "
                                 "does not match expected velocity\033[0m")
                self.assertEqual(latest_twist_msg.angular.y, 0,
                                 "\033[0;31m Robot's target angular y-velocity "
                                 "does not match expected velocity\033[0m")
                self.assertEqual(latest_twist_msg.angular.z, 0,
                                 "\033[0;31m Robot's target angular z-velocity "
                                 "does not match expected velocity\033[0m")

            # Test for correct node behaviour
            # Test for robot move start
            self.assertTrue(robot_move_start,
                            "\033[0;31m Did not receive twist messages to start robot movement. " +
                            "Please make sure that twist messages are published to the topic " +
                            "'cmd_vel' continuously.\033[0m")

            # Test for stop and stop message
            self.assertTrue(
                robot_move_stop, "\033[0;31m Did not recieve any twist message to stop the robot\033[0m")
            self.assertEqual(robot_move_stop_twist_msg.linear.x, 0,
                             "\033[0;31m Robot's stop linear x-velocity does not match expected velocity\033[0m")
            self.assertEqual(robot_move_stop_twist_msg.linear.y, 0,
                             "\033[0;31m Robot's stop linear y-velocity does not match expected velocity\033[0m")
            self.assertEqual(robot_move_stop_twist_msg.linear.z, 0,
                             "\033[0;31m Robot's stop linear z-velocity does not match expected velocity\033[0m")

            self.assertEqual(robot_move_stop_twist_msg.angular.x, 0,
                             "\033[0;31m Robot's stop angular x-velocity does not match expected velocity\033[0m")
            self.assertEqual(robot_move_stop_twist_msg.angular.y, 0,
                             "\033[0;31m Robot's stop angular y-velocity does not match expected velocity\033[0m")
            self.assertEqual(robot_move_stop_twist_msg.angular.z, 0,
                             "\033[0;31m Robot's stop angular z-velocity does not match expected velocity\033[0m")

            # Test for correct distance
            stop_distance = np.sqrt(
                (robot_move_stop_position.x - robot_move_start_position.x) ** 2 +
                (robot_move_stop_position.y - robot_move_start_position.y) ** 2 +
                (robot_move_stop_position.z - robot_move_start_position.z) ** 2)
            distance_tol_min = robot_target_distance - 0.1
            distance_tol_max = robot_target_distance + 0.1
            self.assertTrue(distance_tol_min <= stop_distance <= distance_tol_max,
                            "\033[0;31m Robot did not stop between " + str(distance_tol_min) +
                            " and " + str(distance_tol_max) + " m. \033[0m")

            # Test if straight_drive exited
            # self.assertNotIn("straight_drive", self.node.get_node_names(),
            #            "Node 'straight_drive' did not exit after sending stop command to robot")

        finally:
            self.node.destroy_subscription(twist_subscriber)
            self.node.destroy_subscription(odom_subscriber)
