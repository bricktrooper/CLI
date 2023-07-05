from sys import argv
from cli import CLI

def foo(prefix, args):
	print("foo")
	cli = CLI(prefix, 0)
	cli.subcommand("hello", hello)
	cli.subcommand("world", world, min = 1, max = 2, usage = "<x> [y]")
	cli.run(args)

def bar(prefix, args):
	print("bar")

def hello(prefix, args):
	print("hello")
	cli = CLI(prefix, 0)
	cli.subcommand("dead", dead, min = 0, max = 3, usage = "[x] [y] [z]")
	cli.subcommand("beef", beef, min = 0, max = 0, usage = "")
	cli.run(args)

def world(prefix, args):
	print("world")

def dead(prefix, args):
	print("dead")

def beef(prefix, args):
	print("beef")

def main():
	prefix = argv.pop(0)
	cli = CLI(prefix, 0, verbose=True)
	cli.subcommand("foo", foo)
	cli.subcommand("bar", bar, min = 1, max = 1, usage = "<x>")
	return cli.run(argv)

exit(main())
