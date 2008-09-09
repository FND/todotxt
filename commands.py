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
		add active item

		@param text (str): new item text
		@return: None
		"""
		self.items.add(text)
		self.store.put("active", [text], append = True)
		# TODO: display item ID

	def remove(self, id):
		"""
		remove active item

		@param id (str): item ID
		@return: None
		@raise ValueError: invalid item ID
		"""
		self.items.remove(int(id))
		self.store.put("active", self.items.active)

	def append(self, id, text):
		"""
		append active item

		@param id (str): item ID
		@param text (str): new item text
		@return: None
		@raise ValueError: invalid item ID
		"""
		self.items.append(int(id), text)
		self.store.put("active", self.items.active)

	def replace(self, id, text):
		"""
		replace active item

		@param id (str): item ID
		@param text (str): new item text
		@return: None
		@raise ValueError: invalid item ID
		"""
		self.items.replace(int(id), text)
		self.store.put("active", self.items.active)

	def flag(self, id):
		"""
		flag active item

		@param id (str): item ID
		@return: None
		@raise ValueError: invalid item ID
		"""
		self.items.flag(int(id), useUTC = True) # TODO: UTC setting to be read from config
		self.store.put("active", self.items.active)

	def prioritize(self, id, priority):
		"""
		set priority of active item

		@param id (str): item ID
		@return: None
		@raise ValueError: invalid item ID
		"""
		self.items.prioritize(int(id), priority)
		self.store.put("active", self.items.active)

	def list(self, filters = None):
		"""
		display items

		@param filters (str): space-separated list of filter terms
		@return: None
		"""
		items = self.items.filter(self, filters)
		# TODO: colorize
		print "\n".join(items)

	def listAll(self, filters = None):
		"""
		display items

		@param filters (str): space-separated list of filter terms
		@return: None
		"""
		items = self.items.filter(self, filters, includeClosed = True)
		# TODO: colorize
		print "\n".join(items)

	def listPriorities(self, filters = None):
		"""
		display prioritized items

		@param filters (str): space-separated list of filter terms
		@return: None
		"""
		items = self.items.filter(self, filters, prioritiesOnly = True)
		# TODO: colorize
		print "\n".join(items)

	def removeDuplicates(self):
		"""
		remove duplicate items

		@return: None
		"""
		self.items.removeDuplicates()

	def archive(self):
		"""
		archive flagged items

		@return: None
		"""
		self.items.removeDuplicates()

	def generateReport(self):
		print "active: %s" % len(self.items.active)
		print "closed: %s" % len(self.items.closed)

	def help(self):
		pass # TODO

