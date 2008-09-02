import time
import re
import util

class Items:
	def __init__(self):
		self.active = []
		self.closed = []
		self.flagChar = "x"
		self.priorityTemplate = "(%s)"
		self.priorityValues = "[A-Za-z]"
		self.priorityPattern = re.compile(r"\s?%s|%s\s?".replace("%s", "\([A-Za-z]\)"))

	def add(self, text):
		"""
		add new active item

		@param text (str): item text
		@return (int): item index
		"""
		self.active.append(text)
		return len(self.active) - 1

	def remove(self, id):
		"""
		remove active item

		@param id (int): item ID
		@return (str): item text
		@raise IndexError: item does not exist
		"""
		return self.active.pop(id)

	def append(self, id, text):
		"""
		add text to active item

		@param id (int): item ID
		@param text (str): additional item text
		@return (str): new item text
		@raise IndexError: item does not exist
		"""
		self.active[id] += text
		return self.active[id]

	def replace(self, id, text):
		"""
		replace active item

		@param id (int): item ID
		@param text (str): new item text
		@return (str): old item text
		@raise IndexError: item does not exist
		"""
		old = self.active[id]
		self.active[id] = text
		return old

	def flag(self, id, useUTC = True):
		"""
		flag active item and add timestamp

		@param id (int): item ID
		@param useUTC (bool): use UTC for timestamp
		@return (str): new item text
		@raise IndexError: item does not exist
		"""
		timeFormat = "%Y-%m-%d" # TODO: customizable?
		if useUTC:
			date = time.strftime(timeFormat, time.gmtime())
		else:
			date = time.strftime(timeFormat, time.localtime())
		self.active[id] = "%s %s %s" % (self.flagChar, date, self.active[id])
		return self.active[id]

	def prioritize(self, id, priority): # XXX: rewrite to be more elegant; disallow non-leading priorities?
		"""
		set priority of active item

		@param id (int): item ID
		@param priority (str): Latin letter (A-Z) or empty string
		@return (str): new item text
		@raise IndexError: item does not exist
		@raise ValueError: invalid priority
		"""
		isPriority = re.compile(r"^%s$" % self.priorityValues).search(priority)
		if not (isPriority or priority == ""):
			raise ValueError("invalid priority")
		if isPriority:
			priorityStr = self.priorityTemplate % priority.upper()
		else:
			priorityStr = ""
		self.active[id] = self.priorityPattern.sub("", self.active[id])
		self.active[id] = "%s %s" % (priorityStr, self.active[id])
		if priority == "": # XXX: hacky?
			self.active[id] = self.active[id].lstrip()
		return self.active[id]

	def filter(self, filters = [], prioritiesOnly = False, includeClosed = False):
		"""
		filter items

		@param filters (list): filter terms
		@param prioritiesOnly (bool): filter by priorities only
		@param includeClosed (bool): include closed items
		@return (list): matching items
		"""
		items = self.active[:]
		if includeClosed:
			items.extend(self.closed)
		if prioritiesOnly:
			if filters:
				filters = [self.priorityTemplate % f.upper() for f in filters]
				return [i for i in items if util.containsAny(i, filters)]
			else:
				return [i for i in items if self.priorityPattern.search(i)]
		else:
			return [i for i in items if util.containsAll(i, filters)]

	def display(self, items, colored = True): # XXX: does not belong here?
		"""
		display items

		@param items (list): items
		@param colored (bool): colored output
		@return: None
		"""
		pass # TODO

	def removeDuplicates(self):
		"""
		remove duplicate items

		@return: None
		"""
		for item in self.active:
			if self.active.count(item) > 1:
				self.active.remove(item)

	def archive(self):
		"""
		move flagged items from active to closed

		@param id (int): item ID
		@return: None
		@raise IndexError: item does not exist
		"""
		for i, item in enumerate(self.active):
			if item.startswith("%s " % self.flagChar):
				item = self.active.pop(i)
				self.closed.append(item)

