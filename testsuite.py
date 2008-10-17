"""
Python test suite

using unittest and coverage

TODO:
* make coverage optional
* read modules from directory listing
"""

import sys
import unittest
import coverage

def run(modules):
	"""
	run test suite on given modules

	test modules must be named after their respective parent modules,
	using the prefix "test_" (e.g. "foo" :: "test_foo")

	@param modules (list): module names
	@return (bool): success
	"""
	testModules = ["test_" + module for module in modules] # TODO
	initCoverage()
	suite = unittest.TestLoader().loadTestsFromNames(testModules)
	runner = unittest.TextTestRunner(sys.stdout, verbosity = 2)
	results = runner.run(suite)
	endCoverage()
	reportCoverage(modules)
	return results.wasSuccessful()

def initCoverage():
	coverage.erase()
	coverage.use_cache(0)
	coverage.start()

def endCoverage():
	coverage.stop()

def reportCoverage(modules):
	"""
	report test coverage for given modules

	@param modules (list): module names
	"""
	modules = [__import__(module) for module in modules]
	coverage.report(modules, ignore_errors = 0, show_missing = 1)

if __name__ == "__main__":
	status = run(sys.argv[1:])
	sys.exit(not status)
