from sys import argv
from cli import Command

def foo(prefix, args):
	print("foo")
	command = Command(prefix, 0)
	command.branch(hello, "hello")
	command.leaf(world, "world", "<x> [y]", 1, 2)
	command.run(args)

def bar(prefix, args):
	print("bar")

def hello(prefix, args):
	print("hello")
	command = Command(prefix, 0)
	command.leaf(dead, "dead", "[x] [y] [z]", 0, 3)
	command.leaf(beef, "beef", "", 0, 0)
	command.run(args)

def world(prefix, args):
	print("world")

def dead(prefix, args):
	print("dead")

def beef(prefix, args):
	print("beef")

def main():
	prefix = argv.pop(0)
	command = Command(prefix, 0)
	command.branch(foo, "foo")
	command.leaf(bar, "bar", "<x>", 1, 1)
	return command.run(argv)

exit(main())
