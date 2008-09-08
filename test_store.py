import unittest
import os
import shutil
import store

class FileStoreTestCase(unittest.TestCase):
	def setUp(self):
		self.files = ["/tmp/test/foo", "/tmp/test/bar", "/tmp/test/baz"]
		self.store = store.FileStore(*self.files)
		try:
			shutil.rmtree("/tmp/test/")
		except OSError:
			pass
		os.mkdir("/tmp/test")
		for filename in self.files:
			f = open(filename, "w")
			f.write("lorem ipsum\ndolor sit amet")
			f.close()

	def tearDown(self):
		shutil.rmtree("/tmp/test/")

	def testInitRequiresArguments(self):
		"""__init__ requires arguments for active, closed and report"""
		expected = TypeError
		self.assertRaises(expected, store.FileStore)
		self.assertRaises(expected, store.FileStore, "foo")
		self.assertRaises(expected, store.FileStore, "foo", "bar")
		store.FileStore("foo", "bar", "baz")

	def testGetReturnsFileContents(self):
		"""get returns file contents as list of lines"""
		expected = ["lorem ipsum", "dolor sit amet"]
		self.assertEqual(expected, self.store.get("active"))

	def testPutCreatesFile(self):
		"""put creates (or overrides) file"""
		self.store.put("active", ["foo bar", "baz"], False)
		contents = open(self.store.active).read()
		expected = "foo bar\nbaz"
		self.assertEqual(expected, contents)

	def testPutAppendsFile(self):
		"""put appends file contents"""
		self.store.put("active", ["foo bar", "baz"], True)
		contents = open(self.store.active).read()
		expected = "lorem ipsum\ndolor sit amet\nfoo bar\nbaz"
		self.assertEqual(expected, contents)

if __name__ == "__main__":
	unittest.main()

