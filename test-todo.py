#!/usr/bin/env python

import unittest
import todo

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

