from cli import *

def arg1(argv):
	log.success("sub2 arg1")

def arg2(argv):
	log.success("sub2 arg2")

def run(argv):
	command = Command("test sub2", 1, None)
	command.add_subcommand("arg1", arg1, "arg1")
	command.add_subcommand("arg2", arg2, "arg2")
	return command.run(argv)
