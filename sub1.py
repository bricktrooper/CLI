from cli import *

def arg1(argv):
	log.success("sub1 arg1")

def arg2(argv):
	log.success("sub1 arg2")

def run(argv):
	command = Command("test sub1", 1, None)
	command.add_subcommand("arg1", arg1, "arg1")
	command.add_subcommand("arg2", arg2, "arg2")
	return command.run(argv)
