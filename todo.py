#!/usr/bin/env python

"""
TODO.TXT Manager
Author: FND (http://fnd.lewcid.org/blog/)
License: GPL, http://www.gnu.org/copyleft/gpl.html
Version: 2.0.0 alpha

Based on concept by Gina Trapani (http://todotxt.com) and original Python port by Shane Koster.
"""

# To Do -- DEBUG: temporary
# * read settings from file
# * implement date threshold for tasks (items appearing in list only after a certain date)
# * error handling for file I/O
# * switch for custom config file
# * Epydoc: default values for optional function arguments
# * i18n: move strings to separate object
# * use YAML?
# * documentation (switches/options, commands)

import sys
import os
import time
import re
from ConfigParser import SafeConfigParser

# initialization

cfg = None
itm = None

def main(args):
	global cfg
	global itm
	if len(args) < 2:
		usage()
		return
	else:
		cfg = config()
		# process command-line options
		for i in range(2):
			if args[1] == "-p":
				cfg.colorsDisabled = True
				args.pop(1)
			if args[1] == "-c":
				cfgDir = args.pop(2)
				args.pop(1)
		# process configuration
		cfg.read(cfgDir)
		if cfg.colorsDisabled == True:
			purgeDict(cfg.colors)
			purgeDict(cfg.highlightColors)
		itm = items(cfg.file_active, cfg.file_archive, cfg.file_report)
		# process commands
		cmd = args[1]
		params = args[2:]
		dispatch(cmd, params)

def dispatch(command, params):
	"""
	parse commands

	@param command: command
	@type  command: str
	@param params: parameters
	@type  params: list
	"""
	cmd = commands()
	cmds = { # N.B.: lambdas required due to varying number of function arguments
		"add": lambda: cmd.add(params),
		"pri": lambda: cmd.prioritize(params),
		"append": lambda: cmd.append(params),
		"replace": lambda: cmd.replace(params),
		"rm": lambda: cmd.remove(params),
		"flag": lambda: cmd.flag(params),
		"rmdup": lambda: cmd.removeDuplicates(),
		"list": lambda: cmd.list(params),
		"listpri": lambda: cmd.listPriorities(params),
		"archive": lambda: archive(),
		"report": lambda: report(),
		"help": lambda: usage()
	} # DEBUG: can be reused for documentation!?
	# aliases
	cmds["a"] = cmds["add"]
	cmds["p"] = cmds["pri"]
	cmds["ls"] = cmds["list"]
	cmds["lsp"] = cmds["listpri"]
	# execute
	if command in cmds:
		cmds[command]()
	else:
		usage()

# utility functions

def highlightPriorityItems(match):
	"""
	highlight priority items

	@param obj: [DEBUG: unclear]
	@type  obj: [DEBUG: unclear]
	@return: [DEBUG: unclear]
	@rtype : [DEBUG: unclear]
	"""
	global cfg
	if match.group(1) == "(A)":
		return cfg.highlightColors["A"] + match.group(0) + cfg.colors["default"]
	elif match.group(1) == "(B)":
		return cfg.highlightColors["B"] + match.group(0) + cfg.colors["default"]
	elif match.group(1) == "(C)":
		return cfg.highlightColors["C"] + match.group(0) + cfg.colors["default"]
	else:
		return cfg.highlightColors["all"] + match.group(0) + cfg.colors["default"]

def alphaSort(a, b):
	"""
	sort items alphabetically

	@param a: first item
	@type  a: str
	@param b: second item
	@type  b: str
	@return: [DEBUG: unclear]
	@rtype : int
	"""
	if (a[5:] > b[5:]): # DEBUG: why 5?
		return 1
	elif (a[5:] < b[5:]):
		return -1
	else:
		return 0

def purgeDict(dic, value = ""):
	"""
	equalize all values in a dictionary

	@param dic: dictionary
	@type  dic: dict
	@param value: value
	@type  value: [optional] mixed
	@return: None
	"""
	for key in dic:
		dic[key] = value

def info(var): # DEBUG: for debugging only
	"""
	display variable information

	@param var: variable
	@type  var: mixed
	@return: variable information
	@rtype : str
	"""
	return '%s = %r %s' % (var, var, type(var))

# instructions (help)

def usage():
	"""
	display usage instructions

	@return None
	"""
	text = "  Usage: " + sys.argv[0] + """ [options] [task]

  Actions:
    add "<task> +<project> @<context>"
      Add task (project and context notation optional)

    append <ID> "text"
      Adds TEXT TO APPEND to the end of the todo on line NUMBER.
      Quotes optional.

    archive
      Moves done items from todo.txt to done.txt.

    rm NUMBER
      Deletes the item on line NUMBER in todo.txt.

    do NUMBER
      Marks item on line NUMBER as done in todo.txt.

    ls [TERM] [[TERM]...]
      Displays all todo's that contain TERM(s) sorted by priority with line
      numbers.  If no TERM specified, lists entire todo.txt.

    lspri [PRIORITY]
      Displays all items prioritized PRIORITY.
      If no PRIORITY specified, lists all prioritized items.

    pri NUMBER PRIORITY
      Adds PRIORITY to todo on line NUMBER.  If the item is already
      prioritized, replaces current priority with new PRIORITY.
      PRIORITY must be an uppercase letter between A and Z.

    replace NUMBER "UPDATED TODO"
      Replaces todo on line NUMBER with UPDATED TODO.

    remdup
      Removes exact duplicate lines from todo.txt.

    report
      Adds the number of open todo's and closed done's to report.txt.

  Options:
    -p    plain mode (no colors)

  More on the todo.txt manager at
  http://todotxt.com
  Version 1.5.2-python
  Copyleft 2006, Gina Trapani (ginatrapani@gmail.com)
  Copyleft 2006, Shane Koster (shane.koster@gmail.com)
"""
	print text

# configuration -- DEBUG: make proper use of ConfigParser defaults

# command handlers

class commands:
	def add(self, params):
		"""
		[DEBUG: to do]

		@param params: parameters to pass through
		@type  params: list
		@return None
		"""
		if params:
			addItem(" ".join(params), itm.active)
		else:
			print "Usage: " + sys.argv[0] + " add <text> [+<project>] [@<context>]" # DEBUG: duplication; cf. usage() (also see below)

	def prioritize(self, params):
		"""
		[DEBUG: to do]

		@param params: parameters to pass through
		@type  params: list
		@return None
		"""
		if len(params) == 2 and params[0].isdigit() and params[1].isalpha():
			prioritize(int(params[0]), params[1])
		elif len(params) == 1 and params[0].isdigit():
			prioritize(int(params[0]), "")
		else:
			print "Usage: " + sys.argv[0] + " pri <ID> [<priority>]"

	def append(self, params):
		"""
		[DEBUG: to do]

		@param params: parameters to pass through
		@type  params: list
		@return None
		"""
		if len(params) > 1 and params[0].isdigit():
			modifyItem("append", int(params[0]), " ".join(params[1:]))
		else:
			print "Usage: " + sys.argv[0] + " append <ID> <text>"

	def replace(self, params):
		"""
		[DEBUG: to do]

		@param params: parameters to pass through
		@type  params: list
		@return None
		"""
		if len(params) > 2 and params[0].isdigit():
			modifyItem("replace", int(params[0]), " ".join(params[1:]))
		else:
			print "Usage: " + sys.argv[0] + " replace <ID> <text>"

	def remove(self, params):
		"""
		[DEBUG: to do]

		@param params: parameters to pass through
		@type  params: list
		@return None
		"""
		if len(params) == 1 and params[0].isdigit():
			modifyItem("remove", int(params[0]))
		else:
			print "Usage: " + sys.argv[0] + " rm <ID>"

	def flag(self, params):
		"""
		[DEBUG: to do]

		@param params: parameters to pass through
		@type  params: list
		@return None
		"""
		if len(params) == 1 and params[0].isdigit():
			modifyItem("flag", int(params[0]))
		else:
			print "Usage: " + sys.argv[0] + " do <ID>"

	def list(self, params):
		"""
		[DEBUG: to do]

		@param params: parameters to pass through
		@type  params: list
		@return None
		"""
		if len(params) > 0:
			listItems(params)
		else:
			listItems()

	def listPriorities(self, params):
		"""
		[DEBUG: to do]

		@param params: parameters to pass through
		@type  params: list
		@return None
		"""
		if len(params) > 0:
			pattern = ["\([" + params[1] + "]\)"]
		else:
			pattern = ["\([A-Z]\)"]
		listItems(pattern)

# item functions

class items:
	def __init__(self, active, archive, report):
		"""
		initialize item files

		@param active: active items' filepath
		@type  active: str
		@param archive: archived items' filepath
		@type  archive: str
		@param report: report's filepath
		@type  report: str
		@return: None
		"""
		self.active = active
		self.archive = archive
		self.report = report

	def get(self, filename):
		"""
		retrieve items from file

		@param filename: full path to source file
		@type  filename: str
		@return: items with IDs
		@rtype : dict
		"""
		i = 0
		items = {}
		for line in open(filename).readlines():
			if line.strip() != "": #and not line.strip().startswith(ignorePrefix): # DEBUG'd
				i += 1
				items[i] = line.strip()
		return items

	def write(self, items, filename):
		"""
		write items to file

		@param items: items with IDs
		@type  items: dict
		@param filename: full path to target file
		@type  filename: str
		@return: None
		"""
		keys = items.keys()
		keys.sort()
		f = open(filename, "w")
		for key in keys:
			f.write(items[key] + os.linesep) # DEBUG: inefficient?
		f.close()

	def add(self, text, filename):
		"""
		add new item

		@param text: item text
		@type  text: str
		@param filename: full path to target file
		@type  filename: str
		@return: None
		"""
		f = open(self.active, "a")
		f.write(text + os.linesep)
		f.close()
		# DEBUG: return/report ID of new item

	def modify(self, action, id, text = ""): # DEBUG: split into three separate functions?
		"""
		modify existing item

		@param action: append, replace, remove, or flag
		@type  action: str
		@param id: item ID
		@type  id: int
		@param text: item text to use for appending/replacing
		@type  text: [optional] str
		@return: None
		"""
		items = getItems(self.active)
		if(itemExists(items, id, True)):
			# appending
			if action == "append": # DEBUG: proper replacement for switch()...case?
				items[id] = items[id] + text
			# replacing
			elif action == "replace":
				items[id] = text
			# removing
			elif action == "remove":
				items.pop(id)
			# flagging
			elif action == "flag": # DEBUG: rename?
				if useUTC:
					date = time.strftime("%Y-%m-%d", time.gmtime())
				else:
					date = time.strftime("%Y-%m-%d", time.localtime())
				items[id] = " ".join(["x", date, items[id]])
				print "#%d marked as done (%s)" % (id, date)
			writeItems(items)
			return True
		else:
			return False

	def prioritize(self, id, priority):
		"""
		set or remove item priority

		@param id: item ID
		@type  id: int
		@param priority: item priority (none if empty string)
		@type  priority: str
		@return: None
		"""
		items = getItems(self.active)
		if(itemExists(items, id, True)):
			priority = priority.upper()
			if priority != "" and not re.match("[A-Z]", priority):
				print "Priority not recognized: " + priority
				return False
			if priority == "":
				# remove existing priority
				items[id] = re.sub(priorityRE, "", items[id])
			elif re.match(priorityRE, items[id]):
				# change existing priority
				items[id] = re.sub(priorityRE, "(" + priority + ") ", items[id])
			else:
				# set priority
				items[id] = "(" + priority + ") " + items[id]
			writeItems(items, self.active)
			return True
		else:
			return False

	def archive(self):
		"""
		move flagged items to archive

		@return: None
		"""
		items = getItems(self.active)
		activeItems = items.copy() # DEBUG: duplication necessary?
		archivedItems = getItems(self.archive)
		# move flagged items to archive
		for k, v in items.iteritems():
			if v.startswith("x "):
				archivedItems[len(archivedItems)] = activeItems.pop(k)
		writeItems(activeItems, self.active)
		writeItems(archivedItems, self.archive)

	def list(self, patterns = None):
		"""
		display items

		@param patterns: filtering pattern(s) (RegEx)
		@type  patterns: [optional] list
		@return: None
		"""
		items = getItems(self.active)
		# apply filtering
		selection = []
		if patterns:
			for k, v in items.iteritems():
				for pattern in patterns:
					if re.search(pattern, v, re.IGNORECASE):
						selection.append("%3d: %s" % (k, v))
		else:
			for k, v in items.iteritems():
				selection.append("%3d: %s" % (k, v))
		#selection.sort() # sort by todo.txt order -- DEBUG'd
		selection.sort(alphaSort) # sort by tasks alphbetically
		# highlight priority items
		for item in selection:
			print priorityRE.sub(highlightPriorities, item) # DEBUG: ?

	def report(self): # DEBUG: integrate birdseye.py?
		"""
		generate overview of active and archived items

		@return: None
		"""
		archiveItems()
		activeItems = getItems(self.active)
		archivedItems = getItems(self.archive)
		date = time.strftime("%Y-%m-%d-%T", time.localtime())
		f = open(self.report, "a")
		string = "%s %d %d" % (date, len(activeItems), len(archivedItems))
		f.write(string + os.linesep)
		f.close()

	def removeDuplicates(self, items):
		pass # DEBUG: to do

	def exists(self, items, id, displayMessage = False):
		"""
		checks whether a specific item ID exists

		@param items: items with IDs
		@type  items: dict
		@param id: item ID
		@type  id: int
		@param displayMessage: display notification on error
		@type  displayMessage: [optional] bool
		@return: item exists
		@rtype : bool
		"""
		if items.has_key(id):
			return True
		else:
			if(displayMessage):
				print "#%d: No such item." % id
			return False

class config:
	def __init__(self, filename = ".todotxt"):
		"""
		default configuration

		@param filename: configuration file
		@type  filename: [optional] str
		@return: None
		"""
		self.file = filename
		#self.priorityRE = re.compile(r"\([A-Z]\) ") # DEBUG'd
		self.priorityRE = re.compile(r".*(\([A-Z]\)).*") # DEBUG: use r"^\([A-Z]\)"?
		self.defaults = {
			# preferences
			"baseDir": "~/todotxt/", # DEBUG: "~" not supported!?
			"file_active": "tasks.txt",
			"file_archive": "archive.txt",
			"file_report": "report.txt",
			"useUTC": False,
			# colors
			"default": "\033[0m",
			"white": "\033[1;37m",
			"black": "\033[0;30m",
			"red": "\033[0;31m",
			"green": "\033[0;32m",
			"blue": "\033[0;34m",
			"yellow": "\033[1;33m",
			"purple": "\033[0;35m",
			"cyan": "\033[0;36m",
			"brown": "\033[0;33m",
			"light gray": "\033[0;37m",
			"dark gray": "\033[1;30m",
			"light red": "\033[1;31m",
			"light green": "\033[1;32m",
			"light blue": "\033[1;34m",
			"light purple": "\033[1;35m",
			"light cyan": "\033[1;36m"
		}
		# highlight colors
		self.defaults["A"] = self.defaults["light red"]
		self.defaults["B"] = self.defaults["yellow"]
		self.defaults["C"] = self.defaults["light blue"]
		self.defaults["all"] = self.defaults["white"]
		# platform-specific settings
		if sys.platform == "win32" or os.name in ["nt", "ce"]: # non-POSIX-compliant platforms -- DEBUG: improve conditions
			defaults["baseDir"] = os.getcwd() + os.sep
			defaults["colorsDisabled"] = True

	def read(self):
		"""
		read configuration file

		@return: None
		"""
		cfg = SafeConfigParser(self.defaults)
		cfg.read(self.file)
		# preferences
		section = "preferences"
		self.baseDir = cfg.get(section, "baseDir")
		self.file_active = cfg.get(section, "file_active")
		self.file_archive = cfg.get(section, "file_archive")
		self.file_report = cfg.get(section, "file_report")
		self.useUTC = cfg.get(section, "useUTC")
		# highlight colors
		section = "priorities"
		for c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
			self.highlightColors = self.colors[cfg.get(section, c)]

	def write(self):
		"""
		write configuration file

		@return: None
		"""
		pass # DEBUG: to do

# startup

if __name__ == "__main__": # skip main() if module was imported
	sys.exit(main(sys.argv))

