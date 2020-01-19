import tkinter as tk
from kareldefinitions import *

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
		self.speed.trace('w', self.update_speed)

		self.scale = tk.Scale(self.slider_frame, orient=tk.HORIZONTAL, variable=self.speed, showvalue=0)
		self.scale.set(INIT_SPEED)
		self.scale.pack()

	def create_canvas(self):
		"""
		This method creates the canvas on which Karel and Karel's 
		world are drawn. 
		"""
		self.canvas = tk.Canvas(self.master, width=self.canvas_width, height=self.canvas_height, bg="white")
		self.canvas.grid(column=1, row=0, sticky="NESW")


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

		self.reset_program = tk.Button(self, highlightthickness=0, text="Reset Program", command=self.reset_program)
		self.reset_program.grid(column=0, row=1, padx=PAD_X, pady=PAD_Y, sticky="ew")

		self.load_world = tk.Button(self, highlightthickness=0, text="Load World", command=self.load_world)
		self.load_world.grid(column=0, row=2, padx=PAD_X, pady=PAD_Y, sticky="ew")
	
	def create_status_label(self):
		"""
		This function creates the status label at the bottom of the window.
		"""
		self.status_label = tk.Label(self.master, text="Welcome to Karel!", bg=LIGHT_GREY)
		self.status_label.grid(row=1, column=0, columnspan=2)

	def inject_namespace(self):
		"""
		This function is responsible for doing some Python hackery
		that associates the generic commands the student wrote in their
		file with specific commands relating to the Karel object that exists
		in the world.

		TODO: Find a better way to do this injection that does not involve
		manually specifying all Karel commands 

		"""
		self.mod.turn_left = self.karel.turn_left
		self.mod.move = self.karel.move
		self.mod.pick_beeper = self.karel.pick_beeper
		self.mod.put_beeper = self.karel.put_beeper
		self.mod.facing_north = self.karel.facing_north
		self.mod.facing_south = self.karel.facing_south
		self.mod.facing_east = self.karel.facing_east
		self.mod.facing_west = self.karel.facing_west
		self.mod.front_is_clear = self.karel.front_is_clear
		self.mod.on_beeper = self.karel.on_beeper

	def execute_task(self):
		self.mod.main()

	def reset_program(self):
		pass

	def load_world(self):
		pass

	def update_speed(self, *args):
		print(self.speed.get())


