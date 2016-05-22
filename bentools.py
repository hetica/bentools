#!/usr/bin/env python3
# -*- coding:utf8 -*-

__appname = "bentools"
__licence = "none"
__version = "0.1"
__author = "Benoit Guibert <benoit.guibert@free.fr>"

import sys
import re

def main():
	try:
		args = open(sys.argv[1])
	except IOError:
		sys.exit("Cannot open given file")
	except IndexError:
		sys.exit("Please indicate a file name")	

def listOptions():
	# parser les arguments de la ligne de commande


	# si 1 argument
		# ...
	# si > 1 argument

# rechercher les différents modules

# afficher les différents modules
	

if __name__ == "__main__":
	main()
