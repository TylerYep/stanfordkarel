from karel.Karel import Karel
from karel.KarelApplication import StudentCode
from karel.KarelWorld import KarelWorld


class TestKarel:
    @staticmethod
    def test_checkerboard_karel():
        code_file = "CheckerboardKarel"

        world = execute_karel_code(code_file)

        assert KarelWorld("CheckerboardKarelEnd.w") == world


def execute_karel_code(problem_name):
    world = KarelWorld(problem_name + ".w")
    karel = Karel(world)
    student_code = StudentCode(problem_name + ".py", karel)
    student_code.mod.main()
    return world
