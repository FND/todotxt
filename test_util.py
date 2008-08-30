import unittest
import util

class containsAnyTestCase(unittest.TestCase):
	def setUp(self):
		pass

	def tearDown(self):
		pass

	def testReturnsTrueOnPartialMatch(self):
		"""containsAny returns True if a search term is found"""
		seq = "foo"
		terms = ["f", "b", "a"]
		expected = True
		self.assertEqual(expected, util.containsAny(seq, terms))

	def testReturnsFalseOnNoMatch(self):
		"""containsAny returns False if no search term is found"""
		seq = "foo"
		terms = ["b", "a", "r"]
		expected = False
		self.assertEqual(expected, util.containsAny(seq, terms))

class containsAllTestCase(unittest.TestCase):
	def setUp(self):
		pass

	def tearDown(self):
		pass

	def testReturnsTrueOnMatch(self):
		"""containsAll returns True if all search terms are found"""
		seq = "foo"
		terms = ["f", "o"]
		expected = True
		self.assertEqual(expected, util.containsAll(seq, terms))

	def testReturnsFalseOnPartialMatch(self):
		"""containsAll returns False if not all search terms are found"""
		seq = "foo"
		terms = ["f", "o", "b"]
		expected = False
		self.assertEqual(expected, util.containsAll(seq, terms))

if __name__ == "__main__":
	unittest.main()

