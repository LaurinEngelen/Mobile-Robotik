__author__ = "Michael Blaich, Florian Drescher, Christopher Gogl"

import numpy as np
from exercise2.task2 import *


def test_joint_angles_for_circle_motion():
    km_r = (1, 0, 0.55, 1)
    radius = 0.25
    positions_in_circle = 25
    robot = Robot()

    expected_alphas = np.array([0., 0.086, 0.165, 0.231, 0.281, 0.311, 0.322, 0.311,
                                0.281, 0.231, 0.165, 0.086, 0., -0.086, -0.165, -0.231,
                                -0.281, -0.311, -0.322, -0.311, -0.281, -0.231, -0.165, -0.086,
                                -0.])
    expected_beta_1s = np.array([1.036, 1.032, 1.019, 0.999, 0.971, 0.938, 0.899, 0.859, 0.818,
                                 0.78, 0.75, 0.73, 0.723, 0.73, 0.75, 0.78, 0.818, 0.859,
                                 0.899, 0.938, 0.971, 0.999, 1.019, 1.032, 1.036])
    expected_beta_2s = np.array([-0.896, -0.907, -0.938, -0.986, -1.047, -1.116, -1.186, -1.255,
                                 -1.318, -1.371, -1.412, -1.437, -1.445, -1.437, -1.412, -1.371,
                                 -1.318, -1.255, -1.186, -1.116, -1.047, -0.986, -0.938, -0.907,
                                 -0.896])

    alphas, beta_1s, beta_2s = np.round(joint_angles_for_circle_motion(robot, km_r, radius, positions_in_circle), 3)

    assert np.array_equal(alphas, expected_alphas)
    assert np.array_equal(beta_1s, expected_beta_1s)
    assert np.array_equal(beta_2s, expected_beta_2s)
