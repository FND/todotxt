class FileStore: # XXX: should be subclass of generic Store; cf. commands.__init__
	def __init__(self, active, closed, report):
		"""
		@param active (str): filepath for active items
		@param closed (str): filepath for closed items
		@param report (str): filepath for report
		@return: None
		"""
		self.active = active
		self.closed = closed
		self.report = report

	def get(self, entity):
		"""
		retrieve data from file

		@param entity (str): storage entity (active, closed, report)
		@return: None
		@raise IOError: cannot read file
		"""
		filepath = getattr(self, entity)
		return [i.rstrip() for i in open(filepath, "r")]

	def put(self, entity, items, append):
		"""
		write data to file

		@param entity (str): storage entity (active, closed, report)
		@param items (list): items
		@param append (bool): use append rather than overwriting existing data
		@return: None
		@raise IOError: cannot write to file
		"""
		filepath = getattr(self, entity)
		if append:
			f = open(filepath, "a")
			f.write("%s\n" % "\n".join(items))
		else:
			f = open(filepath, "w")
			f.write("%s\n" % "\n".join(items))
		f.close()

