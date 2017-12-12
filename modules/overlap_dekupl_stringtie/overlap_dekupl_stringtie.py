#!/usr/bin/env python3
# -*- coding:utf8 -*-

"""
TODO
- considere strand
"""

__appname__     = "overlap_dekupl_stringtie"
__shortdesc__   = "return dekupl contigs matching on stringtie transcripts."
__licence__     = "none"
__version__     = "0.6"
__date__        = '2017-11-22'
__modified__    = '2017-12-08'
__author__      = "Benoit Guibert <ben@hetica.fr>"

import os, sys
import argparse
import matplotlib.pyplot as plt
import numpy as np

FEATURES = ["transcript"]

def usage(appname):
    # https://docs.python.org/3/howto/argparse.html?highlight=argparse
    #parser = argparse.ArgumentParser()
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
    ### MANDATORY
    parser.add_argument("contigfile",
                        help = "file to overlapping (bed)",
                        metavar = ('file.bed'),
                        nargs = 1,
                        )
    parser.add_argument("gtfref",
                        help = "reference file (gtf)",
                        metavar = ('ref.gtf'),
                        nargs = 1,
                        )
    ### OUTPUT
    parser.add_argument('-o', '--output',
                        help = "output file name, default stdout",
                        metavar = ('file'),
                        nargs = 1
                        )
    ### EXPAND
    parser.add_argument('-e', '--expand',
                        help = "expand region in bp",
                        metavar = ('int'),
                        nargs = 1,
                        type = int,
                        )
    ### QUIET
    parser.add_argument('-q', '--quiet',
                        help = "doesn't show results",
                        action = 'store_true',
                        )
    ### GRAPH
    parser.add_argument('-g', '--graph',
                        help = "show graph",
                        action = "store_true",
                        )
    ### SUMMARY
    parser.add_argument('-s', '--stats',
                        help = "show stats",
                        action = "store_true",
                        )
    
    ### VERSIONNING
    parser.add_argument('-v', '--version',
                        action='version',
                        version="%(prog)s version {}".format(__version__)  # l'action "version"
                        )
    ### Go to "usage()" without arguments
    if len(sys.argv)==1:
        parser.print_help()
        sys.exit(1)
    return parser.parse_args()


def main(appname):
    # args = usage()
    args, subname = usage(appname)
    contigs_file = args.contigfile[0]
    ref_file = args.gtfref[0]
    ### check files
    check_files(contigs_file, ref_file)
    ### parse and set dict of gtf ref
    d_ref_file = ref_dict(ref_file, args.expand)
    #print(d_ref_file.content['18'])
    ### compute 
    res = CountByGenes(d_ref_file.content, contigs_file)
    #print(res.summary)
    ## print results in stdin or file
    res.setOutput(args.output, args.quiet, args.stats)
    ### show graph
    if args.graph:
        res.getGraph()
    ### Show summary
    if args.stats and not args.quiet:
        print(res.getSummary(d_ref_file.getSummary(res.count)))
    ### miscelanous tests
    # for a in res.getAll(): print(a)
    # print(res.getGene('MSTRG.2475'))    # ok
    # print(res.getGene('MSTRG.4695'))    # ok
    # print(res.getChromList(res.chr_list))
    # print(res.getOutput())
       
    
class CountByGenes:
    """ Class doc """
    count = {}
    chr_list = []
    summary = {}
    
    def __init__ (self, d_ref_file, contigs_file):
        """ Class initialiser """
        with open(contigs_file) as stream:
            for line in stream:
                #sys.stdout.write(line)
                chr, start, stop, seq, strand, *rest = line.split('\t')
                if chr in d_ref_file.keys():
                    contig_matched = False
                    for gene in d_ref_file[chr]:
                        if not chr in self.count:
                            self.count[chr] = {}
                        if int(start) < d_ref_file[chr][gene][0] and int(stop) >= d_ref_file[chr][gene][0]:
                            contig_matched = True
                            if not gene in self.count[chr]:
                                self.count[chr][gene] = {
                                            'count': 1,
                                            'start': d_ref_file[chr][gene][0],
                                            'stop' : d_ref_file[chr][gene][1],
                                            'score' : 0,
                                            'strand' : d_ref_file[chr][gene][2],
                                            'pos': [(start, stop)],
                                            }
                            else:
                                self.count[chr][gene]['count'] += 1
                                self.count[chr][gene]['pos'].append((start, stop))
                        elif int(start) <=  d_ref_file[chr][gene][1] and int(stop) > d_ref_file[chr][gene][0]:
                            contig_matched = True
                            if not gene in self.count[chr]:
                                self.count[chr][gene] = {
                                            'count': 1,
                                            'start': d_ref_file[chr][gene][0],
                                            'stop' : d_ref_file[chr][gene][1],
                                            'score' : '.',
                                            'strand' : d_ref_file[chr][gene][2],
                                            'pos': [(start, stop)],
                                            }
                            else:
                                self.count[chr][gene]['count'] += 1
                                self.count[chr][gene]['pos'].append((start, stop))
                    self.setSummary(chr, 1, 0) if contig_matched else self.setSummary(chr, 0, 1) 
                else: #if not chromosome in reference file
                    self.setSummary(chr, 0, 1) 
    
    def setSummary(self, chr, matched, unmatched):
        if chr in self.summary.keys():
            #self.summary[chr] =  [ x+y for x, y in zip(self.summary[contig[0]], contig[1:]) ]
            self.summary[chr][0] += matched
            self.summary[chr][1] += unmatched
        else:
            self.summary[chr] = [matched, unmatched]
            
    def getSummary(self, transcripts_stats):
        chr_list= []
        totals = [0, 0, 0, 0]
        # populize chr_list
        for chr in self.summary.keys():
            chr_list.append(chr)
        # ordered chr_list
        chr_list = self.getChromList(chr_list)
        ####################### DEV ############################
        #print(self.summary, '\t')
        #print(transcripts_stats)
        
        for chr in self.summary:
            if chr in transcripts_stats:
                [ self.summary[chr].append(i) for i in transcripts_stats[chr]]
            else:
                # if not this chromosome in transcripts, add a couple of 0
                self.summary[chr] += [0, 0]
                
        #print(self.summary, '\t')
        ##################### END DEV ##########################
        # header for print
        summary = "# CHR: Chromosome\n"
        summary += "# C_OK: Contigs Matched\n"
        summary += "# C_KO: Contigs Unmatched\n"
        summary += "# T_OK: Transcript containing Contigs\n"
        summary += "# T_KO: Transcript without Contigs\n"
        summary += "CHR\tC_OK\tC_KO\tT_OK\tT_KO"#\tPercent"
        
        for chr in chr_list:
            # append each results of chr_list for each chromosome
            summary += '\n{chr}\t{values}'.format(chr=chr, values='\t'.join([str(a) for a in self.summary[chr]]))                
            for i, v in enumerate(totals):
                #print(totals[i], self.summary[chr][i])
                totals[i] += self.summary[chr][i]
        summary += '\nTotal\t{}'.format('\t'.join([str(a) for a in totals]))
        return summary
    
    def getChromList(self, chr_list):
        digit = []
        alpha = []
        for i, v in enumerate(chr_list):
            if v.isdigit():
                digit.append(v)
            else:
                alpha.append(v)
        digit.sort(key=int)
        alpha.sort(key=str)
        return digit + alpha
    
    def getGene(self, gene):
        for chr in self.count.keys():
            if gene in self.count[chr].keys():
                return "{}\t{}\t{}\t{}\t{}\t{}\t{};{}".format(
                                    chr,
                                    self.count[chr][gene]['start'], 
                                    self.count[chr][gene]['stop'],
                                    gene,
                                    self.count[chr][gene]['score'],
                                    lf.count[chr][gene]['strand'],
                                    self.count[chr][gene]['count'],
                                    ",".join([ ":".join(map(str, i)) for i in self.count[chr][gene]['pos'] ])
                                    ) 
        return ("not found")
                                
    def getAll(self):
        return self.count.items()
        
    def getOutput(self):
        out = ''
        chr_list = []
        # Make chromosome sorted list
        for k in self.count.keys():
            chr_list.append(k)
        chr_list = self.getChromList(chr_list)
        # Make output
        for chr in chr_list:
            for gene, value in self.count[chr].items():
                out += ("{}\t{}\t{}\t{}\t{}\t{}\t{};{}\n".format(
                        chr, 
                        value['start'], 
                        value['stop'],
                        gene,
                        value['score'],
                        value['strand'], 
                        value['count'], 
                        ",".join([ ":".join(map(str, i)) for i in value['pos'] ])
                        ))
        return out

    def setOutput (self, output_file, quiet, stats):
        out = self.getOutput()
        if output_file:
            with open(output_file[0], 'w') as file:
                file.write(out)
        elif not quiet and not stats:
            print(out)
    
    def getGraph(self):
        genes = []
        nb = []
        for chr in self.count.items():
            for k,v in chr[1].items():
                genes.append(k)
                nb.append(v['count'])
        
        x_pos = np.arange(len(genes))
        plt.figure(figsize=(12,4.5))
        plt.subplots_adjust(left=0.1, right=0.92, top=0.92, bottom=0.12)
        #plt.scatter(x_pos, sorted(nb, reverse=True))
        #plt.plot(x_pos, sorted(nb, reverse=True))
        plt.bar(x_pos, sorted(nb, reverse=True), linewidth=0.18)
        plt.xlabel('Transcripts')
        plt.ylabel('Number of contigs per transcribed region')
        
        plt.savefig('barplot.png')
        plt.show()
        
    def getStats(self):
        pass
            

class ref_dict:
    """ Class doc """
    content = {}
    
    def __init__ (self, ref_file, expand):
        """ Class initialiser """
        # expand is to option "-e --expand"
        expand = expand[0] if expand else 0
        expand *= 1     # if I want apply a multiplier to expand
        start = {}
        with open(ref_file) as stream:
            for line in stream:
                chr, source, feature, start, end, score, strand, frame, attribute = line.split('\t')
                if feature in FEATURES:
                    start = max(0, int(start) - expand )
                    end = int(end) + expand
                    transcript_id = attribute.split(';')[1].split(' ')[2].replace('"','')
                    # create chr if new
                    if not chr in self.content:
                        self.content[chr] = {}
                    self.content[chr][transcript_id] = [ start, end, strand ]
    
    def getSummary(self, counts):
        # for chromosome in transcripts
        stats = {}
        for chr in self.content:
            if not chr in stats:
                stats[chr]= [0, 0] 
            # for transcript in transcripts
            for transcript in self.content[chr]:
                #print(transcript)
                # if transcript in contigs, add 1 in index 0
                if transcript in counts[chr]:
                    stats[chr][0] += 1
                else:       # add 1 in index 1
                    stats[chr][1] += 1
        return stats


def check_files(contigs_file, ref_file):
    # TODO : improve control for BED and GTF files
    if os.path.isfile(contigs_file):
        pass
    else:
        print('{} not a file'.format(contigs_file))
    
    if os.path.isfile(ref_file):
        pass
    else:
        print('{} not a file'.format(ref_file))
    
    
if __name__ == "__main__":
    main(__appname__)
