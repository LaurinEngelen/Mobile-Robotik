import numpy as np
import exercise1.transformations


def test_rot():
    theta = np.pi
    result = exercise1.transformations.rot(theta).round(3)
    expected = np.array([
        [-1, 0],
        [0, -1]
    ]).round(3)
    assert np.array_equal(result, expected), "Arrays are not equal.\n\nExpected:\n{}\n\nGot:\n{}".format(
        "\n".join(["  " + str(row) for row in expected]),
        "\n".join(["  " + str(row) for row in result])
    )


def test_rotx():
    theta = np.pi
    result = exercise1.transformations.rotx(theta).round(3)
    expected = np.array([
        [1, 0, 0],
        [0, -1, 0],
        [0, 0, -1]
    ]).round(3)
    assert np.array_equal(result, expected), "Arrays are not equal.\n\nExpected:\n{}\n\nGot:\n{}".format(
        "\n".join(["  " + str(row) for row in expected]),
        "\n".join(["  " + str(row) for row in result])
    )


def test_roty():
    theta = np.pi
    result = exercise1.transformations.roty(theta).round(3)
    expected = np.array([
        [-1, 0, 0],
        [0, 1, 0],
        [-0, 0, -1]
    ]).round(3)
    assert np.array_equal(result, expected), "Arrays are not equal.\n\nExpected:\n{}\n\nGot:\n{}".format(
        "\n".join(["  " + str(row) for row in expected]),
        "\n".join(["  " + str(row) for row in result])
    )


def test_rotz():
    theta = np.pi
    result = exercise1.transformations.rotz(theta).round(3)
    expected = np.array([
        [-1, 0, 0],
        [0, -1, 0],
        [0, 0, 1]
    ]).round(3)
    assert np.array_equal(result, expected), "Arrays are not equal.\n\nExpected:\n{}\n\nGot:\n{}".format(
        "\n".join(["  " + str(row) for row in expected]),
        "\n".join(["  " + str(row) for row in result])
    )


def test_rot2trans_2D():
    r = np.identity(2)
    result = exercise1.transformations.rot2trans(r).round(3)
    expected = np.identity(3).round(3)
    assert np.array_equal(result, expected), "Arrays are not equal.\n\nExpected:\n{}\n\nGot:\n{}".format(
        "\n".join(["  " + str(row) for row in expected]),
        "\n".join(["  " + str(row) for row in result])
    )


def test_rot2trans_3D():
    r = np.identity(3)
    result = exercise1.transformations.rot2trans(r).round(3)
    expected = np.identity(4).round(3)
    assert np.array_equal(result, expected), "Arrays are not equal.\n\nExpected:\n{}\n\nGot:\n{}".format(
        "\n".join(["  " + str(row) for row in expected]),
        "\n".join(["  " + str(row) for row in result])
    )


def test_trans_2D():
    t = np.array([4, 5])  # depending on your implementation, t = (4, 5) may also be possible
    result = exercise1.transformations.trans(t).round(3)
    expected = np.array([
        [1, 0, 4],
        [0, 1, 5],
        [0, 0, 1]
    ]).round(3)
    assert np.array_equal(result, expected), "Arrays are not equal.\n\nExpected:\n{}\n\nGot:\n{}".format(
        "\n".join(["  " + str(row) for row in expected]),
        "\n".join(["  " + str(row) for row in result])
    )


def test_trans_3D():
    t = np.array([4, 5, 6])  # depending on your implementation, t = (4, 5, 6) may also be possible
    result = exercise1.transformations.trans(t).round(3)
    expected = np.array([
        [1, 0, 0, 4],
        [0, 1, 0, 5],
        [0, 0, 1, 6],
        [0, 0, 0, 1]
    ]).round(3)
    assert np.array_equal(result, expected), "Arrays are not equal.\n\nExpected:\n{}\n\nGot:\n{}".format(
        "\n".join(["  " + str(row) for row in expected]),
        "\n".join(["  " + str(row) for row in result])
    )