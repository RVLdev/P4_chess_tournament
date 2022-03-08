class InterfaceView:
    def __init__(self):
        pass

    @classmethod
    def launch_tournament(cls):
        """ launches the program's menu """
        print("--------\nBonjour, bienvenue dans le gestionnaire de tournois d'échecs")
        cls.display_startmenu()

    @classmethod
    def display_startmenu(cls):
        """ displays the menu """
        print('\nMENU :')
        print('1 TOURNOI : Créer un tournoi')
        print('2 TOURNOI : Afficher un tournoi')
        print('3 JOUEURS : Enregistrer un ou des joueurs dans la base')
        print('4 JOUEURS : Ajouter un joueur à un tournoi')
        print("5 JOUEURS : Mettre à jour le classement")
        print('6 TOUR : Lancer un tour')
        print('7 TOUR : Clôturer un tour')
        print('8 TOUR : Renseigner des scores')
        print('9 REPORTING')
        print('10 Sauvegarder - Charger')
        print('11 Quitter le programme')
        print('Que souhaitez-vous faire ?')

    @classmethod
    def ask_for_players_inclusion(cls):
        print("Voulez_vous ajouter 8 joueurs à ce tournoi (OUI/NON) ? ")

    @classmethod
    def display_add_one_player(cls):
        print("Ajout d'1 joueurs à un tournoi")

    @classmethod
    def ask_for_first_round_launch(cls):
        print('Voulez_vous lancer le 1er tour (OUI/NON)?')

    @classmethod
    def launch_round(cls):
        print('Voulez_vous lancer un tour (OUI/NON)? ')

    @classmethod
    def display_t_rounds_list_full(cls):
        print('Liste des joueurs du tournoi complète')

    @classmethod
    def this_round_closing(cls):
        print('Marquer ce tour comme étant terminé (OUI/NON) ?')

    @classmethod
    def end_round_before_start_new_one(cls):
        print('Vous devez terminer un tour,')
        print("avant de pouvoir en lancer un autre.")

    @classmethod
    def update_scores(cls):
        print('Voulez_vous mettre à jour les scores (OUI/NON) ?')

    @classmethod
    def request_ranking_update(cls):
        print('Mise à jour du classement : ')
        print('1 Classement des joueurs dans un tournoi')
        print('2 Classement général des joueurs')
        print('3 Revenir au menu')
        print('Saisissez 1, 2 ou 3 selon votre choix : ')

    @classmethod
    def request_global_rank_update(cls):
        print('Mettre à jour le classement général des joueurs (OUI/NON)? ')

    @classmethod
    def menu_reporting(cls):
        print('LISTE DES RAPPORTS :')
        print('Quel rapport souhaitez-vous afficher ?')
        print("1 Liste de tous joueurs")
        print("2 Liste de tous joueurs d'un tournoi")
        print("3 Liste de tous les tournois")
        print("4 Liste des tours ('rounds') d'un tournoi")
        print("5 Liste des matches d'un tournoi")

    @classmethod
    def save_or_load_menu(cls):
        print('Que souhaitez-vous faire ?')
        print('1 Sauvegarder')
        print('2 Charger une sauvegarde')

    @classmethod
    def program_saved(cls):
        print('Sauvegarde effectuée')

    @classmethod
    def backup_loaded(cls):
        print('Sauvegarde chargée')

    @classmethod
    def choice_unavailable(cls):
        print('*** Désolé, choix non disponible\n')

    @classmethod
    def exit_programm(cls):
        print('Voulez_vous quitter le programme (OUI/NON) ?')

    @classmethod
    def display_goodbye(cls):
        print('Au revoir')

    @classmethod
    def separator(cls):
        print('------------------------------------\n')
