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

class containsAllTestCase(unittest.TestCase):
	def setUp(self):
		pass

	def tearDown(self):
		pass

	def testMainReturnsTrueOnMatch(self):
		"""containsAll returns True if all search terms are found"""
		seq = "foo"
		terms = ["f", "o"]
		expected = True
		self.assertEquals(expected, main.containsAll(seq, terms))

	def testMainReturnsFalseOnPartialMatch(self):
		"""containsAll returns True if not all search terms are found"""
		seq = "foo"
		terms = ["f", "o", "b"]
		expected = False
		self.assertEquals(expected, main.containsAll(seq, terms))

class ItemsTestCase(unittest.TestCase):
	def setUp(self):
		self.items = main.Items()
		self.items.active = ["lorem", "ipsum", "dolor"]

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

	def testInitInitializesPriorityTemplate(self):
		"""__init__ initializes priority template"""
		expected = "(%s)"
		self.assertEquals(expected, self.items.priorityTemplate)

	def testInitInitializesPriorityValues(self):
		"""__init__ initializes priority values"""
		expected = "[A-Za-z]"
		self.assertEquals(expected, self.items.priorityValues)

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

	def testRemoveRaisesIndexErrorOnFailure(self):
		"""remove raises IndexError if specified item does not exist"""
		expected = IndexError
		self.assertRaises(expected, self.items.remove, 3)

	def testAppendAddsItemText(self):
		"""append adds text to the end of specified item"""
		self.items.append(1, " foo")
		expected = "ipsum foo"
		self.assertEquals(expected, self.items.active[1])

	def testAppendReturnsNewText(self):
		"""append returns new item text"""
		expected = "ipsum foo"
		self.assertEquals(expected, self.items.append(1, " foo"))

	def testAppendRaisesIndexErrorOnFailure(self):
		"""append raises IndexError if specified item does not exist"""
		expected = IndexError
		self.assertRaises(expected, self.items.append, 3, " foo")

	def testReplaceSubstitutesItemText(self):
		"""replace substitutes text of specified item"""
		self.items.replace(1, "foo")
		expected = "foo"
		self.assertEquals(expected, self.items.active[1])

	def testReplaceReturnsOldText(self):
		"""replace returns previous item text"""
		expected = "ipsum"
		self.assertEquals(expected, self.items.replace(1, "foo"))

	def testReplaceRaisesIndexErrorOnFailure(self):
		"""replace raises IndexError if specified item does not exist"""
		expected = IndexError
		self.assertRaises(expected, self.items.replace, 3, "foo")

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

	def testFlagRaisesIndexErrorOnFailure(self):
		"""flag raises IndexError if specified item does not exist"""
		expected = IndexError
		self.assertRaises(expected, self.items.flag, 3)

	def testPrioritizeAddsPriorityPrefix(self):
		"""prioritize adds priority as prefix"""
		expected = "(A) ipsum"
		self.assertEquals(expected, self.items.prioritize(1, "A"))

	def testPrioritizeReplacesExistingPriority(self):
		"""prioritize replaces existing priority"""
		self.items.active[1] = "ipsum (B) foo"
		expected = "(A) ipsum foo"
		self.assertEquals(expected, self.items.prioritize(1, "A"))

	def testPrioritizeSupportsRemovingPriority(self):
		"""prioritize supports removing existing priority"""
		self.items.active[1] = "(A) ipsum"
		expected = "ipsum"
		self.assertEquals(expected, self.items.prioritize(1, ""))

	def testPrioritizeUsesUppercasePriorities(self):
		"""prioritize uses uppercase for priorities"""
		expected = "(A) ipsum"
		self.assertEquals(expected, self.items.prioritize(1, "a"))

	def testPrioritizeRaisesIndexErrorOnFailure(self):
		"""prioritize raises IndexError if specified item does not exist"""
		expected = IndexError
		self.assertRaises(expected, self.items.prioritize, 3, "A")

	def testPrioritizeRaisesValueErrorOnFailure(self):
		"""prioritize raises ValueError if specified priority is invalid"""
		expected = ValueError
		self.assertRaises(expected, self.items.prioritize, 1, "foo")

	def testFilterReturnsAllItemsForEmptyFilters(self):
		"""filter returns all items if no filters have been specified"""
		expected = ["lorem", "ipsum", "dolor"]
		self.assertEquals(expected, self.items.filter())

	def testFilterSupportsActiveAndClosedItems(self):
		"""filter supports active and closed items"""
		self.items.closed = ["sit", "amet"]
		expected = ["lorem", "ipsum", "dolor", "sit", "amet"]
		self.assertEquals(expected, self.items.filter(includeClosed = True))

	def testFilterReturnsItemsMatchingAllFilters(self):
		"""filter returns items matching all filter terms"""
		expected = ["lorem", "dolor"]
		self.assertEquals(expected, self.items.filter(["l", "o"]))

if __name__ == "__main__":
	unittest.main()

