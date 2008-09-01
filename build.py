"""
combine multiple modules into a single single script file
"""

import sys

def main(args = []):
	cfg = {
		"targetFile": "todo.py",
		"modules": args[1:] or ["main", "items", "util"],
		"hashbang": "#!/usr/bin/env python",
		"info": '"""[TBD]"""' # TODO: name, version, author, license etc.
	}
	imports, startup, callables = retrieve(cfg["modules"])
	# output
	text = compose(cfg["hashbang"], cfg["info"], "\n".join(imports), "\n".join(callables), "\n".join(startup))
	f = open(cfg["targetFile"], "w")
	f.write(text)
	f.close()

def retrieve(modules):
	startup = []
	callables = []
	imports = set()
	continued = False
	for module in modules:
		callables.append("# %s" % module)
		for line in open("%s.py" % module, "r"):
			line = line.rstrip()
			if line.startswith("import ") or line.startswith("from "):
				imports.add(line)
			elif line == "import %s" % module:
				pass
			elif line == 'if __name__ == "__main__":':
				startup.append(line)
				continued = True
			elif continued:
				startup.append(line)
			else:
				callables.append(line)
		continued = False
	return list(imports), startup, callables

def compose(hashbang, info, imports, modules, startup):
	return "%s\n\n%s\n\n%s\n\n%s\n\n%s" % (hashbang, info, imports, modules, startup)

if __name__ == "__main__":
	sys.exit(main(sys.argv))

