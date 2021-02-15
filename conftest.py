"""
conftest.py needed for pytest to detect files.
This also contains helper methods for running tests or autograders.
"""
import os

from stanfordkarel.karel_application import StudentCode
from stanfordkarel.karel_program import KarelProgram

PROBLEMS = [
    "checkerboard_karel",
    "collect_newspaper_karel",
    "midpoint_karel",
    "triple_karel",
    "stone_mason_karel",
]
STUDENT_CODE_DIR = "solutions"
TIMEOUT = 10


def execute_karel_code(code_file: str) -> None:
    module_name = os.path.basename(code_file)
    if module_name.endswith(".py"):
        module_name = os.path.splitext(module_name)[0]
    karel = KarelProgram(module_name)
    student_code = StudentCode(code_file)
    student_code.inject_namespace(karel)
    student_code.mod.main()  # type: ignore
    assert karel.compare_with(
        KarelProgram(f"{module_name}_end")
    ), "Resulting world did not match expected result."


def create_solution_worlds() -> None:
    for problem_name in PROBLEMS:
        karel = KarelProgram(problem_name)
        student_code = StudentCode(problem_name)
        student_code.inject_namespace(karel)
        student_code.mod.main()  # type: ignore
        karel.world.save_to_file(os.path.join("worlds", problem_name + "_end.w"))
