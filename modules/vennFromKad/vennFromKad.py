#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, os

__appname__ = "vennFromKad"
__licence__ = "none"
__version__ = "0.1"
__author__ = "Benoit Guibert <benoit.guibert@free.fr>"
__shortdesc__ = "Build a file for a venn diagram from kad output"
__opts__ = []


def main(parent):
    args = argsChk(parent)
    for file in args:
        venn_list = buildVennData(file)
        setFile(file, venn_list)
    # print("App: ", parent)
    # print("Arguments:")


def buildVennData(file):
    with open(file) as stream:
        venn_list = {}
        header = stream.readline().split(';')
        for line in stream:
                name = ""
                sline = line.split('\t')[1:]
                #print(sline)
                if len(sline) > 0:
                    try:
                        for i,item in enumerate(sline):
                            if i == 0:
                                name += item.split('|')[0]
                            else:
                                name += "_" + item.split('|')[0]
                    except IndexError:
                        pass
                    if name in venn_list:
                        venn_list[name] += 1
                    else:
                        venn_list[name] = 1
        return venn_list


def setFile(file, venn_list):
    #print(venn_list)
    venn_table = ""
    for k,v in venn_list.items():
        venn_table += "{}\t{}\n".format(k,v)
    print(venn_table, end="")


def argsChk(parent):
    args = sys.argv[1:] if __appname__ in sys.argv[0] else sys.argv[2:]
    if "-h" in args:
        __opts__.append("-h")
        args.remove("-h")
        helpme(parent)
        sys.exit()
    if len(args) < 1:
        helpme(parent)
        sys.exit()
    return args


def helpme(parent):
    opts = "  -h\t: help\n"
    print("\n{}\n".format(__shortdesc__))
    if parent == __appname__:
        print("Usage:   {} <arguments>".format(__appname__))
        print("     {} -h\n".format(__appname__))
        print(opts)
    else:   
        print("Usage:   {} {} [-h] <arguments>".format(parent, __appname__))
        print("     {} {} -h\n".format(parent, __appname__))
        print(opts)


if __name__ == "__main__":
    main(__appname__)
