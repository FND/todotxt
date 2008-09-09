class Commands:
	def __init__(self, items, store):
		"""
		@param items (Items): item collection
		@param store (FileStore): storage instance
		"""
		self.items = items
		self.store = store

	def add(self, text):
		"""
		add item

		@param text (str): new item text
		"""
		self.items.add(text)
		self.store.put("active", [text], append = True)
		# TODO: display item ID

	def remove(self):
		pass # TODO

	def append(self):
		pass # TODO

	def replace(self):
		pass # TODO

	def flag(self):
		pass # TODO

	def prioritize(self):
		pass # TODO

	def list(self):
		pass # TODO

	def listPriorities(self):
		pass # TODO

	def removeDuplicates(self):
		pass # TODO

	def archive(self):
		pass # TODO

	def generateReport(self):
		pass # TODO

	def help(self):
		pass # TODO

