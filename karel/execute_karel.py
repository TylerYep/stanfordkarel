import tkinter as tk
import importlib
import os
from KarelApplication import KarelApplication
from KarelWorld import KarelWorld
from Karel import Karel

def start_karel_application(args):

	# This process is used to extract a module from an arbitarily located
	# file that contains student code
	# Adapted from https://stackoverflow.com/questions/67631/how-to-import-a-module-given-the-full-path
	module_name = os.path.splitext(os.path.basename(args.code_file))[0]
	spec = importlib.util.spec_from_file_location(module_name, os.path.abspath(args.code_file))
	student_module = importlib.util.module_from_spec(spec)
	spec.loader.exec_module(student_module)

	# Do not proceed if the student has not defined a main function
	if not hasattr(student_module, "main"):
		print("Couldn't find the main() function. Are you sure you have one?")
		return

	# Create the world as specified in the given world file
	world = KarelWorld(args.world_file)

	# Create Karel and assign it to live in the newly created world
	karel = Karel(world)

	# Initialize root Tk Window and spawn Karel application
	root = tk.Tk()
	root.title(module_name)
	app = KarelApplication(karel, world, student_module, master=root)
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
