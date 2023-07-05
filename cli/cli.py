from . import log

ERROR = -1
SUCCESS = 0

class CLI:
	def __init__(self, prefix, min, max = None, verbose = False):
		self.subcommands = {}
		self.prefix = prefix
		self.verbose = verbose

		if max is not None and min > max:
			log.error(f"Minimum cannot be greater than maximum")
			return ERROR

		self.min = min
		self.max = max

		self.log_verbose(f"Initialized '{self.prefix} <{self.min}, {self.max}>'")

	def log_verbose(self, message):
		if self.verbose:
			log.verbose(message)

	def subcommand(self, subcommand, handler, min = None, max = None, usage = None):
		if subcommand in self.subcommands:
			log.error(f"subcommand '{subcommand}' already exists under command '{self.prefix}'")
			return ERROR

		self.subcommands[subcommand] = {
			"handler": handler,
			"usage": usage,   # parameter usage string for leaves
			"min": min,
			"max": max,
			"leaf": min is not None and max is not None and usage is not None
		}

		format = f" {usage}" if self.subcommands[subcommand]["leaf"] else ""
		self.log_verbose(f"Registered '{self.prefix} {subcommand}{format}'")
		return SUCCESS

	@staticmethod
	def verify(args, min, max):
		if args is None:
			log.error("Corrupted arguments")
			return ERROR

		argc = len(args)

		if argc < min:
			log.error("Too few arguments")
			return ERROR

		if max is not None and argc > max:
			log.error("Too many arguments")
			return ERROR

		return argc

	def hint(self):
		for subcommand in self.subcommands:
			usage = self.subcommands[subcommand]["usage"]
			if usage is None:
				usage = ""
			log.info(f"{self.prefix} {subcommand} {usage}")

	def run(self, args):
		argc = CLI.verify(args, self.min, self.max)
		if argc == ERROR:
			self.hint()
			return ERROR

		if argc == 0:
			self.hint()
			return SUCCESS

		subcommand = args.pop(0)
		if subcommand not in self.subcommands:
			log.error(f"No such command '{self.prefix} {subcommand}'")
			self.hint()
			return ERROR

		info = self.subcommands[subcommand]
		if info["leaf"]:
			min = info["min"]
			max = info["max"]
			usage = info["usage"]
			if CLI.verify(args, min, max) == ERROR:
				log.info(f"{self.prefix} {subcommand} {usage}")
				return ERROR

		prefix = f"{self.prefix} {subcommand}"
		return info["handler"](prefix, args)
