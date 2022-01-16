class TournamentView:
    def __init__(self):
        pass
    
    @classmethod
    def ask_tournament_name(self):
        print('Entrez le nom du nouveau tournoi : ')
        
    @classmethod   
    def ask_tournament_place(self):
        print ('Entrez le lieu du tournoi : ')

    @classmethod
    def ask_tournament_date(self):
        print ('Entrez la date du tournoi au format JJ/MM/AAAA :')

    @classmethod
    def get_rounds_list(self):
        pass

    def askfor_tournament_players(self):
        print ('Joueurs du tournoi')
        print ('Choisissez un joueur et entrez son numéro')

    @classmethod
    def ask_tournament_description(self):
        print ('Saisissez les commentaires : ')

    @classmethod
    def ask_time_control(self):
        print ('saisissez bullet, blitz ou coup rapide : ')