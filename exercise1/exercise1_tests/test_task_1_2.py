from exercise1.task_1_2 import *


# Task 2.1 from lecture
def test_exercise_21_a_t_ab():
    """
    Tests the result of exercise_21_a_t_ab() against the correct solution for T^A_B from the lecture.
    """
    result = exercise_21_a_t_ab().round(3)
    expected = np.array([
                [-1, 0, 0, -2],
                [0, -1, 0, 0],
                [0, 0, 1, 0],
                [0, 0, 0, 1]])
    assert np.array_equal(result, expected), "Arrays are not equal.\n\nExpected:\n{}\n\nGot:\n{}".format(
        "\n".join(["  " + str(row) for row in expected]),
        "\n".join(["  " + str(row) for row in result])
    )

def test_exercise_21_a_t_bc():
    """
    Tests the result of exercise_21_a_t_bc() against the correct solution for T^B_C from the lecture.
    """
    assert False

def test_exercise_21_a_t_ac():
    """
    Tests the result of exercise_21_a_t_ac() against the correct solution for T^A_C from the lecture.
    """
    assert False


def test_exercise_21_b_t_ac():
    """
    Tests the result of exercise_21_b_t_ac() against the correct solution for T^A_C from exercise_21_a_t_ac().
    """
    assert False


def test_exercise_21_c_t_ca():
    """
    Tests the result of exercise_21_c_t_ca() against the correct solution for T^C_A from the lecture.
    """
    assert False


def test_exercise_21_d():
    """
    Tests the result of exercise_21_d() against the correct solution for p^A from the lecture.
    The argument p^B of exercise_21_d() must not be in homogenous coordinates, as well as p^A.
    """
    assert False
