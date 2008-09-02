import sys
import commands

def main(args = []):
	try:
		dispatch(args[1], args[2:])
	except IndexError:
		commands.help()

def dispatch(command, params):
	commands = Commands()
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
		cmd.help()

if __name__ == "__main__":
	sys.exit(main(sys.argv))

