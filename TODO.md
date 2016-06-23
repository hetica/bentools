
## bentools

- n'afficher le module init que si l'utilisateur a les droits (trop comliqué ?)


## Module init

### Fonction writeApp()
- vérifier les droits d'écriture dans le répertoire 'modules'
	- sinon, abandonner
- Demander à saisir une description courte pour l'appli
- Modifier le fichier <parent>/bash_completion.d/bentools
- Si root ou sudo, écraer le /etc/bash_completion.d/bentools
- Recharger le fichier /etc/bash_completion.d/bentools
- Afficher un message indiquant que c'est fait et où se trouve l'app


## Module vcfstat

- Ajouter l'affichage par chromosomes (comme idxstat)
