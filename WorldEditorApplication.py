import tkinter as tk
from karel.KarelWorld import KarelWorld
from karel.Karel import Karel
from karel.kareldefinitions import *
from karel.KarelCanvas import KarelCanvas
from tkinter.filedialog import askopenfilename
from tkinter import simpledialog, messagebox

class WorldBuilderApplication(tk.Frame):
	def __init__(self, master=None, window_width=800, window_height=600, canvas_width=600, canvas_height=400):
		# set window background to contrast white Karel canvas 
		master.configure(background=LIGHT_GREY)

		# configure location of canvas to expand to fit window resizing
		master.rowconfigure(0, weight=1)
		master.columnconfigure(1, weight=1)

		super().__init__(master, background=LIGHT_GREY)

		self.icon = DEFAULT_ICON
		self.window_width = window_width
		self.window_height = window_height
		self.canvas_width = canvas_width
		self.canvas_height = canvas_height
		self.master = master
		self.master.title("Karel World Builder")
		self.set_dock_icon()
		self.grid(row=0, column=0)
		self.setup_world()
		self.create_canvas()
		self.create_buttons()



	def set_dock_icon(self):
		# make Karel dock icon image
		img = tk.Image("photo", file="./karel/icon.png")
		self.master.tk.call('wm', 'iconphoto', self.master._w, img)

	def setup_world(self):
		load_existing = messagebox.askyesno("World Selection", "Would you like to load an existing world? \n\nSelecting 'No' will allow you to start with a blank slate.", parent=self.master)
		if load_existing:
			self.load_world(init=True)
		else:
			self.create_new_world(init=True)


	def create_new_world(self, init=False):
		num_avenues = simpledialog.askinteger("New World Size", "How many avenues should the new world have?",
											  parent=self.master, 
											  minvalue=MIN_DIMENSIONS, maxvalue=MAX_DIMENSIONS)

		if not num_avenues: return

		num_streets = simpledialog.askinteger("New World Size", "How many streets should the new world have?",
										 	  parent=self.master, 
										 	  minvalue=MIN_DIMENSIONS, maxvalue=MAX_DIMENSIONS)
		if not num_avenues: return

		if init:
			self.world = KarelWorld()
			self.karel = Karel(self.world)
		else:
			self.world.reload_world()
			self.karel.reset_state()

		self.world.num_avenues = num_avenues
		self.world.num_streets = num_streets
		if not init:
			self.canvas.redraw_all()

	def load_world(self, init=False):
		filename = askopenfilename(initialdir="./worlds", title="Select Karel World", filetypes=[("Karel Worlds", "*.w")])
		# User hit cancel and did not select file, so leave world as-is
		if filename == "": 
			if init:
				self.setup_world()
			return
		
		if init:
			self.world = KarelWorld()
			self.world.reload_world(filename=filename)
			self.karel = Karel(self.world)
		else:
			self.world.reload_world(filename=filename)
			self.karel.reset_state()
		
		if not init:
			self.canvas.redraw_all()	
			self.reset_direction_radio_buttons()
			self.reset_beeper_bag_radio_buttons()

	def create_canvas(self):
		"""
		This method creates the canvas on which Karel and Karel's 
		world are drawn. 
		"""
		self.canvas = KarelCanvas(self.canvas_width, self.canvas_height, self.master, world=self.world, karel=self.karel)
		self.canvas.grid(column=1, row=0, sticky="NESW")
		self.canvas.bind("<Configure>", lambda t: self.canvas.redraw_all())
		self.canvas.bind("<Button-1>", self.handle_mouse_event)
		self.canvas.bind("<B1-Motion>", self.handle_mouse_event)


	def create_buttons(self):
		"""
		This method creates the three buttons that appear on the left
		side of the screen. These buttons control the start of Karel 
		execution, resetting Karel's state, and loading new worlds.
		"""	
		self.program_control_button = tk.Button(self, highlightthickness=0, highlightbackground='white')
		self.program_control_button["text"] = "New World"
		self.program_control_button["command"] = self.create_new_world
		self.program_control_button.grid(column=0, row=0, padx=PAD_X, pady=PAD_Y)

		self.load_world_button = tk.Button(self, highlightthickness=0, text="Load World", command=self.load_world)
		self.load_world_button.grid(column=0, row=2, padx=PAD_X, pady=PAD_Y)

		# TODO: add save world button 

		self.create_direction_radio_buttons()
		self.create_beeper_bag_radio_buttons()
		self.create_action_radio_buttons()

	def create_direction_radio_buttons(self):
		self.dir_radio_frame = tk.Frame(self, bg=LIGHT_GREY)
		self.dir_radio_frame.grid(row=3, column=0, padx=PAD_X, pady=PAD_Y, sticky="ew")

		self.karel_direction_var = tk.StringVar()
		self.karel_direction_var.set(DIRECTIONS_MAP_INVERSE[self.karel.direction])
		self.karel_direction_var.trace("w", self.update_karel_direction)

		dir_label = tk.Label(self.dir_radio_frame, text="Karel Direction: ", bg=LIGHT_GREY)
		dir_label.pack(side="left")
		tk.Radiobutton(self.dir_radio_frame, text="E", variable=self.karel_direction_var,value="east",bg=LIGHT_GREY).pack(side="left") 
		tk.Radiobutton(self.dir_radio_frame, text="W", variable=self.karel_direction_var,value="west",bg=LIGHT_GREY).pack(side="left")
		tk.Radiobutton(self.dir_radio_frame, text="N", variable=self.karel_direction_var,value="north",bg=LIGHT_GREY).pack(side="left")
		tk.Radiobutton(self.dir_radio_frame, text="S", variable=self.karel_direction_var,value="south",bg=LIGHT_GREY).pack(side="left")
		
	def create_beeper_bag_radio_buttons(self):
		self.beeper_bag_radio_frame = tk.Frame(self, bg=LIGHT_GREY)
		self.beeper_bag_radio_frame.grid(row=4, column=0, padx=PAD_X, pady=PAD_Y, sticky="ew")

		self.beeper_bag_var = tk.IntVar()
		self.beeper_bag_var.set(self.karel.num_beepers)
		self.beeper_bag_var.trace("w", self.update_karel_num_beepers)

		beeper_bag_label = tk.Label(self.beeper_bag_radio_frame, text="Beeper Bag: ", bg=LIGHT_GREY)
		beeper_bag_label.pack(side="left")
		tk.Radiobutton(self.beeper_bag_radio_frame, text="Empty", variable=self.beeper_bag_var,value=0,bg=LIGHT_GREY).pack(side="left")
		tk.Radiobutton(self.beeper_bag_radio_frame, text="Infinite", variable=self.beeper_bag_var,value=INFINITY,bg=LIGHT_GREY).pack(side="left")

	def create_action_radio_buttons(self):
		self.action_radio_frame = tk.Frame(self, bg=LIGHT_GREY)
		self.action_radio_frame.grid(row=5, column=0, padx=PAD_X, pady=PAD_Y, sticky="ew")

		self.action_var = tk.StringVar()
		self.action_var.set("move_karel")
		# self.action_var.trace("w", self.update_karel_num_beepers)

		action_label = tk.Label(self.action_radio_frame, text="Action: ", bg=LIGHT_GREY)
		action_label.pack(side="left")
		tk.Radiobutton(self.action_radio_frame, text="Move Karel", variable=self.action_var,value="move_karel",bg=LIGHT_GREY).pack()
		tk.Radiobutton(self.action_radio_frame, text="Add Wall", variable=self.action_var,value="add_wall",bg=LIGHT_GREY).pack()
		tk.Radiobutton(self.action_radio_frame, text="Remove Wall", variable=self.action_var,value="remove_wall",bg=LIGHT_GREY).pack()
		tk.Radiobutton(self.action_radio_frame, text="Add Beeper", variable=self.action_var,value="add_beeper",bg=LIGHT_GREY).pack()
		tk.Radiobutton(self.action_radio_frame, text="Remove Beeper", variable=self.action_var,value="remove_beeper",bg=LIGHT_GREY).pack()
		tk.Radiobutton(self.action_radio_frame, text="Clear All Beepers", variable=self.action_var,value="clear_beepers",bg=LIGHT_GREY).pack()


	def reset_direction_radio_buttons(self):
		self.karel_direction_var.set(DIRECTIONS_MAP_INVERSE[self.karel.direction])

	def reset_beeper_bag_radio_buttons(self):
		self.beeper_bag_var.set(self.karel.num_beepers)

	def update_karel_direction(self, *args):
		new_dir = self.karel_direction_var.get()
		self.karel.direction = DIRECTIONS_MAP[new_dir]
		self.canvas.redraw_karel()

	def update_karel_num_beepers(self, *args):
		new_num_beepers = self.beeper_bag_var.get()
		self.karel.num_beepers = new_num_beepers

	def handle_mouse_event(self, event):
		avenue, street = self.canvas.calculate_location(event.x, event.y)
		action = self.action_var.get()
		if action == "move_karel":
			if avenue != self.karel.avenue or street != self.karel.street:
				self.karel.avenue = avenue
				self.karel.street = street
				self.canvas.redraw_karel()
		print(avenue, street)


if __name__ == "__main__":
	root = tk.Tk()
	world_builder = WorldBuilderApplication(master=root)
	world_builder.mainloop()
