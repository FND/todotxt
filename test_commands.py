import unittest
import os
import shutil
import items
import store
import commands

class CommandsTestCase(unittest.TestCase):
	def setUp(self):
		self.items = items.Items()
		self.items.active = ["lorem ipsum", "dolor sit amet"]
		self.files = ["/tmp/test/foo", "/tmp/test/bar", "/tmp/test/baz"]
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
		f = open(self.files[0], "r")
		contents = f.read()
		f.close()
		expected = "lorem ipsum\ndolor sit amet\nfoo\n"
		self.assertEqual(expected, contents)

if __name__ == "__main__":
	unittest.main()

