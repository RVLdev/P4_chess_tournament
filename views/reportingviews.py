class ReportingViews:
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
    def choice_unavailable(cls):
        print('*** Désolé, choix non disponible\n')

    @classmethod
    def separator(cls):
        print('------------------------------------\n')
