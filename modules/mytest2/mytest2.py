#!/usr/bin/env python3
# -*- coding:utf8 -*-

import sys

__appname = "mytest2"										# required
__licence = "none"
__version = "0.1"
__author = "Benoit Guibert <benoit.guibert@free.fr>"
__shortdesc = "Et lui non plus ne sert à rien"				# required

def helpme(parent):											# required
	print("\nUsage:	{} {} [options] <in.bam> <out.bam>\n".format(parent, __appname))
	
def main(parent, args):										# required
	print("bonjour ", parent)
	for a in args: print(a)

if __name__ == "__main__":
	main(__appname, sys.argv)
