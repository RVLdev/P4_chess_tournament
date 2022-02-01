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
        self.tournament_players_id_list = []
        self.tournament_rounds_id_list = []
        self.t_full_players_list = []
        self.rank_sorted_p_list = []
        self.points_sorted_p_list = []
        self.points_sorted_p_id_list = []
        self.m_list = []  # list of matches from DB
        self.previous_pairs_list = []  # list of previous matches pairs of players

    def create_new_tournament(self, tournament_id=0):
        """create one tournament"""
        tournament = Tournament(
            tournament_id,
            self.ask_tournament_name(),
            self.ask_tournament_place(),
            self.ask_tournament_date(),
            self.ask_tournament_description(),
            self.ask_time_control(),
            self.ask_tournament_rounds_qty(),
            self.create_tournament_players_id_list(),  # doc_ids (L65 & 68)
            self.create_tournament_rounds_id_list,  # rounds doc_ids list
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

    def create_tournament_players_id_list(self):  # players doc_ids
        """ create this tournament's list of 8 players"""
        while len(self.tournament_players_id_list) < 8:
            self.add_player_to_tournament()
        print('liste des joueurs du tournoi complète')
        return self.tournament_players_id_list

    def add_player_to_tournament(self):
        """ add player to tournament_players_id_list """
        # check if player in DB
        requested_player = PlayerController.request_player()
        # if player not in DB, launch its creation and add it to list
        if requested_player is None:
            newplayer = PlayerController.create_player()
            Player.update_player_id()
            self.tournament_players_id_list.append(newplayer.doc_id)
        # if player in DB, add it to list
        else:
            self.tournament_players_id_list.append(requested_player.doc_id)
        return self.tournament_players_id_list

    def create_tournament_rounds_id_list(self, tournament_rounds_qty):  # rounds doc_ids
        while len(self.tournament_rounds_id_list) < tournament_rounds_qty:
            self.add_round_to_t_rounds_list()
        return self.tournament_rounds_id_list

    def add_round_to_t_rounds_list(self):
        """add new round to round matches list"""
        new_round = Round.create_round()
        Round.update_round_id()
        self.tournament_rounds_id_list.append(new_round.doc_id)

    def sort_tournament_players_list_by_rank(self):
        """sort by rank tournament players list"""
        # récupère la liste complète des éléments à trier
        for doc in self.tournament_players_id_list:
            t_full_player = Player.players_db.get(doc_id=doc)
            self.t_full_players_list.append(t_full_player)

        rank_sorted_p_list = sorted(self.t_full_players_list,
                                    key=lambda k: k['p_rank'])
        print(rank_sorted_p_list)  # contient des joueurs 'complets' (pas liste de doc_ids)
        return rank_sorted_p_list

    def update_player_points_qty(self, player_id):  # NEW 28/1 A RELIRE
        """ calculate and update players total points"""
        nbr_players = len(Tournament.tournament_players_id_list)

        for j in range(0, nbr_players/2):
            # Get match 1st player's doc_id and its points nb before match (previous_points_pl1)
            match_pl1_doc_id = RoundController.r_matches_list[j]['chess_player1']
            player1 = Player.players_db.get(doc_id=match_pl1_doc_id)  # ou doc_ids=[]
            previous_points_pl1 = player1['p_total_points']

            # Get match 1st player's new points (match score)
            new_points_pl1 = RoundController.player1_score

            # calculate match 1st player's new total of points & update its points in DB
            new_total_points_pl1 = new_points_pl1 + previous_points_pl1
            Player.players_db.update({'p_total_points': new_total_points_pl1},
                                     doc_id=match_pl1_doc_id)  # ou doc_ids=[]

            # do the same with match 2nd player
            match_pl2_doc_id = RoundController.r_matches_list[j]['chess_player2']
            player2 = Player.players_db.get(doc_id=match_pl2_doc_id)  # ou doc_ids=[]
            previous_points_pl2 = player2['p_total_points']

            new_points_pl2 = RoundController.player2_score
            new_total_points_pl2 = new_points_pl2 + previous_points_pl2
            Player.players_db.update({'p_total_points': new_total_points_pl2},
                                     doc_id=match_pl2_doc_id)  # ou doc_ids=[]

        # update players_db
        Player.update_p_total_points(player_id, Player.player_points_qty)

    # CALCULER PAIRES != celles des tours précédents
    def sort_tournament_players_id_list_by_points(self, rank_sorted_p_list):
        """ get tournament players list sorted by rank and total points """
        points_sorted_p_list = sorted(rank_sorted_p_list,
                                      key=lambda k: k['p_total_points'],
                                      reverse=True)
        print(points_sorted_p_list)  # 'full' players (not only doc_ids)

        for p in points_sorted_p_list:
            self.points_sorted_p_id_list.append(points_sorted_p_list[p]['p_id'])

        return self.points_sorted_p_id_list  # players'doc_ids

    """ For rounds next to 1st round, matches players must be sorted
    by rank and total points. It is also  required to check that
    new pairs of players are different from previous matches pairs."""

    def create_matches_players_id_list(self):
        # get list of previous matches pairs of players
        for item in Match.matches_db:
            self.m_list.append(item)

        nb_matchs = len(self.m_list)
        for n in range(0, nb_matchs):
            self.previous_pairs_list.append([self.m_list[n]['chess_player1'],  # player's doc_id
                                            self.m_list[n]['chess_player2']])
        return self.previous_pairs_list

    def compare_matches_p_pairs(self, points_sorted_p_id_list):
        next_round_p_pairs_list = []  # list of pairs of players for next matches
        i = 1

        def create_test_players_pair(i, points_sorted_p_id_list):
            # create pair of players to be tested
            test_pair = [points_sorted_p_id_list[0],
                         points_sorted_p_id_list[i]]
            return test_pair

        while len(points_sorted_p_id_list) > 0:
            testing_pair = create_test_players_pair(i, points_sorted_p_id_list)
            if testing_pair in self.previous_pairs_list:
                # ALREADY PLAYED pair. New testing_pair :
                i += 1
                testing_pair = create_test_players_pair(i)
            else:
                # UNIQUE pair of players to be added to next round matches
                next_round_p_pairs_list.append(testing_pair)
                # update points_sorted_p_id_list
                del points_sorted_p_id_list[0]
                del points_sorted_p_id_list[i-1]

                if len(points_sorted_p_id_list) > 0:
                    # new testing_pair:
                    i = 1
                    testing_pair = create_test_players_pair(i)
                else:
                    return next_round_p_pairs_list
        return next_round_p_pairs_list

    def create_first_round_matches(self, rank_sorted_p_list):  # MATCHS
        """ create matches for first round """
        matches_qty = len(rank_sorted_p_list)/2
        for i in range(0, matches_qty):
            RoundController.r_matches_list.append(
                Match(
                        rank_sorted_p_list[i]['p_id'],  # doc_id du match_player1
                        rank_sorted_p_list[i+matches_qty]['p_id']  # doc_id du match_player2
                     )
            )

    def create_next_round_matches(self, next_round_p_pairs_list):  # MATCHS
        """ create matches for round > 1 """
        matches_qty = len(next_round_p_pairs_list)
        for i in range(0, matches_qty):
            RoundController.r_matches_list.append(
                Match(
                        next_round_p_pairs_list[i],  # player1 doc_id 
                        next_round_p_pairs_list[i+1]  # i+1 = next player
                     )
            )

    # contient des joueurs 'complets' (pas liste de doc_ids)
    def add_match_to_r_matches_list(self,
                                    rank_sorted_p_list,
                                    points_sorted_p_list):
        """add new match to round's matches' list"""
        # 1 match <=> 2 players
        # for each round, number of matches = number of players/2
        matches_nb = (len(self.tournament_players_id_list))/2

        if len(self.r_matches_list) < matches_nb:
            if len(self.tournament_rounds_id_list) >= 1:
                self.create_next_round_matches(points_sorted_p_list)
            else:
                self.create_first_round_matches(rank_sorted_p_list)
        return RoundController.r_matches_list


class RoundController:
    def __init__(self):
        self.r_matches_list = []  # contiendra joueurs'complets'(pas doc_ids)

    def create_round(self, round_id=0, end_date_time=0):
        """ create a round """
        round = Round(round_id,
                      self.give_round_name(),
                      self.create_r_matches_list(),
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

    def create_r_matches_list(self):
        """ launch creation of the round's matches'list """
        r_matches_list = TournamentController.add_match_to_r_matches_list(
                TournamentController.rank_sorted_p_list,
                TournamentController.points_sorted_p_list)
        return r_matches_list

    def set_start_date_time(self):
        """ give starting date & time of a round """
        round_start = Round.start_round()
        print(round_start)
        return round_start

    def end_round(self):
        """ give closing date & time of a round """
        round_end = Round.close_round()  # ATTENTION MODEL 'def close_round()' à vérifier
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
        print('joueur1: ' + self.r_matches_list[i]['chess_player1']['p_name'])

        MatchView.ask_score_player()
        player1_score = input('saisissez son score (0 ou 0.5 ou 1) : ')

        # dico qui associe player doc_id et new points
        pl_doc_id = self.r_matches_list[i]['chess_player1']
        new_points_player1 = {'pl_doc_id': pl_doc_id,
                              'newpoints': player1_score}

        print('joueur1 : ' + self.r_matches_list[i]['chess_player1']['p_name']
                           + ' score = ' + player1_score)

        return player1_score

    def ask_player2_score(self, i):
        """ get player2 's score"""
        # print "match PLAYER1-NAME / PLAYER2-NAME"
        print('match ' + self.r_matches_list[i]['chess_player1']['p_name']
                       + " / "
                       + self.r_matches_list[i]['chess_player2']['p_name'])

        # print "joueur 2 : PLAYER2-NAME"
        print('joueur2 : '+self.r_matches_list[i]['chess_player2']['p_name'])

        MatchView.ask_score_player()
        player2_score = input('saisissez son score (0 ou 0.5 ou 1) : ')
        print('joueur2 : ' + self.r_matches_list[i]['chess_player2']['p_name']
                           + ' score = ' + player2_score)
        return player2_score


class MatchController:
    def __init__(self):
        pass

    def create_match(self, match_player1, match_player2, match_id=0,
                     player1_score=0, player2_score=0):
        """create one match"""
        match = Match(match_id,
                      match_player1,  # player's doc_id
                      player1_score,
                      match_player2,  # player's doc_id
                      player2_score)
        match.create_match()
        Match.update_match_id()
        return match


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
        requested_player = Player.players_db.get(
            (
                Theplayer.p_name == search_p_name
            ) & (
                Theplayer.p_firstname == search_p_firstname
                )
            )
        # Search donne [{}] (liste contenant joueur),
        # mais 'get' donne directement le joueur {}
        print(requested_player)
        print(requested_player.doc_id)  # player's DOC_ID
        return requested_player.doc_id
