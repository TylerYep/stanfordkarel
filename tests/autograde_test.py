from stanfordkarel.karel import Karel
from stanfordkarel.karel_application import StudentCode
from stanfordkarel.karel_world import KarelWorld

CODE_DIR = "solutions/"


def test_checkerboard_karel():
    execute_karel_code("checkerboard_karel")


def test_collect_newspaper_karel():
    execute_karel_code("collect_newspaper_karel")


def test_midpoint_karel():
    execute_karel_code("midpoint_karel")


def test_triple_karel():
    execute_karel_code("triple_karel")


def test_stone_mason_karel():
    execute_karel_code("stone_mason_karel")


def execute_karel_code(problem_name):
    world = KarelWorld(problem_name)
    karel = Karel(world)
    student_code = StudentCode(CODE_DIR + problem_name + ".py", karel)
    student_code.mod.main()
    assert karel.compare_with(
        Karel(KarelWorld(f"{problem_name}_end"))
    ), "Expected end result of world did not match."
