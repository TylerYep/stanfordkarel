import os

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

for problem_name in PROBLEMS:
    world = KarelWorld(problem_name)
    karel = Karel(world)
    student_code = StudentCode(problem_name + "Solution.py", karel)
    student_code.mod.main()
    world.save_to_file(os.path.join("worlds", problem_name + "End.w"), karel)
