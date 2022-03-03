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
        print('2 TOURNOI : afficher un tournoi')
        print('3 JOUEURS : Enregistrer un ou des joueurs dans la base')
        print('4 JOUEURS : Ajouter un joueur à un tournoi')
        print("5 CLASSEMENT")
        print('6 TOUR : Lancer un tour')
        print('7 TOUR : Clôturer un tour')
        print('8 TOUR : Renseigner des scores')
        print('9 Reporting')
        print('10 Sauvegarder - Charger')
        print('11 Quitter le programme')
        print('Que souhaitez-vous faire ?')

    @classmethod
    def ask_for_players_inclusion(cls):
        print("Voulez_vous ajouter 8 joueurs à ce tournoi (O/N) ? ")

    @classmethod
    def ask_add_one_player(cls):
        print("Voulez_vous ajouter 1 joueurs à un tournoi (O/N) ? ")

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
    def request_ranking_update(cls):
        print('Mise à jour du classement : ')
        print('1 Classement des joueurs dans un tournoi')
        print('2 Classement général des joueurs')
        print('3 Revenir au menu')
        print('Saisissez 1, 2 ou 3 selon votre choix : ')

    @classmethod
    def request_global_rank_update(cls):
        print('Mettre à jour le classement général des joueurs (O/N)? ')

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

    @classmethod
    def separator(cls):
        print('------------------------------------\n')


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
    def display_t_rounds_list(cls):
        print('Liste des tours du tournoi :')

    @classmethod
    def display_t_players_list_is_full(cls):
        print('La liste des joueurs de ce tournoi est complète')

    @classmethod
    def display_players_sorted_rank_n_points(cls):
        print('Joueurs triés par classement & points')

    @classmethod
    def display_first_r_matches_created(cls):
        print('Liste des matchs du 1er tour créée')

    @classmethod
    def display_rounds_list_full(cls):
        print('La liste des tours du tournoi est complète')

    @classmethod
    def display_this_t_rounds_already_created(cls):
        print('Tous les tours de CE tournoi sont déjà créés')

    @classmethod
    def end_tournament(cls):
        print('Tournoi terminé')

    @classmethod
    def display_tournaments_list(cls):
        print("Liste des tournois : ")

    @classmethod
    def please_wait(cls):
        print('Patientez ...')

    @classmethod
    def ask_overwrite_scores(cls):
        print('ATTENTION scores déjà renseignés')
        print('Voulez-vous écraser les valeurs (O/N) ? ')

    @classmethod
    def separator(cls):
        print('------------------------------------\n')


class RoundView:
    def __init__(self):
        pass

    @classmethod
    def display_players_list_full(cls):
        print('Liste des joueurs du tournoi complète')

    @classmethod
    def display_round_date_time_start(cls):
        print('Date et heure de début du tour (round) : ')

    @classmethod
    def display_round_date_time_end(cls):
        print('Date et heure de fin du tour (round)')

    @classmethod
    def ask_tournament_name(cls):
        print('Saisissez le nom du tournoi concerné :')

    @classmethod
    def ask_round_name(cls):
        print('Saisissez le nom du tour concerné :')

    @classmethod
    def separator(cls):
        print('------------------------------------\n')


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

    @classmethod
    def ask_player_points_qty(cls):
        print("Nombre de points : ")

    @classmethod
    def display_absent_player(cls):
        print('Joueur absent de la base de données.')

    @classmethod
    def ask_choice_menu_add_t_player(cls):
        print('Inscription des joueurs du tournoi')
        print('1 joueur précédemment inscrit')
        print('2 nouveau joueur')

    @classmethod
    def add_player(cls):
        print('Ajouter ce joueur au tournoi ?')

    @classmethod
    def display_points_n_rank_sorted_tournament_players(cls):
        print('Liste des joueurs du tournoi triés par nombre de points')

    @classmethod
    def ask_player_to_update_rank(cls):
        print('Le classement de quel joueur voulez-vous mettre à jour ?')

    @classmethod
    def separator(cls):
        print('------------------------------------\n')


class ReportingView:
    def __init__(self):
        pass

    @classmethod
    def one_tournament_players_list(cls):
        print("\nReporting : Liste de tous joueurs d'un tournoi")

    @classmethod
    def all_tournaments_list(cls):
        print('\nReporting : Liste de tous les tournois')

    @classmethod
    def one_tournament_rounds_list(cls):
        print("\nReporting : Liste des tours ('rounds') d'un tournoi")

    @classmethod
    def one_tournament_matches_list(cls):
        print("\nReporting : Liste des matches d'un tournoi")

    @classmethod
    def display_all_players_reporting(cls):
        print('\nReporting : liste de tous les joueurs')
        print('1 triés par ordre alphabétique')
        print('2 triés par classement')
        print('Saisissez 1 ou 2 selon votre choix : ')

    @classmethod
    def display_all_players_alphabetical_order(cls):
        print('\nListe de tous les joueurs triés par ordre alphabétique')

    @classmethod
    def display_all_players_alphabetical_order_details(cls):
        print('En detail : \n -----------')

    @classmethod
    def display_all_players_by_rank(cls):
        print('\nListe de tous les joueurs triés par classement')

    @classmethod
    def display_all_players_by_rank_details(cls):
        print('En detail : \n -----------')

    @classmethod
    def display_tournaments_list(cls):
        print("\nListe des tournois : ")

    @classmethod
    def display_chosen_tournament_players(cls):
        print('\nListe de tous les joueurs du tournoi choisi :')
        print('1 par ordre alphabétique')
        print('2 par classement')
        print('Saisissez 1 ou 2 selon votre choix : ')

    @classmethod
    def display_tournaments_list_details(cls):
        print('En detail : \n -----------')

    @classmethod
    def chosen_t_rounds_names_list(cls):
        print('\nNom des tours du tournoi choisi :')

    @classmethod
    def chosen_t_rounds_details(cls):
        print('En detail : \n -----------')

    @classmethod
    def chosen_round_matches_list(cls):
        print('\nListe des matchs du tour choisi')

    @classmethod       
    def separator(cls):
        print('------------------------------------\n')


class Save_and_load_View:
    def __init__(self):
        pass

    @classmethod
    def ask_programm_saving(cls):
        print("Voulez-vous faire une sauvegarde ? (O/N)")

    @classmethod
    def ask_backup_loading(cls):
        print("Voulez-vous charger une sauvegarde du programme ? (O/N)")
