from enum import Enum, unique

INFINITY = -1
PAD_X = 75
PAD_Y = 10
INIT_SPEED = 50
LIGHT_GREY = "#e5e5e5"

@unique
class Direction(Enum):
	NORTH = 0
	EAST = 1
	SOUTH = 2
	WEST = 3