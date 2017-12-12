#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, os
import argparse

__appname__ = "chimct2albou"
__licence__ = "none"
__version__ = "0.1"
__author__ = "John Doe <john.doe@exemple.com>"
__shortdesc__ = "Convert tsv file from chimCT to csv file"

def parseTSVfile (tsv_file):
    """ Function doc """
    with open(tsv_file) as file:
        # print header
        print('Id', 'Name', 'Chr1', 'Pos1', 'Strand1', 'Chr2', 'Pos2', 'Strand2', 'Chim_value', 'Spanning_junction',
                'Spanning_PE', 'Class', 'Pseudogene', 'Anchored_chimera', 'PE_chimera', 'StringencyTest', 'Fusion_distance', 
                'GSNAP_mapped_reads', 'GSNAP_total_reads', 'GSNAP_ratio', 'mRNA_IDs', 'Annotation_type', 'Description_genes', 
                'Exon_IDs', 'Exon1_end_distance', 'Exon2_end_distance', 'Exon1_rank', 'Exon2_rank', 'Read_id', 'Pos_junction', 
                'Read_seq', 'Profil_support', 'Profil_location', 'Nb_spanning_reads', 'Nb_spanning_PE', 'Primers', sep='\t')
        file.readline()             # avoid first line (maybe Cractools fucking message)
        for line in file:
            # for each line of file
            if line[0] != '#':
                split_line = line.split('\t')
                Id = split_line[0]                                                                              # 1
                Name = split_line[1]                                                                            # 2
                Chr1 = split_line[2]                                                                            # 3
                Pos1 = split_line[3]                                                                            # 4
                Strand1 = split_line[4]                                                                         # 5
                Chr2 = split_line[5]                                                                            # 6
                Pos2 = split_line[6]                                                                            # 7
                Strand2 = split_line[7]                                                                         # 8
                Chim_value = split_line[8]                                                                      # 9
                Spanning_junction = split_line[9]                                                               # 10
                Spanning_PE = split_line[10]                                                                    # 11
                Class = split_line[11]                                                                          # 12
                
                Comments = split_line[12]                                                                       # 
                Pseudogene = 'NA'
                Anchored_chimera = 'NA' 
                PE_chimera = 'NA'
                StringencyTest = 'NA'
                Fusion_distance = 'NA'
                GSNAP_mapped_reads = GSNAP_total_reads = GSNAP_ratio = 'NA'
                for v in Comments.split(','):
                    if 'pseudogene' in v: Pseudogene = 'pseudogene'                                             # 13
                    if 'chimera_anchored' in v: Anchored_chimera = 'anchored'                                   # 14
                    if 'strange_paired_end_support' in v: PE_chimera = 'strange_paired_end_support'             # 15
                    if 'low_support' in  v:
                        StringencyTest = 'low_support'                                                          # 16
                    elif 'high_support' in v:
                        StringencyTest = 'high_support'
                    if 'short_distance' in v:                                                                   # 17
                        Fusion_distance = v.split('=')[1]
                    if 'GSNAPMapping' in v:
                        GSNAP_mapped_reads = v.split('=')[1].split()[0][1:].rstrip("'")                         # 18
                        GSNAP_total_reads = v.split('=')[1].split()[-1][:-1].rstrip("'")                        # 19
                        GSNAP_ratio = str(int(GSNAP_mapped_reads) / int(GSNAP_total_reads))                     # 20
                mRNA_IDs = split_line[13].split('=')[1]                                                         # 21
                Annotation_type = split_line[14].split('=')[1]                                                  # 22
                Description_genes = split_line[15].split('=')[1]                                                # 23
                Exon_IDs = split_line[16].split('=')[1]                                                         # 24
                Exon_end_distance = split_line[17]
                Exon1_end_distance = Exon_end_distance.split('=')[1].split('---')[0]                            # 25
                Exon2_end_distance = Exon_end_distance.split('=')[1].split('---')[1]                            # 26
                Exon_rank = split_line[18]                  
                Exon1_rank = Exon_rank.split('=')[1].split('---')[0]                                            # 27
                Exon2_rank = Exon_rank.split('=')[1].split('---')[1]                                            # 28
                Read_id = split_line[19].split('=')[1]                                                          # 29
                Pos_junction = split_line[20].split('=')[1]                                                     # 30
                Read_seq = split_line[21].split('=')[1]                                                         # 31
                Profil_support = split_line[22].split('=')[1]                                                   # 32
                Profil_location = split_line[23].split('=')[1]                                                  # 33
                Nb_spanning_reads = split_line[24].split('=')[1]                                                # 34
                Nb_spanning_PE = split_line[25].split('=')[1]                                                   # 35
                Primers = split_line[26].split('=')[1].rstrip()                                                 # 36
                # print all line's fields
                print(Id, Name, Chr1, Pos1, Strand1, Chr2, Pos2, Strand2, Chim_value, Spanning_junction, Spanning_PE, 
                Class, Pseudogene, Anchored_chimera, PE_chimera, StringencyTest, Fusion_distance, GSNAP_mapped_reads, 
                GSNAP_total_reads, GSNAP_ratio, mRNA_IDs, Annotation_type, Description_genes, Exon_IDs, 
                Exon1_end_distance, Exon2_end_distance, Exon1_rank, Exon2_rank, Read_id, Pos_junction, Read_seq, 
                Profil_support, Profil_location, Nb_spanning_reads, Nb_spanning_PE, Primers, sep='\t')
   

def usage(appname):
    # https://docs.python.org/3/howto/argparse.html?highlight=argparse
    # add a sub-name in --help (like: bio2mtools sub-name options) when command not in standalone
    # and delete sub-name in sys.args (to avoid confusions with arguments)
    subname = ""
    if not __appname__ in sys.argv[0] and __appname__ in sys.argv[1]:
        subname = "{}".format(__appname__)
        del sys.argv[1]
    
    usage = ('\r{}\n{}.'                            # \r{} to replace the header 'usage:'
            '\nVersion: {}\n\n'                     # version number
            ' usage: %(prog)s {} options'           # usage : prog [sub-name] options...
            .format(''.ljust(len('usage:')), __shortdesc__, __version__, subname)
    )    
    parser = argparse.ArgumentParser(usage=usage)
    ### OPTION
    parser.add_argument("tsvfiles",                          # mandatory positional argument
                        help = 'mandatory files (one or more)',          # help text
                        nargs = 1,                        # argument options number
                        metavar = ("tsvfile1 ..."),     # option name to display
                        )
    ### VERSIONNING
    parser.add_argument('-v', '--version',              # positional argument
                        action='version',               # action "version" is executed and programm stop
                        version="%(prog)s version: {}".format(__version__)  # the action "version"
                        )
    ### Go to "usage()" without arguments
    if len(sys.argv) == 1: # or (__appname__ != appname and len(sys.argv) == 2):
        parser.print_help()
        sys.exit(1)
    return parser.parse_args(), subname

def main(appname):
    # manage argument
    args, module = usage(appname)
    # for each chimct file, parse file
    for tsv_file in args.tsvfiles:
        parseTSVfile(tsv_file)

if __name__ == "__main__":
    main(__appname__)
