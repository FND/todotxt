import unittest
import build

class retrieveTestCase(unittest.TestCase):
	def setUp(self):
		self.modules = ["foo", "bar"]
		# mock file access
		self.open = open
		def mockOpen(name, mode = "r"):
			key = name[:-3]
			return dummyModules()[key].split("\n")
		build.open = mockOpen

	def tearDown(self):
		build.open = self.open

	def testReturnsTuple(self):
		"""retrieve returns tuple consisting of imports, startup and contents"""
		expected = 3
		self.assertEqual(expected, len(build.retrieve(self.modules)))

	def testReturnsImports(self):
		"""retrieve returns import statements"""
		expected = ["import foo", "import bar", "import baz"]
		self.assertEqual(expected, build.retrieve(self.modules)[0])

	def testReturnsStartup(self):
		"""retrieve returns startup statements"""
		expected = [
			'if __name__ == "__main__":',
			"\tsys.exit(main(sys.argv))",
			"\tpass",
			""
		]
		self.assertEqual(expected, build.retrieve(self.modules)[1])

	def testReturnsCallables(self):
		"""retrieve returns callables (excluding import and startup statements)"""
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

