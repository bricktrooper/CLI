from cli import log

ERROR = -1
SUCCESS = 0

SUBCOMMAND_HELP = "help"

class Command:
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
		self.subcommand(SUBCOMMAND_HELP, self.help, "")

	def log_verbose(self, message):
		if self.verbose:
			log.verbose(message)

	def subcommand(self, subcommand, handler, usage):
		if subcommand in self.subcommands:
			log.error(f"Subcommand '{subcommand}' already exists under command '{self.prefix}'")
			return ERROR

		self.subcommands[subcommand] = {
			"handler": handler,
			"usage": usage
		}

		self.log_verbose(f"Registered command '{self.prefix} {subcommand}'")
		return SUCCESS

	def verify(self, args):
		if args is None:
			log.error("Corrupted arguments")
			return ERROR

		argc = len(args)

		if argc < self.min:
			log.error("Too few arguments")
			self.hint()
			return ERROR

		if self.max is not None and argc > self.max:
			log.error("Too many arguments")
			self.hint()
			return ERROR

		return argc

	def help(self, prefix, args):
		for subcommand in self.subcommands:
			usage = self.subcommands[subcommand]["usage"]
			log.info(f"{self.prefix} {subcommand} {usage}")
		return SUCCESS

	def hint(self):
		log.info(f"Try '{self.prefix} {SUBCOMMAND_HELP}'")

	def run(self, args):
		argc = self.verify(args)
		if argc == ERROR:
			return ERROR

		if argc > 0:
			subcommand = args.pop(0)
		else:
			subcommand = SUBCOMMAND_HELP
			self.log_verbose(f"Defaulting to '{self.prefix} {SUBCOMMAND_HELP}'")

		if subcommand not in self.subcommands:
			log.error(f"No such command '{self.prefix} {subcommand}'")
			self.hint()
			return ERROR

		prefix = f"{self.prefix} {subcommand}"
		return self.subcommands[subcommand]["handler"](prefix, args)
