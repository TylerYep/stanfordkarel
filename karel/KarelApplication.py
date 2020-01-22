import tkinter as tk
import math
import cmath
from kareldefinitions import *
from time import sleep
from tkinter.filedialog import askopenfilename
import os

class KarelApplication(tk.Frame):
	def __init__(self, karel, world, mod, master=None, window_width=800, window_height=600, canvas_width=600, canvas_height=400):
		# set window background to contrast white Karel canvas 
		master.configure(background=LIGHT_GREY)

		# configure location of canvas to expand to fit window resizing
		master.rowconfigure(0, weight=1)
		master.columnconfigure(1, weight=1)

		super().__init__(master, background=LIGHT_GREY)
		self.karel = karel
		self.world = world
		self.mod = mod
		self.window_width = window_width
		self.window_height = window_height
		self.canvas_width = canvas_width
		self.canvas_height = canvas_height
		self.master = master
		self.inject_namespace()
		self.grid(row=0, column=0)
		self.create_canvas()
		self.create_buttons()
		self.create_slider()
		self.create_status_label()
		self.draw_world()
		self.draw_karel()

	def create_slider(self):
		"""
		This method creates a frame containing three widgets: 
		two labels on either side of a scale slider to control
		Karel execution speed. 
		"""
		self.slider_frame = tk.Frame(self, bg=LIGHT_GREY)
		self.slider_frame.grid(row=3, column=0, padx=PAD_X, pady=PAD_Y, sticky="ew")

		self.fast_label = tk.Label(self.slider_frame, text="Fast", bg=LIGHT_GREY)
		self.fast_label.pack(side="right")

		self.slow_label = tk.Label(self.slider_frame, text="Slow", bg=LIGHT_GREY)
		self.slow_label.pack(side="left")

		self.speed = tk.IntVar()

		self.scale = tk.Scale(self.slider_frame, orient=tk.HORIZONTAL, variable=self.speed, showvalue=0)
		self.scale.set(self.world.init_speed)
		self.scale.pack()

	def create_canvas(self):
		"""
		This method creates the canvas on which Karel and Karel's 
		world are drawn. 
		"""
		self.canvas = tk.Canvas(self.master, width=self.canvas_width, height=self.canvas_height, bg="white")
		self.canvas.grid(column=1, row=0, sticky="NESW")
		self.canvas.bind("<Configure>", lambda t: self.redraw_canvas())

	def redraw_canvas(self):
		self.canvas.delete("all")
		self.draw_world()
		self.draw_karel()
		self.canvas.update()

	def redraw_karel(self):
		self.canvas.delete("karel")
		self.draw_karel()
		self.canvas.update()

	def redraw_beepers(self):
		"""
		TODO: implement more efficient manner that does not require deleting 
		and redrawing all beepers
		"""
		self.canvas.delete("beeper")
		self.draw_all_beepers()
		self.canvas.update()

	def create_buttons(self):
		"""
		This method creates the three buttons that appear on the left
		side of the screen. These buttons control the start of Karel 
		execution, resetting Karel's state, and loading new worlds.
		"""	
		self.start_program = tk.Button(self, highlightthickness=0, highlightbackground='white')
		self.start_program["text"] = "Start Program"
		self.start_program["command"] = self.execute_task
		self.start_program.grid(column=0, row=0, padx=PAD_X, pady=PAD_Y, sticky="ew")

		self.reset_program = tk.Button(self, highlightthickness=0, text="Reset Program", command=self.reset_world)
		self.reset_program.grid(column=0, row=1, padx=PAD_X, pady=PAD_Y, sticky="ew")

		self.load_world = tk.Button(self, highlightthickness=0, text="Load World", command=self.load_world)
		self.load_world.grid(column=0, row=2, padx=PAD_X, pady=PAD_Y, sticky="ew")
	
	def create_status_label(self):
		"""
		This function creates the status label at the bottom of the window.
		"""
		self.status_label = tk.Label(self.master, text="Welcome to Karel!", bg=LIGHT_GREY)
		self.status_label.grid(row=1, column=0, columnspan=2)

	def karel_action_decorator(self, karel_fn):
		def wrapper():
			# execute Karel function
			karel_fn()
			# redraw canavs with updated state of the world
			self.redraw_karel()
			# TODO: do calculation to dynamically update delay
			sleep(1 - self.speed.get() / 100)
		return wrapper

	def beeper_action_decorator(self, karel_fn):
		def wrapper():
			# execute Karel function
			karel_fn()
			# redraw canavs with updated state of the world
			self.redraw_beepers()
			# TODO: do calculation to dynamically update delay
			sleep(1 - self.speed.get() / 100)
		return wrapper

	def inject_namespace(self):
		"""
		This function is responsible for doing some Python hackery
		that associates the generic commands the student wrote in their
		file with specific commands relating to the Karel object that exists
		in the world.

		TODO: Find a better way to do this injection that does not involve
		manually specifying all Karel commands 

		"""

		self.mod.turn_left = self.karel_action_decorator(self.karel.turn_left)
		self.mod.move = self.karel_action_decorator(self.karel.move)
		self.mod.pick_beeper = self.beeper_action_decorator(self.karel.pick_beeper)
		self.mod.put_beeper = self.beeper_action_decorator(self.karel.put_beeper)
		self.mod.facing_north = self.karel.facing_north
		self.mod.facing_south = self.karel.facing_south
		self.mod.facing_east = self.karel.facing_east
		self.mod.facing_west = self.karel.facing_west
		self.mod.front_is_clear = self.karel.front_is_clear
		self.mod.on_beeper = self.karel.on_beeper
		self.mod.front_is_blocked = self.karel.front_is_blocked
		self.mod.left_is_clear = self.karel.left_is_clear
		self.mod.left_is_blocked = self.karel.left_is_blocked
		self.mod.right_is_clear = self.karel.right_is_clear
		self.mod.right_is_blocked = self.karel.right_is_blocked

	def execute_task(self):
		# Error checking for existence of main function completed in prior file
		try:
			self.status_label.configure(text="Running...", fg="brown")
			self.mod.main()
			# TODO: update status label to indicate successful completion
			self.status_label.configure(text="Finished running.", fg="green")

		except KarelException as e:
			# TODO: parse traceback and deliver helpful error message popup
			# similar to old Karel bug icon + message
			pass


	def reset_world(self):
		self.karel.reset_state()
		self.world.reset_world()
		self.redraw_canvas()
		self.status_label.configure(text="Reset to initial state.", fg="black")


	def load_world(self):
		filename = askopenfilename(initialdir="worlds", title="Select Karel World", filetypes=[("Karel Worlds", "*.w")])
		# User hit cancel and did not select file, so leave world as-is
		if filename == "": return
		self.world.reload_world(filename)
		self.karel.reset_state()
		self.redraw_canvas()
		self.status_label.configure(text=f"Loaded world from {os.path.basename(filename)}.", fg="black")


	def draw_world(self):
		self.init_geometry_values()
		self.draw_bounding_rectangle()
		self.label_axes()
		self.draw_corners()
		self.draw_all_beepers()
		self.draw_all_walls()

	def init_geometry_values(self):
		self.canvas.update()

		# Calculate the maximum possible cell size in both directions
		# We will use the smaller of the two as the bounding cell size
		horizontal_cell_size = (self.canvas.winfo_width() - 2 * BORDER_OFFSET) / self.world.num_avenues
		vertical_cell_size = (self.canvas.winfo_height() - 2 * BORDER_OFFSET) / self.world.num_streets

		# Save this as an instance variable for later use
		self.cell_size = min(horizontal_cell_size, vertical_cell_size)

		self.boundary_height = self.cell_size * self.world.num_streets
		self.boundary_width = self.cell_size * self.world.num_avenues

		# Save all these as instance variables as well
		self.left_x = self.canvas.winfo_width() / 2 - self.boundary_width / 2
		self.top_y = self.canvas.winfo_height() / 2 - self.boundary_height / 2
		self.right_x = self.left_x + self.boundary_width
		self.bottom_y = self.top_y + self.boundary_height

	def draw_bounding_rectangle(self):
		# Draw the external bounding lines of Karel's world
		self.canvas.create_line(self.left_x, self.top_y, self.right_x, self.top_y, width=LINE_WIDTH)
		self.canvas.create_line(self.left_x, self.top_y, self.left_x, self.bottom_y, width=LINE_WIDTH)
		self.canvas.create_line(self.right_x, self.top_y, self.right_x, self.bottom_y, width=LINE_WIDTH)
		self.canvas.create_line(self.left_x, self.bottom_y, self.right_x, self.bottom_y, width=LINE_WIDTH)

	def label_axes(self):
		# Label the avenue axes
		for avenue in range(1, self.world.num_avenues + 1):
			label_x = self.calculate_corner_x(avenue)
			label_y = self.bottom_y + LABEL_OFFSET
			self.canvas.create_text(label_x, label_y, text=str(avenue), font="Arial 10")
		
		# Label the street axes
		for street in range(1, self.world.num_streets + 1):
			label_x = self.left_x - LABEL_OFFSET
			label_y = self.calculate_corner_y(street)
			self.canvas.create_text(label_x, label_y, text=str(street), font="Arial 10")

	def draw_corners(self):
		# Draw all corner markers in the world 
		for avenue in range(1, self.world.num_avenues + 1):
			for street in range(1, self.world.num_streets + 1):
				corner_x = self.calculate_corner_x(avenue)
				corner_y = self.calculate_corner_y(street)
				self.canvas.create_line(corner_x, corner_y - CORNER_SIZE, corner_x, corner_y + CORNER_SIZE)
				self.canvas.create_line(corner_x - CORNER_SIZE, corner_y, corner_x + CORNER_SIZE, corner_y)

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
		self.canvas.create_polygon(points, fill="light grey", outline="black", tag="beeper")

		if count > 1: 
			self.canvas.create_text(corner_x, corner_y, text=str(count), font="Arial 12", tag="beeper")


	def draw_all_walls(self):
		for wall in self.world.walls:
			self.draw_wall(wall)

	def draw_wall(self, wall):
		avenue, street, direction = wall.avenue, wall.street, wall.direction
		corner_x = self.calculate_corner_x(avenue)
		corner_y = self.calculate_corner_y(street)


		if direction == Direction.NORTH:
			self.canvas.create_line(corner_x - self.cell_size / 2, 
									corner_y - self.cell_size / 2, 
									corner_x + self.cell_size / 2, 
									corner_y - self.cell_size / 2,
									width=LINE_WIDTH)
		if direction == Direction.SOUTH:
			self.canvas.create_line(corner_x - self.cell_size / 2, 
									corner_y + self.cell_size / 2, 
									corner_x + self.cell_size / 2, 
									corner_y + self.cell_size / 2, 
									width=LINE_WIDTH)
		if direction == Direction.EAST:
			self.canvas.create_line(corner_x + self.cell_size / 2,
									corner_y - self.cell_size / 2,
									corner_x + self.cell_size / 2,
									corner_y + self.cell_size / 2, 
									width=LINE_WIDTH)
		if direction == Direction.WEST:
			self.canvas.create_line(corner_x - self.cell_size / 2,
									corner_y - self.cell_size / 2,
									corner_x - self.cell_size / 2,
									corner_y + self.cell_size / 2,
									width=LINE_WIDTH)

	def draw_karel(self):
		corner_x = self.calculate_corner_x(self.karel.avenue)
		corner_y = self.calculate_corner_y(self.karel.street)
		center = (corner_x, corner_y)

		karel_origin_x = corner_x - self.cell_size / 2 + KAREL_LEFT_HORIZONTAL_PAD * self.cell_size
		karel_origin_y = corner_y - self.cell_size / 2 + KAREL_VERTICAL_OFFSET * self.cell_size

		self.draw_karel_outer_body(karel_origin_x, karel_origin_y, center, self.karel.direction.value)
		self.draw_karel_inner_components(karel_origin_x, karel_origin_y, center, self.karel.direction.value)
		self.draw_karel_legs(karel_origin_x, karel_origin_y, center, self.karel.direction.value)

	def draw_karel_outer_body(self, x, y, center, direction):
		points = []
		
		# Top-left point (referred to as origin) of Karel's body
		points.extend((x,y))

		# Calculate Karel's height and width as well as missing diag segments
		width = self.cell_size * KAREL_WIDTH
		height = self.cell_size * KAREL_HEIGHT
		lower_left_missing = (self.cell_size * KAREL_LOWER_LEFT_DIAG) / math.sqrt(2)
		upper_right_missing = (self.cell_size * KAREL_UPPER_RIGHT_DIAG) / math.sqrt(2)

		# These two points define Karel's upper right
		points.extend((x + width - upper_right_missing, y))
		points.extend((x + width, y + upper_right_missing))

		# Karel's bottom right edge
		points.extend((x + width, y + height))

		# These two points define Karel's lower left 
		points.extend((x + lower_left_missing, y + height))
		points.extend((x, y + height - lower_left_missing))

		# Complete the polygon
		points.extend((x,y))

		self.rotate_points(center, points, direction)

		self.canvas.create_polygon(points, fill="white", outline="black", width=KAREL_LINE_WIDTH, tag="karel")

	def draw_karel_inner_components(self, x, y, center, direction):
		inner_x = x + self.cell_size * KAREL_INNER_OFFSET
		inner_y = y + self.cell_size * KAREL_INNER_OFFSET

		inner_height = self.cell_size * KAREL_INNER_HEIGHT
		inner_width = self.cell_size * KAREL_INNER_WIDTH

		points = [inner_x, inner_y, inner_x + inner_width, inner_y, inner_x + inner_width, inner_y + inner_height, inner_x, inner_y + inner_height, inner_x, inner_y]
		self.rotate_points(center, points, direction)
		self.canvas.create_polygon(points, fill="white", outline="black", width=KAREL_LINE_WIDTH, tag="karel")

		karel_height = self.cell_size * KAREL_HEIGHT
		mouth_horizontal_offset = self.cell_size * KAREL_MOUTH_HORIZONTAL_OFFSET
		mouth_vertical_offset = self.cell_size * KAREL_MOUTH_VERTICAL_OFFSET
		mouth_width = self.cell_size * KAREL_MOUTH_WIDTH
		mouth_y = inner_y + inner_height + mouth_vertical_offset

		points = [x + mouth_horizontal_offset, mouth_y, x + mouth_horizontal_offset + mouth_width, mouth_y]
		self.rotate_points(center, points, direction)
		self.canvas.create_polygon(points, fill="white", outline="black", width=KAREL_LINE_WIDTH, tag="karel")

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
		self.canvas.create_polygon(points, fill="black", outline="black", width=KAREL_LINE_WIDTH, tag="karel")

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
		self.canvas.create_polygon(points, fill="black", outline="black", width=KAREL_LINE_WIDTH, tag="karel")

	def calculate_corner_x(self, avenue):
		return self.left_x + self.cell_size / 2 + (avenue - 1) * self.cell_size

	def calculate_corner_y(self, street):
		return self.top_y + self.cell_size / 2 + (self.world.num_streets - street) * self.cell_size
	
	def rotate_points(self, center, points, direction):
		"""
		Rotation logic derived from http://effbot.org/zone/tkinter-complex-canvas.htm
		"""
		cangle = cmath.exp(direction*1j)
		center = complex(center[0], center[1])
		for i in range(0, len(points), 2):
			x = points[i]
			y = points[i+1]
			v = cangle * (complex(x,y) - center) + center
			points[i] = v.real 
			points[i+1] = v.imag