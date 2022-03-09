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
from tinydb import TinyDB, Query
import time


class TournamentCtrlr:
    def __init__(self, tournament_id):
        self.tournament_view = TournamentViews()
        self.tournament_id = tournament_id

    def create_new_tournament(self, tournament_id=0, tournament_rounds_qty=4):
        """Creates a tournament and returns its identifier (id)."""
        tournament = Tournament(
            tournament_id,
            TournamentCtrlr.ask_tournament_name(self),
            TournamentCtrlr.ask_tournament_place(self),
            TournamentCtrlr.ask_tournament_date(self),
            TournamentCtrlr.ask_tournament_description(self),
            TournamentCtrlr.ask_time_control(self),
            tournament_rounds_qty,
            tournament_players_id_list=[],
            tournament_rounds_id_list=[]
        )
        tournament.create_tournament()
        new_tournament_id = Tournament.update_tournament_id(self)
        tournament_id = new_tournament_id
        TournamentCtrlr.store_new_tournament_in_database(
            self, new_tournament_id, tournament_id)
        TournamentCtrlr.confirm_tournament_rounds_qty(self, tournament_id)
        return tournament_id

    def read_a_tournament(self):
        """Display a tournament."""
        tournament_id = TournamentCtrlr.request_tournament_id(self)
        if tournament_id == 0:
            pass
        else:
            Tournament.read_tournament(self, tournament_id)
            time.sleep(2)

    def store_new_tournament_in_database(self, new_tournament_id,
                                         tournament_id):
        """Store new tournament in its own database (tournaments_db)."""
        db_all_t = TinyDB('db_all_t.json')
        Tournament.all_tournaments_db = db_all_t.table('all_tournaments_db')
        db = TinyDB('db' + str(tournament_id) + '.json')
        Tournament.tournaments_db = db.table('tournaments_db')

        new_tournament = Tournament.all_tournaments_db.get(
            doc_id=new_tournament_id)
        Tournament.tournaments_db.insert(new_tournament)

    def ask_tournament_name(self):
        """Ask User tournament name."""
        TournamentViews.ask_tournament_name()
        tournament_name = input()
        return tournament_name

    def ask_tournament_place(self):
        """Ask User tournament place."""
        TournamentViews.ask_tournament_place()
        tournament_place = input()
        return tournament_place

    def ask_tournament_date(self):
        """Ask User tournament date(s)."""
        TournamentViews.ask_tournament_date()
        tournament_date = input()
        return tournament_date

    def ask_tournament_description(self):
        """Ask User tournament description and comments."""
        TournamentViews.ask_tournament_description()
        tournament_description = input()
        return tournament_description

    def ask_time_control(self):
        """Ask User time control."""
        TournamentViews.ask_time_control()
        time_control = input()
        return time_control

    def confirm_tournament_rounds_qty(self, tournament_id):
        """Get tournament_rounds_qty confirmation from User."""
        TournamentViews.ask_tournament_rounds_qty()
        tournament_rounds_qty = int(input())
        # load tournament_rounds_qty update into database
        Tournament.update_tournament_rounds_qty(self, tournament_rounds_qty,
                                                tournament_id)
        return tournament_rounds_qty

    def create_tournament_players_id_list(self, tournament_id):
        """Create this tournament's list of 8 players and returns the list
        of the players'ids.
        """
        tournament_players_id_list = []
        while len(tournament_players_id_list) < 8:
            TournamentCtrlr.add_any_player_to_tournament(
                self, tournament_players_id_list, tournament_id)
            # load tournament_players_id_list into database
            Tournament.update_tournament_players_id_list(
                self,
                tournament_players_id_list,
                tournament_id
            )
        RoundViews.display_players_list_full()
        return tournament_players_id_list

    def add_player_to_any_tournament(self):
        """Add a player to any tournament and returns the  list of
        tournaments' players' ids (identifiers).
        """
        tournament_id = TournamentCtrlr.request_tournament_id(self)
        if tournament_id == 0:
            pass
        else:
            tournament_players_id_list = []
            tournament_players_id_list = TournamentCtrlr.get_tourney_players_id_list(
                self, tournament_id)
            if len(tournament_players_id_list) < 8:
                TournamentCtrlr.add_any_player_to_tournament(
                    self, tournament_players_id_list, tournament_id)
                while len(tournament_players_id_list) < 8:
                    TournamentViews.ask_for_player_inclusion()
                    add_pl = input()
                    if add_pl == 'OUI':
                        TournamentCtrlr.add_any_player_to_tournament(
                            self, tournament_players_id_list, tournament_id)
                    else:
                        return tournament_players_id_list
            else:
                TournamentViews.display_t_players_list_is_full()
            return tournament_players_id_list

    def get_tourney_players_id_list(self, tournament_id):
        """Get tournament's players identifiers list
        from tournament database.
        """
        db = TinyDB('db' + str(tournament_id) + '.json')
        Tournament.tournaments_db = db.table('tournaments_db')
        tournament_players_id_list = (Tournament.tournaments_db.get(
            doc_id=tournament_id))['t_players_list']
        return tournament_players_id_list

    def add_any_player_to_tournament(self, tournament_players_id_list,
                                     tournament_id):
        """Add a new or database existing player
        to tournament_players_id_list.
        """
        requested_player_id = PlayerCtrlr.request_player(self)
        if requested_player_id is None:
            TournamentCtrlr.add_tournament_a_new_player(
                self, tournament_players_id_list, tournament_id)
        else:
            TournamentCtrlr.add_tournament_existing_player(
                self, requested_player_id, tournament_players_id_list,
                tournament_id
            )
        print(str(len(tournament_players_id_list)
                  ) + ' joueur(s) ajouté(s) au tournoi')
        TournamentViews.separator()
        return tournament_players_id_list

    def add_tournament_a_new_player(self, tournament_players_id_list,
                                    tournament_id):
        """Add a new player (not in database) to the tournament."""
        PlayerViews.display_please_re_enter()
        new_player_id = PlayerCtrlr.create_new_player(
            self, tournament_id)
        tournament_players_id_list.append(new_player_id)
        Tournament.update_tournament_players_id_list(
            self, tournament_players_id_list, tournament_id)

    def add_tournament_existing_player(self, requested_player_id,
                                       tournament_players_id_list,
                                       tournament_id):
        """Add a player existing in database to the tournament."""
        db = TinyDB('db' + str(tournament_id) + '.json')
        Player.players_db = db.table('players_db')
        db_all_t = TinyDB('db_all_t.json')
        Player.all_players_db = db_all_t.table('all_players_db')

        requested_player = Player.all_players_db.get(
            doc_id=requested_player_id)
        Player.players_db.insert(requested_player)
        tournament_players_id_list.append(requested_player_id)
        Tournament.update_tournament_players_id_list(
            self, tournament_players_id_list, tournament_id)

    def update_tournament_rd_id_list(self, tournament_rounds_id_list,
                                     tournament_id):
        """Update tournament_rounds_id_list in this tournament's database."""
        Tournament.update_tournament_rounds_id_list(
            self, tournament_rounds_id_list, tournament_id)

    def create_any_tournament_round(self):
        """Create any round for a chosen tournament."""
        tournament_id = TournamentCtrlr.request_tournament_id(self)
        if tournament_id == 0:
            pass
        else:
            db = TinyDB('db' + str(tournament_id) + '.json')
            Tournament.tournaments_db = db.table('tournaments_db')
            Tournament.tournament_rounds_id_list = (Tournament.tournaments_db.get(
                doc_id=tournament_id))['t_rounds_list']

            number_of_rounds = (len(Tournament.tournament_rounds_id_list))
            if number_of_rounds < 4:
                if number_of_rounds >= 1:
                    TournamentCtrlr.create_next_round(self, tournament_id)
                else:
                    TournamentCtrlr.create_first_round(self, tournament_id)
            else:
                TournamentViews.display_this_t_rounds_already_created()

    def create_first_round(self, tournament_id):
        """Create the first round of the tournament."""
        r_matches_id_list = []
        Tournament.tournament_rounds_id_list = []
        new_round = RoundCtrlr.create_new_round(self,
                                                tournament_id,
                                                r_matches_id_list,
                                                round_id=0,
                                                end_date_time=0,
                                                start_date_time=0)
        print(new_round.round_name + ' créé')
        new_round_id = TournamentCtrlr.get_new_round_id(
            self, new_round, tournament_id)
        # fill 1st round matches_list and load it into database
        round_id = new_round_id
        r_matches_id_list = TournamentCtrlr.create_first_r_matches_list(
            self, tournament_id, round_id)
        # start round and load start_date_and_time into database
        RoundCtrlr.set_start_date_and_time(self, tournament_id, round_id)
        return round_id

    def create_next_round(self, tournament_id):
        """Create the next rounds of the tournament."""
        db = TinyDB('db' + str(tournament_id) + '.json')
        Tournament.tournaments_db = db.table('tournaments_db')
        tournament_rounds_qty = (Tournament.tournaments_db.get(
            doc_id=tournament_id))['t_round_qty']
        if len(Tournament.tournament_rounds_id_list) < tournament_rounds_qty:
            r_matches_id_list = []
            new_round = RoundCtrlr.create_new_round(self,
                                                    tournament_id,
                                                    r_matches_id_list,
                                                    round_id=0,
                                                    end_date_time=0,
                                                    start_date_time=0,)
            print(new_round.round_name + ' créé')
            new_round_id = TournamentCtrlr.get_new_round_id(
                self, new_round, tournament_id)
            # fill matches_list
            round_id = new_round_id
            r_matches_id_list = TournamentCtrlr.create_next_round_matches_list(
                self, tournament_id, round_id)
            # start round
            RoundCtrlr.set_start_date_and_time(
                self, tournament_id, round_id)
        else:
            TournamentViews.display_rounds_list_full()
        return round_id

    def get_new_round_id(self, new_round, tournament_id):
        """Get the id of a newly created round."""
        Theround = Query()
        new_round_id = (Round.rounds_db.get(
            Theround.r_name == new_round.round_name)).doc_id
        Tournament.tournament_rounds_id_list.append(new_round_id)
        TournamentCtrlr.update_tournament_rd_id_list(
            self, Tournament.tournament_rounds_id_list, tournament_id)
        return new_round_id

    def create_first_r_matches_list(self, tournament_id, round_id):
        """Create matches for tournament's first round."""
        Round.r_matches_id_list = []
        rank_sorted_p_list = TournamentCtrlr.sort_tournament_players_list_by_rank(
            self, tournament_id
        )
        matches_qty = len(rank_sorted_p_list) / 2
        for i in range(0, int(matches_qty)):
            match_player1 = rank_sorted_p_list[i]['p_id']
            match_player2 = rank_sorted_p_list[i + int(matches_qty)]['p_id']
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
        """Sort by rank tournament players list."""
        db = TinyDB('db' + str(tournament_id) + '.json')
        Player.players_db = db.table('players_db')

        # get the list of players to be sorted
        tournament_players_id_list = TournamentCtrlr.get_tourney_players_id_list(
            self, tournament_id)
        t_full_players_list = []
        for pl_id in tournament_players_id_list:  # doc_ids
            t_full_player = Player.players_db.get(doc_id=pl_id)
            t_full_players_list.append(t_full_player)

        # sort the players
        rank_sorted_p_list = sorted(t_full_players_list,
                                    key=lambda k: k['p_rank'])
        t_full_players_list.clear()
        return rank_sorted_p_list

    def create_next_round_matches_list(self, tournament_id, round_id):
        """Create matches for round > 1"""
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

    def compare_matches_p_pairs(self, tournament_id):
        """Prepare and check players pairs for next rounds."""
        next_round_p_pairs_list = []  # list of next matches pairs of players

        points_sorted_p_id_list = TournamentCtrlr.sort_t_players_id_list_by_points(
            self, tournament_id)
        previous_pairs_list = TournamentCtrlr.create_prev_matches_players_id_list(
            self, tournament_id)
        next_round_p_pairs_list = TournamentCtrlr.test_players_pairs(
            self, points_sorted_p_id_list, previous_pairs_list)
        previous_pairs_list.clear()
        points_sorted_p_id_list.clear()
        return next_round_p_pairs_list

    def test_players_pairs(self, points_sorted_p_id_list, previous_pairs_list):
        """Test players pairs to get uniq pairs of players."""
        next_round_p_pairs_list = []
        increment = 1
        while len(points_sorted_p_id_list) > 0:
            testing_pair = TournamentCtrlr.create_test_players_pair(
                self, increment, points_sorted_p_id_list
            )
            if testing_pair in previous_pairs_list:
                if len(points_sorted_p_id_list) < 4:
                    next_round_p_pairs_list.append(testing_pair)
                    return next_round_p_pairs_list
                else:
                    increment += 1
                    testing_pair = TournamentCtrlr.create_test_players_pair(
                        self, increment, points_sorted_p_id_list
                    )
            else:
                # UNIQUE pair of players to be added to next round matches
                next_round_p_pairs_list.append(testing_pair)
                # update points_sorted_p_id_list (avoid re-testing players)
                del points_sorted_p_id_list[0]
                del points_sorted_p_id_list[increment - 1]
                if len(points_sorted_p_id_list) > 0:
                    # new testing_pair:
                    increment = 1
                    testing_pair = TournamentCtrlr.create_test_players_pair(
                        self, increment, points_sorted_p_id_list
                    )
                else:
                    return next_round_p_pairs_list
        return next_round_p_pairs_list

    def sort_t_players_id_list_by_points(self, tournament_id):
        """Sort tournament players list by rank and total points."""
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

    def create_test_players_pair(self, increment, points_sorted_p_id_list):
        """Create pair of players to have its uniqueness tested."""
        test_pair = [points_sorted_p_id_list[0],
                     points_sorted_p_id_list[increment]]
        return test_pair

    def create_prev_matches_players_id_list(self, tournament_id):
        """List the id of previous matches players."""
        db = TinyDB('db' + str(tournament_id) + '.json')
        Match.matches_db = db.table('matches_db')

        id_matches_list = TournamentCtrlr.get_previous_matches_id_list(
            self, tournament_id)
        m_list = []
        for m in id_matches_list:
            prev_matches = Match.matches_db.get(doc_id=m)
            m_list.append(prev_matches)
        number_of_previous_matches = len(m_list)
        previous_pairs_list = []
        for n in range(0, number_of_previous_matches):
            previous_pairs_list.append([m_list[n]['chess_player1'],  # doc_id
                                        m_list[n]['chess_player2']])
        return previous_pairs_list

    def get_previous_matches_id_list(self, tournament_id):
        """Get the list of id of previous matches."""
        this_tournament = Tournament.tournaments_db.get(doc_id=tournament_id)
        tournmt_r_id_list = this_tournament['t_rounds_list']
        rd_match_id_list = []
        for item in tournmt_r_id_list:
            rd_match_id = (Round.rounds_db.get(doc_id=item)
                           )['rnd_matches_list']
            rd_match_id_list.append(rd_match_id)
        del rd_match_id_list[-1]
        i = len(rd_match_id_list)
        id_matches_list = []
        for j in range(0, i):
            for k in rd_match_id_list[j]:
                id_matches_list.append(k)
        return id_matches_list

    def closing_a_tournament_round(self):
        """Close any open round."""
        tournament_id = TournamentCtrlr.request_tournament_id(self)
        if tournament_id == 0:
            pass
        else:
            round_id = TournamentCtrlr.request_round_id(self, tournament_id)
            round_status = TournamentCtrlr.get_round_end(self, tournament_id,
                                                         round_id)
            if round_status != 0:  # round is closed if status != 0
                TournamentViews.display_round_already_closed()
            else:
                end_date_time = RoundCtrlr.closing_this_round(
                    self, tournament_id, round_id)
                return end_date_time

    def get_round_end(self, tournament_id, round_id):
        """Check if round already closed."""
        db = TinyDB('db' + str(tournament_id) + '.json')
        Round.rounds_db = db.table('rounds_db')
        round_end_date_time = (Round.rounds_db.get(doc_id=round_id)
                               )['end_datentime']
        return round_end_date_time

    def loging_this_r_scores(self, tournament_id, round_id):
        """Enter matches scores of current round."""
        db = TinyDB('db' + str(tournament_id) + '.json')
        Match.matches_db = db.table('matches_db')

        r_matches_id_list = (Round.rounds_db.get(doc_id=round_id)
                             )['rnd_matches_list']
        matches_number = len(r_matches_id_list)
        for i in range(0, int(matches_number)):
            player1_id = (Match.matches_db.get(doc_id=r_matches_id_list[i])
                          )['chess_player1']
            player2_id = (Match.matches_db.get(doc_id=r_matches_id_list[i])
                          )['chess_player2']
            player1_score = TournamentCtrlr.ask_player1_score(
                self, tournament_id, player1_id, player2_id
            )
            player2_score = TournamentCtrlr.ask_player2_score(
                self, tournament_id, player1_id, player2_id
            )
            TournamentCtrlr.update_player_points_qty(
                self, player1_id, player2_id, player1_score, player2_score)
            # update matches_db
            match_id = r_matches_id_list[i]
            Match.update_players_scores(self, tournament_id, match_id,
                                        player1_score, player2_score)

    def check_existing_scores(self, tournament_id, round_id):
        """Makes the sum of a round's matches scores
        to check if scores are already input (sum = 0 when no match).
        """
        db = TinyDB('db' + str(tournament_id) + '.json')
        Round.rounds_db = db.table('rounds_db')
        Match.matches_db = db.table('matches_db')
        matches_id_list = []
        scores_list = []

        round_matches_id = ((Round.rounds_db.get(
            doc_id=round_id))['rnd_matches_list'])
        for m_id in round_matches_id:
            matches_id_list.append(m_id)
        for m in matches_id_list:
            score_pl1 = Match.matches_db.get(doc_id=m)['score_player1']
            scores_list.append(score_pl1)
            score_pl2 = Match.matches_db.get(doc_id=m)['score_player2']
            scores_list.append(score_pl2)
        scores_sum = sum(scores_list)
        return scores_sum

    def log_a_round_scores(self):
        """Enter the scores of a round (if closed).
        Propose overwriting (or not) existing scores.
        """
        tournament_id = TournamentCtrlr.request_tournament_id(self)
        if tournament_id > 0:
            round_id = TournamentCtrlr.request_round_id(self, tournament_id)
            round_status = TournamentCtrlr.get_round_end(self, tournament_id,
                                                         round_id)
            if round_status != 0:  # round is closed when status != 0
                scores_sum = TournamentCtrlr.check_existing_scores(
                    self, tournament_id, round_id)
                if scores_sum > 0:
                    TournamentViews.ask_overwrite_scores()
                    overwrite_scores = input()
                    if overwrite_scores == 'NON':
                        pass
                    else:
                        TournamentCtrlr.loging_this_r_scores(
                            self, tournament_id, round_id)
                else:
                    TournamentCtrlr.loging_this_r_scores(
                        self, tournament_id, round_id)
            else:
                TournamentViews.display_round_not_closed()
        else:
            pass

    def request_tournament_id(self):
        """Get a tournament id from its name."""
        db_all_t = TinyDB('db_all_t.json')
        Tournament.all_tournaments_db = db_all_t.table('all_tournaments_db')
        TournamentViews.display_tournaments_list()
        t_name_list = []
        for t in Tournament.all_tournaments_db:
            print(t['t_name'])
            t_name_list.append(t['t_name'])
        RoundViews.ask_tournament_name()
        tournament_name = input()
        if tournament_name in t_name_list:
            Thetournmt = Query()
            tournament_id = (Tournament.all_tournaments_db.get(
                Thetournmt.t_name == tournament_name))['t_id']
            return tournament_id
        else:
            TournamentViews.choice_unavailable()
            time.sleep(2)
            return 0

    def request_round_id(self, tournament_id):
        """Get a round id from the round's name."""
        db = TinyDB('db' + str(tournament_id) + '.json')
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
        round_req = Round.rounds_db.get(Theround.r_name == round_name_req)
        round_id = round_req['r_id']
        return round_id

    def ask_player1_score(self, tournament_id, player1_id, player2_id):
        """Get player1's score."""
        db = TinyDB('db' + str(tournament_id) + '.json')
        Player.players_db = db.table('players_db')

        name_pl1 = Player.players_db.get(doc_id=player1_id)['p_name']
        name_pl2 = Player.players_db.get(doc_id=player2_id)['p_name']
        print('Match ' + name_pl1 + " contre " + name_pl2)
        print('1er joueur : ' + name_pl1)
        player1_score = TournamentCtrlr.display_player_score_input(self)
        return player1_score

    def ask_player2_score(self, tournament_id, player1_id, player2_id):
        """Get player2's score."""
        db = TinyDB('db' + str(tournament_id) + '.json')
        Player.players_db = db.table('players_db')

        name_pl1 = Player.players_db.get(doc_id=player1_id)['p_name']
        name_pl2 = Player.players_db.get(doc_id=player2_id)['p_name']
        print('Match ' + name_pl1 + " contre " + name_pl2)
        print('2eme joueur : ' + name_pl2)
        player2_score = TournamentCtrlr.display_player_score_input(self)
        TournamentViews.separator()
        return player2_score

    def display_player_score_input(self):
        """Displays the User's scores input."""
        player_score = float(input('Saisissez son score (0 ou 0.5 ou 1) : '))
        if player_score == 0:
            return player_score
        elif player_score == 0.5:
            return player_score
        elif player_score == 1:
            return player_score
        else:
            TournamentViews.choice_unavailable()
            TournamentCtrlr.log_a_round_scores(self)

    def update_player_points_qty(self, player1_id, player2_id, player1_score,
                                 player2_score):
        """Update players total points."""
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

    def update_tournament_player_ranking(self):
        """Update tournament player rank with User's information."""
        tournament_id = TournamentCtrlr.request_tournament_id(self)
        if tournament_id == 0:
            pass
        else:
            PlayerCtrlr.get_points_sorted_tournament_players(
                self, tournament_id)
            PlayerViews.ask_player_to_update_rank()
            player_id = PlayerCtrlr.request_tournament_player(
                self, tournament_id)
            if player_id is None:
                pass
            else:
                PlayerViews.ask_player_ranking()
                player_rank = int(input())
                new_player_rank = Player.update_t_player_rank(
                    self, tournament_id, player_id, player_rank)
                return new_player_rank
