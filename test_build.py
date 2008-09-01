import unittest
import build

class retrieveTestCase(unittest.TestCase):
	def setUp(self):
		self.modules = ["foo", "bar"]
		# mock file access
		self.open = open
		def mockOpen(name):
			key = name[:-3]
			return dummyModules()[key].split("\n")
		build.open = mockOpen

	def tearDown(self):
		build.open = self.open

	def testReturnsTuple(self): # TODO
		"""retrieve returns tuple consisting of imports, startup and contents"""
		expected = 3
		self.assertEqual(expected, len(build.retrieve(self.modules)))

	def testReturnsImports(self): # TODO
		"""retrieve returns import statements"""
		expected = ["import foo", "import bar", "import baz"]
		self.assertEqual(expected, build.retrieve(self.modules)[0])

	def testReturnsStartup(self): # TODO
		"""retrieve returns startup statements"""
		expected = [
			'if __name__ == "__main__":',
			"\tsys.exit(main(sys.argv))",
			"\tpass",
			""
		]
		self.assertEqual(expected, build.retrieve(self.modules)[1])

	def testReturnsContents(self): # TODO
		"""retrieve returns module contents (excluding import and startup statements)"""
		expected = [
			"# foo",
			"",
			"",
			"def qux():",
			"\tpass",
			"",
			"# bar",
			"",
			"",
			"def quux():",
			"\tpass",
			""
		]
		self.assertEqual(expected, build.retrieve(self.modules)[2])

def dummyModules():
	modules = {
		"foo": """
import foo
import bar
import baz

def qux():
	pass

if __name__ == "__main__":
	sys.exit(main(sys.argv))
	pass
""",
		"bar": """
import bar

def quux():
	pass
"""
	}
	return modules

if __name__ == "__main__":
	unittest.main()

