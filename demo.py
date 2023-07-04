from sys import argv
from cli import Command

def foo(prefix, args):
	print("foo")
	command = Command(prefix, 1)
	command.subcommand("hello", hello, "<dead|beef>")
	command.subcommand("world", world, "")
	command.run(args)

def bar(prefix, args):
	print("bar")
	command = Command(prefix, 1)
	command.run(args)

def hello(prefix, args):
	print("hello")
	command = Command(prefix, 0)
	command.subcommand("dead", dead, "")
	command.subcommand("beef", beef, "")
	command.run(args)

def world(prefix, args):
	print("world")
	command = Command(prefix, 0)
	command.run(args)

def dead(prefix, args):
	print("dead")
	command = Command(prefix, 0)
	command.run(args)

def beef(prefix, args):
	print("beef")
	command = Command(prefix, 0)
	command.run(args)

def main():
	prefix = argv.pop(0)
	command = Command(prefix, 1, 4)
	command.subcommand("foo", foo, "<hello|there>")
	command.subcommand("bar", bar, "")
	return command.run(argv)

exit(main())
