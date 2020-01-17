import tkinter as tk

class KarelApplication(tk.Frame):
	def __init__(self, master=None, world=None):
		super().__init__(master)
		self.world = world
		self.master = master
		self.pack()
		self.create_widgets()

	def create_widgets(self):	
		self.hi_there = tk.Button(self)
		self.hi_there["text"] = "Hello World\n"
		self.hi_there["command"] = self.say_hi
		self.hi_there.pack(side="top")

		self.quit = tk.Button(self, text="QUIT", fg="red", command = self.master.destroy)
		self.quit.pack(side="bottom")

	def say_hi(self):
		print("hi there, eveyone!")


