__author__ = "Michael Blaich, Florian Drescher, Christopher Gogl"

import numpy as np
from exercise2.task2 import *

# Test for Task 2.1
def test_forward_kinematics2_1():
    robot = Robot()
    result = robot.forward_kinematics(np.radians(40), np.radians(30), np.radians(-10)).round(3)
    expected = (2.525, 1.973, 0.821, 1.000)
    assert np.array_equal(result, expected)

# Further tests for specific arm positions
def test_forward_kinematics_arm_forward():
    robot = Robot(x_r=0, y_r=0, theta=0)
    result = robot.forward_kinematics(np.radians(0), np.radians(0), np.radians(0)).round(3)
    expected = (1.250, 0.000, 0.400, 1.000)
    assert np.array_equal(result, expected)


def test_forward_kinematics_arm_backward_theta():
    robot = Robot(x_r=0, y_r=0, theta=0)
    result = robot.forward_kinematics(np.radians(180), np.radians(0), np.radians(0)).round(3)
    expected = (-0.750, 0.000, 0.400, 1.000)
    assert np.array_equal(result, expected)


def test_forward_kinematics_arm_backward_beta1():
    robot = Robot(x_r=0, y_r=0, theta=0)
    result = robot.forward_kinematics(np.radians(0), np.radians(180), np.radians(0)).round(3)
    expected = (-0.750, 0.000, 0.400, 1.000)
    assert np.array_equal(result, expected)


def test_forward_kinematics_arm_upward():
    robot = Robot(x_r=0, y_r=0, theta=0)
    result = robot.forward_kinematics(np.radians(0), np.radians(90), np.radians(0)).round(3)
    expected = (0.250, 0.000, 1.400, 1.000)
    assert np.array_equal(result, expected)


def test_forward_kinematics_arm_bent_forward():
    robot = Robot(x_r=0, y_r=0, theta=0)
    result = robot.forward_kinematics(np.radians(0), np.radians(90), np.radians(-90)).round(3)
    expected = (0.750, 0.000, 0.900, 1.000)
    assert np.array_equal(result, expected)


def test_forward_kinematics_arm_bent_backward_theta():
    robot = Robot(x_r=0, y_r=0, theta=0)
    result = robot.forward_kinematics(np.radians(180), np.radians(90), np.radians(-90)).round(3)
    expected = (-0.250, 0.000, 0.900, 1.000)
    assert np.array_equal(result, expected)


def test_forward_kinematics_arm_bent_backward_beta2():
    robot = Robot(x_r=0, y_r=0, theta=0)
    result = robot.forward_kinematics(np.radians(0), np.radians(90), np.radians(90)).round(3)
    expected = (-0.250, 0.000, 0.900, 1.000)
    assert np.array_equal(result, expected)

# Extend the tests with more arm position if needed.
