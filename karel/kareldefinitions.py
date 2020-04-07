"""
This file contains all of the constant and class definitions used
throughout the Karel library. Constants here define drawing proportions
for Karel and it's world, initial world parameters, and different exception
and enumeration types, among other things.

Original Author: Nicholas Bowman
Credits: Kylie Jue 
License: MIT
Version: 1.0.0
Email: nbowman@stanford.edu
Date of Creation: 10/1/2019
Last Modified: 3/31/2020
"""


from enum import Enum, unique
import math

"""
General Karel constants
"""

INFINITY = -1
PAD_X = 75
PAD_Y = 10
INIT_SPEED = 50
DEFAULT_ICON = "karel"
LIGHT_GREY = "#e5e5e5"
VALID_WORLD_KEYWORDS = ["dimension", "wall", "beeper", "karel", "speed", "beeperbag", "color"]
VALID_DIRECTIONS = ["east", "west", "north", "south"]
KEYWORD_DELIM = ":"
PARAM_DELIM = ";"
DEFAULT_WORLD_FILE = "DefaultWorld.w"
MIN_DIMENSIONS = 1
MAX_DIMENSIONS = 50
WALL_DETECTION_THRESHOLD = 0.1
DEFAULT_COLOR = "Red"
DEFAULT_SIZE = 8
COLOR_OPTIONS = sorted(["Red", "Black", "Cyan", "Dark Gray", "Gray", "Green", "Light Gray", "Magenta", "Orange", "Pink", "White", "Blue", "Yellow"])
COLOR_MAP = {"Red": "red", "Black": "black", "Cyan": "cyan", "Dark Gray": "gray30", "Gray": "gray55", "Green": "green", "Light Gray": "gray80", "Magenta": "magenta3", "Orange": "orange", "Pink": "pink", "White": "snow", "Blue": "blue", "Yellow": "yellow"}
BLANK = ""
"""
Drawing Constants for Karel Canvas
"""
BORDER_OFFSET = 17
LABEL_OFFSET = 7
CORNER_SIZE = 2
BEEPER_CELL_SIZE_FRAC = 0.4
LINE_WIDTH = 2

"""
Drawing Constants for Karel Robot Icon
All constants are defined relative to the size of a single cell
"""
KAREL_VERTICAL_OFFSET = 0.05
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
KAREL_LINE_WIDTH = 2

"""
Drawing Constants for Simple Karel Robot Icon
All constants are defined relative to the size of a single cell
"""
SIMPLE_KAREL_HEIGHT = 0.7
SIMPLE_KAREL_WIDTH = 0.8

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

DIRECTIONS_MAP_INVERSE = {v:k for k,v in DIRECTIONS_MAP.items()}

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


class KarelException(Exception):
	"""
	The following classes define Karel-specific exceptions
	"""

	def __init__(self, avenue, street, direction, message):
		self.avenue = avenue
		self.street = street
		self.direction = DIRECTIONS_MAP_INVERSE[direction].capitalize()
		self.message = message

	def __str__(self):
		return f"Karel crashed while on avenue {self.avenue} and street {self.street}, facing {self.direction}\nInvalid action: {self.message}"
