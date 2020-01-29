import tkinter as tk
from KarelApplication import KarelApplication
from KarelWorld import KarelWorld
from Karel import Karel
from kareldefinitions import *

def start_karel_application(args):
	# Create the world as specified in the given world file
	world = KarelWorld(args.world_file)

	# Create Karel and assign it to live in the newly created world
	karel = Karel(world)

	# Initialize root Tk Window and spawn Karel application
	root = tk.Tk()
	app = KarelApplication(karel, world, args.code_file, master=root)
	app.mainloop()	


if __name__ == "__main__":
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument(
		'code_file', type=str, 
		help='File path of the code file containing Karel commands'
	)
	parser.add_argument(
		'world_file', type=argparse.FileType('r'), 
		help='File path of the world file describing the world in which to initialize Karel',
	)
	args = parser.parse_args()
	start_karel_application(args)
