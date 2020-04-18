import os
import re
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


def camel_to_snake(name):
    name = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    name = re.sub("([a-z0-9])([A-Z])", r"\1_\2", name).lower()
    if name[0] == "_":
        return name[1:]
    return name


def snake_to_camel(name):
    return "".join(word.title() for word in name.split("_"))


def convert_filenames(folder):
    for filename in os.listdir(folder):
        if ".py" in filename or ".w" in filename:
            new_filename = camel_to_snake(filename)
            full_path = os.path.join(folder, filename)
            full_new_path = os.path.join(folder, new_filename)
            os.rename(full_path, full_new_path)


if __name__ == "__main__":
    # create_solution_worlds()
    # get_solutions_for_testing()
    convert_filenames("worlds")
