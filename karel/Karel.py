from karel.kareldefinitions import *


class Karel():
	def __init__(self, world):
		self._world = world

		self._avenue, self._street = self._world.karel_starting_location
		self._direction = self._world.karel_starting_direction

		self._num_beepers = self._world.karel_starting_beeper_count

	@property
	def avenue(self):
		return self._avenue

	@avenue.setter
	def avenue(self, val):
		self._avenue = val

	@property
	def street(self):
		return self._street

	@street.setter
	def street(self, val):
		self._street = val

	@property
	def direction(self):
		return self._direction

	@direction.setter
	def direction(self, val):
		self._direction = val

	@property
	def num_beepers(self):
		return self._num_beepers

	@num_beepers.setter
	def num_beepers(self, val):
		self._num_beepers = val
	
	def reset_state(self):
		self._avenue, self._street = self._world.karel_starting_location
		self._direction = self._world.karel_starting_direction

		self._num_beepers = self._world.karel_starting_beeper_count

	def move(self):
		if not self.front_is_clear():
			raise KarelException(self._avenue, self._street, self._direction, 
								"Karel attempted to move, but its front was blocked.")

		delta_avenue, delta_street = DIRECTION_DELTA_MAP[self._direction]
		self._avenue += delta_avenue
		self._street += delta_street

	def turn_left(self):
		self._direction = NEXT_DIRECTION_MAP[self._direction]

	def put_beeper(self):
		if self._num_beepers == 0:
			raise KarelException(self._avenue, self._street, self._direction, 
								"Karel attempted to put a beeper, but it had none left in its bag.")

		self._num_beepers -= 1
		self._world.add_beeper(self._avenue, self._street)

	def pick_beeper(self):
		if not self.on_beeper():
			raise KarelException(self._avenue, self._street, self._direction, 
								"Karel attempted to pick up a beeper, but there were none on the current corner.")

		self._num_beepers += 1
		self._world.remove_beeper(self._avenue, self._street)

	def front_is_clear(self):
		return self.direction_is_clear(self._direction)

	def direction_is_clear(self, direction):
		delta_avenue, delta_street = DIRECTION_DELTA_MAP[direction]
		next_avenue = self._avenue + delta_avenue
		next_street = self._street + delta_street
		opposite_direction = NEXT_DIRECTION_MAP[NEXT_DIRECTION_MAP[direction]]

		# front is not clear if we are about to go out of bounds
		if not self._world.in_bounds(next_avenue, next_street):
			return False

		# front is not clear if wall exists in same direction of where we're currently facing
		if self._world.wall_exists(self._avenue, self._street, direction):
			return False

		# must also check for alternate possible representation of wall 
		if self._world.wall_exists(next_avenue, next_street, opposite_direction):
			return False

		# If all previous conditions checked out, then the front is clear
		return True

	def front_is_blocked(self):
		return not self.front_is_clear()

	def left_is_clear(self):
		return self.direction_is_clear(NEXT_DIRECTION_MAP[self._direction])

	def left_is_blocked(self):
		return not self.left_is_clear()

	def right_is_clear(self):
		return self.direction_is_clear(NEXT_DIRECTION_MAP_RIGHT[self._direction])

	def right_is_blocked(self):
		return not self.right_is_clear()

	def on_beeper(self):
		return self._world.beepers[(self.avenue, self.street)] != 0

	def beepers_in_bag(self):
		return self._num_beepers > 0

	def facing_north(self):
		return self.direction == Direction.NORTH

	def facing_east(self):
		return self.direction == Direction.EAST

	def facing_west(self):
		return self.direction == Direction.WEST

	def facing_south(self):
		return self.direction == Direction.SOUTH

	def paint_corner(self, color):
		if color not in COLOR_MAP.values():
			raise KarelException(self._avenue, self._street, self._direction, 
								f"Karel attempted to paint the corner with color {color}, which is not valid.")
		self._world.paint_corner(self.avenue, self.street, color)

	def corner_color_is(self, color):
		return self._world.corner_color(self.avenue, self.street) == color