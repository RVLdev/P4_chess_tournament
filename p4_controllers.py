from p4_models import Tournament
from p4_models import Round
from p4_models import Match
from p4_models import Player
from p4_views import TournamentView
from p4_views import RoundView
from p4_views import PlayerView
from p4_views import MatchView
from tinydb import where, Query


class TournamentController:
    def __init__(self):
        self.tournament_view = TournamentView()
        self.tournament_players_list = []
        self.rounds_list = []

    def create_new_tournament(self, tournament_id=0):
        """create one tournament"""
        tournament = Tournament(
            tournament_id,
            self.ask_tournament_name(),
            self.ask_tournament_place(),
            self.ask_tournament_date(),
            self.create_tournament_players_list(),
            self.ask_tournament_description(),
            self.ask_time_control(),
            self.ask_tournament_rounds_qty()
            )
        tournament.create_tournament()
        Tournament.update_tournament_id()
        return tournament

    def ask_tournament_name(self):
        TournamentView.ask_tournament_name()
        tournament_name = input()
        # vérifications !!!
        return tournament_name

    def ask_tournament_place(self):
        TournamentView.ask_tournament_place()
        tournament_place = input()
        return tournament_place

    def ask_tournament_date(self):
        TournamentView.ask_tournament_date()
        tournament_date = input()
        return tournament_date

    def create_tournament_players_list(self):
        """ create this tournament's list of 8 players"""
        while len(self.tournament_players_list) < 8:
            self.add_player_to_tournament()
        print('liste des joueurs du tournoi complète')
        return self.tournament_players_list

    def add_player_to_tournament(self):
        """ add player to tournament_players_list """
        # check if player in DB
        requested_player = PlayerController.request_player()
        # if player not in DB, launch its creation and add it to list
        if requested_player is None:
            newplayer = PlayerController.create_player()
            self.tournament_players_list.append(newplayer)
        # if player in DB, add it to list
        else:
            self.tournament_players_list.append(requested_player)
        return self.tournament_players_list

    def ask_tournament_description(self):
        """ get tournament description from User"""
        TournamentView.ask_tournament_description()
        tournament_description = input()
        return tournament_description

    def ask_time_control(self):
        """ Get time control information from User"""
        TournamentView.ask_time_control()
        time_control = input()
        return time_control

    def ask_tournament_rounds_qty(self):
        """ Get tournament_rounds_qty from User"""
        TournamentView.ask_tournament_rounds_qty()
        tournament_rounds_qty = input()
        return tournament_rounds_qty

    def sort_tournament_players_list_by_rank(self):
        """sort by rank tournament players list"""
        rank_sorted_p_list = sorted(self.tournament_players_list,
                                  key=lambda k: k['p_rank'])
        print(rank_sorted_p_list)
        return rank_sorted_p_list

    def sort_tournament_players_list_by_points(self, rank_sorted_p_list):
        """ get tournament players list sorted by rank and total points """
        # commencer par tri par rank puis trier par points => les "mêmes pts" seront déjà triés par rank !
        points_sorted_p_list = sorted(rank_sorted_p_list,
                                      key=lambda k: k['p_total_points'], reverse = True)
        print(points_sorted_p_list)
        return points_sorted_p_list


    ##   A TRANSFERER DS TOURNOI - CALCUL A FAIRE et code à compléter/corriger
    # update NB TOTAL POINTS DU JOUEUR ds players_db & tournament_players_list
    def update_player_points_qty(self, player_id):
        # first calculate then update p_total_points
        # calcul ?
        nbr_players = len(Tournament.tournament_players_list)
        for j in range(0, nbr_players):
            player_points = ' calcul???? '
        # udate t_players_list
        Tournament.tournament_players_list[j]['p_total_points'] = player_points

        # update players_db
        Player.update_p_total_points(player_id, Player.player_points_qty)


    def create_first_round_matches(self, rank_sorted_p_list):
        """ create matches for first round """
        matches_qty = len(rank_sorted_p_list)/2
        for i in range(0, matches_qty):
            RoundController.r_matches_list.append(
                Match(
                        rank_sorted_p_list[i],
                        rank_sorted_p_list[i+matches_qty]
                     )
            )

    def create_next_round_matches(self, points_sorted_p_list):
        """ create matches for round > 1 """
        # A COMPLETER : COMPARER nlles paires J1-J2 avec celles de la
        # liste r_matches_list + CORRIGER ci-dessous
        matches_qty = len(points_sorted_p_list)/2
        for i in range(0, matches_qty):
            RoundController.r_matches_list.append(
                Match(
                        points_sorted_p_list[i],
                        points_sorted_p_list[i+1] # i+1 = joueur suivant ds liste totalemt triée
                     )
            )

    # alimente la liste de matchs (initialement vide)
    def add_match_to_r_matches_list(self, rank_sorted_p_list):
        """add new match to round matches list"""
        if len(Round.rounds_db) >= 1:
            self.create_next_round_matches(rank_sorted_p_list)
        else:
            self.create_first_round_matches()
        return RoundController.r_matches_list


class RoundController:
    def __init__(self):
        self.r_matches_list = [] 

    def create_round(self, round_id=0, end_date_time=0):
        """ create a round """
        round = Round(round_id,
                      self.give_round_name(),
                      self.fill_r_matches_list(),
                      self.set_start_date_time(),
                      end_date_time)
        round.create_round()
        Round.update_round_id()
        return round

    def give_round_name(self):
        """ get or ask round name"""
        round_nbr = len(Round.rounds_db)
        round_name = f'{"Round"}{round_nbr+1}'
        return round_name

    def fill_r_matches_list(self):
        """ fill empty round matches list """
        TournamentController.add_match_to_r_matches_list(TournamentController.rank_sorted_p_list)
        return self.r_matches_list


    """ vu : TRANSFEREES DS TOURNOI
    def create_first_round_matches(self):
        matches_qty = len(TournamentController.rank_sorted_p_list)/2
        for i in range(0, matches_qty):
            self.r_matches_list.append(
                Match(
                        TournamentController.rank_sorted_p_list[i],
                        TournamentController.rank_sorted_p_list[i+matches_qty]
                     )
            )
        return self.r_matches_list

    def create_next_round_matches(self):
        # A COMPLETER : COMPARER nlles paires J1-J2 avec celles de la
        # liste r_matches_list + CORRIGER ci-dessous
        matches_qty = len(TournamentController.points_sorted_p_list)/2
        for i in range(0, matches_qty):
            self.r_matches_list.append(
                Match(
                        TournamentController.points_sorted_p_list[i],
                        TournamentController.points_sorted_p_list[i+1] # i+1 = joueur suivant ds liste totalemt triée
                     )
            )
        return self.r_matches_list"""

    def set_start_date_time(self):
        """ give starting date & time of a round """
        round_start = Round.start_round()
        print(round_start)
        return round_start

    def end_round(self):
        """ give closing date & time of a round """
        round_end = Round.close_round() # ATTENTION MODEL 'def close_round()' à vérifier
        print(round_end)

    # update scores in r_matches_list AND matches_db
    def update_r_match_score(self):
        """ update round matches players'score"""
        nbr_matches = len(self.r_matches_list)
        for i in range(0, nbr_matches):
            player1_score = self.ask_player1_score(i, self.r_matches_list)
            player2_score = self.ask_player2_score(i, self.r_matches_list)

            # update r_matches_list
            self.r_matches_list[i]['score_player1'] = player1_score
            self.r_matches_list[i]['score_player2'] = player2_score
            # update matches_db
            match_id = i
            Match.update_players_scores(match_id, player1_score, player2_score)

    def ask_player1_score(self, i):
        """ get player1 's score"""
        # print "match PLAYER1-NAME / PLAYER2-NAME"
        print('match ' + self.r_matches_list[i]['chess_player1']['p_name']
                       + " / "
                       + self.r_matches_list[i]['chess_player2']['p_name'])

        # print "joueur 1 : PLAYER1-NAME"
        print('joueur 1 : ' + self.r_matches_list[i]['chess_player1']['p_name'])

        MatchView.ask_score_player()
        player1_score = input('saisissez son score (0 ou 0.5 ou 1) : ')
        print('joueur 1 : ' + self.r_matches_list[i]['chess_player1']['p_name']
                            + ' score = ' + player1_score)
        return player1_score

    def ask_player2_score(self, i):
        """ get player2 's score"""
        # print "match PLAYER1-NAME / PLAYER2-NAME"
        print('match ' + self.r_matches_list[i]['chess_player1']['p_name']
                       + " / "
                       + self.r_matches_list[i]['chess_player2']['p_name'])

        # print "joueur 2 : PLAYER2-NAME"
        print('joueur 2 : ' + self.r_matches_list[i]['chess_player2']['p_name'])

        MatchView.ask_score_player()
        player2_score = input('saisissez son score (0 ou 0.5 ou 1) : ')
        print('joueur 2 : ' + self.r_matches_list[i]['chess_player2']['p_name']
                            + ' score = ' + player2_score)
        return player2_score

""" TRANSFERE DS TOURNOI 
    # CALCUL A FAIRE et code à compléter/corriger
    # update NB TOTAL POINTS DU JOUEUR ds players_db & tournament_players_list
    def update_player_points_qty(self, player_id):
        # first calculate then update p_total_points
        # calcul ?
        nbr_players = len(Tournament.tournament_players_list)
        for j in range(0, nbr_players):
            player_points = ' calcul???? '
        # udate t_players_list
        Tournament.tournament_players_list[j]['p_total_points'] = player_points

        # update players_db
        Player.update_p_total_points(player_id, Player.player_points_qty)
"""

class MatchController:
    def __init__(self):
        pass

    def create_match(self, match_player1, match_player2, match_id=0,
                     player1_score=0, player2_score=0):
        """create one match"""
        match = Match(match_id,
                      match_player1,
                      player1_score,
                      match_player2,
                      player2_score)
        match.create_match()
        Match.update_match_id()
        return match

    """ TRANSFERE DANS ROUNDCONTROLLER
    def update_match_score(self, match_id, player1_score, player2_score):
        player1_score = self.ask_player1_score()
        player2_score = self.ask_player2_score()
        Match.update_players_scores(match_id, player1_score, player2_score)

    def ask_player1_score(self, Round.r_matches_list):
        # print "match PLAYER1-NAME / PLAYER2-NAME"
        print('match ' + Round.r_matches_list[0]['chess_player1']['p_name']
                       + " / "
                       + Round.r_matches_list[0]['chess_player2']['p_name'])

        # print "joueur 1 : PLAYER1-NAME"
        print('joueur 1 : ' + Round.r_matches_list[0]['chess_player1']['p_name'])

        MatchView.ask_score_player()
        player1_score = input('saisissez son score (0 ou 0.5 ou 1) : ')
        print('joueur 1 : '+ Round.r_matches_list[0]['chess_player1']['p_name']
                           + ' score = ' + player1_score)
        return player1_score

    def ask_player2_score(self):
        pass"""


class PlayerController:
    def __init__(self):
        self.player_view = PlayerView()

    def create_player(self, player_id=0):
        """create one player"""
        player = Player(
            player_id,
            self.ask_player_name(),
            self.ask_player_first_name(),
            self.ask_player_birth_date(),
            self.ask_player_gender(),
            self.ask_player_ranking(),
            player_points_qty=0
        )
        player.create_player()
        Player.update_player_id()
        return player

    def ask_player_name(self):
        """ get player_name from User through player_view """
        PlayerView.ask_player_name()  # cf @classmethod
        player_name = input()
        # vérifications !!!
        return player_name

    def ask_player_first_name(self):
        """ get player_first_name from User through player_view """
        PlayerView.ask_player_first_name()
        player_first_name = input()
        return player_first_name

    def ask_player_birth_date(self):
        """ get player_birth_date from User through player_view """
        PlayerView.ask_player_birth_date()
        player_birth_date = input()
        return player_birth_date

    def ask_player_gender(self):
        """ get player_gender from User through player_view """
        PlayerView.ask_player_gender()
        player_gender = input()
        return player_gender

    def ask_player_ranking(self):
        """ get player_ranking from User through player_view """
        PlayerView.ask_player_ranking()
        player_ranking = input()
        return player_ranking

    def request_player(self):
        """search a player (by his name & firstname) into db"""
        search_p_name = self.ask_player_name()
        search_p_firstname = self.ask_player_first_name()
        Theplayer = Query()
        requested_player = Player.players_db.search(
            (
                Theplayer.p_name == search_p_name
            ) & (
                Theplayer.p_firstname == search_p_firstname
                )
            )
        print(requested_player)  # = list with a dictionnary within !
        return requested_player
