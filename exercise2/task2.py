__author__ = "Michael Blaich, Florian Drescher, Christopher Gogl"

import numpy as np
import matplotlib.pyplot as plt
from exercise1.transformations import *


class Robot:
    def __init__(self, x_r=2, y_r=1, theta=np.radians(30), l=0.6, h=0.2, r=0.1, a=0.1, b=0.1, l_1=0.5, l_2=0.5):
        self.x_r = x_r
        self.y_r = y_r
        self.theta = theta
        self.l = l
        self.h = h
        self.r = r
        self.a = a
        self.b = b
        self.l_1 = l_1
        self.l_2 = l_2

    # Exercise 2.1
    def forward_kinematics(self, alpha=np.radians(0), beta_1=np.radians(0), beta_2=np.radians(0)):
        p_a2 = (0, 0, 0, 1)
        pass

    # Exercise 2.2
    def inverse_kinematics(self, p_r):
        return alpha, beta_1, beta_2

# Exercise 2.3
def joint_angles_for_circle_motion(robot, km_r=(1, 0, 0.55, 1), radius=0.25, positions_in_circle=100):
    # positions_in_circle specifies how many points of the circle should be approached by the arm.
    # This function is not intended for plotting.
    # Instead, it calculates the progression of the joint angles.

    return alphas, beta_1s, beta_2s


def plot_angles(alphas, beta_1s, beta_2s, positions_in_circle=100):
    pass


def plot_circle(reached_points):
    pass


if __name__ == '__main__':
    # Create plots with regular execution. Everything else should be run within tests.
    plot_angles()

    plot_circle()

