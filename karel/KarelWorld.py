class KarelWorld():
	def __init__(self, world_file):
		"""
		Karel World constructor
		Parameters:
			world_file: Open file object containing information about the initial state of Karel's world
		
		"""
		self.world_file = world_file
		self.load_from_file()
	
	def load_from_file(self):
		for line in self.world_file:
			print(line)
