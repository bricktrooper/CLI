import log
import sys

from .utils import *

HELP_COMMAND = "help"

class Command:

	def __init__(self, command, min, max = None):
		self.subcommands = {}
		self.command = command
		self.require_arguments(min, max)

		log.debug(f"Initialized '{self.command} <{self.min}, {self.max}>'")
		self.add_subcommand(HELP_COMMAND, self.help, HELP_COMMAND)

	def add_subcommand(self, subcommand, handler, usage):
		if subcommand in self.subcommands:
			log.error(f"Subcommand '{subcommand}' already exists under command '{self.command}'")
			return ERROR

		self.subcommands[subcommand] = {
			"handler": handler,
			"usage": usage
		}

		log.debug(f"Added command '{self.command} {subcommand}'")
		return SUCCESS

	def require_arguments(self, min, max = None):
		if max is not None and min > max:
			log.error(f"Minimum cannot be greater than maximum")
			return ERROR
		self.min = min
		self.max = max
		return SUCCESS

	def check_arguments(self, argv):
		if argv is None:
			log.error("Corrupted arguments")
			return ERROR

		argc = len(argv)

		if argc < self.min:
			log.error("Too few arguments")
			self.hint_help()
			return ERROR

		if self.max is not None and argc > self.max:
			log.error("Too many arguments")
			self.hint_help()
			return ERROR

		return argc

	def help(self, argv):
		for subcommand in self.subcommands:
			log.info(f"{self.command} {self.subcommands[subcommand]['usage']}")
		return SUCCESS

	def hint_help(self):
		log.info(f"Try '{self.command} {HELP_COMMAND}'")

	def run(self, argv):
		argc = self.check_arguments(argv)
		if argc == ERROR:
			return ERROR

		subcommand = HELP_COMMAND
		if argc > 0:
			subcommand = argv[0]

		if subcommand not in self.subcommands:
			log.error(f"No such command '{self.command} {subcommand}'")
			self.hint_help()
			return ERROR

		result = self.subcommands[subcommand]["handler"](argv[1:])
		return result
