#!/usr/bin/env python3
# -*- coding:utf8 -*-

__appname__     = "filestats"
__shortdesc__   = "Return statistics from gtf or bed file"
__licence__     = "GPL"
__version__     = "0.1"
__author__      = "Benoit Guibert <benoit.guibert@free.fr>"

import sys
import argparse

def main():
    args = usage()
    for file in args.file:
        ftype = filetype_is(file)
        if ftype == "bed":
            stats = bed_stats(file)
            show_bed_stats(stats)
        elif ftype == "gtf":
            chrs, totals_per_type, types = gtf_stats(file)
            show_gtf_result(chrs, totals_per_type, types)
        else:
            print("\nFile format unrecognized\n")
            usage()
        

def usage():
    # https://docs.python.org/3/howto/argparse.html?highlight=argparse
    usage = ('\r{}\n{}.'               # \r{} to replace the header 'usage:'
            '\nVersion: {}\n\n'                      # version number
            '{}{} usage: %(prog)s <file>{}'           # usage
            .format(''.ljust(len('usage:')), __shortdesc__, __version__, bcolors.GREEN, bcolors.BOLD, bcolors.END)
    )
    parser = argparse.ArgumentParser(usage=usage)
    ## Or by description
    # desc = '{} (version: {})'.format(__shortdesc__, __version__)
    # parser = argparse.ArgumentParser(description=desc)
    ### OPTION
    parser.add_argument("file",                         # argument positionnel obligatoire
                        help = "gtf or bed file",       # texte d'aide
                        nargs = 1,                      # nombre d'options pour l'argument
                        metavar = ('<file>'),           # nom de l'option à afficher
                        )
    parser.add_argument('-v', '--version',              # argument optionnel
                        action='version',               # l'action "version" est exécuté et le programme sort
                        version="%(prog)s version: {}".format(__version__)  # l'action "version"
                        )
    ### Go to "usage()" without arguments
    if len(sys.argv)==1:
        parser.print_help()
        sys.exit(1)
    return parser.parse_args()


def is_gtf_ok(file):
    return True


def filetype_is(file):
    return file.split('.')[-1]


def gtf_stats(file):
    types = []                          # types : transcript, exon, etc.
    chrs = {}                           # chromosomes : '2', 'X'
    totals_per_type = {}                # min, max, total seq lenght, number of sequences, mean seq lenght
    seq_number = 0
    seq_per_chr = []
    current_chrom = ''
    with open(file) as stream:
        for line in stream:
            if line[0] != '#':
                sline = line.split()
                chr = sline[0]
                type = sline[2]
                len_seq = int(sline[4]) - int(sline[3]) + 1
                # build summary, chromosome by chromosome
                if not chr in chrs:
                    chrs[chr] = {type: [ len_seq, len_seq, len_seq, 1]}
                    if not type in types:
                        types.append(type)
                else:
                    if not type in chrs[chr]:
                        chrs[chr][type] = [ len_seq, len_seq, len_seq, 1]
                        if not type in types:
                            types.append(type)
                    else:
                        # count by chr/type
                        if type in chrs[chr]:
                            # shortest seq
                            if len_seq < chrs[chr][type][0]:
                                chrs[chr][type][0] = len_seq
                            # longest seq
                            if len_seq > chrs[chr][type][1]:
                                chrs[chr][type][1] = len_seq
                            # total length seq
                            chrs[chr][type][2] = chrs[chr][type][2] + len_seq
                            # count of seq
                            chrs[chr][type][3] += 1
    

    # compute means for each chromosomes (by types)
    for chr in chrs.keys():
        for type, values in chrs[chr].items():
            chrs[chr][type].append(values[2] // values[3])
            #print(chr, ":", type, ":", values)

    # compute totals for each type
    for type in types:
        totals_per_type[type] = [0, 0, 0, 0, 0]
        for chr in chrs:
            # min sequence lenght by type
            if type in chrs[chr]:
                if chrs[chr][type][0] < totals_per_type[type][0] or totals_per_type[type][0] == 0:
                    totals_per_type[type][0] = chrs[chr][type][0]
                # max sequence lenght by type
                if chrs[chr][type][1] > totals_per_type[type][1]:
                    totals_per_type[type][1] = chrs[chr][type][1]
                # total lenght by type
                totals_per_type[type][2] += chrs[chr][type][2]
                # number of sequences by type
                totals_per_type[type][3] += chrs[chr][type][3]
        # mean of sequence length by type
        totals_per_type[type][4] = totals_per_type[type][2] // totals_per_type[type][3]
    # print(chrs)    
    # print (totals_per_type)
    stats = (chrs, totals_per_type, types)
    return stats


def show_gtf_result(chrs, totals, types):
    # header
    lines = build_header()
    # columns header
    lines += '#\t{}\n'.format('\t\t\t\t\t'.join(types))
    lines += '#chr{}\n'.format('\tmin\tmax\ttotal\tnumber\tmean' * len(types))
    #print(lines)
    # chromosomes data
    for i in range(1, 40):
        if str(i) in chrs:
            lines += str(i)
            for type in types:
                if not type in chrs[str(i)]:
                    chrs[str(i)][type] = ['', '', '', '', '']
                lines += '\t{}'.format('\t'.join(map(str, chrs[str(i)][type])))
            lines += '\n'
    if 'X' in chrs:
        lines += 'X'
        for type in types:
            if not type in chrs['X']:
                chrs['X'][type] = ['', '', '', '', '']
            lines += '\t{}'.format('\t'.join(map(str, chrs['X'][type])))
        lines += '\n'
    if 'Y' in chrs:
        lines += 'Y'
        for type in types:
            if not type in chrs['Y']:
                chrs['Y'][type] = ['', '', '', '', '']
            lines += '\t{}'.format('\t'.join(map(str, chrs['Y'][type])))
        lines += '\n'
    if 'M' in chrs:
        lines += 'M'
        for type in types:
            if not type in chrs['M']:
                chrs['M'][type] = ['', '', '', '', '']
            lines += '\t{}'.format('\t'.join(map(str, chrs['M'][type])))
        lines += '\n'
    lines += 'Totals'
    for type in types:
        lines += '\t{}'.format('\t'.join(map(str,totals[type])))
    print(lines)

    
def bed_stats(file):
    stats = {}
    with open(file) as stream:
        for line in stream:
            sline = line.split()
            if line[0] != '#':
                chr = sline[0]
                start = int(sline[1])
                end = int(sline[2])
                len_seq = end - start
                if chr not in stats:
                    stats[sline[0]] = [ len_seq, len_seq, len_seq, 1 ]
                else:
                    # min len for chromosome
                    if len_seq < stats[chr][0]:
                        stats[chr][0] = len_seq
                    # max lenght for chromosome
                    if len_seq > stats[chr][1]:
                        stats[chr][1] = len_seq
                    # total sequence lenght for chromosome
                    stats[chr][2] += len_seq
                    # sequence number for chromosome
                    stats[chr][3] += 1
                
    # compute means
    for chr, values in stats.items():
        stats[chr].append(values[2] // values[3])
    # compute totals
    totals = [0, 0, 0, 0, 0]
    for chr in stats:
        # min of all min sequences
        if stats[chr][0] < totals[0] or totals[0] == 0:
            totals[0] = stats[chr][0]
        # max of all max sequences
        if stats[chr][1] > totals[1]:
            totals[1] = stats[chr][1]
        # total lenght of all sequences
        totals[2] += stats[chr][2]
        # total of all sequences
        totals[3] += stats[chr][3]
        # mean of all sequence lenght
        totals[4] = totals[2] // totals[3]
    stats["totals"] = totals
    return stats


def show_bed_stats(stats):
    lines = build_header()
    lines += '#chr' + '\tmin\tmax\ttotal\tnumber\tmean\n'
    for i in range(1, 30):
        if str(i) in stats:
            lines += str(i)
            lines += '\t{}\n'.format('\t'.join(map(str, stats[str(i)])))
    if 'X' in stats:
        lines += 'X'
        lines += '\t{}\n'.format('\t'.join(map(str, stats['X'])))
    if 'Y' in stats:
        lines += 'Y'
        lines += '\t{}\n'.format('\t'.join(map(str, stats['Y'])))
    if 'M' in stats:
        lines += 'M'
        lines += '\t{}\n'.format('\t'.join(map(str, stats['M'])))
    if 'totals' in stats:
        lines += 'Totals'
        lines += '\t{}\n'.format('\t'.join(map(str, stats['totals'])))
    print(lines)


def build_header():
    # build header
    header = (
            "# {} version: {}\n"
            "# Command: {}\n"
            "# min: min sequence length\n"
            "# max: max sequence length\n"
            "# total: total length of sequences\n"
            "# number: number of sequences\n"
            "# mean: average of sequence length\n"
            .format(__appname__, __version__, ' '.join(sys.argv))
    )
    return header


class bcolors:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


if __name__ == "__main__":
    main()
    
