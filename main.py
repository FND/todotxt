import sys

from commands import Commands
from items import Items
from store import FileStore

def main(args):
	items = Items()
	store = FileStore("/tmp/active.txt", "/tmp/done.txt", "/tmp/report.txt") # TODO: to be read from config
	commands = Commands(items, store)
	try:
		dispatch(commands, args[1], args[2:])
	except IndexError:
		commands.help()

def dispatch(commands, command, params):
	cmd = {
		"add": commands.add,
		"pri": commands.prioritize,
		"append": commands.append,
		"replace": commands.replace,
		"rm": commands.remove,
		"flag": commands.flag,
		"rmdup": commands.removeDuplicates,
		"list": commands.list,
		"listpri": commands.listPriorities,
		"archive": commands.archive,
		"report": commands.generateReport,
		"help": commands.help
	}
	# aliases
	cmd["a"] = cmd["add"]
	cmd["p"] = cmd["pri"]
	cmd["ls"] = cmd["list"]
	cmd["lsp"] = cmd["listpri"]
	try:
		cmd[command](*params)
	except (NameError, TypeError): # unknown command or spurious parameters
		commands.help()

if __name__ == "__main__":
	sys.exit(main(sys.argv))

