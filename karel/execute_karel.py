import tkinter as tk
from KarelApplication import KarelApplication
from KarelWorld import KarelWorld

def start_karel_application(args):
	print(args)
	world = KarelWorld(args.world_file)
	root = tk.Tk()
	app = KarelApplication(master=root, world=world)
	app.mainloop()	


if __name__ == "__main__":
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument(
		'code_file', type=argparse.FileType('r'), 
		help='File path of the code file containing Karel commands'
	)
	parser.add_argument(
		'world_file', type=argparse.FileType('r'), 
		help='File path of the world file describing the world in which to initialize Karel',
	)
	args = parser.parse_args()
	start_karel_application(args)
