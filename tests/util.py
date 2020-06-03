import os
import re
import shutil

from stanfordkarel.karel import Karel
from stanfordkarel.karel_application import StudentCode

PROBLEMS = [
    "CheckerboardKarel",
    "CollectNewspaperKarel",
    "MidpointKarel",
    "TripleKarel",
    "StoneMasonKarel",
]

PROBLEM_FILES = [
    "checkerboard_karel",
    "collect_newspaper_karel",
    "midpoint_karel",
    "triple_karel",
    "stone_mason_karel",
]


def execute_karel_code(problem_name, folder_path="solutions"):
    karel = Karel(problem_name)
    student_code = StudentCode(os.path.join(folder_path, problem_name + ".py"), karel)
    student_code.mod.main()
    assert karel.compare_with(
        Karel(f"{problem_name}_end")
    ), "Expected end result of world did not match."


def create_solution_worlds():
    for problem_name in PROBLEMS:
        karel = Karel(problem_name)
        student_code = StudentCode(problem_name + "_solution.py", karel)
        student_code.mod.main()
        karel.world.save_to_file(os.path.join("worlds", problem_name + "_end.w"), karel)


def get_solutions_for_testing():
    for problem_name in PROBLEMS:
        src = os.path.join("examples", problem_name + "_solution.py")
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
