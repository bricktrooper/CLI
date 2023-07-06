from . import log

ERROR = -1
SUCCESS = 0

class Subcommand:
	def __init__(self, handler, name, usage = None, min = None, max = None, leaf = False):
		self.handler = handler
		self.name = name
		self.usage = usage
		self.min = min
		self.max = max
		self.leaf = leaf

class Command:
	def __init__(self, prefix, min, max = None, verbose = False):
		if max is not None and min > max:
			log.error(f"Minimum cannot be greater than maximum")
			return ERROR

		self.min = min
		self.max = max
		self.subcommands = {}
		self.prefix = prefix
		self.verbose = verbose

		self.log_verbose(f"Initialized '{self.prefix} <{self.min}, {self.max}>'")

	def log_verbose(self, message):
		if self.verbose:
			log.verbose(message)

	def branch(self, handler, name):
		if name in self.subcommands:
			log.error(f"'{name}' already exists under '{self.prefix}'")
			return ERROR

		self.subcommands[name] = Subcommand(handler, name, leaf = False)
		self.log_verbose(f"Registered branch '{self.prefix} {name}'")
		return SUCCESS

	def leaf(self, handler, name, usage, min, max):
		if name in self.subcommands:
			log.error(f"'{name}' already exists under '{self.prefix}'")
			return ERROR

		self.subcommands[name] = Subcommand(handler, name, usage, min, max, leaf = True)
		self.log_verbose(f"Registered leaf '{self.prefix} {name} {usage}'")
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
		for name in self.subcommands:
			usage = self.subcommands[name].usage
			if usage is None:
				usage = ""
			log.info(f"{self.prefix} {name} {usage}")

	def run(self, args):
		argc = Command.verify(args, self.min, self.max)
		if argc == ERROR:
			self.hint()
			return ERROR

		if argc == 0:
			self.hint()
			return SUCCESS

		name = args.pop(0)
		if name not in self.subcommands:
			log.error(f"No such command '{self.prefix} {name}'")
			self.hint()
			return ERROR

		subcommand = self.subcommands[name]
		if subcommand.leaf:
			if Command.verify(args, subcommand.min, subcommand.max) == ERROR:
				log.info(f"{self.prefix} {name} {subcommand.usage}")
				return ERROR

		prefix = f"{self.prefix} {name}"
		return subcommand.handler(prefix, args)
