
## global

* La liste des modules est un peu lente à afficher -> une autre solution ?
* Évaluer la possibiliter de parser un fichier d'emblée dans le template
* Ajouter à la création d'une nouvelle app 4 fichiers (sur la racine de l'app)
    - TODO.md
    - CHANGELOG.md (avec une section v0.1, avec la date et une ligne indiquant la création)
    - README.md
    - licence
* Créer une nouvelle variable globale pour catégoriser les app avec --help
* BUG : si on ajoute un module qui a un nom de commande linux, on a des trucs bizarres (test, ls)
    * tester si la nouvelle app correspond à une commande bash
* Sortir le manager des modules
    * cela permet de supprimer 'manager' pour ne conserver que '-a --add', '-d --del', '-c --completion'
    * En créant un répertoire lib et en mettant le manager dedans ??
    * modifier le --help pour s'adapter 
* créer une option --todo (qui affiche le contenu du TODO.md, ou qui le lance dans un éditeur) 
* créer une option --changelog ( qui affiche le contenu de CHANGELOG.md, ou qui le lance dans un éditeur)
* créer une option --readme  (qui affiche le contenu de READE.md)


## manager

### Fonction writeApp()
- vérifier les droits d'écriture dans le répertoire 'modules'  
    - sinon, abandonner  

