from controllers.matchcontroller import MatchCtrlr
from controllers.playercontroller import PlayerCtrlr
from controllers.roundcontroller import RoundCtrlr
from models.matchmodel import Match
from models.playermodel import Player
from models.roundmodel import Round
from models.tournamentmodel import Tournament
from views.playerviews import PlayerViews
from views.roundviews import RoundViews
from views.tournamentviews import TournamentViews
from tinydb import TinyDB, where, Query


class TournamentCtrlr:
    def __init__(self, tournament_id):
        self.tournament_view = TournamentViews()
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

    def dis_bonjour_tctrl(self):  #TEST INITIAL - A SUPPRIMER
        print ('Bonjour de la classe TournamentCtrlr - fichier tournamentcontroller')

    def read_a_tournament(self):
        tournament_id = TournamentCtrlr.request_tournament_id(self)
        Tournament.read_tournament(self, tournament_id)

    def create_new_tournament(self, tournament_id=0, tournament_rounds_qty=4):
        """create a tournament"""
        tournament = Tournament(
            tournament_id,
            TournamentCtrlr.ask_tournament_name(self),
            TournamentCtrlr.ask_tournament_place(self),
            TournamentCtrlr.ask_tournament_date(self),
            TournamentCtrlr.ask_tournament_description(self),
            TournamentCtrlr.ask_time_control(self),
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

        TournamentCtrlr.confirm_tournament_rounds_qty(self, tournament_id)
        return tournament_id

    def ask_tournament_name(self):
        """ask User tournament name"""
        TournamentViews.ask_tournament_name()
        tournament_name = input()
        return tournament_name

    def ask_tournament_place(self):
        """ask User tournament place"""
        TournamentViews.ask_tournament_place()
        tournament_place = input()
        return tournament_place

    def ask_tournament_date(self):
        """ask User tournament date(s)"""
        TournamentViews.ask_tournament_date()
        tournament_date = input()
        return tournament_date

    def ask_tournament_description(self):
        """ask User tournament description and comments"""
        TournamentViews.ask_tournament_description()
        tournament_description = input()
        return tournament_description

    def ask_time_control(self):
        """ask User time control"""
        TournamentViews.ask_time_control()
        time_control = input()
        return time_control

    def confirm_tournament_rounds_qty(self, tournament_id):
        """Get tournament_rounds_qty confirmation from User"""
        TournamentViews.ask_tournament_rounds_qty()
        tournament_rounds_qty = int(input())
        # load tournament_rounds_qty update into DB
        Tournament.update_tournament_rounds_qty(self, tournament_rounds_qty,
                                                tournament_id)
        return tournament_rounds_qty

    def create_tournament_players_id_list(self, tournament_id):  # doc_ids
        """create this tournament's list of 8 players"""
        tournament_players_id_list = []
        while len(tournament_players_id_list) < 8:
            TournamentCtrlr.add_player_to_tournament(
                self, tournament_players_id_list, tournament_id)
            # load tournament_players_id_list into DB
            Tournament.update_tournament_players_id_list(
                self,
                tournament_players_id_list,
                tournament_id
                )
        RoundViews.display_players_list_full()
        return tournament_players_id_list

    def add_a_player_to_a_tournament(self):
        """ add any player to any tournament"""
        tournament_id = TournamentCtrlr.request_tournament_id(self)

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
            TournamentCtrlr.add_player_to_tournament(
                self, tournament_players_id_list, tournament_id)
            while len(tournament_players_id_list) < 8:
                TournamentViews.ask_for_player_inclusion()
                add_pl = input()
                if add_pl == 'O':
                    TournamentCtrlr.add_player_to_tournament(
                        self, tournament_players_id_list, tournament_id)
                else:
                    return tournament_players_id_list
        else:
            TournamentViews.display_t_players_list_is_full()
        return tournament_players_id_list

    def add_player_to_tournament(self, tournament_players_id_list,
                                 tournament_id):
        """add a new or DB existing player to tournament_players_id_list"""
        requested_player_id = PlayerCtrlr.request_player(self)
        # if player is new, launch its creation and add it to tournament
        if requested_player_id is None:
            print("Pour l'ajouter, merci de saisir à nouveau : ")
            new_player = PlayerCtrlr.create_new_player(
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
            TournamentViews.separator()
        return tournament_players_id_list

    def update_tournament_rd_id_list(self, tournament_rounds_id_list,
                                     tournament_id):
        """update tournament_rounds_id_list in this tournament's DB"""
        Tournament.update_tournament_rounds_id_list(self,
                                                    tournament_rounds_id_list,
                                                    tournament_id)

    def create_a_tournament_round(self):
        """ create any round for a chosen tournament""" 
        tournament_id = TournamentCtrlr.request_tournament_id(self)
        
        db = TinyDB('db'+str(tournament_id)+'.json')
        Tournament.tournaments_db = db.table('tournaments_db')
        Tournament.tournament_rounds_id_list = (Tournament.tournaments_db.get(
            doc_id=tournament_id))['t_rounds_list']

        round_nb = (len(Tournament.tournament_rounds_id_list))
        if round_nb < 4:
            if round_nb >= 1:
                TournamentCtrlr.create_next_round(self, tournament_id)
            else:
                TournamentCtrlr.create_first_round(self, tournament_id)
        else:
            TournamentViews.display_this_t_rounds_already_created()

    def create_first_round(self, tournament_id):
        """ create the first round of the tournament"""
        r_matches_id_list = []
        Tournament.tournament_rounds_id_list = []
        new_round = RoundCtrlr.create_new_round(
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
        TournamentCtrlr.update_tournament_rd_id_list(
            self, Tournament.tournament_rounds_id_list, tournament_id)

        # fill 1st round matches_list and load it into DB
        round_id = new_round_id
        r_matches_id_list = TournamentCtrlr.create_first_r_matches_list(
            self, tournament_id, round_id)
        # start 1st round and load start_date_and_time into DB
        RoundViews.display_round_date_time_start()
        self.start_date_time = RoundCtrlr.start_round(self)
        RoundCtrlr.update_start_date_and_time(
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
            new_round = RoundCtrlr.create_new_round(
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
            TournamentCtrlr.update_tournament_rd_id_list(
                self, Tournament.tournament_rounds_id_list, tournament_id)

            # fill matches_list
            round_id = new_round_id
            r_matches_id_list = TournamentCtrlr.create_next_round_matches_list(
                self, tournament_id, round_id)
            # start round
            RoundViews.display_round_date_time_start()
            self.start_date_time = RoundCtrlr.start_round(self)
            RoundCtrlr.update_start_date_and_time(
                self, tournament_id, self.start_date_time, round_id)
            print(self.start_date_time)
        else:
            TournamentViews.display_rounds_list_full()
        return round_id

    def create_first_r_matches_list(self, tournament_id, round_id):
        """create matches for first round"""
        Round.r_matches_id_list = []
        rank_sorted_p_list = TournamentCtrlr.sort_tournament_players_list_by_rank(
            self, tournament_id
            )
        matches_qty = len(rank_sorted_p_list)/2
        for i in range(0, int(matches_qty)):
            match_player1 = rank_sorted_p_list[i]['p_id']
            match_player2 = rank_sorted_p_list[i+int(matches_qty)]['p_id']
            # create a match and get back its id
            new_m_id = MatchCtrlr.create_new_match(self,
                                                        tournament_id,
                                                        match_player1,
                                                        match_player2,
                                                        match_id=0,
                                                        player1_score=0,
                                                        player2_score=0)
            Round.r_matches_id_list.append(new_m_id)
            Round.update_r_matches_list(self, tournament_id, round_id,
                                        Round.r_matches_id_list)

        TournamentViews.display_first_r_matches_created()
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
        next_round_p_pairs_list = TournamentCtrlr.compare_matches_p_pairs(
            self, tournament_id)
        matches_qty = len(next_round_p_pairs_list)
        for i in range(0, int(matches_qty)):
            match_player1 = next_round_p_pairs_list[i][0]  # player1 doc_id
            match_player2 = next_round_p_pairs_list[i][1]
            new_m_id = MatchCtrlr.create_new_match(
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
        rank_sorted_p_list = TournamentCtrlr.sort_tournament_players_list_by_rank(
            self, tournament_id)

        points_sorted_p_list = sorted(rank_sorted_p_list,
                                      key=lambda k: k['p_total_points'],
                                      reverse=True)

        points_sorted_p_id_list = []
        for p in points_sorted_p_list:
            points_sorted_p_id_list.append(p['p_id'])
        TournamentViews.display_players_sorted_rank_n_points()
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
        points_sorted_p_id_list = TournamentCtrlr.sort_t_players_id_list_by_points(
            self, tournament_id)

        TournamentViews.please_wait()
        next_round_p_pairs_list = []  # list of next matches pairs of players
        previous_pairs_list = TournamentCtrlr.create_prev_matches_players_id_list(
            self, tournament_id)

        i = 1
        while len(points_sorted_p_id_list) > 0:
            testing_pair = TournamentCtrlr.create_test_players_pair(
                self, i, points_sorted_p_id_list
                )
            if testing_pair in previous_pairs_list:
                if len(points_sorted_p_id_list) < 4:
                    next_round_p_pairs_list.append(testing_pair)
                    return next_round_p_pairs_list
                else:
                    i += 1
                    testing_pair = TournamentCtrlr.create_test_players_pair(
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
                    testing_pair = TournamentCtrlr.create_test_players_pair(
                        self, i, points_sorted_p_id_list
                        )
                else:
                    return next_round_p_pairs_list

        self.previous_pairs_list.clear()
        points_sorted_p_id_list.clear()
        return next_round_p_pairs_list

    def closing_this_round(self, tournament_id, round_id):
        """Close current round by adding round_end_date_time"""
        RoundViews.display_round_date_time_end()
        end_date_time = RoundCtrlr.close_round(self,)
        # load round_end_date_time into DB
        Round.update_round_end_date_time(self, tournament_id, round_id,
                                         end_date_time)
        print(end_date_time)
        return end_date_time

    def closing_a_round(self):
        """close any round"""
        tournament_id = TournamentCtrlr.request_tournament_id(self)
        round_id = TournamentCtrlr.request_round_id(self, tournament_id)
        RoundViews.display_round_date_time_end()
        end_date_time = RoundCtrlr.close_round(self)
        # load round_end_date_time into DB
        Round.update_round_end_date_time(self, tournament_id, round_id,
                                         end_date_time)
        print(end_date_time)
        return end_date_time

    def updating_this_r_scores(self, tournament_id, round_id):
        """update matches scores of current round"""
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
            player1_score = TournamentCtrlr.ask_player1_score(
                  self, tournament_id, player1_id, player2_id)
            player2_score = TournamentCtrlr.ask_player2_score(
                  self, tournament_id, player1_id, player2_id)

            TournamentCtrlr.update_player_points_qty(
                self, player1_id, player2_id, player1_score, player2_score)

            # update matches_db
            match_id = r_matches_id_list[i]
            Match.update_players_scores(self, tournament_id, match_id,
                                        player1_score, player2_score)

    def update_matches_scores_players_points(self):
        """ update a round matches players'score and players'total points"""
        tournament_id = TournamentCtrlr.request_tournament_id(self)
        round_id = TournamentCtrlr.request_round_id(self, tournament_id)

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
            score_pl2 = Match.matches_db.get(doc_id=m)['score_player2']
            scores_list.append(score_pl2)
        scores_sum = sum(scores_list)

        if scores_sum > 0:
            TournamentViews.ask_overwrite_scores()
            overwrite_scores = input()
            if overwrite_scores == 'N':
                pass
            else:
                TournamentCtrlr.updating_this_r_scores(self, tournament_id,
                                                      round_id)
        else:
            TournamentCtrlr.updating_this_r_scores(self, tournament_id,
                                                  round_id)

    def request_tournament_id(self):
        """get a tournament id from its name"""
        db_all_t = TinyDB('db_all_t.json')
        Tournament.all_tournaments_db = db_all_t.table('all_tournaments_db')

        TournamentViews.display_tournaments_list()
        for t in Tournament.all_tournaments_db:
            print(t['t_name'])
        RoundViews.ask_tournament_name()
        tournament_name = input()
        Thetournmt = Query()
        chosen_tournament = (Tournament.all_tournaments_db.get(
            Thetournmt.t_name == tournament_name))
        tournament_id = chosen_tournament['t_id']  #04/03 corr .doc_id par ['t_id']
        return tournament_id

    def request_round_id(self, tournament_id):
        """get a round id from the round name"""
        db = TinyDB('db'+str(tournament_id)+'.json')
        Tournament.tournaments_db = db.table('tournaments_db')
        Round.rounds_db = db.table('rounds_db')
        Thetournmt = Query()
        rounds_id_list = (Tournament.tournaments_db.get(
            Thetournmt.t_id == tournament_id))['t_rounds_list']

        TournamentViews.display_t_rounds_list()
        for rd_id in rounds_id_list:
            round_name = (Round.rounds_db.get(doc_id=rd_id))['r_name']
            print(round_name)
        RoundViews.ask_round_name()
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
        if player1_score == 0:
            return player1_score
        elif player1_score == 0.5:
            return player1_score
        elif player1_score == 1:
            return player1_score
        else:
            TournamentViews.choice_unavailable()
            TournamentCtrlr.update_matches_scores_players_points(self)

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
        if player2_score == 0:
            return player2_score
        elif player2_score == 0.5:
            return player2_score
        elif player2_score == 1:
            return player2_score
        else:
            TournamentViews.choice_unavailable()
            TournamentCtrlr.update_matches_scores_players_points(self)
        TournamentViews.separator()
        
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

    def update_players_ranking(self):
        """ update player rank with User's information"""
        tournament_id = TournamentCtrlr.request_tournament_id(self)
        PlayerCtrlr.display_points_sorted_tournament_players(
            self, tournament_id)
        PlayerViews.ask_player_to_update_rank()
        player_id = PlayerCtrlr.request_tournament_player(self,
                                                               tournament_id)
        if player_id is None:
            pass
        else:
            PlayerViews.ask_player_ranking()
            player_rank = int(input())
            new_player_rank = Player.update_t_player_rank(self, 
                                                          tournament_id,
                                                          player_id,
                                                          player_rank)
            return new_player_rank

