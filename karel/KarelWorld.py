"""
This file defines the class definition of a Karel world.

The sub header comment defines important notes about the Karel
world file format. 

Original Author: Nicholas Bowman
Credits: Kylie Jue 
License: MIT
Version: 1.0.0
Email: nbowman@stanford.edu
Date of Creation: 10/1/2019
Last Modified: 3/31/2020
"""

"""
General Notes About World Construction 
- Streets run EAST-WEST (rows)
- Avenues run NORTH-SOUTH (columns)

World File Constraints:
- World file should specify one component per line in the format
  KEYWORD: PARAMETERS
- Any lines with no colon delimiter will be ignored
- The accepted KEYWORD, PARAMETER combinations are as follows:
	- Dimension: (num_avenues, num_streets)
	- Wall: (avenue, street); direction
	- Beeper: (avenue, street) count
	- Karel: (avenue, street); direction
	- Color: (avenue, street); color
	- Speed: delay
	- BeeperBag: num_beepers
- Multiple parameter values for the same keyword should be separated by a semicolon
- All numerical values (except delay) must be expressed as ints. The exception
  to this is that the number of beepers can also be INFINITY
- Any specified color values must be valid TKinter color strings, and are limited
  to the set of colors 
- Direction is case-insensitive and can be one of the following values:
	- East
	- West
	- North 
	- South	
"""

from karel.kareldefinitions import *
import collections
import re
import copy

class KarelWorld():
	def __init__(self, world_file=None):
		"""
		Karel World constructor
		Parameters:
			world_file: Open file object containing information about the initial state of Karel's world
		"""
		self._world_file = world_file

		# Map of beeper locations to the count of beepers at that location
		self._beepers = collections.defaultdict(int)

		# Map of corner colors, defaults to None
		self._corner_colors = collections.defaultdict(lambda: "")

		# Set of Wall objects placed in the world
		self._walls = set()

		# Dimensions of the world
		self._num_streets = 1
		self._num_avenues = 1

		# Initial Karel state saved to enable world reset
		self._karel_starting_location = (1, 1)
		self._karel_starting_direction = Direction.EAST
		self._karel_starting_beeper_count = 0

		# Initial speed slider setting
		self._init_speed = INIT_SPEED

		# If a world file has been specified, load world details from the file
		if self._world_file:
			self.load_from_file()

		# Save initial beeper state to enable world reset
		self._init_beepers = copy.deepcopy(self._beepers)

	@property
	def karel_starting_location(self):
		return self._karel_starting_location

	@property
	def karel_starting_direction(self):
		return self._karel_starting_direction

	@property
	def karel_starting_beeper_count(self):
		return self._karel_starting_beeper_count
	
	@property
	def init_speed(self):
		return self._init_speed

	@property
	def num_streets(self):
		return self._num_streets

	@num_streets.setter
	def num_streets(self, val):
		self._num_streets = val

	@property
	def num_avenues(self):
		return self._num_avenues
	
	@num_avenues.setter
	def num_avenues(self, val):
		self._num_avenues = val

	@property
	def beepers(self):
		return self._beepers

	@property
	def corner_colors(self):
		return self._corner_colors
	
	@property
	def walls(self):
		return self._walls
	
	def load_from_file(self):
		def parse_line(line):
			# Ignore blank lines and lines with no comma delineator
			if not line or ":" not in line:
				return None, None, False

			params = {}
			components = line.strip().split(KEYWORD_DELIM)
			keyword = components[0].lower()

			# only accept valid keywords as defined in world file spec
			if keyword not in VALID_WORLD_KEYWORDS:
				return None, None, False

			param_list = components[1].split(PARAM_DELIM)

			for param in param_list:
				param = param.strip().lower()

				# first check to see if the parameter is a direction value
				if param in VALID_DIRECTIONS:
					params["dir"] = DIRECTIONS_MAP[param]
				else:
					# next check to see if parameter encodes a location
					coordinate = re.match(r"\((\d+),\s*(\d+)\)", param)
					if coordinate:
						avenue = int(coordinate.group(1))
						street = int(coordinate.group(2))
						params["loc"] = (avenue, street)
					else:
						# finally check to see if parameter encodes a numerical value or color string
						val = None
						if param.isdigit():
							val = int(param)
						elif keyword == "speed":
							# double values are only allowed for speed parameter
							try:
								val = int(100 * float(param))
							except ValueError:
								# invalid parameter value, do not process
								continue
						elif keyword == "beeperbag":
							# handle the edge case where Karel has infinite beepers
							if param == "infinity" or param == "infinite":
								val = INFINITY
						elif keyword == "color":
							# TODO: add check for valid color? 
							val = param 
						# only store non-null values
						if val is not None: params["val"] = val

			return keyword.lower(), params, True


		for i, line in enumerate(self._world_file):
			keyword, params, is_valid = parse_line(line)

			# skip invalid lines (comments, incorrectly formatted, invalid keyword)
			if not is_valid:
				# print(f"Ignoring line {i} of world file: {line.strip()}")
				continue

			# TODO: add error detection for keywords with insufficient parameters

			# handle all different possible keyword cases
			if keyword == "dimension":
				# set world dimensions based on location values
				self._num_avenues, self._num_streets = params["loc"]

			elif keyword == "wall":
				# build a wall at the specified location
				avenue, street = params["loc"]
				direction = params["dir"]
				self._walls.add(Wall(avenue, street, direction))

			elif keyword == "beeper":
				# add the specified number of beepers to the world
				avenue, street = params["loc"]
				count = params["val"]
				self._beepers[(avenue, street)] += count

			elif keyword == "karel":
				# Give Karel initial state values
				avenue, street = params["loc"]
				direction = params["dir"]
				self._karel_starting_location = (avenue, street)
				self._karel_starting_direction = direction

			elif keyword == "beeperbag":
				# Set Karel's initial beeper bag count
				count = params["val"]
				self._karel_starting_beeper_count = count

			elif keyword == "speed":
				# Set delay speed of program execution
				speed = params["val"]
				self._init_speed = speed

			elif keyword == "color":
				# Set corner color to be specified color
				avenue, street = params["loc"]
				color = params["val"]
				self._corner_colors[(avenue, street)] = color

	def add_beeper(self, avenue, street):
		self._beepers[(avenue, street)] += 1

	def remove_beeper(self, avenue, street):
		if self._beepers[(avenue, street)] == 0:
			return
		self._beepers[(avenue, street)] -= 1

	def add_wall(self, wall):
		alt_wall = self.get_alt_wall(wall)
		if wall not in self._walls and alt_wall not in self._walls:
			self._walls.add(wall)

	def remove_wall(self, wall):
		alt_wall = self.get_alt_wall(wall)
		if wall in self._walls:
			self._walls.remove(wall)
		if alt_wall in self._walls:
			self._walls.remove(alt_wall)
		
	def get_alt_wall(self, wall):
		if wall.direction == Direction.NORTH:
			return Wall(wall.avenue, wall.street + 1, Direction.SOUTH)
		if wall.direction == Direction.SOUTH:
			return Wall(wall.avenue, wall.street - 1, Direction.NORTH)
		if wall.direction == Direction.EAST:
			return Wall(wall.avenue + 1, wall.street, Direction.WEST)
		if wall.direction == Direction.WEST:
			return Wall(wall.avenue - 1, wall.street, Direction.EAST)

	def paint_corner(self, avenue, street, color):
		self._corner_colors[(avenue, street)] = color

	def corner_color(self, avenue, street):
		return self._corner_colors[(avenue, street)]

	def reset_corner(self, avenue, street):
		self._beepers[(avenue, street)] = 0
		self._corner_colors[(avenue, street)] = ""

	def wall_exists(self, avenue, street, direction):
		wall = Wall(avenue, street, direction)
		return wall in self._walls

	def in_bounds(self, avenue, street):
		return avenue > 0 and street > 0 and avenue <= self._num_avenues and street <= self._num_streets

	def reset_world(self):
		"""
		Reset initial state of beepers in the world
		"""
		self._beepers = copy.deepcopy(self._init_beepers)
		self._corner_colors = collections.defaultdict(lambda: "")

	def reload_world(self, filename=None):
		"""
		TODO: Do better decomp to not just copy constructor
		"""
		
		self._beepers = collections.defaultdict(int)
		self._corner_colors = collections.defaultdict(lambda: "")
		self._walls = set()

		self._num_streets = 1
		self._num_avenues = 1

		self._karel_starting_location = (1, 1)
		self._karel_starting_direction = Direction.EAST
		self._karel_starting_beeper_count = 0

		self._init_speed = INIT_SPEED

		if filename:
			self._world_file = open(filename, 'r')
			self.load_from_file()

		self._init_beepers = copy.deepcopy(self._beepers)

	def save_to_file(self, filename, karel):
		with open(filename, "w") as f:
			# First, output dimensions of world
			f.write(f"Dimension: ({self.num_avenues}, {self.num_streets})\n")

			# Next, output all walls
			for wall in self._walls:
				f.write(f"Wall: ({wall.avenue}, {wall.street}); {DIRECTIONS_MAP_INVERSE[wall.direction]}\n")

			# Next, output all beepers
			for loc, count in self._beepers.items():
				f.write(f"Beeper: ({loc[0]}, {loc[1]}); {count}\n")

			# Next, output all color information
			for loc, color in self._corner_colors.items():
				if color:
					f.write(f"Color: ({loc[0]}, {loc[1]}); {color}\n")

			# Next, output Karel information
			f.write(f"Karel: ({karel.avenue}, {karel.street}); {DIRECTIONS_MAP_INVERSE[karel.direction]}\n")
			
			# Finally, output beeperbag info
			beeper_output = karel.num_beepers if karel.num_beepers >= 0 else "INFINITY"
			f.write(f"BeeperBag: {beeper_output}\n")
