class RoundViews:
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
