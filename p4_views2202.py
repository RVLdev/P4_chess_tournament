import time


class InterfaceView:
    def __init__(self):
        pass
    @classmethod
    def launch_tournament(cls):
        """ launches the program's menu """
        print("Bonjour, bienvenue dans le gestionnaire de tournois d'échecs")
        time.sleep(1)
        cls.display_startmenu()

    @classmethod
    def display_startmenu(cls):
        """ displays the menu """
        print('\nMENU :')
        print('1 TOURNOI : Créer un tournoi')
        print('2 JOUEURS : Enregistrer un ou des joueurs')
        print("3 JOUEURS : Mettre à jour le classement d'un joueur")
        print('4 TOUR : Lancer un tour')
        print('5 TOUR : Clôturer un tour')
        print('6 TOUR : Renseigner les scores')
        print('7 Reporting')
        print('8 Sauvegarder - Charger')
        print('9 Quitter le programme')
        print('Que souhaitez-vous faire ?')

    @classmethod
    def menu_reporting(cls):
        print ('LISTE DES RAPPORTS :')
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
    def ask_for_new_tourney_players(cls):
        print("Tournoi en cours de création : Merci d'ajouter un joueur")
        

    @classmethod
    def ask_for_player_inclusion(cls):
        print("Liste des joueurs incomplète. Merci d'ajouter un joueur")
        """print('(O/N) Saisissez O pour Oui, N pour Non : ')"""

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
    def display_t_players_list_full(self):
        print('Liste des joueurs du tournoi complète')
    
    @classmethod  
    def end_tournament(cls):
        print('Tournoi terminé')
    
    @classmethod
    def display_tournaments_list(cls):
        print("Liste des tournois : ")


class RoundView:
    def __init__(self):
        pass

    def launch_round(self):
        print('Voulez_vous lancer un tour (O/N)? ')

    def display_round_date_time_start(self):
        print('Date et heure de début du tour (round) : ')

    def this_round_closing(self):  # 10/02 pr simulation
        print('Marquer ce tour comme étant terminé (O/N) ?')

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
    def update_scores(cls):
        print('Saisie des scores')

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
    
    @classmethod
    def request_rank_update(cls):
        print('Voulez_vous mettre à jour le classement des joueurs ? O/N')

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
        print("Reporting : Liste de tous joueurs d'un tournoi")

    def all_tournaments_list(self):
        print("Reporting : Liste de tous les tournois")

    def one_tournament_rounds_list(self):
        print("Reporting : Liste des tours ('rounds') d'un tournoi")

    def one_tournament_matches_list(self):
        print("Reporting : Liste des matches d'un tournoi")

    def display_all_players_reporting(self):
        print('Reporting : liste de tous les joueurs')
        print('1 triés par ordre alphabétique')
        print('2 triés par classement')
        print('Saisissez 1 ou 2 selon votre choix : ')

    def display_all_players_alphabetical_order(self):
        print('Liste de tous les joueurs triés par ordre alphabétique')

    def display_all_players_alphabetical_order_details(self):
        print('En detail : ')
        print('----------')

    def display_all_players_by_rank(self):
        print('Liste de tous les joueurs triés par classement')

    def display_all_players_by_rank_details(self):
        print('En detail : ')
        print('----------')

    def display_tournaments_list(self):
        print("Liste des tournois : ")

    def display_chosen_tournament_players(self):
        print('Liste de tous les joueurs du tournoi choisi :')
        print('1 par ordre alphabétique')
        print('2 par classement')
        print('Saisissez 1 ou 2 selon votre choix : ')

    def display_tournaments_list_details(self):
        print('En detail : ')
        print('----------')

    def chosen_t_rounds_names_list(self):
        print('Nom des tours du tournoi choisi :')

    def chosen_t_rounds_details(self): 
        print('En detail : ')
        print('----------')

    def chosen_round_matches_list(self):
        print('Liste des matchs du tour choisi')


class Save_and_load_View:
    def __init__(self):
        pass

    def ask_programm_saving(self):
        print("Voulez-vous faire une sauvegarde ? (O/N)")

    def ask_backup_loading(self):
        print("Voulez-vous charger une sauvegarde du programme ? (O/N)")
