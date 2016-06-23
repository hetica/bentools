#!/usr/bin/env python3
# -*- coding:utf8 -*-

# http://biopython.org/wiki/SeqIO

__appname = "sff2fastq"
__licence = "none"
__version = "0.1"
__author = "Benoit Guibert <benoit.guibert@free.fr>"
__shortdesc = "Convert ssf files (Roche454) to fastq"

import sys, os, argparse
try:
	from Bio import SeqIO
except ImportError:
	print("ImportError: No module named 'Bio'")
	print("Maybe, you should be install it:")
	print("try 'sudo apt-get install python-biopython' on Ubuntu")
	print("or sudo pip3 install biopython")
	sys.exit()

def sff2fastx(sffile, typeseq):
	fastxFile = os.path.basename(sffile).split(".")[0] + "." + typeseq
	print(fastxFile)
	try:
		count = SeqIO.convert(sffile, "sff", fastxFile, typeseq)
	except AssertionError:
		pass
	except IOError:
		print("No such file or directory: {}".format(sffile))
		exit()

def argsChk(parent, args):
	if "-h" in args:
		__opts.append("-h")
		args.remove("-h")
		helpme(parent)
	if len(args) < 1:
		helpme(parent)
		sys.exit()

def helpme(parent):
	print("\n{}\n".format(__shortdesc))
	helpdesc =	"Options:\n\tfasta or fastq\t: output file format, default fastq\n\t-h\t\t: help"
	if parent == __appname:
		print("Usage:	{} [fasta|fastq] input1.ssf input2.ssf ...\n".format(__appname))
		print(helpdesc)
	else:	
		print("Usage:	{} {} [-h] [fasta|fastq] <arguments\n".format(parent, __appname))
		print(helpdesc)

def main (parent, args):
	del args[0]
	argsChk(parent, args)

	# checks fasta or fastq options, fastq by défaut
	typeseq = "fastq"
	for i,a in enumerate(args):
		if a == "fasta" or a == "fastq":
			typeseq = args.pop(i)
			
	for a in range(0, len(args)):
		sffile = args[a]
		sff2fastx(args[a], typeseq)
		
if __name__ == "__main__":
	main(__appname, sys.argv)
