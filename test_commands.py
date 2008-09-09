import unittest
import os
import shutil
import time
import items
import store
import commands

class CommandsTestCase(unittest.TestCase):
	def setUp(self):
		self.items = items.Items()
		self.items.active = ["lorem ipsum", "dolor sit amet"]
		self.files = ["/tmp/test/foo", "/tmp/test/bar"]
		self.store = store.FileStore(*self.files)
		self.cmd = commands.Commands(self.items, self.store)
		try:
			shutil.rmtree("/tmp/test/")
		except OSError:
			pass
		os.mkdir("/tmp/test")
		for filename in self.files:
			f = open(filename, "w")
			f.write("%s\n" % "\n".join(self.items.active))
			f.close()

	def tearDown(self):
		shutil.rmtree("/tmp/test/")

	def testAddAppendsNewItem(self):
		"""add appends new item"""
		self.cmd.add("foo")
		expected = ["lorem ipsum", "dolor sit amet", "foo"]
		self.assertEqual(expected, self.items.active)

	def testAddStoresNewItem(self):
		"""add stores new item"""
		self.cmd.add("foo")
		expected = "lorem ipsum\ndolor sit amet\nfoo\n"
		self.assertEqual(expected, getFileContents(self.files[0]))

	def testRemoveDeletesItem(self):
		"""remove deletes existing item"""
		self.cmd.remove("0")
		expected = "dolor sit amet\n"
		self.assertEqual(expected, getFileContents(self.files[0]))

	def testAppendAddsText(self):
		"""append adds text to existing item"""
		self.cmd.append("0", " foo")
		expected = "lorem ipsum foo"
		self.assertEqual(expected, self.items.active[0])

	def testReplaceSubstitutesText(self):
		"""replace substitutes existing item"""
		self.cmd.replace("0", "foo")
		expected = "foo"
		self.assertEqual(expected, self.items.active[0])

	def testFlagPrependsFlagString(self):
		"""flag prepends flag and timestamp to existing item"""
		self.cmd.flag("0")
		expected = "x %s lorem ipsum" % time.strftime("%Y-%m-%d", time.gmtime())
		self.assertEqual(expected, self.items.active[0])

	def testFlagUsesPreferredTimezone(self): # XXX: largely irrelevant because flag only uses date!?
		"""flag uses preferred timezoned (as per configuration) for timestamp"""
		self.cmd.flag("0")
		if time.localtime() == time.gmtime():
			raise RuntimeWarning("test ambiguous (local time == UTC)")
		expected = "x %s lorem ipsum" % time.strftime("%Y-%m-%d", time.localtime())
		self.assertEqual(expected, self.items.active[0])

	def testPrioritizeAddsPriority(self):
		"""prioritize adds priority as prefix"""
		self.cmd.prioritize("0", "a")
		expected = "(A) lorem ipsum"
		self.assertEqual(expected, self.items.active[0])

def getFileContents(filepath):
	f = open(filepath, "r")
	contents = f.read()
	f.close()
	return contents

if __name__ == "__main__":
	unittest.main()

