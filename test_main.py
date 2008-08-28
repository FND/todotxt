import unittest
import time
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
		self.items.active = ["lorem", "ipsum", "dolor"]
		pass

	def tearDown(self):
		pass

	def testInitInitializesActiveItems(self):
		"""__init__ initializes active items"""
		expected = ["lorem", "ipsum", "dolor"] # populated due to setUp
		self.assertEquals(expected, self.items.active)

	def testInitInitializesClosedItems(self):
		"""__init__ initializes closed items"""
		expected = []
		self.assertEquals(expected, self.items.closed)

	def testInitInitializesFlagChar(self):
		"""__init__ initializes flag character"""
		expected = "x"
		self.assertEquals(expected, self.items.flagChar)

	def testAddAppendsItem(self):
		"""add creates new active item"""
		self.items.add("foo")
		expected = ["lorem", "ipsum", "dolor", "foo"]
		self.assertEquals(expected, self.items.active)

	def testAddReturnsID(self):
		"""add returns new item ID"""
		expected = 3
		self.assertEquals(expected, self.items.add("foo"))

	def testRemoveDeletesItem(self):
		"""remove deletes specified active item"""
		self.items.remove(1)
		expected = ["lorem", "dolor"]
		self.assertEquals(expected, self.items.active)

	def testRemoveReturnsOldText(self):
		"""remove returns deleted item's text"""
		expected = "ipsum"
		self.assertEquals(expected, self.items.remove(1))

	def testRemoveReturnsFalseOnFailure(self):
		"""remove returns False if specified item does not exist"""
		expected = False
		self.assertEquals(expected, self.items.remove(3))

	def testAppendAddsItemText(self):
		"""append adds text to the end of specified item"""
		self.items.append(1, " foo")
		expected = "ipsum foo"
		self.assertEquals(expected, self.items.active[1])

	def testAppendReturnsNewText(self):
		"""append returns new item text"""
		expected = "ipsum foo"
		self.assertEquals(expected, self.items.append(1, " foo"))

	def testAppendReturnsFalseOnFailure(self):
		"""append returns False if specified item does not exist"""
		expected = False
		self.assertEquals(expected, self.items.append(3, " foo"))

	def testReplaceSubstitutesItemText(self):
		"""replace substitutes text of specified item"""
		self.items.replace(1, "foo")
		expected = "foo"
		self.assertEquals(expected, self.items.active[1])

	def testReplaceReturnsOldText(self):
		"""replace returns previous item text"""
		expected = "ipsum"
		self.assertEquals(expected, self.items.replace(1, "foo"))

	def testReplaceReturnsFalseOnFailure(self):
		"""replace returns False if specified item does not exist"""
		expected = False
		self.assertEquals(expected, self.items.replace(3, "foo"))

	def testFlagAddsFlagChar(self):
		"""flag adds flag character as first prefix"""
		self.items.flag(1)
		expected = "x "
		self.assertEquals(expected, self.items.active[1][0:2])

	def testFlagAddsTimestamp(self):
		"""flag adds timestamp as second prefix"""
		self.items.flag(1)
		expected = time.strftime("%Y-%m-%d", time.gmtime())
		self.assertEquals(expected, self.items.active[1][2:12])

	def testFlagTimestampUsesISO8603Date(self):
		"""flag timestamp uses ISO-8601 date format"""
		self.items.flag(1, False)
		expected = time.strftime("%Y-%m-%d", time.localtime())
		self.assertEquals(expected, self.items.active[1][2:12])

	def testFlagUsesUTCByDefault(self):
		"""flag timestamp uses UTC by default"""
		self.items.flag(1)
		expected = time.strftime("%Y-%m-%d", time.gmtime())
		self.assertEquals(expected, self.items.active[1][2:12])

	def testFlagSupportsLocalTime(self):
		"""flag timestamp supports local time"""
		self.items.flag(1, False)
		expected = time.strftime("%Y-%m-%d", time.localtime())
		self.assertEquals(expected, self.items.active[1][2:12])

if __name__ == "__main__":
	unittest.main()

