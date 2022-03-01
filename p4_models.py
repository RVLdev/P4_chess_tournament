from tinydb import Query, TinyDB


class Tournament:
    """ defines an object 'tournament' : (shape, characteristics)"""
    def __init__(self, tournament_id, tournament_name, tournament_place,
                 tournament_date, tournament_description,
                 tournament_time_control, tournament_rounds_qty,
                 tournament_rounds_id_list, tournament_players_id_list):

        self.tournament_id = tournament_id
        self.tournament_name = tournament_name
        self.tournament_place = tournament_place
        self.tournament_date = tournament_date
        self.tournament_description = tournament_description
        self.tournament_time_control = tournament_time_control
        self.tournament_rounds_qty = tournament_rounds_qty
        self.tournament_players_id_list = tournament_players_id_list
        self.tournament_rounds_id_list = tournament_rounds_id_list
        tournament_rounds_id_list = []

        """creation of a database for tournaments """
        # global DB
        db_all_t = TinyDB('db_all_t.json')
        Tournament.all_tournaments_db = db_all_t.table('all_tournaments_db')

        # backup DB
        self.db_backup = TinyDB('db_backup.json')
        Tournament.t_db = self.db_backup.table('tournaments_db')

    def create_tournament(self):
        """create one tournament"""
        Tournament.all_tournaments_db.insert(
            {
                't_id': self.tournament_id,
                't_name': self.tournament_name,
                't_place': self.tournament_place,
                't_date': self.tournament_date,
                't_description': self.tournament_description,
                't_time_control': self.tournament_time_control,
                't_round_qty': self.tournament_rounds_qty,
                't_players_list': self.tournament_players_id_list,
                't_rounds_list': self.tournament_rounds_id_list
            }
            )

    def read_tournament(self, tournament_id):
        """ display a tournament"""
        db = TinyDB('db'+str(tournament_id)+'.json')
        Tournament.tournaments_db = db.table('tournaments_db')
        that_tournament = Tournament.tournaments_db.get(doc_id=tournament_id)
        print(that_tournament)
        return that_tournament

    def update_tournament_id(self):  # ok
        """ default new tournament id = 0
        Update tournament_id to become its doc_id value """
        new_tournmt_id = Tournament.all_tournaments_db.get(
            Tournament.Thetournmt.t_id == 0)
        tournament_id = new_tournmt_id.doc_id
        Tournament.all_tournaments_db.update({'t_id': tournament_id},
                                             doc_ids=[tournament_id])
        return tournament_id

    def update_tournament_rounds_qty(self,
                                     tournament_rounds_qty,
                                     tournament_id):  # ok
        """update rounds quantity of the tournament"""
        db = TinyDB('db'+str(tournament_id)+'.json')
        Tournament.tournaments_db = db.table('tournaments_db')
        Tournament.tournaments_db.update({
            't_round_qty': tournament_rounds_qty},
                                         doc_ids=[tournament_id])

    def update_tournament_players_id_list(self, tournament_players_id_list,
                                          tournament_id):

        """ update the players id list of the tournament"""
        db = TinyDB('db'+str(tournament_id)+'.json')
        Tournament.tournaments_db = db.table('tournaments_db')
        Tournament.tournaments_db.update({
            't_players_list': tournament_players_id_list},
                                         doc_ids=[tournament_id])

    def update_tournament_rounds_id_list(self, tournament_rounds_id_list,
                                         tournament_id):
        """ update the rounds id list of the tournament"""
        db = TinyDB('db'+str(tournament_id)+'.json')
        Tournament.tournaments_db = db.table('tournaments_db')
        Tournament.tournaments_db.update({
            't_rounds_list': tournament_rounds_id_list},
                                         doc_ids=[tournament_id])

    """def delete_tournament(self, tournament_id):
        # delete a tournament from its DB
        db = TinyDB('db'+str(tournament_id)+'.json')
        Tournament.tournaments_db = db.table('tournaments_db')
        Tournament.tournaments_db.remove(doc_id=tournament_id)"""


class Round:
    def __init__(self, round_id, round_name, r_matches_id_list,
                 start_date_time, end_date_time):
        self.round_id = round_id
        self.round_name = round_name
        self.r_matches_id_list = r_matches_id_list
        r_matches_id_list = []
        self.start_date_time = start_date_time
        self.end_date_time = end_date_time

        # backup DB
        self.db_backup = TinyDB('db_backup.json')
        Round.r_db = self.db_backup.table('rounds_db')

    def create_round(self, tournament_id):
        """ create a round """
        db = TinyDB('db'+str(tournament_id)+'.json')
        Round.rounds_db = db.table('rounds_db')
        Round.rounds_db.insert({'r_id': self.round_id,
                                'r_name': self.round_name,
                                'rnd_matches_list': self.r_matches_id_list,
                                'start_datentime': self.start_date_time,
                                'end_datentime': self.end_date_time,
                                })

    def update_round_id(self, tournament_id):
        """ update round_id to become = doc_id """
        db = TinyDB('db'+str(tournament_id)+'.json')
        Theround = Query()
        Round.rounds_db = db.table('rounds_db')
        new_round = Round.rounds_db.get(Theround.r_id == 0)
        round_id = new_round.doc_id
        Round.rounds_db.update({'r_id': round_id}, doc_ids=[round_id])
        return round_id

    def update_r_matches_list(self, tournament_id, round_id,
                              r_matches_id_list):
        """update the rounds' matches list"""
        db = TinyDB('db'+str(tournament_id)+'.json')
        Round.rounds_db = db.table('rounds_db')
        Round.rounds_db.update({
            'rnd_matches_list': r_matches_id_list}, doc_ids=[round_id])

    def update_start_date_time(self, tournament_id,
                               start_date_time, round_id):
        """ update a round start date & time  """
        db = TinyDB('db'+str(tournament_id)+'.json')
        Round.rounds_db = db.table('rounds_db')
        Round.rounds_db.update({
            'start_datentime': start_date_time}, doc_ids=[round_id])

    """def read_round(self, tournament_id, round_id):
        # display a round
        db = TinyDB('db'+str(tournament_id)+'.json')
        Round.rounds_db = db.table('rounds_db')
        Round.rounds_db.get(doc_id=round_id)
        return Round()"""

    def update_round_end_date_time(self, tournament_id,
                                   round_id, end_date_time):
        """ update a round end date & time"""
        db = TinyDB('db'+str(tournament_id)+'.json')
        Round.rounds_db = db.table('rounds_db')
        Round.rounds_db.update({
                'end_datentime': end_date_time}, doc_ids=[round_id])

    """def delete_round(self, tournament_id, round_id):
        # delete a round from tournament's DB
        db = TinyDB('db'+str(tournament_id)+'.json')
        Round.rounds_db = db.table('rounds_db')
        Round.rounds_db.remove(doc_id=round_id)"""


class Match:
    """ defines an object 'match' : (shape, characteristics)"""
    def __init__(self, match_id, match_player1, match_player2,
                 player1_score=0, player2_score=0):
        self.match_id = match_id
        self.match_player1 = match_player1
        self.match_player2 = match_player2
        self.player1_score = player1_score
        self.player2_score = player2_score

        # backup DB
        self.db_backup = TinyDB('db_backup.json')
        Match.m_db = self.db_backup.table('matches_db')

    def create_match(self, tournament_id):
        """ create a match (and save it in tournament DB) """
        db = TinyDB('db'+str(tournament_id)+'.json')
        Match.matches_db = db.table('matches_db')
        Match.matches_db.insert(
            {
                'm_id': self.match_id,
                'chess_player1': self.match_player1,
                'chess_player2': self.match_player2,
                'score_player1': self.player1_score,
                'score_player2': self.player2_score
            }
        )

    def update_match_id(self, tournament_id):
        """ update match_id to become = doc_id """
        db = TinyDB('db'+str(tournament_id)+'.json')
        Thematch = Query()
        Match.matches_db = db.table('matches_db')
        new_match = Match.matches_db.get(Thematch.m_id == 0)
        match_id = new_match.doc_id
        Match.matches_db.update({'m_id': match_id}, doc_ids=[match_id])
        return match_id

    def update_players_scores(self, tournament_id, match_id,
                              player1_score, player2_score):
        """ update players scores and save them in tournament DB"""
        db = TinyDB('db'+str(tournament_id)+'.json')
        Match.matches_db = db.table('matches_db')
        Match.matches_db.update({
            'score_player1': player1_score}, doc_ids=[match_id])
        Match.matches_db.update({
            'score_player2': player2_score}, doc_ids=[match_id])


class Player:
    """ defines an object 'player' : (shape, characteristics)"""
    def __init__(self, player_id, player_name, player_first_name,
                 player_birth_date, player_gender, player_rank,
                 player_points_qty=0):
        self.player_id = player_id
        self.player_name = player_name
        self.player_first_name = player_first_name
        self.player_birth_date = player_birth_date
        self.player_gender = player_gender
        self.player_rank = player_rank
        self.player_points_qty = player_points_qty
        # gobal DB
        db_all_t = TinyDB('db_all_t.json')
        Player.all_players_db = db_all_t.table('all_players_db')
        # backup DB
        self.db_backup = TinyDB('db_backup.json')
        Player.p_db = self.db_backup.table('players_db')

    def create_player(self):
        """ create (and save to global DB) a player """
        db_all_t = TinyDB('db_all_t.json')
        Player.all_players_db = db_all_t.table('all_players_db')
        Player.all_players_db.insert(
            {
                'p_id': self.player_id,  # tinyDB doc_id de l'instance
                'p_name': self.player_name,
                'p_firstname': self.player_first_name,
                'p_birthdate': self.player_birth_date,
                'p_gender': self.player_gender,
                'p_rank': self.player_rank,
                'p_total_points': self.player_points_qty
            }
        )

    def update_player_id(self):
        """update player_id to become = doc_id"""
        db_all_t = TinyDB('db_all_t.json')
        Player.Theplayer = Query()
        Player.all_players_db = db_all_t.table('all_players_db')
        new_player = Player.all_players_db.get(Player.Theplayer.p_id == 0)
        player_id = new_player.doc_id
        Player.all_players_db.update({'p_id': player_id}, doc_ids=[player_id])
        return player_id

    def update_playr_rank(self, player_id, player_rank):
        """ update a player rank in global DB through its ID"""
        db_all_t = TinyDB('db_all_t.json')
        Player.all_players_db = db_all_t.table('all_players_db')
        Player.all_players_db.update({
            'p_rank': player_rank}, doc_ids=[player_id])

    def update_t_player_rank(self, tournament_id, player_id, player_rank):
        """ update player rank in tournament's DB"""
        db = TinyDB('db'+str(tournament_id)+'.json')
        Player.players_db = db.table('players_db')
        Player.players_db.update({
            'p_rank': player_rank}, doc_ids=[player_id])


class Save_and_load:
    def __init__(self):
        # self.db = TinyDB('db.json')
        self.db_backup = TinyDB('db_backup.json')
        self.db_backup.drop_table('_default')

    def save_in_db_backup(self):
        """Create a backup of players, matches, rounds and tournaments"""
        db_all_t = TinyDB('db_all_t.json')
        Tournament.all_tournaments_db = db_all_t.table('all_tournaments_db')
        tournaments_id_list = []
        for t in Tournament.all_tournaments_db:
            tournaments_id_list.append(t['t_id'])

        for tournament_id in tournaments_id_list:
            db = TinyDB('db'+str(tournament_id)+'.json')

            Tournament.tournaments_db = db.table('tournaments_db')
            Round.rounds_db = db.table('rounds_db')
            Match.matches_db = db.table('matches_db')
            Player.players_db = db.table('players_db')

            self.db_backup = TinyDB('db_backup'+str(tournament_id)+'.json')
            Player.p_db = self.db_backup.table('players_db')
            Match.m_db = self.db_backup.table('matches_db')
            Round.r_db = self.db_backup.table('rounds_db')
            Tournament.t_db = self.db_backup.table('tournaments_db')
            # empty backup
            Player.p_db.truncate()
            Match.m_db.truncate()
            Round.r_db.truncate()
            Tournament.t_db.truncate()

            # save in db_backup
            for each_player in Player.players_db:
                Player.p_db.insert(each_player)
            for each_tournament in Tournament.tournaments_db:
                Tournament.t_db.insert(each_tournament)
            for each_round in Round.rounds_db:
                Round.r_db.insert(each_round)
            for each_match in Match.matches_db:
                Match.m_db.insert(each_match)

    def load_db_backup(self):
        """ load a backup of players, matches, rounds and tournaments"""
        db_all_t = TinyDB('db_all_t.json')
        Tournament.all_tournaments_db = db_all_t.table('all_tournaments_db')
        tournaments_id_list = []
        for t in Tournament.all_tournaments_db:
            tournaments_id_list.append(t['t_id'])

        for tournament_id in tournaments_id_list:
            db = TinyDB('db'+str(tournament_id)+'.json')

            Tournament.tournaments_db = db.table('tournaments_db')
            Round.rounds_db = db.table('rounds_db')
            Match.matches_db = db.table('matches_db')
            Player.players_db = db.table('players_db')

            self.db_backup = TinyDB('db_backup'+str(tournament_id)+'.json')
            Player.p_db = self.db_backup.table('players_db')
            Match.m_db = self.db_backup.table('matches_db')
            Round.r_db = self.db_backup.table('rounds_db')
            Tournament.t_db = self.db_backup.table('tournaments_db')

            # empty current DB tables
            Player.players_db.truncate()
            Match.matches_db.truncate()
            Round.rounds_db.truncate()
            Tournament.tournaments_db.truncate()

            # load tables with backup
            for each_player in Player.p_db:
                Player.players_db.insert(each_player)
            for each_match in Match.m_db:
                Match.matches_db.insert(each_match)
            for each_round in Round.r_db:
                Round.rounds_db.insert(each_round)
            for each_tournament in Tournament.t_db:
                Tournament.tournaments_db.insert(each_tournament)
            db.drop_table('_default')
