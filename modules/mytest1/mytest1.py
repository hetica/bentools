#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ce module ne sert strictement à rien
"""

import sys, os

__appname = "mytest1"										# required
__licence = "none"
__version = "0.1"
__author = "Benoit Guibert <benoit.guibert@free.fr>"
__shortdesc = "this module is useless"						# required


def helpme(parent):											# required
	print("\nUsage:	{} {} [options] <in.sff> <out.fastq>\n".format(parent, __appname))


def main(parent, args):										# required
	"""Pas glop"""
	print("App caller: ", parent)
	for a in args:
		print(a)


if __name__ == "__main__":
	main(__appname, sys.argv)
