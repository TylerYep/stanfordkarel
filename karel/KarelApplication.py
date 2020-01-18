import tkinter as tk

class KarelApplication(tk.Frame):
	def __init__(self, karel, world, mod, master=None):
		super().__init__(master)
		self.karel = karel
		self.world = world
		self.mod = mod
		self.master = master
		self.inject_namespace()
		self.pack()
		self.create_widgets()

	def create_widgets(self):	
		self.hi_there = tk.Button(self)
		self.hi_there["text"] = "Hello World\n"
		self.hi_there["command"] = self.execute_task
		self.hi_there.pack(side="top")

		self.quit = tk.Button(self, text="QUIT", fg="red", command = self.master.destroy)
		self.quit.pack(side="bottom")

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


