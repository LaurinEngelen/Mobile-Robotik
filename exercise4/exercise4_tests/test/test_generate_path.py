__author__ = "Michael Blaich, Florian Drescher, Christopher Gogl"

# default imports
import pytest
import unittest

# required launch imports
from launch import LaunchDescription
from launch_ros.actions import Node
from launch_testing.actions import ReadyToTest
from ament_index_python import get_package_share_directory

# ROS imports
import rclpy
from nav_msgs.msg import Path
from geometry_msgs.msg import PoseStamped

# additional packages import
import numpy as np
import os.path

distance_between_path_points = 0.1
distance_between_path_upper_tolerance = 0.05


@pytest.mark.rostest
def generate_test_description():
    path_config = os.path.join(
        get_package_share_directory('exercise4_tests'), 'config', 'default_path.yaml')

    generate_path_node = Node(
        package='my_diffdrive_kinematics',
        executable='generate_path',
        name='generate_path_node',
        parameters=[path_config]
    )

    return (
        LaunchDescription([
            generate_path_node,
            ReadyToTest(),
        ]),
        {
        }
    )


class TestGeneratePath(unittest.TestCase):
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
        self.node = rclpy.create_node('test_generate_path')

    def tearDown(self):
        self.node.destroy_node()

    def test_straight_drive(self, launch_service, proc_output):
        path_msgs_rec_buffer: list[Path] = []

        path_xs = [0.0, 2.0, 3.0, 4.0]
        path_ys = [0.5, 0.5, 1.5, 1.5]
        base_path_content_included = {}

        for i in range(len(path_xs)):
            base_path_content_included[i] = False

        path_subscriber = self.node.create_subscription(
            Path,
            'path',
            lambda msg: path_msgs_rec_buffer.append(msg),
            10
        )

        try:
            # Allow test to run for 30 seconds
            rclpy.spin_once(self.node, timeout_sec=30)

            # Test for a received path msg
            self.assertEqual(len(path_msgs_rec_buffer), 1,
                             "Did not receive any path messages. "
                             "Please make sure that path messages are published to the topic "
                             "'path' continuously.")

            # Test path contents
            path = path_msgs_rec_buffer[0]
            base_path_idx = 0
            for i in range(len(path.poses) - 1):
                current: PoseStamped = path.poses[i]
                if np.round(path_xs[base_path_idx], 3) == current.pose.position.x and \
                        np.round(path_ys[base_path_idx], 3) == current.pose.position.y:
                    # Base path step is included
                    base_path_content_included[base_path_idx] = True
                    base_path_idx += 1

                # Check distance
                next: PoseStamped = path.poses[i + 1]
                x_a = current.pose.position.x
                y_a = current.pose.position.y
                x_b = next.pose.position.x
                y_b = next.pose.position.y

                d = np.sqrt((x_a - x_b) ** 2 + (y_a - y_b) ** 2)
                upper_bound = distance_between_path_points + \
                    distance_between_path_upper_tolerance

                self.assertLessEqual(d, upper_bound,
                                     "Distance of position at index " +
                                     str(i) + " to the next position in the path "
                                              "was greater than upper tolerance " +
                                     str(upper_bound) + ". "
                                                        "x,y of current idx: (" + str(x_a) +
                                     "," + str(y_a) + "); "
                                                      "x,y of next idx: (" + str(x_b) +
                                     "," + str(y_b) + ")")
                self.assertNotAlmostEqual(d, 0, 3,
                                          "Position at index " +
                                          str(i) +
                                          " is equal to the next position."
                                          " The path contains duplicate positions")

            if np.round(path_xs[base_path_idx], 3) == path.poses[i + 1].pose.position.x and \
                    np.round(path_ys[base_path_idx], 3) == path.poses[i + 1].pose.position.y:
                # Base path step is included
                base_path_content_included[base_path_idx] = True
                base_path_idx += 1

            # Check if base path is included in received path
            for idx in base_path_content_included.keys():
                self.assertTrue(base_path_content_included[idx],
                                "The point at index " +
                                str(idx) +
                                " from the base path in the default_path.yaml "
                                "is not included in the received path")

        finally:
            self.node.destroy_subscription(path_subscriber)
