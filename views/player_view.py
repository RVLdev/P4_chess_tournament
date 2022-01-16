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

    def ask_player_points_qty(self): # A GERER DS TOURNOI
        print("player_points_qty : ")

    def ask_choice_menu_add_t_player(self):
        print('Inscription des joueurs du tournoi')
        print('1 joueur précédemment inscrit')
        print('2 nouveau joueur')