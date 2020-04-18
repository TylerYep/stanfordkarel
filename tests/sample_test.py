from stanfordkarel.karel import Karel
from stanfordkarel.karel_application import StudentCode
from stanfordkarel.karel_world import KarelWorld


class TestKarel:
    @staticmethod
    def test_checkerboard_karel():
        code_file = "CheckerboardKarel"

        world = execute_karel_code(code_file)

        assert KarelWorld("CheckerboardKarelEnd") == world


def execute_karel_code(problem_name):
    world = KarelWorld(problem_name)
    karel = Karel(world)
    student_code = StudentCode(problem_name + ".py", karel)
    student_code.mod.main()
    return world
