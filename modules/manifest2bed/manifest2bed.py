#!/usr/bin/env python3
# -*- coding:utf8 -*-

"""
A partir du fichier "Manifest" fournit par Illumina, je vais faire un fichier bed.

1. récuperer la partie [Targets]
--------------------------------
Le fichier contient 3 sections, header, probes et targets.
J'ai découpé le fichier en deux fichiers "PROBES" et "TARGETS"

Section [Probes]
- cat TruSeq_CAT_Manifest_TC0081897-CAT_PROBES.txt | awk -F"\t" '{ print $6 "\t" $7 "\t" $8 "\t" $1 "\t0\t" $9 }' > TruSeq_CAT_Manifest_TC0081897-CAT_PROBES.bed

2. Récupérer les champs 4, 5, 6, 1, 7 (en mettant un 0 au score)
----------------------------------------------------------------
A priori, plutôt récupérer la section [Targets]

Section [Targets]
- cat TruSeq_CAT_Manifest_TC0081897-CAT_TARGETS.txt | awk -F"\t" '{ print $4 "\t" $5 "\t" $6 "\t" $1 "\t0\t" $7 }' | tr -s " " "_" > TruSeq_CAT_Manifest_TC0081897-CAT_TARGETS.bed

3. Regrouper 
------------
	* regrouper les lignes par le champs name ($1) jusqu'à la parenthèse (mais pas le dernier nombre), 
	* en prenant le + petit "start" et la plus grand "End"
	* et en enlevant du nom le dernier nombre
"""


__appname = "manifest2bed"
__shortdesc = "Translate Illumina manifest to BED file."
__licence = "none"
__version = "0.1"
__author = "Benoit Guibert <benoit.guibert@free.fr>"

def helpme(parent):											# required
	print("\nUsage:	{} {} <manifest file> <output.bed>\n".format(parent, __appname))

def args_ck(parent, args):
	if len(args) != 3:
		helpme(parent)
		sys.exit()

def main(parent, args):
	args_ck(parent, args)
	print("Work in progress...")

if __name__ == "__main__":
	main(parent, sys.argv)
