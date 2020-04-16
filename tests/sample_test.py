from karel.Karel import Karel
from karel.KarelApplication import StudentCode
from karel.KarelWorld import KarelWorld


class TestKarel:
    @staticmethod
    def test_checkerboard_karel():
        code_file = "CheckerboardKarel"

        world = execute_karel_problem(code_file)

        assert KarelWorld("CheckerboardKarelEnd.w") == world


def execute_karel_problem(code_file):
    world = KarelWorld(code_file + ".w")
    karel = Karel(world)
    student_code = StudentCode(code_file + ".py", karel)
    student_code.mod.main()
    return world
