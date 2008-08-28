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

	def testRemoveDeletesItem(self):
		"""remove deletes specified active item"""
		self.items.active = ["foo", "bar", "baz"]
		self.items.remove(1)
		expected = ["foo", "baz"]
		self.assertEquals(expected, self.items.active)

	def testRemoveReturnsOldText(self):
		"""remove returns deleted item's text"""
		self.items.active = ["foo", "bar", "baz"]
		expected = "bar"
		self.assertEquals(expected, self.items.remove(1))

	def testRemoveReturnsFalseOnFailure(self):
		"""remove returns False if specified item does not exist"""
		self.items.active = ["foo", "bar", "baz"]
		expected = False
		self.assertEquals(expected, self.items.remove(3))

	def testAppendAddsItemText(self):
		"""append adds text to the end of specified item"""
		self.items.active = ["foo", "bar", "baz"]
		self.items.append(1, " foo")
		expected = "bar foo"
		self.assertEquals(expected, self.items.active[1])

	def testAppendReturnsNewText(self):
		"""append returns new item text"""
		self.items.active = ["foo", "bar", "baz"]
		expected = "bar foo"
		self.assertEquals(expected, self.items.append(1, " foo"))

	def testAppendReturnsFalseOnFailure(self):
		"""append returns False if specified item does not exist"""
		self.items.active = ["foo", "bar", "baz"]
		expected = False
		self.assertEquals(expected, self.items.append(3, " foo"))

	def testReplaceSubstitutesItemText(self):
		"""replace substitutes text of specified item"""
		self.items.active = ["foo", "bar", "baz"]
		self.items.replace(1, "foo")
		expected = "foo"
		self.assertEquals(expected, self.items.active[1])

	def testReplaceReturnsOldText(self):
		"""replace returns previous item text"""
		self.items.active = ["foo", "bar", "baz"]
		expected = "bar"
		self.assertEquals(expected, self.items.replace(1, "foo"))

	def testReplaceReturnsFalseOnFailure(self):
		"""replace returns False if specified item does not exist"""
		self.items.active = ["foo", "bar", "baz"]
		expected = False
		self.assertEquals(expected, self.items.replace(3, "foo"))

if __name__ == "__main__":
	unittest.main()

