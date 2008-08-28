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

def main(args = []):
	return # TODO

class Items:
	def __init__(self):
		self.active = []
		self.closed = []

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
		"""
		try:
			return self.active.pop(id)
		except IndexError:
			return False

	def append(self, id, text):
		"""
		add text to active item

		@param id: item ID
		@type  id: int
		@param text: additional item text
		@type  text: str
		@return: new item text (False on failure)
		@rtype : str or bool
		"""
		try:
			self.active[id] += text
			return self.active[id]
		except IndexError:
			return False

	def replace(self, id, text):
		"""
		replace active item

		@param id: item ID
		@type  id: int
		@param text: new item text
		@type  text: str
		@param append: append instead of replacing item text
		@type  append: bool
		@return: old item text (False on failure)
		@rtype : str or bool
		"""
		try:
			old = self.active[id]
			self.active[id] = text
			return old # XXX: logically insane?
		except IndexError:
			return False

	def archive(self, id):
		pass # TODO

if __name__ == "__main__":
	sys.exit(main(sys.argv))

