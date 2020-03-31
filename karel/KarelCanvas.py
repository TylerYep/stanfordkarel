"""
This file defines the canvas upon which a Karel world is drawn. This 
class defines all necessary methods to draw all components of a Karel
world, including walls, beepers, and Karel itself. All Karel applications
contains exactly one Karel Canvas object and each Karel Canvas object 
holds information about one Karel World and one Karel object. 

Original Author: Nicholas Bowman
Credits: Kylie Jue 
License: MIT
Version: 1.0.0
Email: nbowman@stanford.edu
Date of Creation: 10/1/2019
Last Modified: 3/31/2020
"""

from karel.kareldefinitions import * 
import tkinter as tk
import cmath


class KarelCanvas(tk.Canvas):
	def __init__(self, width, height, master, world=None, karel=None, bg="white"):
		super().__init__(master, width=width, height=height, bg=bg)
		self.world = world
		self.karel = karel
		self.icon = DEFAULT_ICON
		self.draw_world()
		self.draw_karel()

	def set_icon(self, icon):
		self.icon = icon

	def redraw_all(self):
		self.delete("all")
		self.draw_world()
		self.draw_karel()
		self.update()

	def redraw_karel(self, update=True):
		self.delete("karel")
		self.draw_karel()
		if update: self.update()

	def redraw_beepers(self, update=True):
		self.delete("beeper")
		self.draw_all_beepers()
		if update: self.update()

	def redraw_corners(self, update=True):
		self.delete("corner")
		self.draw_corners()
		if update: self.update()

	def redraw_walls(self, update=True):
		self.delete("wall")
		self.draw_all_walls()
		if update: self.update()

	def draw_world(self):
		self.init_geometry_values()
		self.draw_bounding_rectangle()
		self.label_axes()
		self.draw_corners()
		self.draw_all_beepers()
		self.draw_all_walls()

	def init_geometry_values(self):
		self.update()

		# Calculate the maximum possible cell size in both directions
		# We will use the smaller of the two as the bounding cell size
		horizontal_cell_size = (self.winfo_width() - 2 * BORDER_OFFSET) / self.world.num_avenues
		vertical_cell_size = (self.winfo_height() - 2 * BORDER_OFFSET) / self.world.num_streets

		# Save this as an instance variable for later use
		self.cell_size = min(horizontal_cell_size, vertical_cell_size)

		self.boundary_height = self.cell_size * self.world.num_streets
		self.boundary_width = self.cell_size * self.world.num_avenues

		# Save all these as instance variables as well
		self.left_x = self.winfo_width() / 2 - self.boundary_width / 2
		self.top_y = self.winfo_height() / 2 - self.boundary_height / 2
		self.right_x = self.left_x + self.boundary_width
		self.bottom_y = self.top_y + self.boundary_height

	def draw_bounding_rectangle(self):
		# Draw the external bounding lines of Karel's world
		self.create_line(self.left_x, self.top_y, self.right_x, self.top_y, width=LINE_WIDTH)
		self.create_line(self.left_x, self.top_y, self.left_x, self.bottom_y, width=LINE_WIDTH)
		self.create_line(self.right_x, self.top_y, self.right_x, self.bottom_y, width=LINE_WIDTH)
		self.create_line(self.left_x, self.bottom_y, self.right_x, self.bottom_y, width=LINE_WIDTH)

	def label_axes(self):
		# Label the avenue axes
		for avenue in range(1, self.world.num_avenues + 1):
			label_x = self.calculate_corner_x(avenue)
			label_y = self.bottom_y + LABEL_OFFSET
			self.create_text(label_x, label_y, text=str(avenue), font="Arial 10")
		
		# Label the street axes
		for street in range(1, self.world.num_streets + 1):
			label_x = self.left_x - LABEL_OFFSET
			label_y = self.calculate_corner_y(street)
			self.create_text(label_x, label_y, text=str(street), font="Arial 10")

	def draw_corners(self):
		# Draw all corner markers in the world 
		for avenue in range(1, self.world.num_avenues + 1):
			for street in range(1, self.world.num_streets + 1):
				color = self.world.corner_color(avenue, street)
				corner_x = self.calculate_corner_x(avenue)
				corner_y = self.calculate_corner_y(street)
				if not color:
					self.create_line(corner_x, corner_y - CORNER_SIZE, corner_x, corner_y + CORNER_SIZE, tag="corner")
					self.create_line(corner_x - CORNER_SIZE, corner_y, corner_x + CORNER_SIZE, corner_y, tag="corner")
				else:
					self.create_rectangle(corner_x - self.cell_size / 2, corner_y - self.cell_size / 2,
										  corner_x + self.cell_size / 2, corner_y + self.cell_size / 2, 
										  fill=color, tag="corner", outline="")

	def draw_all_beepers(self):
		for location, count in self.world.beepers.items():
			self.draw_beeper(location, count)

	def draw_beeper(self, location, count):
		# handle case where defaultdict returns 0 count by not drawing beepers
		if count == 0: return 

		corner_x = self.calculate_corner_x(location[0])
		corner_y = self.calculate_corner_y(location[1])
		beeper_radius = self.cell_size * BEEPER_CELL_SIZE_FRAC

		points = [corner_x, corner_y - beeper_radius, corner_x + beeper_radius, corner_y, corner_x, corner_y + beeper_radius, corner_x - beeper_radius, corner_y]
		self.create_polygon(points, fill="light grey", outline="black", tag="beeper")

		if count > 1: 
			self.create_text(corner_x, corner_y, text=str(count), font="Arial 12", tag="beeper")

	def draw_all_walls(self):
		for wall in self.world.walls:
			self.draw_wall(wall)

	def draw_wall(self, wall):
		avenue, street, direction = wall.avenue, wall.street, wall.direction
		corner_x = self.calculate_corner_x(avenue)
		corner_y = self.calculate_corner_y(street)

		if direction == Direction.NORTH:
			self.create_line(corner_x - self.cell_size / 2, 
							 corner_y - self.cell_size / 2, 
							 corner_x + self.cell_size / 2, 
							 corner_y - self.cell_size / 2,
							 width=LINE_WIDTH, tag="wall")
		if direction == Direction.SOUTH:
			self.create_line(corner_x - self.cell_size / 2, 
							 corner_y + self.cell_size / 2, 
							 corner_x + self.cell_size / 2, 
							 corner_y + self.cell_size / 2, 
							 width=LINE_WIDTH, tag="wall")
		if direction == Direction.EAST:
			self.create_line(corner_x + self.cell_size / 2,
							 corner_y - self.cell_size / 2,
							 corner_x + self.cell_size / 2,
							 corner_y + self.cell_size / 2, 
							 width=LINE_WIDTH, tag="wall")
		if direction == Direction.WEST:
			self.create_line(corner_x - self.cell_size / 2,
							 corner_y - self.cell_size / 2,
							 corner_x - self.cell_size / 2,
							 corner_y + self.cell_size / 2,
							 width=LINE_WIDTH, tag="wall")

	def draw_karel(self):
		corner_x = self.calculate_corner_x(self.karel.avenue)
		corner_y = self.calculate_corner_y(self.karel.street)
		center = (corner_x, corner_y)

		if self.icon == "karel":
			karel_origin_x = corner_x - self.cell_size / 2 + KAREL_LEFT_HORIZONTAL_PAD * self.cell_size
			karel_origin_y = corner_y - self.cell_size / 2 + KAREL_VERTICAL_OFFSET * self.cell_size

			self.draw_karel_body(karel_origin_x, karel_origin_y, center, self.karel.direction.value)
			self.draw_karel_legs(karel_origin_x, karel_origin_y, center, self.karel.direction.value)
		elif self.icon == "simple":
			self.draw_simple_karel_icon(center, self.karel.direction.value)

	def generate_external_karel_points(self, x, y, center, direction):
		outer_points = []
		
		# Top-left point (referred to as origin) of Karel's body
		outer_points.extend((x,y))

		# Calculate Karel's height and width as well as missing diag segments
		width = self.cell_size * KAREL_WIDTH
		height = self.cell_size * KAREL_HEIGHT
		lower_left_missing = (self.cell_size * KAREL_LOWER_LEFT_DIAG) / math.sqrt(2)
		upper_right_missing = (self.cell_size * KAREL_UPPER_RIGHT_DIAG) / math.sqrt(2)

		# These two points define Karel's upper right
		outer_points.extend((x + width - upper_right_missing, y))
		outer_points.extend((x + width, y + upper_right_missing))

		# Karel's bottom right edge
		outer_points.extend((x + width, y + height))

		# These two points define Karel's lower left 
		outer_points.extend((x + lower_left_missing, y + height))
		outer_points.extend((x, y + height - lower_left_missing))

		# Complete the polygon
		outer_points.extend((x,y))

		# Rotate all external body points to get correct Karel orientation
		self.rotate_points(center, outer_points, direction)

		return outer_points

	def generate_internal_karel_points(self, x, y, center, direction):
		
		# Calculate dimensions and location of Karel's inner eye
		inner_x = x + self.cell_size * KAREL_INNER_OFFSET
		inner_y = y + self.cell_size * KAREL_INNER_OFFSET
		inner_height = self.cell_size * KAREL_INNER_HEIGHT
		inner_width = self.cell_size * KAREL_INNER_WIDTH

		# Define inner body points
		inner_points = [inner_x, inner_y, inner_x + inner_width, inner_y, inner_x + inner_width, inner_y + inner_height, inner_x, inner_y + inner_height, inner_x, inner_y]
		self.rotate_points(center, inner_points, direction)

		return inner_points

	def draw_karel_body(self, x, y, center, direction):
		outer_points = self.generate_external_karel_points(x, y, center, direction)
		inner_points = self.generate_internal_karel_points(x, y, center, direction)

		# Non-convex polygon that determines Karel's entire body is a
		# combination of the two sets of points defining internal and external
		# components
		entire_body_points = outer_points + inner_points

		# First draw the filled non-convex polygon
		self.create_polygon(entire_body_points, fill="white", outline="", width=KAREL_LINE_WIDTH, tag="karel")
		
		# Then draw the transparent exterior edges of Karel's body
		self.create_polygon(outer_points, fill="", outline="black", width=KAREL_LINE_WIDTH, tag="karel")
		self.create_polygon(inner_points, fill="", outline="black", width=KAREL_LINE_WIDTH, tag="karel")

		# Define dimensions and location of Karel's mouth
		karel_height = self.cell_size * KAREL_HEIGHT
		mouth_horizontal_offset = self.cell_size * KAREL_MOUTH_HORIZONTAL_OFFSET
		mouth_vertical_offset = self.cell_size * KAREL_MOUTH_VERTICAL_OFFSET
		inner_y = y + self.cell_size * KAREL_INNER_OFFSET
		inner_height = self.cell_size * KAREL_INNER_HEIGHT
		mouth_width = self.cell_size * KAREL_MOUTH_WIDTH

		mouth_y = inner_y + inner_height + mouth_vertical_offset

		# Define, rotate, and draw points
		mouth_points = [x + mouth_horizontal_offset, mouth_y, x + mouth_horizontal_offset + mouth_width, mouth_y]
		self.rotate_points(center, mouth_points, direction)
		self.create_polygon(mouth_points, fill="white", outline="black", width=KAREL_LINE_WIDTH, tag="karel")

	def draw_karel_legs(self, x, y, center, direction):
		leg_length = self.cell_size * KAREL_LEG_LENGTH
		foot_length = self.cell_size * KAREL_FOOT_LENGTH
		leg_foot_width = self.cell_size * KAREL_LEG_FOOT_WIDTH

		vertical_offset = self.cell_size * KAREL_LEG_VERTICAL_OFFSET
		horizontal_offset = self.cell_size * KAREL_LEG_HORIZONTAL_OFFSET

		# Generate points for left leg
		points = []
		points.extend((x, y + vertical_offset))
		points.extend((x - leg_length, y + vertical_offset))
		points.extend((x - leg_length, y + vertical_offset + foot_length))
		points.extend((x - leg_length + leg_foot_width, y + vertical_offset + foot_length))
		points.extend((x - leg_length + leg_foot_width, y + vertical_offset + leg_foot_width))
		points.extend((x, y + vertical_offset + leg_foot_width))
		points.extend((x, y + vertical_offset))

		self.rotate_points(center, points, direction)
		self.create_polygon(points, fill="black", outline="black", width=KAREL_LINE_WIDTH, tag="karel")

		# Reset point of reference to be bottom left rather than top_left
		y = y + self.cell_size * KAREL_HEIGHT

		# Generate points for right leg
		points = []
		points.extend((x + horizontal_offset, y))
		points.extend((x + horizontal_offset, y + leg_length))
		points.extend((x + horizontal_offset + foot_length, y + leg_length))
		points.extend((x + horizontal_offset + foot_length, y + leg_length - leg_foot_width))
		points.extend((x + horizontal_offset + leg_foot_width, y + leg_length - leg_foot_width))
		points.extend((x + horizontal_offset + leg_foot_width, y))
		points.extend((x + horizontal_offset, y))

		self.rotate_points(center, points, direction)
		self.create_polygon(points, fill="black", outline="black", width=KAREL_LINE_WIDTH, tag="karel")

	def draw_simple_karel_icon(self, center, direction):
		simple_karel_width = self.cell_size * SIMPLE_KAREL_WIDTH
		simple_karel_height = self.cell_size * SIMPLE_KAREL_HEIGHT
		center_x, center_y = center
		points = []
		points.extend((center_x - simple_karel_width / 2 , center_y - simple_karel_height / 2))
		points.extend((center_x - simple_karel_width / 2 , center_y + simple_karel_height / 2))
		points.extend((center_x, center_y + simple_karel_height / 2))
		points.extend((center_x + simple_karel_width / 2, center_y))
		points.extend((center_x, center_y - simple_karel_height / 2))
		points.extend((center_x - simple_karel_width / 2 , center_y - simple_karel_height / 2))
		self.rotate_points(center, points, direction)
		self.create_polygon(points, fill="white", outline="black", width=KAREL_LINE_WIDTH, tag="karel")

	def calculate_corner_x(self, avenue):
		return self.left_x + self.cell_size / 2 + (avenue - 1) * self.cell_size

	def calculate_corner_y(self, street):
		return self.top_y + self.cell_size / 2 + (self.world.num_streets - street) * self.cell_size

	def click_in_world(self, x, y):
		x = x - self.left_x 
		y = y - self.top_y
		return 0 <= x < self.boundary_width and 0 <= y < self.boundary_height

	def calculate_location(self, x, y):
		x = x - self.left_x
		y = y - self.top_y
		return int(max(x,0) // self.cell_size) + 1, int(max((self.boundary_height - 1 - y), 0) // self.cell_size) + 1

	def find_nearest_wall(self, x, y, avenue, street):
		corner_x = self.calculate_corner_x(avenue)
		corner_y = self.calculate_corner_y(street)

		if x > (corner_x + self.cell_size / 2 - self.cell_size * WALL_DETECTION_THRESHOLD):
			# Check for a wall to the east
			return Wall(avenue, street, Direction.EAST)
		if x < (corner_x - self.cell_size / 2 + self.cell_size * WALL_DETECTION_THRESHOLD):
			# Check for a wall to the west
			return Wall(avenue, street, Direction.WEST)
		if y > (corner_y + self.cell_size / 2 - self.cell_size * WALL_DETECTION_THRESHOLD):
			# Check for a wall to the south
			return Wall(avenue, street, Direction.SOUTH)
		if y < (corner_y - self.cell_size / 2 + self.cell_size * WALL_DETECTION_THRESHOLD):
			# Check for a wall to the north
			return Wall(avenue, street, Direction.NORTH)

		# No wall within threshold distance
		return None
		
	@staticmethod
	def rotate_points(center, points, direction):
		"""
		Rotation logic derived from http://effbot.org/zone/tkinter-complex-canvas.htm
		"""
		cangle = cmath.exp(direction*1j)
		center = complex(center[0], center[1])
		for i in range(0, len(points), 2):
			x = points[i]
			y = points[i+1]
			v = cangle * (complex(x, y) - center) + center
			points[i] = v.real 
			points[i+1] = v.imag
