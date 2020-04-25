from stanfordkarel.karel import Karel
from stanfordkarel.karel_world import KarelWorld


def execute_karel_code(problem_name):
    world = KarelWorld(problem_name)
    karel = Karel(world)
    print(karel)


execute_karel_code(
    "collect_newspaper_karel"
)  #  stone_mason_karel   checkerboard_karel, collect_newspaper_karel
