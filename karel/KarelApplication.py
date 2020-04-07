"""
This file defines the GUI for running Karel programs. 

Original Author: Nicholas Bowman
Credits: Kylie Jue 
License: MIT
Version: 1.0.0
Email: nbowman@stanford.edu
Date of Creation: 10/1/2019
Last Modified: 3/31/2020
"""

import tkinter as tk
from karel.kareldefinitions import *
from karel.KarelCanvas import KarelCanvas
from time import sleep
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showerror, showwarning
import os
import traceback as tb
import inspect
import importlib.util
import sys


class KarelApplication(tk.Frame):
	def __init__(self, karel, world, code_file, master=None, window_width=800, window_height=600, canvas_width=600, canvas_height=400):
		# set window background to contrast white Karel canvas 
		master.configure(background=LIGHT_GREY)

		# configure location of canvas to expand to fit window resizing
		master.rowconfigure(0, weight=1)
		master.columnconfigure(1, weight=1)

		# set master geometry
		master.geometry(str(window_width) + "x" + str(window_height))

		super().__init__(master, background=LIGHT_GREY)

		self.karel = karel
		self.world = world
		self.code_file = code_file
		if not self.load_student_module():
			master.destroy()
			return
		self.icon = DEFAULT_ICON
		self.window_width = window_width
		self.window_height = window_height
		self.canvas_width = canvas_width
		self.canvas_height = canvas_height
		self.master = master
		self.master.title(self.module_name)
		self.set_dock_icon()
		self.inject_namespace()
		self.grid(row=0, column=0)
		self.create_menubar()
		self.create_canvas()
		self.create_buttons()
		self.create_slider()
		self.create_status_label()

	def set_dock_icon(self):
		# make Karel dock icon image
		img = tk.Image("photo", file="./karel/icon.png")
		self.master.tk.call('wm', 'iconphoto', self.master._w, img)

	def load_student_module(self):
		# This process is used to extract a module from an arbitarily located
		# file that contains student code
		# Adapted from https://stackoverflow.com/questions/67631/how-to-import-a-module-given-the-full-path
		self.base_filename = os.path.basename(self.code_file)
		self.module_name = os.path.splitext(self.base_filename)[0]
		spec = importlib.util.spec_from_file_location(self.module_name, os.path.abspath(self.code_file))
		try:
			self.mod = importlib.util.module_from_spec(spec)
			spec.loader.exec_module(self.mod)
		except Exception as e:
			# Handle syntax errors and only print location of error
			print("here")
			print("\n".join(tb.format_exc(limit=0).split("\n")[1:]))
			return False

		# Do not proceed if the student has not defined a main function
		if not hasattr(self.mod, "main"):
			print("Couldn't find the main() function. Are you sure you have one?")
			return False

		return True

	def create_menubar(self):
		menubar = tk.Menu(self.master)

		fileMenu = tk.Menu(menubar, tearoff=False)
		menubar.add_cascade(label="File", menu=fileMenu)
		fileMenu.add_command(label="Exit", underline=1,
							 command=self.master.quit, accelerator="Cmd+W")

		iconmenu = tk.Menu(menubar, tearoff=0)
		menubar.add_cascade(label="Select Icon", menu=iconmenu)

		iconmenu.add_command(label="Karel", command=lambda: self.set_icon("karel"))
		iconmenu.add_command(label="Simple", command=lambda: self.set_icon("simple"))

		self.bind_all("<Command-w>", self.quit)

		self.master.config(menu=menubar)

	def quit(self, event):
		sys.exit(0)

	def set_icon(self, icon):
		self.canvas.set_icon(icon)
		self.canvas.redraw_karel()

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
		self.canvas = KarelCanvas(self.canvas_width, self.canvas_height, self.master, world=self.world, karel=self.karel)
		self.canvas.grid(column=1, row=0, sticky="NESW")
		self.canvas.bind("<Configure>", lambda t: self.canvas.redraw_all())

	def create_buttons(self):
		"""
		This method creates the three buttons that appear on the left
		side of the screen. These buttons control the start of Karel 
		execution, resetting Karel's state, and loading new worlds.
		"""	
		self.program_control_button = tk.Button(self, highlightthickness=0, highlightbackground='white')
		self.program_control_button["text"] = "Run Program"
		self.program_control_button["command"] = self.run_program
		self.program_control_button.grid(column=0, row=0, padx=PAD_X, pady=PAD_Y, sticky="ew")

		self.load_world_button = tk.Button(self, highlightthickness=0, text="Load World", command=self.load_world)
		self.load_world_button.grid(column=0, row=2, padx=PAD_X, pady=PAD_Y, sticky="ew")
	
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
			self.canvas.redraw_karel()
			# delay by specified amount
			sleep(1 - self.speed.get() / 100)
		return wrapper

	def beeper_action_decorator(self, karel_fn):
		def wrapper():
			# execute Karel function
			karel_fn()
			# redraw canavs with updated state of the world
			self.canvas.redraw_beepers()
			self.canvas.redraw_karel()
			# delay by specified amount
			sleep(1 - self.speed.get() / 100)
		return wrapper

	def corner_action_decorator(self, karel_fn):
		def wrapper(color):
			# execute Karel function
			karel_fn(color)
			# redraw canvas with updated state of the world
			self.canvas.redraw_corners()
			self.canvas.redraw_beepers()
			self.canvas.redraw_karel()
			# delay by specified amount
			sleep(1 - self.speed.get() / 100)
		return wrapper 

	def inject_namespace(self):
		"""
		This function is responsible for doing some Python hackery
		that associates the generic commands the student wrote in their
		file with specific commands relating to the Karel object that exists
		in the world.
		"""

		self.mod.turn_left = self.karel_action_decorator(self.karel.turn_left)
		self.mod.move = self.karel_action_decorator(self.karel.move)
		self.mod.pick_beeper = self.beeper_action_decorator(self.karel.pick_beeper)
		self.mod.put_beeper = self.beeper_action_decorator(self.karel.put_beeper)
		self.mod.facing_north = self.karel.facing_north
		self.mod.facing_south = self.karel.facing_south
		self.mod.facing_east = self.karel.facing_east
		self.mod.facing_west = self.karel.facing_west
		self.mod.not_facing_north = self.karel.not_facing_north
		self.mod.not_facing_south = self.karel.not_facing_south
		self.mod.not_facing_east = self.karel.not_facing_east
		self.mod.not_facing_west = self.karel.not_facing_west
		self.mod.front_is_clear = self.karel.front_is_clear
		self.mod.beepers_present = self.karel.beepers_present
		self.mod.no_beepers_present = self.karel.no_beepers_present
		self.mod.beepers_in_bag = self.karel.beepers_in_bag
		self.mod.no_beepers_in_bag = self.karel.no_beepers_in_bag
		self.mod.front_is_blocked = self.karel.front_is_blocked
		self.mod.left_is_clear = self.karel.left_is_clear
		self.mod.left_is_blocked = self.karel.left_is_blocked
		self.mod.right_is_clear = self.karel.right_is_clear
		self.mod.right_is_blocked = self.karel.right_is_blocked
		self.mod.paint_corner = self.corner_action_decorator(self.karel.paint_corner)
		self.mod.corner_color_is = self.karel.corner_color_is

	def disable_buttons(self):
		self.program_control_button.configure(state="disabled")
		self.load_world_button.configure(state="disabled")

	def enable_buttons(self):
		self.program_control_button.configure(state="normal")
		self.load_world_button.configure(state="normal")

	def display_error_traceback(self, e):
		print("Traceback (most recent call last):")
		display_frames = []
		# walk through all the frames in stack trace at time of failure
		for frame, lineno in tb.walk_tb(e.__traceback__):
			frame_info = inspect.getframeinfo(frame)
			# get the name of the file corresponding to the current frame
			filename = frame_info.filename
			# Only display frames generated within the student's code
			if self.base_filename in filename:
				display_frames.append((frame, lineno))
		
		print(("".join(tb.format_list(tb.StackSummary.extract(display_frames)))).strip())
		print(f"{type(e).__name__}: {str(e)}")

	def run_program(self):
		# Error checking for existence of main function completed in prior file
		try:
			self.status_label.configure(text="Running...", fg="brown")
			self.disable_buttons()
			self.mod.main()
			self.status_label.configure(text="Finished running.", fg="green")

		except (KarelException, NameError) as e:
			# Generate popup window to let the user know their program crashed
			self.status_label.configure(text="Program crashed, check console for details.", fg="red")
			self.display_error_traceback(e)
			self.update()
			showwarning("Karel Error", "Karel Crashed!\nCheck the terminal for more details.")

		finally:
			# Update program control button to force user to reset world before running program again
			self.program_control_button["text"] = "Reset World"
			self.program_control_button["command"] = self.reset_world 
			self.enable_buttons()

	def reset_world(self):
		self.karel.reset_state()
		self.world.reset_world()
		self.canvas.redraw_all()
		self.status_label.configure(text="Reset to initial state.", fg="black")
		# Once world has been reset, program control button resets to "run" mode
		self.program_control_button["text"] = "Run Program"
		self.program_control_button["command"] = self.run_program 
		self.update()

	def load_world(self):
		filename = askopenfilename(initialdir="../worlds", title="Select Karel World", filetypes=[("Karel Worlds", "*.w")], parent=self.master)
		# User hit cancel and did not select file, so leave world as-is
		if filename == "": return
		self.world.reload_world(filename=filename)
		self.karel.reset_state()
		self.canvas.redraw_all()
		# Reset speed slider
		self.scale.set(self.world.init_speed)
		self.status_label.configure(text=f"Loaded world from {os.path.basename(filename)}.", fg="black")

		# Make sure program control button is set to 'run' mode
		self.program_control_button["text"] = "Run Program"
		self.program_control_button["command"] = self.run_program 