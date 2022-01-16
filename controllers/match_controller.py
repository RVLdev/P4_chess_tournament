from ..models.match_model import Match
from ..controllers.tournament_controller import TournamentController
from ..views.match_view import MatchView

class MatchController:
    def __init__(self):
        pass

    def create_match(self, player1, player2, player1_score, player2_score):
        player1 = self.get_first_round_pairs() # A PRECISER
        player1_score = 0
        player2 = self.get_first_round_pairs() # A PRECISER
        player2_score = 0
        match = Match(player1,
                      player1_score,
                      player2,
                      player2_score)
        match.save_match()
        return match

    def set_first_round_matches(self): # A REDIGER
        # sort players list (TournamentController.tournament_players_list) by rank
        # make pairs of players
        #create matches for first round

    def sort_players_list_by_rank(self): # COMMENT TRIER ?
        rank_sorted_players_list = []
        # tri ?
        return rank_sorted_players_list

    # trop compliqué :   match1 --> player1 = pair1(1) et player2 = pair1(2) ?
    def make_pairs_of_players(self, player1, player2, rank_sorted_players_list): # pour tour suivant - A REDIGER
        pair1 = (rank_sorted_players_list(1), rank_sorted_players_list(5))
        pair2 = (rank_sorted_players_list(2), rank_sorted_players_list(6))
    
        
    def save_match(self):
        """ send to match-model for DB saving"""
        self.Match.save_match()    
    
    def get_player_score(self):
        self.MatchView.ask_score_player()
        player_score = input()
        return player_score


    def sort_first_round_players(self):
        sorted_players_list = []
        #...
        return sorted_players_list

    def create_first_round_matches(self, sorted_players_list): # PAS CLAIR
        # CdC dit listes, pourquoi pas dictionnaires ==> LES 2 OK
        match1 = ({'player1': sorted_players_list(1), 'score1': 0}, 
                  {'player2': sorted_players_list(5), 'score2': 0})
        # ou  liste de listes:
        match1 = ((sorted_players_list(1), 0), (sorted_players_list(5), 0))