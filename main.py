#!/usr/bin/env python

"""
TODO.TXT Manager

Author: FND (http://fnd.lewcid.org/blog/)
License: GPL (http://www.gnu.org/copyleft/gpl.html)
Version: 2.0.0 alpha

Based on concept by Gina Trapani (http://todotxt.com).
Original Python port by Shane Koster.
"""

import sys
import time
import re
import util

def main(args = []):
	return # TODO

class Items: # TODO: move to dedicated module
	def __init__(self):
		self.active = []
		self.closed = []
		self.flagChar = "x"
		self.priorityTemplate = "(%s)"
		self.priorityValues = "[A-Za-z]"
		self.priorityPattern = re.compile(r"\s?%s|%s\s?".replace("%s", "\([A-Za-z]\)"))

	def get(self, source): # XXX: does not belong here?
		pass # TODO

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

	def display(self, items, colored = True):
		"""
		display items

		@param items (list): items
		@param colored (bool): colored output
		@return: None
		"""
		pass # TODO

	def archive(self, id):
		pass # TODO

if __name__ == "__main__":
	sys.exit(main(sys.argv))

