#!/usr/bin/env python3
# -*- coding:utf8 -*-

__appname__ = "enstsearch"
__shortdesc__ = "Build fasta file from transcripts list against reference transcriptome fasta file."
__licence__ = "none"
__version__ = "0.2"
__author__ = "Benoit Guibert <benoit.guibert@free.fr>"

## A MODIFIER SELON SES BESOINS
list='''ENST00000245255.7 
        ENST00000356766 ENST00000332271 ENST00000299001 ENST00000446230 
        ENST00000537419 ENST00000543336 ENST00000545603 ENST00000305879 
        ENST00000546575 ENST00000546739 ENST00000546931 ENST00000548538 
        ENST00000549083.1 ENST00000552336 ENST00000552395 ENST00000552397'''
# ref='GRCh38.cdna.all.sample.fa'
ref='GRCh38.cdna.sample.fa'
#######

def main():
    list_transcripts = [s.split('.')[0] for s in list.split()]
    print_line = 0
    
    with open(ref) as stream:
        for line in stream:
            if line[0] == '>':
                ref_transcript = line.split()[0][1:].split('.')[0]
                if ref_transcript in list_transcripts:
                    print(line[:-1])
                    print_line = 1
                else:
                    print_line = 0
            else:
                if print_line:
                    print(line[:-1])

if __name__ == "__main__":
    main()

