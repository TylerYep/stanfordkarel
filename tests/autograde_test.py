from stanfordkarel.karel import Karel
from stanfordkarel.karel_application import StudentCode
from stanfordkarel.karel_world import KarelWorld


class TestAutogradeKarel:
    @staticmethod
    def test_checkerboard_karel():
        execute_karel_code("checkerboard_karel")

    @staticmethod
    def test_collect_newspaper_karel():
        execute_karel_code("collect_newspaper_karel")

    @staticmethod
    def test_midpoint_karel():
        execute_karel_code("midpoint_karel")

    @staticmethod
    def test_triple_karel():
        execute_karel_code("triple_karel")

    @staticmethod
    def test_stone_mason_karel():
        execute_karel_code("stone_mason_karel")


def execute_karel_code(problem_name):
    world = KarelWorld(problem_name)
    karel = Karel(world)
    student_code = StudentCode(problem_name + ".py", karel)
    student_code.mod.main()
    assert KarelWorld(f"{problem_name}_end") == world, "Expected end result of world did not match."
