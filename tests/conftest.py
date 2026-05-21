"""
conftest.py needed for pytest to detect files.
This also contains helper methods for running tests or autograders.
"""

from pathlib import Path

from stanfordkarel.didyoumean import add_did_you_mean
from stanfordkarel.karel_executor import inject_karel_api
from stanfordkarel.karel_program import KarelException, KarelProgram
from stanfordkarel.student_code import StudentCode

PROBLEMS = (
    "checkerboard_karel",
    "collect_newspaper_karel",
    "midpoint_karel",
    "triple_karel",
    "stone_mason_karel",
)
STUDENT_CODE_DIR = Path("solutions")
TIMEOUT = 10


def execute_karel_code(
    code_file: Path, world_name: str = "", expected_error: str = ""
) -> None:
    world_name = world_name or code_file.stem
    karel = KarelProgram(world_name)
    try:
        student_code = StudentCode(code_file)
    except (SyntaxError, RuntimeError) as e:
        assert str(e) == expected_error  # noqa: PT017
        return

    inject_karel_api(student_code, karel)
    try:
        student_code.main()
        assert karel.compare_with(KarelProgram(f"{world_name}_end")), (
            "Resulting world did not match expected result."
        )
    except (KarelException, NameError) as e:
        add_did_you_mean(e)
        assert str(e) == expected_error  # noqa: PT017


def create_solution_worlds() -> None:
    for problem_name in PROBLEMS:
        karel = KarelProgram(problem_name)
        student_code = StudentCode(Path(f"problems/{problem_name}.py"))
        inject_karel_api(student_code, karel)
        student_code.main()
        karel.world.save_to_file(Path(f"worlds/{problem_name}_end.w"))
