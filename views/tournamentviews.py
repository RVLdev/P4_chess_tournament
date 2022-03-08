
class TournamentViews:
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
        print('Entrez la date du tournoi :')

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
        print("Voulez_vous ajouter des joueurs à ce tournoi (OUI/NON) ? ")

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
    def display_round_already_closed(cls):
        print('Tour déjà terminé')

    @classmethod
    def display_round_not_closed(cls):
        print('Tour non terminé !')

    @classmethod
    def ask_overwrite_scores(cls):
        print('ATTENTION scores déjà renseignés')
        print('Voulez-vous écraser les valeurs (OUI/NON) ? ')

    @classmethod
    def choice_unavailable(cls):
        print('*** Désolé, choix non disponible\n')

    @classmethod
    def separator(cls):
        print('------------------------------------\n')
