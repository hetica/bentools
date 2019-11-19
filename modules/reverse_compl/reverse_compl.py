#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, os

__appname__ = "reverse_compl"
__licence__ = "none"
__version__ = "0.1"
__author__ = "Benoit Guibert <benoit.guibert@free.fr>"
__shortdesc__ = "Return reverse complement from one or more sequence"
__opts__ = []

def main(parent):
    args = argsChk(parent)
    alphabet = {'A':'T','a':'t','C':'G','c':'g','G':'C','g':'c','T':'A','t':'a','N':'N','n':'n'}
    revcompl = lambda x: ''.join([alphabet[B] for B in x][::-1])
    for a in args:
        print(a)
        print(revcompl(a))
        print("---")

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
    opts = "  -h\t: help\n"
    print("\n{}\nVersion: {}\n".format(__shortdesc__, __version__))
    if parent == __appname__:
        print("Usage:   {} [-h] <sequence_1> [<sequence_n>]\n".format(__appname__))
        print(opts)
    else:
        print("Usage:   {} {} [-h] <sequence_1> [<sequence_n>]\n".format(parent, __appname__))
        print(opts)
    sys.exit()


if __name__ == "__main__":
    main(__appname__)
