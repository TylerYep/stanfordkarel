from kareldefinitions import *

class Karel():
	def __init__(self, world):
		self._world = world

		self._avenue, self._street = self._world.karel_starting_location
		self._direction = self._world.karel_starting_direction

		self._num_beepers = self._world.karel_starting_beeper_count

	@property
	def avenue(self):
		return self._avenue

	@property
	def street(self):
		return self._street

	@property
	def direction(self):
		return self._direction

	@property
	def num_beepers(self):
		return self._num_beepers
	
	
	def reset_state(self):
		self._avenue, self._street = self._world.karel_starting_location
		self._direction = self._world.karel_starting_direction

		self._num_beepers = self._world.karel_starting_beeper_count

	def turn_left(self):
		self._direction = NEXT_DIRECTION_MAP[self._direction]

	def move(self):
		if not self.front_is_clear():
			# TODO: throw a helpful exception
			raise Exception

		delta_avenue, delta_street = DIRECTION_DELTA_MAP[self._direction]
		self._avenue += delta_avenue
		self._street += delta_street

	def put_beeper(self):
		if self._num_beepers == 0:
			# TODO: throw helpful excpetion here 
			raise Exception

		self._num_beepers -= 1
		self._world.add_beeper(self._avenue, self._street)

	def pick_beeper(self):
		if not self.on_beeper():
			# TODO: throw helpful exception here
			raise Exception

		self._num_beepers += 1
		self._world.remove_beeper(self._avenue, self._street)

	def facing_north(self):
		return self.direction == Direction.NORTH

	def facing_east(self):
		return self.direction == Direction.EAST

	def facing_west(self):
		return self.direction == Direction.WEST

	def facing_south(self):
		return self.direction == Direction.SOUTH

	def front_is_clear(self):
		delta_avenue, delta_street = DIRECTION_DELTA_MAP[self._direction]
		next_avenue = self._avenue + delta_avenue
		next_street = self._street + delta_street
		opposite_direction = NEXT_DIRECTION_MAP[NEXT_DIRECTION_MAP[self._direction]]

		# front is not clear if we are about to go out of bounds
		if not self._world.in_bounds(next_avenue, next_street):
			return False

		# front is not clear if wall exists in same direction of where we're currently facing
		if self._world.wall_exists(self._avenue, self._street, self._direction):
			return False

		# must also check for alternate possible representation of wall 
		if self._world.wall_exists(next_avenue, next_street, opposite_direction):
			return False

		return True

	def on_beeper(self):
		return self._world.beepers[(self.avenue, self.street)] != 0
