__author__ = "Michael Blaich, Florian Drescher, Christopher Gogl"

# default imports
import time
import pytest
import unittest

# required launch imports
from launch import LaunchDescription
from launch_ros.actions import Node
from launch_testing.actions import ReadyToTest
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python import get_package_share_directory

# ROS imports
import rclpy
from nav_msgs.msg import Odometry, Path
from geometry_msgs.msg import PoseStamped, Pose, Twist

# additional packages import
import numpy as np
import os.path


@pytest.mark.rostest
def generate_test_description():
    follow_config = os.path.join(
        get_package_share_directory('my_diffdrive_kinematics'), 'config', 'follower_config.yaml')
    path_config = os.path.join(
        get_package_share_directory('exercise4_tests'), 'config', 'default_path.yaml')

    line_follower_node = Node(
        package='my_diffdrive_kinematics',
        executable='line_follower',
        name='line_follower_node',
        parameters=[follow_config]
    )
    generate_path_node = Node(
        package='my_diffdrive_kinematics',
        executable='generate_path',
        name='generate_path_node',
        parameters=[path_config]
    )
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('turtlebot3_gazebo'), 'launch', 'empty_world.launch.py')])
    )
    return (
        LaunchDescription([
            line_follower_node,
            generate_path_node,
            gazebo,
            ReadyToTest(),
        ]),
        {
        }
    )


def distance(current_pose: Pose, target_pose: PoseStamped):
    dx = current_pose.position.x - target_pose.pose.position.x
    dy = current_pose.position.y - target_pose.pose.position.y
    return np.sqrt(dx ** 2 + dy ** 2)


class TestLineFollowerNode(unittest.TestCase):
    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)
        self.path_msg_rec = None

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
        self.node = rclpy.create_node('test_line_follower')
        self.dist_to_path_threshold = 0.3
        self.path_following_success_threshold = 0.7
        self.d_star = 0.5

    def tearDown(self):
        self.node.destroy_node()

    def path_callback(self, msg: Path):
        if self.path_msg_rec is None:
            self.path_msg_rec = msg
            self.node.destroy_subscription(self.path_subscriber)

    def test_line_follower(self, launch_service, proc_output):
        odom_msgs_rec_buffer: list[Odometry] = []
        twist_msgs_rec_buffer: list[Twist] = []
        self.path_msg_rec: Path = None
        stop_flag = False

        odom_subscriber = self.node.create_subscription(
            Odometry,
            'odom',
            lambda msg: odom_msgs_rec_buffer.append(msg),
            10
        )
        self.path_subscriber = self.node.create_subscription(
            Path,
            'path',
            self.path_callback,
            10
        )
        cmd_vel_subscriber = self.node.create_subscription(
            Twist,
            'cmd_vel',
            lambda msg: twist_msgs_rec_buffer.append(msg),
            10
        )

        try:
            end_time = time.time() + 120
            while time.time() < end_time:
                # Allow test to run for 120 seconds
                rclpy.spin_once(self.node, timeout_sec=30)
                if len(twist_msgs_rec_buffer) > 0:
                    latest_twist_msg = twist_msgs_rec_buffer[-1]
                    if latest_twist_msg.linear.x == 0 and latest_twist_msg.angular.z == 0:
                        # wait for node to send stop twist msg
                        stop_flag = True
                        break

            self.assertTrue(
                stop_flag, "Did not receive a stop command within 120. "
                           "Make sure the line follower sent a stop message "
                           "after reaching the path's end.")
            # Test for a received path msg
            self.assertGreater(len(odom_msgs_rec_buffer), 0,
                               "Did not receive any odom messages. "
                               "Please make sure that odom messages are published to the topic "
                               "'odom' continuously.")

            self.assertIsNotNone(self.path_msg_rec, "Did not receive any path messages. "
                                                    "Please make sure that path messages "
                                                    "are published to the topic"
                                                    "'path' continuously.")

            matched_path_points = 0
            for pose in self.path_msg_rec.poses:
                pose: PoseStamped = pose
                path_position = pose.pose.position
                for odom in odom_msgs_rec_buffer:
                    odom_position = odom.pose.pose.position
                    d = np.sqrt((path_position.x - odom_position.x) ** 2
                                + (path_position.y - odom_position.y) ** 2)
                    if (d < self.dist_to_path_threshold):
                        matched_path_points += 1
                        break

            path_share_in_tolerance = float(
                matched_path_points) / len(self.path_msg_rec.poses)
            self.assertGreaterEqual(path_share_in_tolerance, self.path_following_success_threshold,
                                    "Robot did not follow path accuratly enough. "
                                    "Only %lf%% were reached with distance of %lf or closer. "
                                    "Try to adjust linear and angular velocity gain. "
                                    "Requirement: %lf%%" %
                                    (path_share_in_tolerance * 100,
                                     self.dist_to_path_threshold,
                                     self.path_following_success_threshold * 100))

            dist_target = distance(odom_msgs_rec_buffer[-1].pose.pose,
                                   self.path_msg_rec.poses[-1])
            dist_limit = self.d_star + 0.1
            self.assertLessEqual(dist_target, dist_limit, "Robot stopped to far away "
                                 "from goal position: " + str(dist_target) +
                                 ". Max allowed distance to path's end is: " + str(dist_limit))

        finally:
            self.node.destroy_subscription(odom_subscriber)
            self.node.destroy_subscription(self.path_subscriber)
            self.node.destroy_subscription(cmd_vel_subscriber)
