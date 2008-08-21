# To Do:
# * explore doctest:
#	http://docs.python.org/lib/module-doctest.html
#	http://docs.python.org/lib/doctest-simple-testfile.html

import unittest
import todo

class DispatchTestCase(unittest.TestCase):
	def setUp(self):
		self.CommandsBackup = todo.Commands
		def dummyWithParams(self, params):
			pass
		def dummyWithoutParams(self):
			pass
		global itm
		itm = todo.Items("/tmp/foo", "/tmp/bar", "/tmp/baz")
		todo.Commands.add = dummyWithParams
		todo.Commands.prioritize = dummyWithParams
		todo.Commands.append = dummyWithParams
		todo.Commands.replace = dummyWithParams
		todo.Commands.remove = dummyWithParams
		todo.Commands.flag = dummyWithParams
		todo.Commands.removeDuplicates = dummyWithoutParams
		todo.Commands.list = dummyWithParams # XXX: params optional
		todo.Commands.listPriorities = dummyWithParams # XXX: params optional
		todo.Items.archive = dummyWithoutParams
		todo.Items.generateReport = dummyWithoutParams
		todo.usage = dummyWithoutParams
	def tearDown(self):
		todo.Commands = self.CommandsBackup
	def testDispatchAdd(self):
		todo.dispatch("add", ["foo", "bar"])

class TodoTestCase(unittest.TestCase):
	def testInfo(self):
		self.assertEquals("1 = 1 <type 'int'>", todo.info(1))
		self.assertEquals("a = 'a' <type 'str'>", todo.info("a"))
	def testAlphaSort(self):
		self.assertEquals(-1, todo.alphaSort("abcdefg", "abcdefh"))
		self.assertEquals(1, todo.alphaSort("abcdefh", "abcdefg"))
		self.assertEquals(0, todo.alphaSort("abcdefg", "abcdefg"))
		self.assertEquals(0, todo.alphaSort("aaaaa", "zzzzz"))
	def testHighlightPriorities(self):
		item = "testtodo"
		for priority in ("A", "B", "C", "X"):
			self.assertEquals(todo.priorityColors[priority] + "(%s)" % priority + " " + item + todo.colors["default"], todo.priorityRE.sub(todo.highlightPriorities, "(%s) %s" % (priority, item)))

class DisableColorTestCase(unittest.TestCase):
	def setUp(self):
		self.priorityColorsBackup = todo.priorityColors
	def tearDown(self):
		todo.priorityColors = self.priorityColorsBackup
	def testDisableColor(self):
		todo.disableColors()
		for color in todo.priorityColors.values():
			self.assertEquals("", color)

if __name__ == '__main__':
	unittest.main()

