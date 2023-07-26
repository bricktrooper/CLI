from distutils.core import setup

setup(
    name = "cli",
	version = "0.1.0",
	description = "An API for creating a command line interface with positional arguments.",
	author = "Kyle Pinto",
	author_email = "kylepinto1018@gmail.com",
    url = "https://github.com/bricktrooper/CLI",
	packages = ["cli"],
	dependencies = ["log"],
)
