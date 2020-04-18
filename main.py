import os
import shutil

from stanfordkarel.karel import Karel
from stanfordkarel.karel_application import StudentCode
from stanfordkarel.karel_world import KarelWorld

PROBLEMS = [
    "CheckerboardKarel",
    "CollectNewspaperKarel",
    "MidpointKarel",
    "TripleKarel",
    "StoneMasonKarel",
]


def create_solution_worlds():
    for problem_name in PROBLEMS:
        world = KarelWorld(problem_name)
        karel = Karel(world)
        student_code = StudentCode(problem_name + "Solution.py", karel)
        student_code.mod.main()
        world.save_to_file(os.path.join("worlds", problem_name + "End.w"), karel)


def get_solutions_for_testing():
    for problem_name in PROBLEMS:
        src = os.path.join("examples", problem_name + "Solution.py")
        dest = os.path.join(".", problem_name + ".py")
        shutil.copy(src, dest)


def convert_to_lowercase():
    pass


if __name__ == "__main__":
    # create_solution_worlds()
    # get_solutions_for_testing()
    pass
