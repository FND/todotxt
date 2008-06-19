#!/usr/bin/env python

"""
TODO.TXT Manager
Author:     Shane Koster <shane.koster@gmail.com> 
Concept by: Gina Trapani (ginatrapani@gmail.com
License:    GPL, http://www.gnu.org/copyleft/gpl.html
Version:    1.5.2-py
More info:  http://todotxt.com
"""

import re
import os
import sys
import time

TODO_DIR = "/home/skoster/share/todo"

# Your todo/done/report.txt locations
TODO_FILE   = TODO_DIR + "/todo.txt"
DONE_FILE   = TODO_DIR + "/done.txt"
REPORT_FILE = TODO_DIR + "/report.txt"
TMP_FILE    = TODO_DIR + "/todo.tmp"

NONE         = ""
BLACK        = "\033[0;30m"
RED          = "\033[0;31m"
GREEN        = "\033[0;32m"
BROWN        = "\033[0;33m"
BLUE         = "\033[0;34m"
PURPLE       = "\033[0;35m"
CYAN         = "\033[0;36m"
LIGHT_GREY   = "\033[0;37m"
DARK_GREY    = "\033[1;30m"
LIGHT_RED    = "\033[1;31m"
LIGHT_GREEN  = "\033[1;32m"
YELLOW       = "\033[1;33m"
LIGHT_BLUE   = "\033[1;34m"
LIGHT_PURPLE = "\033[1;35m"
LIGHT_CYAN   = "\033[1;36m"
WHITE        = "\033[1;37m"
DEFAULT      = "\033[0m"

# === PRIORITY COLORS ===
PRI_A = YELLOW   # color for A priority
PRI_B = GREEN  # color for B priority
PRI_C = LIGHT_BLUE   # color for B priority
PRI_X = WHITE   # color for rest of them

def usage():
    text = "  Usage: " + sys.argv[0] + """ [options] [ACTION] [PARAM...]

  Actions:
    add "THING I NEED TO DO p:project @context"
      Adds TODO ITEM to your todo.txt.
      Project and context notation optional.
      Quotes optional.
  
    append NUMBER "TEXT TO APPEND"
      Adds TEXT TO APPEND to the end of the todo on line NUMBER.
      Quotes optional.
  
    archive
      Moves done items from todo.txt to done.txt.
  
    del NUMBER
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
    -nc : Turns off colors

  More on the todo.txt manager at
  http://todotxt.com
  Version 1.5.2-python
  Copyleft 2006, Gina Trapani (ginatrapani@gmail.com)
  Copyleft 2006, Shane Koster (shane.koster@gmail.com)
"""
    print text

def getTaskDict():
    """a utility method to obtain a dictionary of tasks from the TODO file"""
    count = 0
    tasks = {}
    # build a dictionary of the todo list items
    for line in open(TODO_FILE).readlines():
        if (line.strip() == ""): continue
        count = count + 1
        tasks[count] = line.rstrip()
    return tasks
    
def getDoneDict():
    """a utility method to obtain a dictionary of tasks from the DONE file"""
    count = 0
    tasks = {}
    # build a dictionary of the todo list items
    for line in open(DONE_FILE).readlines():
        if (line.strip() == ""): continue
        count = count + 1
        tasks[count] = line.rstrip()
    return tasks
    
def writeTasks(taskDict):
    """a utility method to write a dictionary of tasks to the TODO file"""
    keys = taskDict.keys()
    keys.sort()
    f = open(TODO_FILE, "w")
    for key in keys:
        f.write(taskDict[key] + os.linesep)
    f.close()
    
def writeDone(doneDict):
    keys = doneDict.keys()
    keys.sort()
    f = open(DONE_FILE, "w")
    for key in keys:
        f.write(doneDict[key] + os.linesep)
    f.close()

def add(text):
    """add a new task to the TODO file"""
    f = open(TODO_FILE, "a")
    f.write(text + os.linesep)
    f.close()

def append(item, text=""):
    """append text to a given task"""
    tasks = getTaskDict()
    if (not tasks.has_key(item)):
        print "%d: No such todo." % item
        sys.exit(1)
    tasks[item] = " ".join([tasks[item], text])
    writeTasks(tasks)

def archive():
    tasks = getTaskDict()
    done = getDoneDict()
    tasksCopy = tasks.copy()
    for k,v in tasks.iteritems():
        if v.startswith("x"):
            done[len(done)] = tasksCopy.pop(k)
    writeDone(done)
    writeTasks(tasksCopy)

def delete(item):
    tasks = getTaskDict()
    if (not tasks.has_key(item)):
        print "%d: No such todo." % item
        sys.exit(1)
    tasks.pop(item)
    writeTasks(tasks)

def do(item):
    tasks = getTaskDict()
    if (not tasks.has_key(item)):
        print "%d: No such todo." % item
        sys.exit(1)
    date = time.strftime("%Y-%m-%d", time.localtime())
    tasks[item] = " ".join(["x", date, tasks[item]])
    writeTasks(tasks)
    print "%d marked as done." % item

def list(patterns=None):
    items = [] 
    tasks = getTaskDict()

    if (patterns):
        for k,v in tasks.iteritems():
            match = True
            # make sure all patterns are matched
            for pattern in patterns:
                if (not re.search(pattern, v, re.IGNORECASE)): match = False

            if (match == True): items.append("%3d: %s" % (k, v))
    else:
        for k,v in tasks.iteritems():
            items.append("%3d: %s" % (k, v)) 

    #items.sort() # sort by todo.txt order
    items.sort(alphaSort) # sort by tasks alphbetically

    re_pri = re.compile(r".*(\([A-Z]\)).*")
    for item in items: 
        print re_pri.sub(highlightPriority, item)

def alphaSort(a, b):
    """sorting function to sort tasks alphabetically"""
    if (a[5:] > b[5:]): return 1
    elif (a[5:] < b[5:]): return -1
    else: return 0

def highlightPriority(matchobj):
    """color replacement function used when highlighting priorities"""
    if (matchobj.group(1) == "(A)"):
        return PRI_A + matchobj.group(0) + DEFAULT
    elif (matchobj.group(1) == "(B)"):
        return PRI_B + matchobj.group(0) + DEFAULT
    elif (matchobj.group(1) == "(C)"):
        return PRI_B + matchobj.group(0) + DEFAULT
    else: 
        return PRI_X + matchobj.group(0) + DEFAULT

def prioritize(item, newpriority):
    newpriority = newpriority.upper()
    tasks = getTaskDict()
    if (not tasks.has_key(item)):
        print "%d: No such todo." % item
        sys.exit(1)
    if (newpriority != "" and not re.match("[A-Z]", newpriority)):
        print "Priority not recognized: " + newpriority
        sys.exit(1)

    re_pri = re.compile(r"\([A-Z]\) ")

    if (newpriority == ""):
        # remove the existing priority
        tasks[item] = re.sub(re_pri, "", tasks[item])
    elif (re.match(re_pri, tasks[item])):
        tasks[item] = re.sub(re_pri, "(" + newpriority + ") ", tasks[item])
    else:
        tasks[item] = "(" + newpriority + ") " + tasks[item]

    writeTasks(tasks)

def replace(item, text):
    """replace text to a given task"""
    tasks = getTaskDict()
    if (not tasks.has_key(item)):
        print "%d: No such todo." % item
        sys.exit(1)
    tasks[item] = text
    writeTasks(tasks)

def removeDuplicates():
    pass

def report():
    # archive first
    archive()

    active = getTaskDict()
    closed = getDoneDict()

    date = time.strftime("%Y-%m-%d-%T", time.localtime())
    f = open(REPORT_FILE, 'a')
    string = "%s %d %d" % (date, len(active), len(closed))
    f.write(string + os.linesep)
    f.close()

if __name__ == "__main__":
    if (len(sys.argv) < 2):
        usage()
        sys.exit()
    else:
        if (sys.argv[1] == "-nc"):
            PRI_A = NONE
            PRI_B = NONE
            PRI_C = NONE
            PRI_X = NONE
            action = sys.argv[2]
            args = sys.argv[3:]
        else:
            action = sys.argv[1]
            args = sys.argv[2:]

    if (action == "add"):
        if (args): add("".join(args))
        else: print "Usage: " + sys.argv[0] + " add TEXT [p:PROJECT] [@CONTEXT]"
    elif (action == "append"):
        if (len(args) > 1 and args[0].isdigit()): 
            append(int(args[0]), "".join(args[1:]))
        else:
            print "Usage: " + sys.argv[0] + " append <item_num> TEXT"
    elif (action == "archive"):
        archive()
    elif (action == "del"):
        if (len(args) == 1 and args[0].isdigit()):
            delete(int(args[0]))
        else:
            print "Usage: " + sys.argv[0] + " del <item_num>"
    elif (action == "do"):
        if (len(args) == 1 and args[0].isdigit()):
            do(int(args[0]))
        else:
            print "Usage: " + sys.argv[0] + " do <item_num>"
    elif (action == "ls" or action == "list"):
        if (len(args) > 0):
            list(args)
        else:
            list()
    elif (action == "lspri" or action == "listpri"):
        if (len(args) > 0): 
            x = ["\([" + args[0] + "]\)"]
        else: 
            x = ["\([A-Z]\)"]
        list(x)
    elif (action == "pri"):
        if (len(args) == 2 and args[0].isdigit() and args[1].isalpha()): 
            prioritize(int(args[0]), args[1])
        elif (len(args) == 1 and args[0].isdigit()): 
            # remove the existing priority
            prioritize(int(args[0]), "")
        else:
            print "Usage: " + sys.argv[0] + " pri <item_num> [PRIORITY]"
    elif (action == "replace"):
        if (len(args) > 2 and args[0].isdigit()):
            replace(int(args[0]), " ".join(args[1:]))
        else:
            print "Usage: " + sys.argv[0] + " replace <item_num> TEXT"
    elif (action == "remdup"):
        removeDuplicates()
    elif (action == "report"):
        report()
    else:
        usage()

