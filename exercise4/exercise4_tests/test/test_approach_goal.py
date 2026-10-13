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
import os.path

robot_velocity_max = 0.25
robot_omega_max = 2.5
robot_tolerance = 0.1
robot_target_x = 1.5
robot_target_y = 1.0


@pytest.mark.rostest
def generate_test_description():
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('turtlebot3_gazebo'), 'launch', 'empty_world.launch.py')])
    )

    aproach_goal_node = Node(
        package='my_diffdrive_kinematics',
        executable='approach_goal',
        prefix=['bash -c \'sleep 10; $0 $@\''],
        # parameters=[{"v": str(robot_velocity), "distance": str(robot_target_distance)}]
        arguments=['--ros-args -p x:=1.5 -p y:=1.0 -p tol:=0.1 -p v_max:=0.25 -p omega_max:=2.5']
    )

    return (
        LaunchDescription([
            gazebo,
            aproach_goal_node,
            ReadyToTest(),
        ]),
        {
        }
    )


class TestApproachGoal(unittest.TestCase):
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
        self.node = rclpy.create_node('test_approach_goal')

    def tearDown(self):
        self.node.destroy_node()

    def test_approach_goal(self, launch_service, proc_output):
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
            robot_move_stop = False
            robot_move_stop_position = None
            robot_move_stop_twist_msg = None
            end_time = time.time() + 120
            while time.time() < end_time:
                rclpy.spin_once(self.node, timeout_sec=30)
                if not robot_move_start:
                    if len(odom_msgs_rec_buffer) > 0 and len(twist_msgs_rec_buffer) > 0:
                        # wait for node to send drive twist msg
                        if twist_msgs_rec_buffer[-1].linear.x > 0:
                            robot_move_start = True
                    continue

                latest_twist_msg = twist_msgs_rec_buffer[-1]
                if latest_twist_msg.linear.x == 0 and latest_twist_msg.angular.z == 0:
                    # wait for node to send stop twist msg
                    robot_move_stop_position = odom_msgs_rec_buffer[-1].pose.pose.position
                    robot_move_stop_twist_msg = latest_twist_msg
                    robot_move_stop = True
                    break

                # test for correct twist msg content
                self.assertLessEqual(latest_twist_msg.linear.x, robot_velocity_max,
                                     "Robot's target linear x-velocity"
                                     " exceeds the given maximum velocity")
                self.assertEqual(latest_twist_msg.linear.y, 0,
                                 "Robot's target linear y-velocity"
                                 " does not match expected velocity")
                self.assertEqual(latest_twist_msg.linear.z, 0,
                                 "Robot's target linear z-velocity"
                                 " does not match expected velocity")

                self.assertEqual(latest_twist_msg.angular.x, 0,
                                 "Robot's target angular x-velocity"
                                 " does not match expected velocity")
                self.assertEqual(latest_twist_msg.angular.y, 0,
                                 "Robot's target angular y-velocity"
                                 " does not match expected velocity")
                self.assertLessEqual(latest_twist_msg.angular.z, robot_omega_max,
                                     "Robot's target angular z-velocity"
                                     " exceeds the given maximum velocity")

            # Test for correct node behaviour
            # Test for robot move start
            self.assertTrue(robot_move_start,
                            "Did not receive twist messages to start robot movement. " +
                            "Please make sure that twist messages are published to the topic " +
                            "'cmd_vel' continuously.")

            # Test for stop and stop message
            self.assertTrue(
                robot_move_stop, "Did not recieve any twist message to stop the robot")
            self.assertEqual(robot_move_stop_twist_msg.linear.x, 0,
                             "Robot's stop linear x-velocity does not match expected velocity")
            self.assertEqual(robot_move_stop_twist_msg.linear.y, 0,
                             "Robot's stop linear y-velocity does not match expected velocity")
            self.assertEqual(robot_move_stop_twist_msg.linear.z, 0,
                             "Robot's stop linear z-velocity does not match expected velocity")

            self.assertEqual(robot_move_stop_twist_msg.angular.x, 0,
                             "Robot's stop angular x-velocity does not match expected velocity")
            self.assertEqual(robot_move_stop_twist_msg.angular.y, 0,
                             "Robot's stop angular y-velocity does not match expected velocity")
            self.assertEqual(robot_move_stop_twist_msg.angular.z, 0,
                             "Robot's stop angular z-velocity does not match expected velocity")

            # Test for correct distance
            target_tol_min_x = robot_target_x - robot_tolerance
            target_tol_max_x = robot_target_x + robot_tolerance
            target_tol_min_y = robot_target_y - robot_tolerance
            target_tol_max_y = robot_target_y + robot_tolerance
            self.assertTrue(target_tol_min_x <= robot_move_stop_position.x <= target_tol_max_x,
                            "Robot did not stop in expected x Tolerance: " +
                            str(target_tol_min_x) + " and " + str(target_tol_max_x))
            self.assertTrue(target_tol_min_y <= robot_move_stop_position.y <= target_tol_max_y,
                            "Robot did not stop in expected y Tolerance: " +
                            str(target_tol_min_y) + " and " + str(target_tol_max_y))

        finally:
            self.node.destroy_subscription(twist_subscriber)
            self.node.destroy_subscription(odom_subscriber)
