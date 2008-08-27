import unittest
import main

class mainTestCase(unittest.TestCase):
	def setUp(self):
		pass

	def tearDown(self):
		pass

	def testMainReturnsNoneOnSuccess(self):
		"""main returns None on success"""
		expected = None
		self.assertEquals(expected, main.main())

class ItemsTestCase(unittest.TestCase):
	def setUp(self):
		self.items = main.Items()
		pass

	def tearDown(self):
		pass

	def testInitCreatesActiveItems(self):
		"""__init__ creates active items"""
		expected = []
		self.assertEquals(expected, self.items.active)

	def testInitCreatesClosedItems(self):
		"""__init__ creates closed items"""
		expected = []
		self.assertEquals(expected, self.items.closed)

	def testAddAppendsItem(self):
		"""add creates new active item"""
		self.items.add("foo")
		expected = ["foo"]
		self.assertEquals(expected, self.items.active)

	def testAddReturnsID(self):
		"""add returns new item ID"""
		expected = 0
		self.assertEquals(expected, self.items.add("foo"))

	def testRemoveRemovesItem(self):
		"""remove deletes specified active item"""
		self.items.active = ["foo", "bar", "baz"]
		self.items.remove(1)
		expected = ["foo", "baz"]
		self.assertEquals(expected, self.items.active)

	def testRemoveReturnsText(self):
		"""remove returns deleted item's text"""
		self.items.active = ["foo", "bar", "baz"]
		expected = "bar"
		self.assertEquals(expected, self.items.remove(1))

if __name__ == "__main__":
	unittest.main()

