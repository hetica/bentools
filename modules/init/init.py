#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Create a new app for bentools (also it can run autonomously)
"""

import sys, os												# required

__appname = "init"											# required
__licence = "none"
__version = "0.1"
__author = "Benoit Guibert <benoit.guibert@free.fr>"
__shortdesc = "Create a new app for bentools"
__opts = []

def content(appname, shortdesc):
	newappcontent = """#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, os

__appname = "{app}"
__licence = "none"
__version = "0.1"
__author = "Benoit Guibert <benoit.guibert@free.fr>"
__shortdesc = "{desc}"

def main(parent, args):
	del args[0]
	argsChk(parent, args)
	print("App: ", parent)
	print("Arguments:")
	for a in args:
		print(" " + a)
	print("Work in progress...")

def argsChk(parent, args):
	if "-h" in args:
		__opts.append("-h")
		args.remove("-h")
		helpme(parent)
	if len(args) < 1:
		helpme(parent)
		sys.exit()

def helpme(parent):
	print("\n{}\n".format(__shortdesc))
	if parent == __appname:
		print("{eol}Usage:	{par} [options] <arguments{eol}".format(__appname))
	else:	
		print("{eol}Usage:	{par} {par} [options] <arguments{eol}".format(parent, __appname))

if __name__ == "__main__":
	main(__appname, sys.argv)
""".format(app=appname,desc=shortdesc, par="{}", eol="\\n" )
	return newappcontent

def writeApp(appname, parent, shortdesc):
	# trouver l'emplacement de l'application parent
	modulesdir = (os.path.dirname((os.path.dirname(__file__))))
	# vérifier les droits d'écriture dans le répertoire
	# ...
	parentdir = os.path.dirname(modulesdir)
	# copier l'app dans <parent>/modules/<app>/<app.py>
	appdir = modulesdir + "/" + appname
	appfull = modulesdir + "/" + appname + "/" + appname + ".py"
	if os.path.isdir(appdir):
		print("\n Module '{}' still exists, abort...".format(appname))
		print(" Remove '{}' directory to continue\n".format(appdir))
		sys.exit()
	os.mkdir(appdir)
	with open( appfull, "w") as fic:
		contenu = fic.write(content(appname, shortdesc))
	st = os.stat(appfull)
	os.chmod(appfull, st.st_mode | 0o111)

	# modifier le fichier <parent>/bash_completion.d/bentools
	
	# si root ou sudo, écraer le /etc/bash_completion.d/bentools
	# recharger le fichier /etc/bash_completion.d/bentools
	# Afficher un message indiquant où se trouve l'app
	print("\nLe module {} à été créé".format(appname))
	print("Dans le répertoire {}".format(appdir))
	print("\nIl reste à modifier le /etc/path_completion/{} pour l'autocompletion".format(parent))

def argsChk(parent, args):
	"""checks arguments"""
	if "-h" in args:
		__opts.append("-h")
		args.remove("-h")
		helpme(parent)
	if len(args) != 1:
		helpme(parent)
		sys.exit()

def helpme(parent):											# required
	print("\n{}\n".format(__shortdesc))
	if parent == __appname:
		print("\nUsage:	{} <name_of_new_app>\n".format(__appname))
	else:	
		print("\nUsage:	{} {} <name_of_new_app>\n".format(parent, __appname))


def main(parent, args):										# required
	del args[0]												# avoid app name
	argsChk(parent, args)
	print("App: ", parent)
	print("Arguments:")
	for a in args:
		print(" " + a)
	print("Work in progress...")
	shortdesc="Description de l'app" # demander la description courte
	writeApp(args[0], parent, shortdesc)
	#print(content(args[0], shortdesc))


if __name__ == "__main__":
	main(__appname, sys.argv)								# required



