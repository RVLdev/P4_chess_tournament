class InterfaceView:
    def __init__(self):
        pass

    @classmethod
    def launch_tournament(cls):
        """ launches the program's menu """
        print("Bonjour, bienvenue dans le gestionnaire de tournois d'échecs")
        cls.display_startmenu()

    @classmethod
    def display_startmenu(cls):
        """ displays the menu """
        print('\nMENU :')
        print('1 TOURNOI : Créer un tournoi')
        print('2 JOUEURS : Enregistrer un ou des joueurs')
        print('3 JOUEURS : Ajouter un joueur à un tournoi')
        print("4 JOUEURS : Mettre à jour le classement d'un joueur")
        print('5 TOUR : Lancer un tour')
        print('6 TOUR : Clôturer un tour')
        print('7 TOUR : Renseigner des scores')
        print('8 Reporting')
        print('9 Sauvegarder - Charger')
        print('0 Quitter le programme')
        print('Que souhaitez-vous faire ?')

    @classmethod
    def ask_for_players_inclusion(cls):
        print("Voulez_vous ajouter 8 joueurs à ce tournoi (O/N) ? ")

    @classmethod
    def ask_add_one_player(cls):
        print("Voulez_vous ajouter 1 joueurs à ce tournoi (O/N) ? ")

    @classmethod
    def ask_for_first_round_launch(cls):
        print('Voulez_vous lancer le 1er tour ?')

    @classmethod
    def launch_round(cls):
        print('Voulez_vous lancer un tour (O/N)? ')

    @classmethod
    def display_t_rounds_list_full(cls):
        print('Liste des joueurs du tournoi complète')

    @classmethod
    def this_round_closing(cls):
        print('Marquer ce tour comme étant terminé (O/N) ?')

    @classmethod
    def update_scores(cls):
        print('Voulez_vous mettre à jour les scores (O/N) ?')

    @classmethod
    def request_rank_update(cls):
        print('Voulez_vous mettre à jour le classement des joueurs ? O/N')

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
        print('Voulez_vous quitter le programme (O/N) ?')


class TournamentView:
    def __init__(self):
        pass

    @classmethod
    def ask_tournament_name(cls):
        print('Entrez le nom du tournoi : ')

    @classmethod
    def ask_tournament_place(cls):
        print('Entrez le lieu du tournoi : ')

    @classmethod
    def ask_tournament_date(cls):
        print('Entrez la date du tournoi au format JJ/MM/AAAA :')

    @classmethod
    def ask_tournament_description(cls):
        print('Saisissez les commentaires : ')

    @classmethod
    def ask_time_control(cls):
        print('saisissez bullet, blitz ou coup rapide : ')

    @classmethod
    def ask_tournament_rounds_qty(cls):
        print('Le nombre de tours par défaut est 4')
        print('Saisissez le nombre de tours souhaité : ')

    @classmethod
    def ask_for_new_tourney_players(cls):
        print("Tournoi en cours de création : Merci d'ajouter un joueur")

    @classmethod
    def ask_for_player_inclusion(cls):
        print("Voulez_vous ajouter des joueurs à ce tournoi (O/N) ? ")
        
    @classmethod
    def display_t_players_list_is_full(cls):   
        print('La liste des joueurs de ce tournoi est complète')

    @classmethod
    def display_rounds_list_full(cls):
        print('La liste des tours du tournoi est complète')

    @classmethod
    def end_tournament(cls):
        print('Tournoi terminé')

    @classmethod
    def display_tournaments_list(cls):
        print("Liste des tournois : ")

    @classmethod
    def please_wait(cls):
        print('Patientez ...')


class RoundView:
    def __init__(self):
        pass

    @classmethod
    def display_players_list_full(cls):
        print('Liste des joueurs du tournoi complète')

    def display_round_date_time_start(self):
        print('Date et heure de début du tour (round) : ')

    def display_round_date_time_end(self):
        print('Date et heure de fin du tour (round)')

    def ask_tournament_name(self):
        print('Saisissez le nom du tournoi concerné :')

    def ask_round_name(self):
        print('Saisissez le nom du tour concerné :')


class MatchView:
    def __init__(self):
        pass

    @classmethod
    def ask_score_player(cls):
        print("Score du joueur: ")


class PlayerView:
    def __init__(self):
        pass

    @classmethod
    def ask_player_name(cls):
        print("Nom du joueur : ")

    @classmethod
    def ask_player_first_name(cls):
        print("Prénom du joueur : ")

    @classmethod
    def ask_player_birth_date(cls):
        print("Date de naissance : ")

    @classmethod
    def ask_player_gender(cls):
        print("Sexe (H / F) : ")

    @classmethod
    def ask_player_ranking(cls):
        print("Classement du joueur : ")

    def ask_player_points_qty(self):  # A GERER DS TOURNOI
        print("Nombre de points : ")

    @classmethod
    def ask_choice_menu_add_t_player(cls):
        print('Inscription des joueurs du tournoi')
        print('1 joueur précédemment inscrit')
        print('2 nouveau joueur')

    @classmethod
    def add_player(cls):
        print('Ajouter ce joueur au tournoi ?')


class ReportingView:
    def __init__(self):
        pass

    def one_tournament_players_list(self):
        print("\nReporting : Liste de tous joueurs d'un tournoi")

    def all_tournaments_list(self):
        print('\nReporting : Liste de tous les tournois')

    def one_tournament_rounds_list(self):
        print("\nReporting : Liste des tours ('rounds') d'un tournoi")

    def one_tournament_matches_list(self):
        print("\nReporting : Liste des matches d'un tournoi")

    def display_all_players_reporting(self):
        print('\nReporting : liste de tous les joueurs')
        print('1 triés par ordre alphabétique')
        print('2 triés par classement')
        print('Saisissez 1 ou 2 selon votre choix : ')

    def display_all_players_alphabetical_order(self):
        print('\nListe de tous les joueurs triés par ordre alphabétique')

    def display_all_players_alphabetical_order_details(self):
        print('En detail : ')
        print('----------')

    def display_all_players_by_rank(self):
        print('\nListe de tous les joueurs triés par classement')

    def display_all_players_by_rank_details(self):
        print('En detail : ')
        print('----------')

    def display_tournaments_list(self):
        print("\nListe des tournois : ")

    def display_chosen_tournament_players(self):
        print('\nListe de tous les joueurs du tournoi choisi :')
        print('1 par ordre alphabétique')
        print('2 par classement')
        print('Saisissez 1 ou 2 selon votre choix : ')

    def display_tournaments_list_details(self):
        print('En detail : ')
        print('----------')

    def chosen_t_rounds_names_list(self):
        print('\nNom des tours du tournoi choisi :')

    def chosen_t_rounds_details(self):
        print('En detail : ')
        print('----------')

    def chosen_round_matches_list(self):
        print('\nListe des matchs du tour choisi')


class Save_and_load_View:
    def __init__(self):
        pass

    def ask_programm_saving(self):
        print("Voulez-vous faire une sauvegarde ? (O/N)")
        


    def ask_backup_loading(self):
        print("Voulez-vous charger une sauvegarde du programme ? (O/N)")
