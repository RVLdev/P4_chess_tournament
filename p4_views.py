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

    """@classmethod
    def ask_for_tournament_players(cls):
        print('Joueurs du tournoi')
        print('Choisissez un joueur et entrez son numéro')"""

    @classmethod
    def ask_for_player_inclusion(cls):
        print("Liste des joueurs incomplète. Merci d'ajouter un joueur")
        """print('Saisissez O pour Oui, N pour Non : ')"""

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
    def end_tournament(cls):
        print('Tournoi terminé')


class RoundView:
    def __init__(self):
        pass

    def launch_round(self):
        print('lancer un nouveau tour ?')
        print('Saisissez O pour Oui, N pour Non : ')

    def ask_round_closing(self):  # 10/02 pr simulation
        print('Voulez-vous terminer un tour (O/N): ')

    def close_a_round(self):
        print('Pour terminer un tour : suivez les instructions')  # à mettre ds INTERFACE

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
