import log
import sys

from utils import *

class Command:
	def __init__(self, command):
		self.subcommands = {}
		self.command = command
		self.require_args(0, None)
		self.add_subcommand("help", self.help, "help")

	def add_subcommand(self, subcommand, handler, usage):
		if subcommand in self.subcommands:
			log.error(f"Subcommand '{subcommand}' already exists under command '{self.command}'")
			return ERROR

		self.subcommands[subcommand] = {
			"handler": handler,
			"usage": usage
		}

		log.debug(f"Added subcommand '{subcommand}' under command '{self.command}'")
		return SUCCESS

	def require_args(self, min, max = None):
		if max is not None and min > max:
			log.error(f"Minimum arguments cannot be greater than maximum arguments")
			return ERROR
		self.min = min
		self.max = max
		return SUCCESS

	def help(self, argv):
		argc = check_args(argv, 0)
		if argc == ERROR:
			return ERROR
		for subcommand in self.subcommands:
			log.info(f"{self.command} {self.subcommands[subcommand]['usage']}")
		return SUCCESS

	def run(self, argv):
		argc = check_args(argv, self.min, self.max)
		if argc == ERROR:
			return ERROR

		subcommand = "help"
		if argc > 0:
			subcommand = argv[0]

		if subcommand not in self.subcommands:
			log.error(f"No such subcommand '{subcommand}' under command '{self.command}'")
			return ERROR

		result = self.subcommands[subcommand]["handler"](argv[1:])
		return result
