# P4_chess_tournament

DESCRIPTION

Projet 4 du parcours OpenClassrooms "Developpeur d'appli Python" : réalisation d'un programme, hors ligne, de gestion de tournois d'échecs.
L'utilisateur peut créer un tournoi, ajouter des joueurs, lancer un tour, le clôturer, saisir les scores des joueurs, mettre à jour le classement, consulter quelques statistiques et sauvegarder le programme à partir du menu ainsi qu'entre 2 actions de sa part.

PREALABLES & DEROULEMENT

Avertissement : Les scripts ont été créés et testés dans un environnement Windows, avec Python3.10.0, 
pip 22.0.3, flake8 v.4.0.1 et son plugin flake8-html (v 0.4.1)
Les commandes suivantes peuvent différer selon votre propre environnement.

Pour commencer, ouvrir un terminal de commande (Git Bash, par exemple).

Créer le répertoire de travail (commande : mkdir) qui accueillera les scripts Python.

Puis créer un environnement virtuel à la racine du répertoire de travail (python -m venv env).

Initialiser Git dans le répertoire de travail (git init).

Charger, dans votre répertoire de travail, les fichiers déposés sur GitHub 
(lien : https://github.com/RVLdev/P4_chess_tournament.git) :
- .init
- p4_interface.py
- setup.cfg
- dossier controllers
- dossier models
- dossier views
- dossier flake8_rapport

Activer l'environnement virtuel (. env/Scripts/activate - sous Windows).

Lancer l'interface (python p4_interface.py). Le menu du gestionnaire s'affiche.

L'utilisateur lance/effectue une action en saisissant le numéro correspondant.

Pour le stockage/la sauvegarde, le programme génère des fichiers .json, à la racine du projet.

La dernière option du menu permet de quitter le programme de gestion de tournois d'échecs.

Désactiver l'environnement virtuel (deactivate).

Peluchage du code
-----------------
Installer flake8 puis flake8-html (pip install) dans le répertoire du projet.

Le fichier setup.cfg configure flake8 afin de générer un rapport html dans un répertoire nommé flake8_rapport.
Un exemple est fourni dans les pièces déposées sur GitHub.

Remarque : chaque nouveau rapport écrase le précédent. 

Pour conserver l'exemple, dans le fichier de configuration renommez le répertoire destinataire (htmldir = nouveau_nom_du_repertoire), avant de lancer un nouveau rapport.

Pour créer un rapport, toujours à la racine du projet, tapez :  flake8

Dans le dossier destinataire (flake8_rapport, si vous ne l'avez pas renommé), ouvrez le fichier index.html.
