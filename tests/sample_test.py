from CollectNewspaperKarel import main
from karel.Karel import Karel
from karel.KarelWorld import KarelWorld
from karel.KarelApplication import StudentCode


class TestKarel:
    @staticmethod
    def test_checkerboard_karel():
        code_file = "CheckerboardKarel"
        world = KarelWorld(code_file + ".w")
        karel = Karel(world)
        student_code = StudentCode(code_file + ".py", karel)

        student_code.mod.main()

        assert KarelWorld("CheckerboardKarelEnd.w") == world
