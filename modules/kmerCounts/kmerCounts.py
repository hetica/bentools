#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, os
import argparse
import gzip
from collections import defaultdict

__appname__   = "kmerCounts"
__licence__   = "none"
__version__   = "0.1"
__date__      = '2019-11-18'
__modified__  = '2019-11-18'
__author__    = "Benoit Guibert <benoit.guibert@free.fr>"
__shortdesc__ = "kmerCounts Count abundance of kmers of a single sequence in fastq file."


ALPHABET = {'A':'T','T':'A','G':'C','C':'G','a':'t','t':'a','c':'g','g':'c','N':'N','n':'n'}

def usage(appname):
    # https://docs.python.org/3/howto/argparse.html?highlight=argparse
    # add a sub-name in --help (like: bentools sub-name options) when command not in standalone
    # and delete sub-name in sys.args (to avoid confusions with arguments)
    subname = ""
    if not __appname__ in sys.argv[0] and __appname__ in sys.argv[1]:
        subname = "{}".format(__appname__)
        del sys.argv[1]

    usage = ('\r{}\n{}.'                            # \r{} to replace the header 'usage:'
            '\nVersion: {}\n\n'                     # version number
            'usage: %(prog)s {} options'           # usage : prog [sub-name] options...
            .format(''.ljust(len('usage:')), __shortdesc__, __version__, subname)
    )
    parser = argparse.ArgumentParser(usage=usage)
    ### OPTION
    parser.add_argument("seq",                          # mandatory positional argument
                        help = 'sequence',          # help text
                        metavar = "sequence",     # option name to display
                        )
    parser.add_argument("fastq",                          # mandatory positional argument
                        help = 'fastq',          # help text
                        metavar = "fastq_file",     # option name to display
                        )
    ### ARGUMENT WITH OPTION
    parser.add_argument("-s", "--straight",
                        help = "just straight, no reverse complement",
                        action = "store_true",
                        )
    ### ARGUMENT WITHOUT OPTION
    parser.add_argument('-d', '--debug',                    # positional argument
                        action = "store_true",          # argument doesn't need option, i.e. tag
                        help = "Increase volubility",
                        )
    ### ARGUMENT WITH PREDEFINED OPTION
    parser.add_argument("-k", "--kmer",
                        type = int,
                        default = 31,
                        help = "kmer length (default: 31)",
                        metavar = 'int',
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
    args, module = usage(appname)
    kmer = Kmer(args)
    kmer.show_res()


class Kmer:
    """ Class doc """

    def __init__(self, args):
        """ Class initialiser """
        self.seq = args.seq
        self.k = args.kmer
        self.debug = args.debug
        self.fastq = args.fastq
        self.straight = args.straight
        ### Check sequence
        self._check_seq()
        ### Count number of different kmer in sequence
        self.count = self._kmers_count()
        ### Compute abundance
        self.abundances = self._abundances()
        self.mean = None


    def _check_seq(self):
        """ Check characters in sequence """
        for char in self.seq:
            if char.upper() not in ALPHABET:
                sys.exit("ErrorSeq: not a valid sequence")

    def _kmers_count(self):
        """ How many kmer in this sequence ? """
        n_kmer = len(self.seq) - self.k + 1
        if n_kmer < 1:
            sys.exit("Sequence must be larger than length of kmer")
        else:
            return n_kmer

    def _abundances(self):
        """ Compute abundance using boyer-more algorithm """
        nline = 0
        abundances = defaultdict()
        try:
            with gzip.open(self.fastq, 'rt') as f:
                for line in f:
                    nline, abundances = self._count_abundances(line, nline, abundances)
        except OSError:
            with open(self.fastq) as f:
                for line in f:
                    nline, abundances =  self._count_abundances(line, nline, abundances)
        return abundances

    def _count_abundances(self, line, nline, abundances):
        if nline % 4 == 1:
            start = 0
            end = self.k
            for i in range(self.count):
                seq = self.seq[start:end]
                if seq in abundances:
                    abundances[seq] += boyer_moore_match(line.rstrip(), seq)
                else:
                    abundances[seq] = boyer_moore_match(line.rstrip(), seq)
                if not self.straight:
                    if seq in abundances:
                        abundances[seq] += boyer_moore_match(line.rstrip(), rev_comp(seq))
                    else:
                        abundances[seq] = boyer_moore_match(line.rstrip(), rev_comp(seq))
                start += 1
                end += 1
        nline += 1
        return nline, abundances

    def show_res(self):
        """ Show results """
        print("kmer: abundance")
        for k,v in self.abundances.items():
            print(f"  {k}: {v}")
        print(f"Total abundance: {sum(self.abundances.values())}")
        print(f"kmers in sequence: {self.count} (seq: {len(self.seq)}, k-mer: {self.k})")


def rev_comp(seq):
    return ''.join([{'A':'T','a':'t','C':'G','c':'g','G':'C','g':'c','T':'A','t':'a','N':'N','n':'n'}[B] for B in seq][::-1])


def boyer_moore_match(text, pattern):
    """Find occurrence of pattern in text."""
    abundance = 0
    last = last_occurrence(pattern, ALPHABET)
    m = len(pattern)
    n = len(text)
    i = m - 1  # text index
    j = m - 1  # pattern index
    while i < n:
        if text[i] == pattern[j]:
            if j == 0:
                abundance += 1
                l = last(text[i])
                i = i + m - min(j, 1+l)
                j = m - 1
            else:
                i -= 1
                j -= 1
        else:
            l = last(text[i])
            i = i + m - min(j, 1+l)
            j = m - 1
    return abundance


class last_occurrence(object):
    """Last occurrence functor."""

    def __init__(self, pattern, alphabet):
        """
        Generate a dictionary with the last occurrence of each alphabet
        letter inside the pattern.
        """
        self.occurrences = dict()
        for letter in alphabet:
            self.occurrences[letter] = pattern.rfind(letter)

    def __call__(self, letter):
        """
        Return last position of the specified letter inside the pattern.
        Return -1 if letter not found in pattern.
        """
        return self.occurrences[letter]


if __name__ == "__main__":
    main(__appname__)
