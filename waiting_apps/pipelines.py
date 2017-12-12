#!/usr/bin/env python3
# -*- coding:utf8 -*-

# read stdin (from pipe) of do something

import sys

def main():
    if sys.stdin.isatty():                      # method called "isatty()" returns true if associated with a terminal.
        print('not read from stdin')            # if TRUE --> no stdin
    else:                                       # read stdin
        for line in sys.stdin:
            sys.stdout.write(line)

if __name__ == "__main__":
    main()

"""
1. --> usage()
    1.1. si pas de paramètres ET pas de pipe --> --help
2. --> main()
"""
