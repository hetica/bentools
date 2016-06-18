#!/usr/bin/env python3
# -*- coding:utf8 -*-
"""
Extract informations from vcf file(s)
"""

import sys, os

__appname = "vcfstat"
__shortdesc = "Extract informations from vcf file(s)"
__licence = "none"
__version = "0.1"
__author = "Benoit Guibert <benoit.guibert@free.fr>"

vcfnamelist = []
nbsiteslist = []
nbsnplist = []
nbinslist = []
nbdellist = []
nbcomplexlist = []
header="Vcf_names\tVariant_number\tsnp\tins\tdel\tcomplex_mnp"
totals = [0, 0, 0, 0, 0]


def helpme(parent):											# required
	"""print usage of the command"""
	print("\n{}\n".format(__shortdesc))
	if parent == __appname:
		print("Usage: {} [-t|-a] <*.vcf>\n".format(__appname))
	else:
		print("Usage:	{} {} [-t|-a] <*.vcf>\n".format(parent, __appname))
	print(" -t	: print totals only")
	print(" -a	:print details and totals\n")

def argsChk(parent, args):
	"""checks arguments"""
	opts=""												# print details
	if "-t" in args:									
		args.remove("-t")
		opts="t"										# print totals 
	if "-a" in args:
		args.remove("-a")
		opts="a"										# print details and totals
	if len(args) < 1:									
		helpme(parent)
		sys.exit()
	return opts

def fileChk(f):
	"""
	- check if file format is OK
	- try to know the variant caller source of file
	- call extractInfosByFile() method
	"""
	with open(f) as fic:
		content = fic.readlines()
		if len(content) == 0:
			sys.stderr.write("file {} empty: abort\n".format(f))
			return
	for i in range(0,10):
		if "source=" and "freeBayes" in content[i]:
			varcaller="freebayes"
			extractInfosByFile(f, content, varcaller)
			return
	varcaller="other"
	extractInfosByFile(f, content, varcaller)


def extractInfosByFile(f, content, varcaller):
	"""Extracts informations file by file"""
	nbsites=0
	typesVariants = [0, 0, 0, 0]					# snp, ins, del, complex
	# Name of file
	vcfnamelist.append(".".join(os.path.basename(f).split(".")[:-1]))			# basename without extension
	# number of sites
	numline=0
	for l in content:
		numline +=1
		if l[0] != "#":
			nbsites +=1
			# extracts types of variants
			extractVariantsByLine(f, l, numline, typesVariants, varcaller)
	nbsiteslist.append(nbsites)
	nbsnplist.append(typesVariants[0])
	nbinslist.append(typesVariants[1])
	nbdellist.append(typesVariants[2])
	nbcomplexlist.append(typesVariants[3])
	
def extractVariantsByLine(f, l, numline, typesVariants, varcaller):
	"""
	Extract variant informations, line by line
	some variant caller could be receive special traitment (cf freebayes)
	"""
	if varcaller == "freebayes":
		try:
			variants = l.split("\t")[7].split(";")[40].split("=")[1].split(",")
		except IndexError:
			print("error IndexError in file {}, line {}".format(f, numline) )
			sys.exit ()
		for a in variants:
			if "snp" in a: typesVariants[0] +=1
			elif "ins" in a: typesVariants[1] +=1
			elif "del" in a: typesVariants[2] +=1
			else: typesVariants[3] +=1
	else:
		ref = l.split("\t")[3]
		alt = l.split("\t")[4].split(",")
		# print(l, " - ", ref, " - ", alt)
		for a in alt:
			if len(ref) == len(a): typesVariants[0] +=1
			if len(ref) < len(a): typesVariants[1] +=1
			if len(ref) > len(a): typesVariants[2] +=1
		typesVariants[3] = "."

def outputDetails(args):
	"""Print informations file by file"""
	print(header)
	for i,a in enumerate(vcfnamelist):
		
		print("{}\t{}\t{}\t{}\t{}\t{}".format(
				vcfnamelist[i], nbsiteslist[i],
				nbsnplist[i], nbinslist[i],
				nbdellist[i], nbcomplexlist[i]))

def outputTotals(opts):
	"""Print totals"""
	for i,a in enumerate(vcfnamelist):
		totals[0] += nbsiteslist[i]
		totals[1] += nbsnplist[i]
		totals[2] += nbinslist[i]
		totals[3] += nbdellist[i]
		#if type(totals[4]) is int:
		try:
			totals[4] += nbcomplexlist[i]
		except TypeError:
			pass
	if opts == "a" : print ("---")
	print(header)
	print("totals\t{}\t{}\t{}\t{}\t{}".format(totals[0], totals[1], totals[2], totals[3], totals[4]))
	

def main(parent, args):										# required
	del args[0]												# avoid app name
	opts = argsChk(parent, args)
	for f in args:
		fileChk(f)
	if opts == "":
		outputDetails(args)
	if opts == "a":
		outputDetails(args)
		outputTotals(opts)
	if opts == "t":
		outputTotals(opts)
	

if __name__ == "__main__":
	main(__appname, sys.argv)								# required
