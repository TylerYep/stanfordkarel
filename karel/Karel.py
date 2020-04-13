"""
This file defines the Karel class, which provides the actual 
implementation of all functions described in the Karel Reference
Guide. 

All instances of a Karel object store a reference to the world
in which they exist. Each Karel object exists on a given
(avenue, street) intersection and holds a certain number of beepers
in its beeper bag.


Original Author: Nicholas Bowman
Credits: Kylie Jue 
License: MIT
Version: 1.0.0
Email: nbowman@stanford.edu
Date of Creation: 10/1/2019
Last Modified: 3/31/2020
"""

from karel.kareldefinitions import *

class Karel():
	def __init__(self, world):
		"""
		This functions instantiates a new Karel instance and sets its 
		location and current number of beepers to be the default starting
		values as indicated by the given world object. 

		Parameters: 
			world (KarelWorld) - The world that Karel should exists in

		Returns: None
		"""
		self._world = world

		self._avenue, self._street = self._world.karel_starting_location
		self._direction = self._world.karel_starting_direction

		self._num_beepers = self._world.karel_starting_beeper_count

	@property
	def avenue(self):
		"""
		This property can be used to access Karel's current avenue location. 

		Parameters: None
		Returns:
			avenue (int) - The current avenue Karel is standing on. 
		"""
		return self._avenue

	@avenue.setter
	def avenue(self, val):
		"""
		This property can be used to set Karel's current avenue location.

		Parameters: 
			val (int) - The new avenue that Karel will be standing on.
		Returns: None
		"""
		self._avenue = val

	@property
	def street(self):
		"""
		This property can be used to access Karel's current street location. 
		
		Parameters: None
		Returns:
			street (int) - The current street Karel is standing on. 
		"""
		return self._street

	@street.setter
	def street(self, val):
		"""
		This property can be used to set Karel's current street location.

		Parameters: 
			val (int) - The new street that Karel will be standing on.
		Returns: None
		"""
		self._street = val

	@property
	def direction(self):
		"""
		This property can be used to access Karel's current direction. 
		
		Parameters: None
		Returns:
			street (Direction[Enum]) - The current direction Karel is facing. 
		"""
		return self._direction

	@direction.setter
	def direction(self, val):
		"""
		This property can be used to set Karel's current direction.

		Parameters: 
			val (Direction[Enum]) - The new direction that Karel will be facing.
		Returns: None
		"""		
		self._direction = val

	@property
	def num_beepers(self):
		"""
		This property can be used to access Karel's current number of beepers. 
		
		Parameters: None
		Returns:
			num_beepers (int) - The current number of beepers Karel has. 
		"""
		return self._num_beepers

	@num_beepers.setter
	def num_beepers(self, val):
		"""
		This property can be used to set Karel's current number of beepers.

		Parameters: 
			val (int) - The new number of beepers that Karel will have.
		Returns: None
		"""		
		self._num_beepers = val
	
	def reset_state(self):
		"""
		This function is used to reset Karel's location and direction to the original
		starting parameters as indicated by the world that Karel lives in.

		Parameters: None
		Returns: None
		"""
		self._avenue, self._street = self._world.karel_starting_location
		self._direction = self._world.karel_starting_direction

		self._num_beepers = self._world.karel_starting_beeper_count

	def move(self):
		"""
		This function moves Karel forward one space in the direction that it is 
		currently facing. If Karel's front is not clear (blocked by wall or boundary
		of world) then a KarelException will be raised). 

		Parameters: None
		Returns: None
		"""
		if not self.front_is_clear():
			raise KarelException(self._avenue, self._street, self._direction, 
								"Karel attempted to move, but its front was blocked.")

		delta_avenue, delta_street = DIRECTION_DELTA_MAP[self._direction]
		self._avenue += delta_avenue
		self._street += delta_street

	def turn_left(self):
		"""
		This function turns Karel 90 degrees counterclockwise. 

		Parameters: None
		Returns: None
		"""
		self._direction = NEXT_DIRECTION_MAP[self._direction]

	def put_beeper(self):
		"""
		This function places a beeper on the corner that Karel is currently standing
		on and decreases Karel's beeper count by 1. If Karel has no more beepers in its
		beeper bag, then this function raises a KarelException. 

		Parameters: None
		Returns: None
		"""
		if self._num_beepers == 0:
			raise KarelException(self._avenue, self._street, self._direction, 
								"Karel attempted to put a beeper, but it had none left in its bag.")

		if self._num_beepers != INFINITY:
			self._num_beepers -= 1

		self._world.add_beeper(self._avenue, self._street)

	def pick_beeper(self):
		"""
		This function removes a beeper from the corner that Karel is currently standing on
		and increases Karel's beeper count by 1. If there are no beepers on Karel's current
		corner, then this function raises a KarelException. 

		Parameters: None
		Returns: None
		"""
		if not self.beepers_present():
			raise KarelException(self._avenue, self._street, self._direction, 
								"Karel attempted to pick up a beeper, but there were none on the current corner.")

		if self._num_beepers != INFINITY:
			self._num_beepers += 1

		self._world.remove_beeper(self._avenue, self._street)

	def front_is_clear(self):
		"""
		This function returns a boolean indicating whether or not there is a wall
		in front of Karel.

		Parameters: None
		Returns: 
			is_clear (Bool) - True if there is no wall in front of Karel
							  False otherwise
		"""
		return self.direction_is_clear(self._direction)

	def direction_is_clear(self, direction):
		"""
		This is a helper function that returns a boolean indicating whether
		or not there is a barrier in the specified direction of Karel. 

		Parameters: 
			direction (Direction[Enum]) - The direction in which to check for a barrier

		Returns: 
			is_clear (Bool) - True if there is no barrier in the specified direction
							  False otherwise
		"""
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
		"""
		This function returns a boolean indicating whether there is a wall
		in front of Karel.

		Parameters: None
		Returns: 
			is_blocked (Bool) - True if there is a wall in front of Karel
							  	False otherwise
		"""
		return not self.front_is_clear()

	def left_is_clear(self):
		"""
		This function returns a boolean indicating whether or not there is a wall
		to the left of Karel.

		Parameters: None
		Returns: 
			is_clear (Bool) - True if there is no wall to the left of Karel
							  False otherwise
		"""
		return self.direction_is_clear(NEXT_DIRECTION_MAP[self._direction])

	def left_is_blocked(self):
		"""
		This function returns a boolean indicating whether there is a wall
		to the left of Karel.

		Parameters: None
		Returns: 
			is_blocked (Bool) - True if there is a wall to the left of Karel
							  	False otherwise
		"""
		return not self.left_is_clear()

	def right_is_clear(self):
		"""
		This function returns a boolean indicating whether or not there is a wall
		to the right of Karel.

		Parameters: None
		Returns: 
			is_clear (Bool) - True if there is no wall to the right of Karel
							  False otherwise
		"""
		return self.direction_is_clear(NEXT_DIRECTION_MAP_RIGHT[self._direction])

	def right_is_blocked(self):
		"""
		This function returns a boolean indicating whether there is a wall
		to the right of Karel.

		Parameters: None
		Returns: 
			is_blocked (Bool) - True if there is a wall to the right of Karel
							  	False otherwise
		"""
		return not self.right_is_clear()

	def beepers_present(self):
		"""
		This function returns a boolean indicating whether or not there is 
		a beeper on Karel's current corner.

		Parameters: None
		Returns:
			beeepers_on_corner (Bool) - True if there is at least one beeper on Karel's current corner
										False otherwise
		"""
		return self._world.beepers[(self.avenue, self.street)] != 0

	def no_beepers_present(self):
		return not self.beepers_present()

	def beepers_in_bag(self):
		"""
		This function returns a boolean indicating whether or not there is 
		at least one beeper in Karel's beeper bag.

		Parameters: None
		Returns:
			beepers_in_bag (Bool) - True if there is at least one beeper in Karel's bag
									False otherwise
		"""
		# Can't check > 0 because INFINITY beepers is -1
		return self._num_beepers != 0

	def no_beepers_in_bag(self):
		# Only 0 beepers in bag indicates empty bag – negative numbers represent INFINITY
		return self._num_beepers == 0

	def facing_north(self):
		"""
		This function returns a boolean indicating whether or not Karel is currently
		facing North. 

		Parameters: None
		Returns:
			facing_north (Bool) - True if Karel is currently facing North
								  False otherwise
		"""
		return self.direction == Direction.NORTH

	def not_facing_north(self):
		return not self.facing_north()

	def facing_east(self):
		"""
		This function returns a boolean indicating whether or not Karel is currently
		facing East. 

		Parameters: None
		Returns:
			facing_east (Bool) - True if Karel is currently facing East
								 False otherwise
		"""
		return self.direction == Direction.EAST

	def not_facing_east(self):
		return not self.facing_east()

	def facing_west(self):
		"""
		This function returns a boolean indicating whether or not Karel is currently
		facing West. 

		Parameters: None
		Returns:
			facing_west (Bool) - True if Karel is currently facing West
								 False otherwise
		"""
		return self.direction == Direction.WEST

	def not_facing_west(self):
		return not self.facing_west()

	def facing_south(self):
		"""
		This function returns a boolean indicating whether or not Karel is currently
		facing South. 

		Parameters: None
		Returns:
			facing_south (Bool) - True if Karel is currently facing South
								  False otherwise
		"""
		return self.direction == Direction.SOUTH

	def not_facing_south(self):
		return not self.facing_south()

	def paint_corner(self, color):
		"""
		This function makes Karel paint it's current corner the indicated color.
		This function will raise a KarelExcpetion if the indicated color is not one 
		of the valid predefined colors. For this list of colors, check the 
		kareldefinitions.py file.

		Parameters: 
			color (str) - The color string specifying which color to paint the corner
		Returns: None
		"""
		if color and color not in COLOR_MAP.values():
			raise KarelException(self._avenue, self._street, self._direction, 
								f"Karel attempted to paint the corner with color {color}, which is not valid.")
		self._world.paint_corner(self.avenue, self.street, color)

	def corner_color_is(self, color):
		"""
		This function returns a boolean indicating whether or not Karel's current
		corner is the specified color.

		Parameters: 
			color (str) - Color string representing the color to check the current corner for
		Returns:
			is_color (Bool) - True if Karel's current corner is the specified color
							  False otherwise
		"""	
		return self._world.corner_color(self.avenue, self.street) == color