INFINITY = -1
PAD_X = 75
PAD_Y = 10
INIT_SPEED = 50
LIGHT_GREY = "#e5e5e5"
VALID_WORLD_KEYWORDS = ["dimension", "wall", "beeper", "karel", "speed", "beeperbag"]
VALID_DIRECTIONS = ["east", "west", "north", "south"]
KEYWORD_DELIM = ":"
PARAM_DELIM = ";"

class Wall():
	def __init__(self, street, avenue, direction):
		self._street = street
		self._avenue = avenue
		self._direction = direction

	def __eq__(self, other):
		return self._street == other.street and \
				self._avenue == other.avenue and \
				self._direction == other.direction

	def __hash__(self):
		return hash((self._street, self._avenue, self._direction))

	def __repr__(self):
		return f"({self._avenue}, {self._street}) {self._direction}"

	@property
	def street(self):
		return self._street
	
	@property
	def avenue(self):
		return self._avenue

	@property
	def direction(self):
		return self._direction
	
class Direction(Enum):
	NORTH = 0
	EAST = 1
	SOUTH = 2
	WEST = 3

DIRECTIONS_MAP = {"north": Direction.NORTH, "east": Direction.EAST, "south": Direction.SOUTH, "west": Direction.WEST}
