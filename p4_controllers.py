# version pour correction stockage .json
import time
from p4_v2models import Tournament
from p4_v2models import Round
from p4_v2models import Match
from p4_v2models import Player
from p4_v2models import Save_and_load
from p4_views_v2inchangee import TournamentView
from p4_views_v2inchangee import RoundView
from p4_views_v2inchangee import PlayerView
from p4_views_v2inchangee import ReportingView
from p4_views_v2inchangee import Save_and_load_View
from tinydb import TinyDB, where, Query
from datetime import datetime


class TournamentCtlr:
    def __init__(self, tournament_id):
        self.tournament_view = TournamentView()
        self.tournament_id = tournament_id
        self.tournament_rounds_qty = 4
        self.tournament_players_id_list = []
        self.tournament_rounds_id_list = []
        self.t_full_players_list = []
        self.r_matches_id_list = []
        self.first_round_matches = []
        self.rank_sorted_p_list = []
        self.points_sorted_p_list = []
        self.points_sorted_p_id_list = []
        self.m_list = []
        self.previous_pairs_list = []
    """
        self.db_all_t = TinyDB('db_all_t.json')  ##
        Tournament.all_tournaments_db = self.db_all_t.table(
            'all_tournaments_db')  ##

        self.db = TinyDB('db'+str(tournament_id)+'.json')
        self.Thetournmt = Query()
        self.tournaments_db = self.db.table('tournaments_db')
        self.Theplayer = Query()
        self.players_db = self.db.table('players_db')
        self.Theround = Query()
        self.rounds_db = self.db.table('rounds_db')
        self.Thematch = Query()
        self.matches_db = self.db.table('matches_db')

        self.db_backup = TinyDB('db_backup.json')
        self.p_db = self.db_backup.table('players_db')
        self.m_db = self.db_backup.table('matches_db')
        self.r_db = self.db_backup.table('rounds_db')
        self.t_db = self.db_backup.table('tournaments_db')
    """

    def read_a_tournament(self):
        tournament_id = TournamentCtlr.request_tournament_id(self)
        Tournament.read_tournament(self, tournament_id)

    def create_new_tournament(self, tournament_id=0, tournament_rounds_qty=4):
        """create a tournament"""
        tournament = Tournament(
            tournament_id,
            TournamentCtlr.ask_tournament_name(self),
            TournamentCtlr.ask_tournament_place(self),
            TournamentCtlr.ask_tournament_date(self),
            TournamentCtlr.ask_tournament_description(self),
            TournamentCtlr.ask_time_control(self),
            tournament_rounds_qty,  # 4 by default
            tournament_players_id_list=[],  # doc_ids
            tournament_rounds_id_list=[]   # doc_ids
            )
        tournament.create_tournament()
        new_tournament_id = Tournament.update_tournament_id(self)
        tournament_id = new_tournament_id

        db_all_t = TinyDB('db_all_t.json')
        Tournament.all_tournaments_db = db_all_t.table('all_tournaments_db')
        db = TinyDB('db'+str(tournament_id)+'.json')
        Tournament.tournaments_db = db.table('tournaments_db')
        # get tournament to store it in its DB
        new_tournament = Tournament.all_tournaments_db.get(
            doc_id=new_tournament_id)
        Tournament.tournaments_db.insert(new_tournament)

        TournamentCtlr.confirm_tournament_rounds_qty(self, tournament_id)
        return tournament_id

    def ask_tournament_name(self):
        """ask User tournament name"""
        TournamentView.ask_tournament_name()
        tournament_name = input()
        return tournament_name

    def ask_tournament_place(self):
        """ask User tournament place"""
        TournamentView.ask_tournament_place()
        tournament_place = input()
        return tournament_place

    def ask_tournament_date(self):
        """ask User tournament date(s)"""
        TournamentView.ask_tournament_date()
        tournament_date = input()
        return tournament_date

    def ask_tournament_description(self):
        """ask User tournament description and comments"""
        TournamentView.ask_tournament_description()
        tournament_description = input()
        return tournament_description

    def ask_time_control(self):
        """ask User time control"""
        TournamentView.ask_time_control()
        time_control = input()
        return time_control

    def confirm_tournament_rounds_qty(self, tournament_id):
        """Get tournament_rounds_qty confirmation from User"""
        TournamentView.ask_tournament_rounds_qty()
        tournament_rounds_qty = int(input())
        # load tournament_rounds_qty update into DB
        Tournament.update_tournament_rounds_qty(self, tournament_rounds_qty,
                                                tournament_id)
        return tournament_rounds_qty

    def create_tournament_players_id_list(self, tournament_id):  # doc_ids
        """create this tournament's list of 8 players"""
        tournament_players_id_list = []
        while len(tournament_players_id_list) < 8:
            TournamentCtlr.add_player_to_tournament(
                self, tournament_players_id_list, tournament_id)
            # load tournament_players_id_list into DB
            Tournament.update_tournament_players_id_list(
                self,
                tournament_players_id_list,
                tournament_id
                )
        RoundView.display_players_list_full()
        return tournament_players_id_list

    def add_a_player_to_a_tournament(self):
        """ add any player to any tournament"""
        tournament_id = TournamentCtlr.request_tournament_id(self)

        db_all_t = TinyDB('db_all_t.json')
        Tournament.all_tournaments_db = db_all_t.table('all_tournaments_db')
        db = TinyDB('db'+str(tournament_id)+'.json')
        Tournament.tournaments_db = db.table('tournaments_db')

        tournament_players_list = []
        tournament_players_id_list = []
        tournament_players_list = (Tournament.tournaments_db.get(
            doc_id=tournament_id))['t_players_list']

        for id in tournament_players_list:
            tournament_players_id_list.append(id)

        if len(tournament_players_id_list) < 8:
            """tournament_id = (Tournament.tournaments_db.get(
                Thetournmt.t_name == tournament_name))['t_id']"""
            TournamentCtlr.add_player_to_tournament(
                self, tournament_players_id_list, tournament_id)
            while len(tournament_players_id_list) < 8:
                TournamentView.ask_for_player_inclusion()
                add_pl = input()
                if add_pl == 'O':
                    TournamentCtlr.add_player_to_tournament(
                        self, tournament_players_id_list, tournament_id)
                else:
                    return tournament_players_id_list
        else:
            TournamentView.display_t_players_list_is_full()
        return tournament_players_id_list

    def add_player_to_tournament(self, tournament_players_id_list,
                                 tournament_id):
        """add a new or DB existing player to tournament_players_id_list"""
        requested_player_id = PlayerController.request_player(self)
        # if player is new, launch its creation and add it to tournament
        if requested_player_id is None:
            print("Pour l'ajouter, merci de saisir à nouveau : ")
            new_player = PlayerController.create_new_player(
                self, tournament_id, player_id=0)
            db = TinyDB('db'+str(tournament_id)+'.json')
            Player.players_db = db.table('players_db')
            Theplayer = Query()
            new_player_id = (Player.players_db.get(
                (
                 Theplayer.p_name == new_player['p_name']
                ) & (
                 Theplayer.p_firstname == new_player['p_firstname']
                )
            )).doc_id
            tournament_players_id_list.append(new_player_id)
            Tournament.update_tournament_players_id_list(
                self, tournament_players_id_list, tournament_id)
            Save_and_load_View.ask_programm_saving(self)
            prog_saving = input()
            if prog_saving == 'O':
                Save_and_load_Ctrl.save_program(self)
            else:
                pass
        # if player in global DB, add it to tournament
        else:
            db_all_t = TinyDB('db_all_t.json')
            Player.all_players_db = db_all_t.table('all_players_db')
            requested_player = Player.all_players_db.get(
                doc_id=requested_player_id)

            db = TinyDB('db'+str(tournament_id)+'.json')
            Player.players_db = db.table('players_db')
            Player.players_db.insert(requested_player)

            tournament_players_id_list.append(requested_player_id)
            Tournament.update_tournament_players_id_list(
                self, tournament_players_id_list, tournament_id)
            print(tournament_players_id_list)
            Save_and_load_View.ask_programm_saving(self)
            prog_saving = input()
            if prog_saving == 'O':
                Save_and_load_Ctrl.save_program(self)
            else:
                pass
        return tournament_players_id_list

    def update_tournament_rd_id_list(self, tournament_rounds_id_list,
                                     tournament_id):
        """update tournament_rounds_id_list in this tournament's DB"""
        Tournament.update_tournament_rounds_id_list(self,
                                                    tournament_rounds_id_list,
                                                    tournament_id)

    def create_a_tournament_round(self):
        """ create any round for a chosen tournament"""
        db_all_t = TinyDB('db_all_t.json')
        Tournament.all_tournaments_db = db_all_t.table('all_tournaments_db')
        tournament_id = TournamentCtlr.request_tournament_id(self)
        db = TinyDB('db'+str(tournament_id)+'.json')
        Tournament.tournaments_db = db.table('tournaments_db')

        # get tournament ID in global DB
        TournamentView.display_tournaments_list()
        for t in Tournament.all_tournaments_db:
            print(t['t_name'])
        RoundView.ask_tournament_name(self)
        tournament_name = input()
        Thetournmt = Query()
        tournament_id = (Tournament.all_tournaments_db.get(
            Thetournmt.t_name == tournament_name))['t_id']
        Tournament.tournament_rounds_id_list = (Tournament.tournaments_db.get(
            doc_id=tournament_id))['t_rounds_list']

        round_nb = (len(Tournament.tournament_rounds_id_list))
        if round_nb < 4:
            if round_nb >= 1:
                TournamentCtlr.create_next_round(self, tournament_id)
            else:
                TournamentCtlr.create_first_round(self, tournament_id)
        else:
            TournamentView.display_this_t_rounds_already_created()

    def create_first_round(self, tournament_id):
        """ create the first round of the tournament"""
        r_matches_id_list = []
        Tournament.tournament_rounds_id_list = []
        new_round = RoundController.create_new_round(
            self,
            tournament_id,
            r_matches_id_list,
            round_id=0,
            end_date_time=0,
            start_date_time=0
            )
        print(new_round.round_name + ' créé')
        # get new_round id
        Theround = Query()
        new_round_id = (Round.rounds_db.get(
            Theround.r_name == new_round.round_name
            )).doc_id
        Tournament.tournament_rounds_id_list.append(new_round_id)
        # load tournament_rd_id_list into DB
        TournamentCtlr.update_tournament_rd_id_list(
            self, Tournament.tournament_rounds_id_list, tournament_id)

        # fill 1st round matches_list and load it into DB
        round_id = new_round_id
        r_matches_id_list = TournamentCtlr.create_first_r_matches_list(
            self, tournament_id, round_id)
        # start 1st round and load start_date_and_time into DB
        RoundView.display_round_date_time_start(self)
        self.start_date_time = RoundController.start_round(self)
        RoundController.update_start_date_and_time(
            self, tournament_id, self.start_date_time, round_id)
        print(self.start_date_time)

        return round_id

    def create_next_round(self, tournament_id):
        """create the next rounds of the tournament"""
        db = TinyDB('db'+str(tournament_id)+'.json')
        Tournament.tournaments_db = db.table('tournaments_db')
        tournament_rounds_qty = (Tournament.tournaments_db.get(
            doc_id=tournament_id))['t_round_qty']
        if len(Tournament.tournament_rounds_id_list) < tournament_rounds_qty:
            r_matches_id_list = []
            new_round = RoundController.create_new_round(
                self,
                tournament_id,
                r_matches_id_list,
                round_id=0,
                end_date_time=0,
                start_date_time=0,
                )
            print(new_round.round_name + ' créé')

            # get new_round id
            Theround = Query()
            new_round_id = (Round.rounds_db.get(
                Theround.r_name == new_round.round_name
                )).doc_id
            Tournament.tournament_rounds_id_list.append(new_round_id)
            TournamentCtlr.update_tournament_rd_id_list(
                self, Tournament.tournament_rounds_id_list, tournament_id)

            # fill matches_list
            round_id = new_round_id
            r_matches_id_list = TournamentCtlr.create_next_round_matches_list(
                self, tournament_id, round_id)
            # start round
            RoundView.display_round_date_time_start(self)
            self.start_date_time = RoundController.start_round(self)
            RoundController.update_start_date_and_time(
                self, tournament_id, self.start_date_time, round_id)
            print(self.start_date_time)

        else:
            TournamentView.display_rounds_list_full(self)
        return round_id

    def create_first_r_matches_list(self, tournament_id, round_id):
        """create matches for first round"""
        Round.r_matches_id_list = []
        rank_sorted_p_list = TournamentCtlr.sort_tournament_players_list_by_rank(
            self, tournament_id
            )
        matches_qty = len(rank_sorted_p_list)/2
        for i in range(0, int(matches_qty)):
            match_player1 = rank_sorted_p_list[i]['p_id']
            match_player2 = rank_sorted_p_list[i+int(matches_qty)]['p_id']
            # create a match and get back its id
            new_m_id = MatchController.create_new_match(self,
                                                        tournament_id,
                                                        match_player1,
                                                        match_player2,
                                                        match_id=0,
                                                        player1_score=0,
                                                        player2_score=0)
            Round.r_matches_id_list.append(new_m_id)
            Round.update_r_matches_list(self, tournament_id, round_id,
                                        Round.r_matches_id_list)

        TournamentView.display_first_r_matches_created()
        rank_sorted_p_list.clear()
        return Round.r_matches_id_list

    def sort_tournament_players_list_by_rank(self, tournament_id):
        """sort by rank tournament players list"""
        db = TinyDB('db'+str(tournament_id)+'.json')
        Player.players_db = db.table('players_db')

        # get the list of players to be sorted
        self.tournament_players_id_list = (Tournament.tournaments_db.get(
            doc_id=tournament_id))['t_players_list']
        t_full_players_list = []
        for pl_id in self.tournament_players_id_list:  # doc_ids
            t_full_player = Player.players_db.get(doc_id=pl_id)
            t_full_players_list.append(t_full_player)

        # sort the players
        rank_sorted_p_list = sorted(t_full_players_list,
                                    key=lambda k: k['p_rank'])
        t_full_players_list.clear()
        return rank_sorted_p_list

    def create_next_round_matches_list(self, tournament_id, round_id):
        """ create matches for round > 1 """
        Round.r_matches_id_list = []
        next_round_p_pairs_list = TournamentCtlr.compare_matches_p_pairs(
            self, tournament_id)
        matches_qty = len(next_round_p_pairs_list)
        for i in range(0, int(matches_qty)):
            match_player1 = next_round_p_pairs_list[i][0]  # player1 doc_id
            match_player2 = next_round_p_pairs_list[i][1]
            new_m_id = MatchController.create_new_match(
                self,
                tournament_id,
                match_player1,  # player1 doc_id
                match_player2,  # i+1 = next player
                match_id=0,
                player1_score=0,
                player2_score=0
                )
            Round.r_matches_id_list.append(new_m_id)
            Round.update_r_matches_list(self, tournament_id, round_id,
                                        Round.r_matches_id_list)
        next_round_p_pairs_list.clear()
        return Round.r_matches_id_list

    def sort_t_players_id_list_by_points(self, tournament_id):
        """ get tournament players list sorted by rank and total points """
        rank_sorted_p_list = TournamentCtlr.sort_tournament_players_list_by_rank(
            self, tournament_id)

        points_sorted_p_list = sorted(rank_sorted_p_list,
                                      key=lambda k: k['p_total_points'],
                                      reverse=True)

        points_sorted_p_id_list = []
        for p in points_sorted_p_list:
            points_sorted_p_id_list.append(p['p_id'])
        TournamentView.display_players_sorted_rank_n_points()
        rank_sorted_p_list.clear()
        return points_sorted_p_id_list  # players'doc_ids

    def create_test_players_pair(self, i, points_sorted_p_id_list):
        """create pair of players to have its uniqueness tested"""
        test_pair = [points_sorted_p_id_list[0],
                     points_sorted_p_id_list[i]]
        return test_pair

    def create_prev_matches_players_id_list(self, tournament_id):
        """List the id of previous matches players"""
        db = TinyDB('db'+str(tournament_id)+'.json')
        Match.matches_db = db.table('matches_db')

        # get list of previous matches pairs of players
        this_tournament = Tournament.tournaments_db.get(doc_id=tournament_id)
        tournmt_r_id_list = this_tournament['t_rounds_list']
        rd_match_id_list = []
        for item in tournmt_r_id_list:
            rd_match_id = (Round.rounds_db.get(doc_id=item)
                           )['rnd_matches_list']
            rd_match_id_list.append(rd_match_id)
        del rd_match_id_list[-1]  # del empty list (new round)

        i = len(rd_match_id_list)
        id_matches_list = []

        for j in range(0, i):
            for k in rd_match_id_list[j]:
                id_matches_list.append(k)

        m_list = []
        for m in id_matches_list:
            prev_matches = Match.matches_db.get(doc_id=m)
            m_list.append(prev_matches)

        nb_prev_matchs = len(m_list)
        previous_pairs_list = []
        for n in range(0, nb_prev_matchs):
            previous_pairs_list.append([m_list[n]['chess_player1'],  # doc_id
                                        m_list[n]['chess_player2']])
        return previous_pairs_list

    def compare_matches_p_pairs(self, tournament_id):
        """check players pairs to get uniq players players"""
        points_sorted_p_id_list = TournamentCtlr.sort_t_players_id_list_by_points(
            self, tournament_id)

        TournamentView.please_wait()
        next_round_p_pairs_list = []  # list of next matches pairs of players
        previous_pairs_list = TournamentCtlr.create_prev_matches_players_id_list(
            self, tournament_id)

        i = 1
        while len(points_sorted_p_id_list) > 0:
            testing_pair = TournamentCtlr.create_test_players_pair(
                self, i, points_sorted_p_id_list
                )
            if testing_pair in previous_pairs_list:
                if len(points_sorted_p_id_list) < 4:
                    next_round_p_pairs_list.append(testing_pair)
                    return next_round_p_pairs_list
                else:
                    i += 1
                    testing_pair = TournamentCtlr.create_test_players_pair(
                        self, i, points_sorted_p_id_list
                        )
            else:
                # UNIQUE pair of players to be added to next round matches
                next_round_p_pairs_list.append(testing_pair)

                # update points_sorted_p_id_list (avoid re-testing players)
                del points_sorted_p_id_list[0]
                del points_sorted_p_id_list[i-1]

                if len(points_sorted_p_id_list) > 0:
                    # new testing_pair:
                    i = 1
                    testing_pair = TournamentCtlr.create_test_players_pair(
                        self, i, points_sorted_p_id_list
                        )
                else:
                    return next_round_p_pairs_list
        # print('next_round_p_pairs_list')  # Check
        # print(next_round_p_pairs_list)

        self.previous_pairs_list.clear()
        points_sorted_p_id_list.clear()
        return next_round_p_pairs_list

    def closing_this_round(self, tournament_id, round_id):
        """Close current round by adding round_end_date_time"""
        RoundView.display_round_date_time_end(self)
        end_date_time = RoundController.close_round(self,)
        # load round_end_date_time into DB
        Round.update_round_end_date_time(self, tournament_id, round_id,
                                         end_date_time)
        print(end_date_time)
        return end_date_time

    def closing_a_round(self):
        """close any round"""
        tournament_id = TournamentCtlr.request_tournament_id(self)
        round_id = TournamentCtlr.request_round_id(self, tournament_id)
        RoundView.display_round_date_time_end(self)
        end_date_time = RoundController.close_round(self)
        # load round_end_date_time into DB
        Round.update_round_end_date_time(self, tournament_id, round_id,
                                         end_date_time)
        print(end_date_time)
        return end_date_time

    def updating_this_r_scores(self, tournament_id, round_id):
        """update matches scores of current round"""
        time.sleep(2)
        db = TinyDB('db'+str(tournament_id)+'.json')
        Match.matches_db = db.table('matches_db')

        r_matches_id_list = (Round.rounds_db.get(doc_id=round_id)
                             )['rnd_matches_list']
        nbr_matches = len(r_matches_id_list)
        for i in range(0, int(nbr_matches)):

            player1_id = (Match.matches_db.get(doc_id=r_matches_id_list[i])
                          )['chess_player1']
            player2_id = (Match.matches_db.get(doc_id=r_matches_id_list[i])
                          )['chess_player2']
            player1_score = TournamentCtlr.ask_player1_score(
                  self, tournament_id, player1_id, player2_id)
            player2_score = TournamentCtlr.ask_player2_score(
                  self, tournament_id, player1_id, player2_id)

            TournamentCtlr.update_player_points_qty(
                self, player1_id, player2_id, player1_score, player2_score)

            # update matches_db
            match_id = r_matches_id_list[i]
            Match.update_players_scores(self, tournament_id, match_id,
                                        player1_score, player2_score)
            Save_and_load_View.ask_programm_saving(self)
            prog_saving = input()
            if prog_saving == 'O':
                Save_and_load_Ctrl.save_program(self)
            else:
                pass

    def update_matches_scores_players_points(self):
        """ update a round matches players'score and players'total points"""
        tournament_id = TournamentCtlr.request_tournament_id(self)
        round_id = TournamentCtlr.request_round_id(self, tournament_id)

        db = TinyDB('db'+str(tournament_id)+'.json')
        Round.rounds_db = db.table('rounds_db')
        Match.matches_db = db.table('matches_db')
        Player.players_db = db.table('players_db')

        # check if scores already updated :
        round_matches_id = ((Round.rounds_db.get(
            doc_id=round_id))['rnd_matches_list'])
        matches_id_list = []
        for m_id in round_matches_id:
            matches_id_list.append(m_id)

        matches_list = []
        scores_list = []
        for m in matches_id_list:
            a_match = Match.matches_db.get(doc_id=m)
            matches_list.append(a_match)

            score_pl1 = Match.matches_db.get(doc_id=m)['score_player1']
            scores_list.append(score_pl1)
            score_pl2 = Match.matches_db.get(doc_id=m)['score_player1']
            scores_list.append(score_pl2)
        scores_sum = sum(scores_list)

        if scores_sum > 0:
            TournamentView.ask_overwrite_scores()
            overwrite_scores = input()
            if overwrite_scores == 'N':
                pass
            else:
                TournamentCtlr.updating_this_r_scores(self, tournament_id,
                                                      round_id)
        else:
            TournamentCtlr.updating_this_r_scores(self, tournament_id,
                                                  round_id)

        Save_and_load_View.ask_programm_saving(self)
        prog_saving = input()
        if prog_saving == 'O':
            Save_and_load_Ctrl.save_program(self)
        else:
            pass

    def request_tournament_id(self):
        """get a tournament id from its name"""
        db_all_t = TinyDB('db_all_t.json')
        Tournament.all_tournaments_db = db_all_t.table('all_tournaments_db')

        TournamentView.display_tournaments_list()
        for t in Tournament.all_tournaments_db:
            print(t['t_name'])
        RoundView.ask_tournament_name(self)
        tournament_name = input()
        Thetournmt = Query()
        chosen_tournament = (Tournament.all_tournaments_db.get(
            Thetournmt.t_name == tournament_name))
        tournament_id = chosen_tournament.doc_id
        return tournament_id

    def request_round_id(self, tournament_id):
        """get a round id from the round name"""
        db = TinyDB('db'+str(tournament_id)+'.json')
        Tournament.tournaments_db = db.table('tournaments_db')
        Round.rounds_db = db.table('rounds_db')
        Thetournmt = Query()
        rounds_id_list = (Tournament.tournaments_db.get(
            Thetournmt.t_id == tournament_id))['t_rounds_list']

        TournamentView.display_t_rounds_list()
        for rd_id in rounds_id_list:
            round_name = (Round.rounds_db.get(doc_id=rd_id))['r_name']
            print(round_name)
        RoundView.ask_round_name(self)
        round_name_req = input()
        Theround = Query()
        round_id = (Round.rounds_db.get(Theround.r_name == round_name_req)
                    )['r_id']
        return round_id

    def ask_player1_score(self, tournament_id, player1_id, player2_id):
        """ get player1 's score"""
        # print "match PLAYER1-NAME / PLAYER2-NAME"
        # get chess_players names
        db = TinyDB('db'+str(tournament_id)+'.json')
        Player.players_db = db.table('players_db')

        name_pl1 = Player.players_db.get(doc_id=player1_id)['p_name']
        name_pl2 = Player.players_db.get(doc_id=player2_id)['p_name']
        print('Match ' + name_pl1 + " contre " + name_pl2)
        print('1er joueur : ' + name_pl1)

        player1_score = float(input('Saisissez son score (0 ou 0.5 ou 1) : '))
        return player1_score

    def ask_player2_score(self, tournament_id, player1_id, player2_id):
        """ get player2 's score"""
        # print "match PLAYER1-NAME / PLAYER2-NAME"
        # get chess_players names
        db = TinyDB('db'+str(tournament_id)+'.json')
        Player.players_db = db.table('players_db')

        name_pl1 = Player.players_db.get(doc_id=player1_id)['p_name']
        name_pl2 = Player.players_db.get(doc_id=player2_id)['p_name']
        print('Match ' + name_pl1 + " contre " + name_pl2)
        print('2eme joueur : ' + name_pl2)

        player2_score = float(input('Saisissez son score (0 ou 0.5 ou 1) : '))
        return player2_score

    def update_player_points_qty(self, player1_id, player2_id, player1_score,
                                 player2_score):
        """ Update players total points"""
        pl1_points = (Player.players_db.get(doc_id=player1_id)
                      )['p_total_points']
        pl2_points = (Player.players_db.get(doc_id=player2_id)
                      )['p_total_points']

        pl1_new_points = pl1_points + player1_score
        Player.players_db.update({'p_total_points': pl1_new_points},
                                 doc_ids=[player1_id])
        pl2_new_points = pl2_points + player2_score
        Player.players_db.update({'p_total_points': pl2_new_points},
                                 doc_ids=[player2_id])


class RoundController:
    def __init__(self, r_matches_id_list):
        self.r_matches_id_list = r_matches_id_list

    def create_new_round(self, tournament_id, r_matches_id_list, round_id=0,
                         end_date_time=0, start_date_time=0):
        """ create a round """
        round = Round(round_id,
                      RoundController.give_round_name(self, tournament_id),
                      r_matches_id_list,
                      start_date_time,
                      end_date_time)
        round.create_round(tournament_id)
        self.round_id = Round.update_round_id(self, tournament_id)

        return round

    def give_round_name(self, tournament_id):
        """ get or ask round name"""
        this_tourney = Tournament.tournaments_db.get(doc_id=tournament_id)
        round_nbr = len(this_tourney['t_rounds_list'])
        round_name = f'{"Round"}{round_nbr+1}'
        return round_name

    def start_round(self):
        """generate date & time for the begining of a round"""
        start_date_and_time = str(datetime.now())
        return start_date_and_time

    def update_start_date_and_time(self, tournament_id,
                                   start_date_time, round_id):
        """ update round start date_and_time in DB """
        Round.update_start_date_time(self, tournament_id,
                                     start_date_time, round_id)

    def close_round(self):
        """set end date and time"""
        end_date_time = str(datetime.now())
        return end_date_time

    def update_round_end_date_time(self, round_id, end_date_time):
        """ update round end date_and_time in DB """
        Round.update_round_end_date_time(self, round_id, end_date_time)


class MatchController:
    def __init__(self, match_player1, match_player2):
        self.match_player1 = match_player1
        self.match_player2 = match_player2

    def create_new_match(self, tournament_id, match_player1, match_player2, match_id=0,
                         player1_score=0, player2_score=0):
        """create one match"""
        match = Match(match_id,
                      match_player1,  # player's doc_id
                      match_player2,
                      player1_score,  # player's doc_id
                      player2_score)
        match.create_match(tournament_id)
        self.match_id = Match.update_match_id(self, tournament_id)
        return self.match_id


class PlayerController:
    def __init__(self):
        self.player_view = PlayerView()

    def create_new_player(self, tournament_id, player_id=0):
        """create one player"""
        player = Player(
            player_id,
            PlayerController.ask_player_name(self),
            PlayerController.ask_player_first_name(self),
            PlayerController.ask_player_birth_date(self),
            PlayerController.ask_player_gender(self),
            PlayerController.ask_player_ranking(self),
            player_points_qty=0
        )
        player.create_player()
        new_player_id = Player.update_player_id(self)
        new_player = Player.all_players_db.get(doc_id=new_player_id)

        db = TinyDB('db'+str(tournament_id)+'.json')
        Player.players_db = db.table('players_db')
        Player.players_db.insert(new_player)

        return new_player

    def create_new_player_in_db_all(self, player_id=0):
        """create one player in global DB"""
        player = Player(
            player_id,
            PlayerController.ask_player_name(self),
            PlayerController.ask_player_first_name(self),
            PlayerController.ask_player_birth_date(self),
            PlayerController.ask_player_gender(self),
            PlayerController.ask_player_ranking(self),
            player_points_qty=0
        )
        player.create_player()
        Player.update_player_id(self)

    def ask_player_name(self):
        """ get player_name from User through player_view """
        PlayerView.ask_player_name()
        player_name = input()
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
        player_rank = int(input())
        return player_rank

    def update_players_ranking(self):
        """ update player rank with User's information"""
        player_id = PlayerController.request_player(self)
        if player_id is None:
            pass
        else:
            PlayerView.ask_player_ranking()
            player_rank = int(input())
            new_player_rank = Player.update_playr_rank(self, player_id,
                                                       player_rank)
            return new_player_rank

    def request_player(self):
        """search a player (by his name & firstname) into db"""
        db_all_t = TinyDB('db_all_t.json')
        Player.all_players_db = db_all_t.table('all_players_db')

        search_p_name = PlayerController.ask_player_name(self)
        search_p_first_name = PlayerController.ask_player_first_name(self)
        Theplayer = Query()
        searched_player = Player.all_players_db.get(
            (
                Theplayer.p_name == search_p_name
            ) & (
                Theplayer.p_firstname == search_p_first_name
                )
            )
        print(searched_player)
        if searched_player is None:
            PlayerView.display_absent_player()
            time.sleep(2)
            return searched_player
        else:
            return searched_player.doc_id


class ReportingController:
    def __init__(self):
        db = TinyDB('db.json')
        Tournament.tournaments_db = db.table('tournaments_db')
        Round.rounds_db = db.table('rounds_db')
        Match.matches_db = db.table('matches_db')
        Player.players_db = db.table('players_db')

    """ List of all participants
    1/ by alphabetical order
    2/ by ranking
    """

    def display_all_players_reporting(self):
        db_all_t = TinyDB('db_all_t.json')
        Player.Theplayer = Query()
        Player.all_players_db = db_all_t.table('all_players_db')

        all_players_list = []
        for pl in Player.all_players_db:
            all_players_list.append(pl)

        ReportingView.display_all_players_reporting(self)
        sorting_choice = input()

        if sorting_choice == '1':
            ReportingView.display_all_players_alphabetical_order(self)
            """Liste de tous les acteurs triés par ordre alphabétique"""
            pl_list = (len(all_players_list))
            players_name_list = []
            for i in range(0, pl_list):
                players_name_list.append(all_players_list[i]['p_name'])
            players_name_list.sort
            print(players_name_list)
            time.sleep(2)

            # details :
            ReportingView.display_all_players_alphabetical_order_details(self)
            for p in players_name_list:
                print(Player.all_players_db.search(where('p_name') == p))
            time.sleep(5)

        else:
            ReportingView.display_all_players_by_rank(self)
            rank_sorted_all_players_list = sorted(all_players_list,
                                                  key=lambda k: k['p_rank'])

            pl_list = (len(rank_sorted_all_players_list))
            players_name_list = []
            for j in range(0, pl_list):
                players_name_list.append(
                    rank_sorted_all_players_list[j]['p_name'])
            print(players_name_list)
            time.sleep(2)

            ReportingView.display_all_players_by_rank_details(self)
            for j in rank_sorted_all_players_list:
                print(j)
            time.sleep(5)

    """ List of all players of ONE tournament
    1/ by alphabetical order
    2/ by ranking
    """
    def display_tournament_players(self):
        ReportingView.one_tournament_players_list(self)
        ReportingView.display_tournaments_list(self)
        tournament_id = TournamentCtlr.request_tournament_id(self)
        db = TinyDB('db'+str(tournament_id)+'.json')
        Tournament.tournaments_db = db.table('tournaments_db')
        Player.players_db = db.table('players_db')

        tournament_requested = (Tournament.tournaments_db.get(
            doc_id=tournament_id))

        tournament_pl_id_list = []
        for t in (tournament_requested['t_players_list']):
            tournament_pl_id_list.append(t)

        tournament_players_list = []
        for pl_id in tournament_pl_id_list:
            tournament_pl = Player.players_db.get(doc_id=pl_id)
            tournament_players_list.append(tournament_pl)

        ReportingView.display_chosen_tournament_players(self)
        sorting_choice = input()
        if sorting_choice == '1':
            ReportingView.display_all_players_alphabetical_order(self)
            players_name_list = []
            for i in range(0, len(tournament_players_list)):
                players_name_list.append(tournament_players_list[i]['p_name'])
            players_name_list.sort
            print(players_name_list)
            time.sleep(5)
            # details :
            ReportingView.display_all_players_alphabetical_order_details(self)
            for p in players_name_list:
                print(Player.players_db.search(where('p_name') == p))
            time.sleep(5)

        else:
            ReportingView.display_all_players_by_rank(self)
            rank_sorted_tournament_players_list = sorted(
                tournament_players_list, key=lambda k: k['p_rank'])

            pl_list = (len(rank_sorted_tournament_players_list))
            players_name_list = []
            for j in range(0, pl_list):
                players_name_list.append(
                    rank_sorted_tournament_players_list[j]['p_name'])
            print(players_name_list)
            time.sleep(5)
            ReportingView.display_all_players_by_rank_details(self)
            for j in rank_sorted_tournament_players_list:
                print(j)
            time.sleep(5)

    """ List of all tournaments """
    def display_all_tournaments(self):
        db_all_t = TinyDB('db_all_t.json')
        Tournament.all_tournaments_db = db_all_t.table('all_tournaments_db')

        ReportingView.all_tournaments_list(self)
        ReportingView.display_tournaments_list(self)
        for t in Tournament.all_tournaments_db:
            print(t['t_name'])
        time.sleep(2)

        ReportingView.display_tournaments_list_details(self)
        tournaments_id_list = []
        for tournament in Tournament.all_tournaments_db:
            tournaments_id_list.append(tournament.doc_id)

            tournament_id = tournament.doc_id

            db = TinyDB('db'+str(tournament_id)+'.json')
            Tournament.tournaments_db = db.table('tournaments_db')
            t_details = Tournament.tournaments_db.get(doc_id=tournament_id)
            print(t_details)

        time.sleep(5)

    """ List of all rounds of ONE tournament """
    def tournament_all_rounds(self):
        ReportingView.one_tournament_rounds_list(self)
        tournament_id = TournamentCtlr.request_tournament_id(self)
        db = TinyDB('db'+str(tournament_id)+'.json')
        Tournament.tournaments_db = db.table('tournaments_db')
        Round.rounds_db = db.table('rounds_db')

        chosen_tournament = (Tournament.tournaments_db.get(
            doc_id=tournament_id))

        ReportingView.chosen_t_rounds_names_list(self)
        t_rounds_list = []
        t_round_id_list = (chosen_tournament['t_rounds_list'])
        for rd_id in (t_round_id_list):
            t_round = Round.rounds_db.get(doc_id=rd_id)
            t_rounds_list.append(t_round)
            print(t_round['r_name'])
        time.sleep(2)

        ReportingView.chosen_t_rounds_details(self)
        for t in (t_rounds_list):
            print(t)
        time.sleep(5)

    """ List of all matches of ONE tournament """

    def tournament_all_matches(self):
        ReportingView.one_tournament_matches_list(self)
        tournament_id = TournamentCtlr.request_tournament_id(self)
        db = TinyDB('db'+str(tournament_id)+'.json')
        Tournament.tournaments_db = db.table('tournaments_db')
        Round.rounds_db = db.table('rounds_db')
        Match.matches_db = db.table('matches_db')
        Player.players_db = db.table('players_db')

        chosen_tournament = (Tournament.tournaments_db.get(
            doc_id=tournament_id))
        matches_id_list = []
        t_rounds_id_list = (chosen_tournament['t_rounds_list'])  # doc_id

        if len(t_rounds_id_list) < 1:
            print("Aucun tour n'a été lancé pour ce tournoi")
            pass
        else:
            for rd_id in t_rounds_id_list:
                one_round_matches_id = ((Round.rounds_db.get(
                    doc_id=rd_id))['rnd_matches_list'])

                for m_id in one_round_matches_id:
                    matches_id_list.append(m_id)

            ReportingView.chosen_round_matches_list(self)
            matches_list = []
            for m in matches_id_list:
                a_match = Match.matches_db.get(doc_id=m)
                matches_list.append(a_match)

                chess_player1 = Match.matches_db.get(
                    doc_id=m)['chess_player1']
                name_pl1 = Player.players_db.get(
                    doc_id=chess_player1)['p_name']
                score_pl1 = Match.matches_db.get(doc_id=m)['score_player1']

                chess_player2 = Match.matches_db.get(
                    doc_id=m)['chess_player2']
                name_pl2 = Player.players_db.get(
                    doc_id=chess_player2)['p_name']
                score_pl2 = Match.matches_db.get(doc_id=m)['score_player1']
                print('match id ' + str(m)
                      + ' ' + str(name_pl1)
                      + ' score: ' + str(score_pl1)
                      + ' contre ' + str(name_pl2)
                      + ' score: ' + str(score_pl2))
        time.sleep(5)


class Save_and_load_Ctrl:
    def __init__(self):
        pass

    def save_program(self):
        # save all data of the whole program
        Save_and_load.save_in_db_backup(self)

    def load_progam(self):
        # load a backup of the program
        Save_and_load.load_db_backup(self)
