#!/usr/bin/env python
# -*- coding:utf8 -*-

__appname = "diff"
__shortdesc = "Show differences between two strings."
__licence = "none"
__version = "0.1"
__author = "Benoit Guibert <benoit.guibert@free.fr>"



def main():
    k1='ATCGCTACTAG'
    k2='AAC CGACTTG'

    diff = ('| '[a==b] for a,b in zip(k1, k2))

    print(k1); print(''.join(diff)) ; print(k2)


if __name__ == "__main__":
    main()
