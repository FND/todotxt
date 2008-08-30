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

def main(args = []):
	return # TODO

def containsAll(seq, terms): # TODO: move to utils module
	"""
	check whether a sequence contains all of the given terms

	@param seq (str, list, tuple): sequence to investigate
	@param terms (list, tuple): terms to match
	@return (bool): match
	"""
	for t in terms:
		if t not in seq:
			return False
	return True

class Items: # TODO: move to dedicated module
	def __init__(self):
		self.active = []
		self.closed = []
		self.flagChar = "x"
		self.priorityTemplate = "(%s)"
		self.priorityValues = "[A-Za-z]"

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
		validPattern = re.compile(r"^%s$" % self.priorityValues)
		isPriority = True if re.match(validPattern, priority) else False
		if isPriority or priority == "":
			if isPriority:
				priorityStr = self.priorityTemplate % priority.upper()
			else:
				priorityStr = ""
			priorityPattern = self.priorityTemplate.replace(r")", r"\)").replace(r"(", r"\(") % self.priorityValues
			priorityPattern = re.compile(r"\s?%s|%s\s?" % (priorityPattern, priorityPattern))
			self.active[id] = re.sub(priorityPattern, "", self.active[id])
			self.active[id] = "%s %s" % (priorityStr, self.active[id])
			if priority == "": # XXX: hacky?
				self.active[id] = self.active[id].lstrip()
			return self.active[id]
		else:
			raise ValueError("invalid priority")

	def filter(self, filters = [], includeClosed = False):
		"""
		filter items

		@param filters (list): filter terms
		@param includeClosed (bool): include closed items
		@return (list): matching items
		"""
		items = self.active[:]
		if includeClosed:
			items.extend(self.closed)
		return [i for i in items if containsAll(i, filters)]

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

