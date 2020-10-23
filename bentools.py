#!/usr/bin/env python3
# -*- coding:utf8 -*-

import sys, os
import importlib                            # I could have use __import__ also

__appname__ = "bentools"
__licence__ = "GPL"
__version__ = "0.7.0"
__author__ = "Benoit Guibert <benoit.guibert@free.fr>"
__modulespath__ = os.path.dirname( os.path.realpath( __file__ ) ) + "/modules/"


def loadModule(m):
    """Load sub-command"""
    sys.path.append(__modulespath__ + m)
    module = importlib.import_module(m, package=None)
    return module


def helpme():
    "First level help"
    appname = os.path.split(sys.argv[0])[1]
    print("\nProgram: {} (Tools for small Bioinformatics stuffs)".format(__appname__))
    print("Version: {}".format(__version__))
    print("\nUsage:\t{} <command> [options]".format(__appname__))
    print("\nAvailable modules:")
    print(modules_list())
    sys.exit()


def modules_list ():
    """ List all available modules"""
    module_list = ''
    modulesList = os.listdir(__modulespath__)
    max_length = max(len(a) for a in modulesList) + 2
    for m in modulesList:
        module = loadModule(m)
        module_list += "  {}{}\n".format(m.ljust(max_length), module.__shortdesc__)
    return module_list


def main():
    nbArgs = len(sys.argv)
    # if none argument: print global help
    if nbArgs == 1:
        helpme()
    elif not sys.argv[1] in os.listdir(__modulespath__):
        print("\nModule '{}' not found".format(sys.argv[1]))
        print("\nModules availables:")
        print(modules_list())
        sys.exit()
    else:
        module = loadModule(sys.argv[1])
        module.main(__appname__)


if __name__ == "__main__":
    main()
