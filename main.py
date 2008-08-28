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

def main(args = []):
	return # TODO

class Items:
	def __init__(self):
		self.active = []
		self.closed = []
		self.flagChar = "x"

	def get(self, source): # XXX: does not belong here?
		pass # TODO

	def add(self, text):
		"""
		add new active item

		@param text: item text
		@type  text: str
		@return: item index
		@rtype : int
		"""
		self.active.append(text)
		return len(self.active) - 1

	def remove(self, id):
		"""
		remove active item

		@param id: item ID
		@type  id: int
		@return: item text
		@rtype : str
		@raise IndexError: item does not exist
		"""
		return self.active.pop(id)

	def append(self, id, text):
		"""
		add text to active item

		@param id: item ID
		@type  id: int
		@param text: additional item text
		@type  text: str
		@return: new item text
		@rtype : str
		@raise IndexError: item does not exist
		"""
		self.active[id] += text
		return self.active[id]

	def replace(self, id, text):
		"""
		replace active item

		@param id: item ID
		@type  id: int
		@param text: new item text
		@type  text: str
		@return: old item text
		@rtype : str
		@raise IndexError: item does not exist
		"""
		old = self.active[id]
		self.active[id] = text
		return old

	def flag(self, id, useUTC = True):
		"""
		flag active item and add timestamp

		@param id: item ID
		@type  id: int
		@param useUTC: use UTC for timestamp
		@type  useUTC: bool
		@return: new item text
		@rtype : str
		@raise IndexError: item does not exist
		"""
		timeFormat = "%Y-%m-%d" # TODO: customizable?
		if useUTC:
			date = time.strftime(timeFormat, time.gmtime())
		else:
			date = time.strftime(timeFormat, time.localtime())
		self.active[id] = "%s %s %s" % (self.flagChar, date, self.active[id])
		return self.active[id]

	def archive(self, id):
		pass # TODO

if __name__ == "__main__":
	sys.exit(main(sys.argv))

