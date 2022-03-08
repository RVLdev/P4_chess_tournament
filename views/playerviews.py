class PlayerViews:
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
    def display_please_re_enter(cls):
        print("Pour l'ajouter, merci de saisir à nouveau : ")

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
