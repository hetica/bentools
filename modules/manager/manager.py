#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Manage modules
"""

import sys, os
import time
import grp
#from subprocess import Popen, PIPE
from pathlib import Path
import shutil
from getpass import getpass

__appname__ = "init"
__licence__ = "none"
__version__ = "0.1"
__author__ = "Benoit Guibert <benoit.guibert@free.fr>"
__shortdesc__ = "Manage {} modules".format(sys.argv[0].split('/')[-1])
__opts__ = []


def autocomplete (parent):
    ### Build autocompletion file
    module_path = "/".join(os.path.realpath(__file__).split('/')[:-2])
    modules = " ".join(os.listdir(module_path))

    # content of autocompletion file
    """ Function doc """
    content = """# Build by {parent} to uodate module completion
_{parent}()
{op}
  local cur prev opts
  COMPREPLY=()
  cur="${op}COMP_WORDS[COMP_CWORD]{cp}"
  prev="${op}COMP_WORDS[COMP_CWORD-1]{cp}"
  opts="{modules}"

  case $prev in
      {parent})
          COMPREPLY=( $(compgen -W "${op}opts{cp}" -- ${op}cur{cp}) )
          ;;
  esac
  return 0  
{cp}
complete -F _{parent} -o default {parent}
    """.format(parent=parent, modules=modules, op='{', cp='}')

    ### check if bash_completion is here
    autocomplete_dir = str(Path.home()) + '/.bashrc.d'
    if not os.path.exists(autocomplete_dir):
        os.makedirs(autocomplete_dir)
    
    ### Modify .bashrc if not entry
    bashrc_file = str(Path.home()) + '/.bashrc'
    keyword = '.bashrc.d/' + parent + '_completion'
    print(keyword)
    bashrc_new_header = "\n# build by {parent}, do not change it!\n".format(parent=parent)
    bashrc_new_body = "[ -d $HOME/.bashrc.d ] && source $HOME/.bashrc.d/{parent}_completion\n".format(parent=parent)
    with open( bashrc_file, 'r+') as stream:
        bashrc = stream.read()
        if not keyword in bashrc:
            stream.write(bashrc_new_header + bashrc_new_body)
        
    ### Write completion file
    bold = '\033[1m'
    end = '\033[0m'
    completion_file = autocomplete_dir + '/' + parent + '_completion'
    with open(completion_file, 'w') as file: 
        file.write(content)
        print('\nPlease execute :\n{bold}source {comp_file}{end}\nto refresh {parent} completion\n'.
                    format(comp_file=completion_file, parent=parent, bold=bold, end=end))
    

def appContent(parent, appname, shortdesc):
    newappcontent = """#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, os
import argparse

__appname__   = "{app}"
__licence__   = "none"
__version__   = "0.1"
__date__      = '{date}'
__modified__  = '{date}'
__author__    = "John Doe <john.doe@exemple.com>"
__shortdesc__ = "{desc}"


def usage(appname):
    # https://docs.python.org/3/howto/argparse.html?highlight=argparse
    # add a sub-name in --help (like: {parent} sub-name options) when command not in standalone
    # and delete sub-name in sys.args (to avoid confusions with arguments)
    subname = ""
    if not __appname__ in sys.argv[0] and __appname__ in sys.argv[1]:
        subname = "{par}".format(__appname__)
        del sys.argv[1]
    
    usage = ('{ret}{par}{nwl}{par}.'                            # {ret}{par} to replace the header 'usage:'
            '{nwl}Version: {par}{nwl}{nwl}'                     # version number
            ' usage: %(prog)s {par} options'           # usage : prog [sub-name] options...
            .format(''.ljust(len('usage:')), __shortdesc__, __version__, subname)
    )    
    parser = argparse.ArgumentParser(usage=usage)
    ### OPTION
    parser.add_argument("option1",                          # mandatory positional argument
                        help = 'mandatory file (one or more)',          # help text
                        nargs = "+",                        # argument options number
                        metavar = ("file_1 [file_n]"),     # option name to display
                        )
    ### ARGUMENT WITH OPTION
    parser.add_argument("-g", "--genome",
                        help = "reference genome (fasta file)",
                        metavar = 'genome',
                        nargs = 1,
                        required = True,
                        )
    ### ARGUMENT WITHOUT OPTION
    parser.add_argument('--verbose',                    # positional argument
                        action = "store_true",          # argument doesn't need option, i.e. tag
                        help = "Increase volubility",
                        )
    ### ARGUMENT WITH PREDEFINED OPTION
    parser.add_argument("-n", "--number",               # positional argument
                        type = int,                     # must be an integer
                        choices = [1,2,3],              # between 1 and 3
                        help = "a number from 1 to 3",
                        )
    ### VERSIONNING
    parser.add_argument('-v', '--version',              # positional argument
                        action='version',               # action "version" is executed and programm stop
                        version="%(prog)s version: {par}".format(__version__)  # the action "version"
                        )
    ### Go to "usage()" without arguments
    if len(sys.argv) == 1: # or (__appname__ != appname and len(sys.argv) == 2):
        parser.print_help()
        sys.exit(1)
    return parser.parse_args(), subname

def main(appname):
    args, module = usage(appname)
    print("Application: ", appname, module)
    print(args)
    print("Work in progress...")

if __name__ == "__main__":
    main(__appname__)
""".format(date=time.strftime('%Y-%m-%d') , parent=parent, app=appname,desc=shortdesc, par="{}", nwl="\\n", ret="\\r", tab="\\t" )
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
        fic.write(appContent(parent, appname, shortdesc))
    st = os.stat(appfull)
    os.chmod(appfull, st.st_mode | 0o111)
    
    # modifier le fichier <parent>/bash_completion.d/bentools
    
    # si root ou sudo, écraer le /etc/bash_completion.d/bentools
    # recharger le fichier /etc/bash_completion.d/bentools
    # Afficher un message indiquant où se trouve l'app
    print("\nModule {} has been created in directory {}".format(appname, appdir))
    return True


def deleteApp (appname, parent, shortdesc):
    """ Function doc """
    # trouver l'emplacement de l'application parent
    modulesdir = (os.path.dirname((os.path.dirname(__file__))))
    # vérifier les droits d'écriture dans le répertoire
    # ...
    parentdir = os.path.dirname(modulesdir)
    # copier l'app dans <parent>/modules/<app>/<app.py>
    appdir = modulesdir + "/" + appname
    if not os.path.isdir(appdir):
        print("\n Module '{}' not found, abort...\n".format(appname))
        sys.exit()
    shutil.rmtree(appdir)
    print('\nModule {} has been deleted'.format(appname))
    return True
    

def argsChk(parent):
    args = sys.argv[1:] if __appname__ in sys.argv[0] else sys.argv[2:]
    """checks arguments"""
    if "-h" in args:
        __opts__.append("-h")
        args.remove("-h")
        helpme(parent)
    try:
        if '--add' in args:
            ind = args.index('--add')
            return { 'type':'add', 'name': args[ind+1]}
        if '--del' in args:
            ind = args.index('--del')
            return { 'type':'del', 'name': args[ind+1]}
        if '--comp' in args:
            ind = args.index('--comp')
            return { 'type':'complete'}
    except IndexError:
        helpme(parent)
    if len(args) != 2:
        helpme(parent)
    return[args[0]]
        

def helpme(parent):
    print("\n{}\n".format(__shortdesc__))
    if parent == __appname__:
        print("Usage:")
        print("\t{} --add <app_name>\t: append a new app".format(__appname__))
        print("\t{} --del <app_name>\t: delete an app".format(__appname__))
        print("\t{} --comp\t\t\t: update auto-completion\n".format(__appname__))
    else:   
        print("Usage:")
        print("\t{} {} --add <app_name>\t: append a new app".format(parent, __appname__))
        print("\t{} {} --del <app_name>\t: delete an app".format(parent, __appname__))
        print("\t{} {} --comp\t\t\t: update auto-completion\n".format(parent, __appname__))
    sys.exit()


def main(parent):
    args = argsChk(parent)
    shortdesc="short app description"               # TODO : ask for short description
    complete_ok = False                                   # to autocomplete
    if args['type'] == 'add':
        complete_ok = writeApp(args['name'], parent, shortdesc)
    if args['type'] == 'del':
        complete_ok = deleteApp(args['name'], parent, shortdesc)
    if args['type'] == 'complete':
        complete_ok = True
    if complete_ok: autocomplete(parent)


if __name__ == "__main__":
    main(__appname__)                               # required


