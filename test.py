import sys
import sub1
import sub2

from cli import *

command = Command("test", 1, None)
command.add_subcommand("sub1", sub1.run, "sub1")
command.add_subcommand("sub2", sub2.run, "sub2")

def run():
	return command.run(sys.argv[1:])

exit(run())
