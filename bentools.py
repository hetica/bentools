#!/usr/bin/env python3
# -*- coding:utf8 -*-

import sys, os
import importlib					# I could have use __import__ also

__appname = "bentools"
__licence = "GPL"
__version = "0.3"
__author = "Benoit Guibert <benoit.guibert@free.fr>"
__modulespath = os.path.dirname( os.path.realpath( __file__ ) ) + "/modules/"

def loadModule(__modulespath, m):
	"Load sub-command"
	sys.path.append(__modulespath + m)
	module = importlib.import_module(m, package=None)
	return module

def helpme():
	"First level help"
	appname = os.path.split(sys.argv[0])[1]
	print("\nProgram: {} (Tools for small Bioinformatics stuffs)".format(__appname))
	print("Version: {}".format(__version))
	print("\nUsage:\t{} <command> [options]".format(__appname))
	print("\nCommands:")
	modulesList = os.listdir(__modulespath)
	for m in modulesList:
		module = loadModule(__modulespath, m)
		tab="\t"
		if len(module.__appname) < 5: tab += tab	# manage spaces between appname & short description
		print("\t", module.__appname, tab, module.__shortdesc)
	print("")
	sys.exit()

def main():
	nbArgs = len(sys.argv)
	# if none argument: print global help
	if nbArgs == 1:
		helpme()
	# if two arguments, print sub-command help
	if nbArgs == 2:
		try:
			module = loadModule(__modulespath, sys.argv[1])
			module.helpme(__appname)
		except ImportError:
			print("No module named '{}'".format(sys.argv[1]))
			helpme()
	# if more than two arguments, load main function of sub-command
	if nbArgs > 2:
		try:
			module = loadModule(__modulespath, sys.argv[1])
			module.main(__appname, sys.argv[1:])
		except:
			sys.exit()

if __name__ == "__main__":
	main()
