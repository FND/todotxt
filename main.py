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
		return self.active.pop(id)

	def modify(self, id, text):
		pass # TODO

	def archive(self, id):
		pass # TODO

if __name__ == "__main__":
	sys.exit(main(sys.argv))

