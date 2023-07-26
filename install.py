import os
import shutil

os.system("git clone https://github.com/bricktrooper/CLI repo")
os.system("pip install repo/")
shutil.rmtree("repo/", ignore_errors = True)
shutil.rmtree("build", ignore_errors = True)
shutil.rmtree("dist/", ignore_errors = True)
shutil.rmtree("cli.egg-info", ignore_errors = True)
