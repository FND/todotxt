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
	imports, startup, contents = retrieve(cfg["modules"])
	# output
	text = compose(cfg["hashbang"], cfg["info"], "\n".join(imports), "\n".join(contents), "\n".join(startup))
	f = open(cfg["targetFile"], "w")
	f.write(text)
	f.close()

def retrieve(modules):
	startup = []
	contents = []
	imports = set()
	continued = False
	for module in modules:
		contents.append("# %s" % module)
		for line in open("%s.py" % module):
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
				contents.append(line)
		continued = False
	return list(imports), startup, contents

def compose(hashbang, info, imports, modules, startup):
	return "%s\n\n%s\n\n%s\n\n%s\n\n%s" % (hashbang, info, imports, modules, startup)

if __name__ == "__main__":
	sys.exit(main(sys.argv))

