"""
conftest.py needed for pytest to detect files.
This also contains helper methods for running tests or autograders.
"""
import os

from stanfordkarel.karel import Karel
from stanfordkarel.karel_application import StudentCode

PROBLEMS = [
    "checkerboard_karel",
    "collect_newspaper_karel",
    "midpoint_karel",
    "triple_karel",
    "stone_mason_karel",
]
STUDENT_CODE_DIR = "solutions"
TIMEOUT = 10


def execute_karel_code(code_file):
    module_name = os.path.basename(code_file)
    if module_name.endswith(".py"):
        module_name = os.path.splitext(module_name)[0]
    karel = Karel(module_name)
    student_code = StudentCode(code_file, karel)
    student_code.mod.main()
    assert karel.compare_with(
        Karel(f"{module_name}_end")
    ), "Resulting world did not match expected result."


def create_solution_worlds():
    for problem_name in PROBLEMS:
        karel = Karel(problem_name)
        student_code = StudentCode(problem_name, karel)
        student_code.mod.main()
        karel.world.save_to_file(os.path.join("worlds", problem_name + "_end.w"), karel)
