class TournamentView:
    def __init__(self):
        pass

    @classmethod
    def ask_tournament_name(self):
        print('Entrez le nom du nouveau tournoi : ')

    @classmethod
    def ask_tournament_place(self):
        print('Entrez le lieu du tournoi : ')

    @classmethod
    def ask_tournament_date(self):
        print('Entrez la date du tournoi au format JJ/MM/AAAA :')

    @classmethod
    def get_rounds_list(self):
        pass

    def askfor_tournament_players(self):
        print('Joueurs du tournoi')
        print('Choisissez un joueur et entrez son numéro')

    @classmethod
    def ask_tournament_description(self):
        print('Saisissez les commentaires : ')

    @classmethod
    def ask_time_control(self):
        print('saisissez bullet, blitz ou coup rapide : ')


class RoundView:
    def __init__(self):
        pass

    def ask_round_name(self):
        pass

    def close_a_round(self):
        print('Tour terminé')  # afficher aussi "end_date_time" ?


class MatchView:
    def __init__(self):
        pass

    @classmethod
    def ask_score_player(cls):
        print("player_score: ")


class PlayerView:
    def __init__(self):
        pass

    @classmethod
    def ask_player_name(cls):
        print("player_name : ")

    @classmethod
    def ask_player_first_name(cls):
        print("player_first_name : ")

    @classmethod
    def ask_player_birth_date(cls):
        print("player_birth_date : ")

    @classmethod
    def ask_player_gender(cls):
        print("player_gender : ")

    @classmethod
    def ask_player_ranking(cls):
        print("player_ranking : ")

    def ask_player_points_qty(self):  # A GERER DS TOURNOI
        print("player_points_qty : ")

    @classmethod
    def ask_choice_menu_add_t_player(cls):
        print('Inscription des joueurs du tournoi')
        print('1 joueur précédemment inscrit')
        print('2 nouveau joueur')

    @classmethod
    def add_player(cls):
        print('Ajouter ce joueur au tournoi ?')
