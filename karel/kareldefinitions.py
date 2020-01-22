from enum import Enum, unique
import math

INFINITY = -1
PAD_X = 75
PAD_Y = 10
INIT_SPEED = 50
LIGHT_GREY = "#e5e5e5"
VALID_WORLD_KEYWORDS = ["dimension", "wall", "beeper", "karel", "speed", "beeperbag"]
VALID_DIRECTIONS = ["east", "west", "north", "south"]
KEYWORD_DELIM = ":"
PARAM_DELIM = ";"

"""
Drawing Constants for Karel Canvas
"""
BORDER_OFFSET = 17
LABEL_OFFSET = 7
CORNER_SIZE = 2
BEEPER_CELL_SIZE_FRAC = 0.35
LINE_WIDTH = 2

"""
Drawing Constants for Karel Robot
All constants are defined relative to the size of a single cell
"""
KAREL_VERTICAL_OFFSET = 0.03125
KAREL_LEFT_HORIZONTAL_PAD = 0.29 
KAREL_HEIGHT = 0.76
KAREL_WIDTH = 0.58
KAREL_INNER_HEIGHT = 0.38
KAREL_INNER_WIDTH = 0.28125
KAREL_INNER_OFFSET = 0.125
KAREL_MOUTH_WIDTH = 0.1375
KAREL_MOUTH_HORIZONTAL_OFFSET = 0.2625
KAREL_MOUTH_VERTICAL_OFFSET = 0.125
KAREL_UPPER_RIGHT_DIAG = 0.2
KAREL_LOWER_LEFT_DIAG = 0.13125
KAREL_LEG_LENGTH = 0.15
KAREL_FOOT_LENGTH = 0.1875
KAREL_LEG_FOOT_WIDTH = 0.075
KAREL_LEG_VERTICAL_OFFSET = 0.5
KAREL_LEG_HORIZONTAL_OFFSET = 0.2625
KAREL_LINE_WIDTH = 1


class Wall():
	def __init__(self, avenue, street, direction):
		self._avenue = avenue
		self._street = street
		self._direction = direction

	def __eq__(self, other):
		return  self._avenue == other.avenue and \
				self._street == other.street and \
				self._direction == other.direction

	def __hash__(self):
		return hash((self._avenue, self._street, self._direction))

	def __repr__(self):
		return f"({self._avenue}, {self._street}) {self._direction}"

	@property
	def avenue(self):
		return self._avenue

	@property
	def street(self):
		return self._street

	@property
	def direction(self):
		return self._direction

@unique	
class Direction(Enum):
	EAST = 0
	SOUTH = math.pi / 2
	WEST = math.pi 
	NORTH = 3 * math.pi / 2

DIRECTIONS_MAP = {
	"north": Direction.NORTH, 
	"east": Direction.EAST,
	"south": Direction.SOUTH, 
	"west": Direction.WEST
}

NEXT_DIRECTION_MAP = {
	Direction.NORTH: Direction.WEST, 
	Direction.WEST: Direction.SOUTH, 
  	Direction.SOUTH: Direction.EAST, 
	Direction.EAST: Direction.NORTH
}

NEXT_DIRECTION_MAP_RIGHT = {v:k for k,v in NEXT_DIRECTION_MAP.items()}

# This map associates directions with the delta that Karel
# undergoes if it were to move one step in that direction
# delta is in terms of (avenue, street)
DIRECTION_DELTA_MAP = {
	Direction.NORTH: (0, 1),
	Direction.EAST: (1, 0),
	Direction.SOUTH: (0, -1),
	Direction.WEST: (-1, 0)
}

"""
The following classes define Karel-specific exceptions
"""
class KarelException(Exception):
	pass
