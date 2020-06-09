"""
To autograde a program, change the default directory used in execute_karel_code
to a folder with the student's implementation of the function.

"""
# import pytest

from conftest import execute_karel_code

STUDENT_CODE_DIR = "problems"
TIMEOUT = 30


# @pytest.mark.timeout(TIMEOUT)
def test_checkerboard_karel():
    execute_karel_code("checkerboard_karel", STUDENT_CODE_DIR)


# @pytest.mark.timeout(TIMEOUT)
def test_collect_newspaper_karel():
    execute_karel_code("collect_newspaper_karel", STUDENT_CODE_DIR)


# @pytest.mark.timeout(TIMEOUT)
def test_midpoint_karel():
    execute_karel_code("midpoint_karel", STUDENT_CODE_DIR)


# @pytest.mark.timeout(TIMEOUT)
def test_triple_karel():
    execute_karel_code("triple_karel", STUDENT_CODE_DIR)


# @pytest.mark.timeout(TIMEOUT)
def test_stone_mason_karel():
    execute_karel_code("stone_mason_karel", STUDENT_CODE_DIR)
