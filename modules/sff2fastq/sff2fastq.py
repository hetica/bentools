#!/usr/bin/env python3
# -*- coding:utf8 -*-

# http://biopython.org/wiki/SeqIO

__appname__ = "sff2fastq"
__licence__ = "none"
__version__ = "0.1"
__author__ = "Benoit Guibert <benoit.guibert@free.fr>"
__shortdesc__ = "Convert ssf files (Roche454) to fastq"
__opts__ = []

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

def argsChk(parent):
    args = sys.argv[1:] if __appname__ in sys.argv[0] else sys.argv[2:]
    if "-h" in args:
        __opts__.append("-h")
        args.remove("-h")
        helpme(parent)
    if len(args) < 1:
        helpme(parent)
    return args

def helpme(parent):
    print("\n{}\n".format(__shortdesc__))
    helpdesc =  "Options:\n\tfasta or fastq\t: output file format, default fastq\n\t-h\t\t: help\n"
    if parent == __appname__:
        print("Usage:   {} [fasta|fastq] input1.ssf input2.ssf ...\n".format(__appname__))
        print(helpdesc)
    else:   
        print("Usage:   {} {} [-h] [fasta|fastq] <arguments\n".format(parent, __appname__))
        print(helpdesc)
    sys.exit()

def main (parent):
    args = argsChk(parent)

    # checks fasta or fastq options, fastq by défaut
    typeseq = "fastq"
    for i,a in enumerate(args):
        if a == "fasta" or a == "fastq":
            typeseq = args.pop(i)
            
    for a in range(0, len(args)):
        sffile = args[a]
        sff2fastx(args[a], typeseq)
        
if __name__ == "__main__":
    main(__appname__)
