from kareldefinitions import *

class Karel():
	def __init__(self, world):
		self._world = world

		self._avenue, self._street = self._world.karel_starting_location

	@property
	def avenue(self):
		return self._avenue

	@property
	def street(self):
		return self._street
		
	def turn_left(self):
		print("Turning left!")

	def move(self):
		print("Moving!")

	def put_beeper(self):
		print("Putting beeper!")

	def pick_beeper(self):
		print("Picking beeper!")

	def facing_north(self):
		return False

	def facing_east(self):
		return False

	def facing_west(self):
		return False

	def facing_south(self):
		return False

	def front_is_clear(self):
		return False

	def on_beeper(self):
		return False
