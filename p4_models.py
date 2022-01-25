from tinydb import TinyDB
from datetime import datetime


class Tournament:
    """ defines an object 'tournament' : (shape, characteristics)"""
    def __init__(self, tournament_id, tournament_name, tournament_place,
                 tournament_date, tournament_players_list,
                 tournament_description,
                 tournament_time_control,
                 tournament_rounds_list=['round1', 'round2', 'round3',
                                         'round4'],
                 tournament_rounds_qty=4,):

        self.tournament_id = tournament_id
        self.tournament_name = tournament_name
        self.tournament_place = tournament_place
        self.tournament_date = tournament_date
        self.tournament_rounds_list = tournament_rounds_list
        self.tournament_players_list = tournament_players_list
        self.tournament_description = tournament_description
        self.tournament_time_control = tournament_time_control
        self.tournament_rounds_qty = tournament_rounds_qty

        tournament_rounds_list = []

        """creation of a database for tournaments """
        self.db = TinyDB('db.json')
        self.tournaments_db = self.db.table('tournaments_db')

    def create_tournament(self):
        """create one tournament"""
        self.tournaments_db.insert(
            {
                't_id': self.tournament_id,
                't_name': self.tournament_name,
                't_place': self.tournament_place,
                't_date': self.tournament_date,
                't_players_list': self.tournament_players_list,
                't_description': self.tournament_description,
                't_time_control': self.tournament_time_control,
                't_rounds_list': self.tournament_rounds_list,
                't_round_qty': self.tournament_rounds_qty
            }
            )

    def read_tournament(self, tournament_id):
        self.tournaments_db.get(doc_id=tournament_id)
        return Tournament()

    def update_tournament_id(self, tournament_id):
        self.tournaments_db.update({'t_id': self.tournament_id},
                                   doc_id=tournament_id)

    def delete_tournament(self, tournament_id):
        self.tournaments_db.remove(doc_id=tournament_id)


class Round:
    def __init__(self, round_id, round_name, r_matches_list,
                 start_date_time, end_date_time):
        self.round_id = round_id
        self.round_name = round_name
        self.r_matches_list = r_matches_list
        self.start_date_time = start_date_time
        self.end_date_time = end_date_time

        """creation of a database for rounds """
        self.db = TinyDB('db.json')
        self.rounds_db = self.db.table('rounds_db')

    def create_round(self):
        """ create a round """
        self.rounds_db.insert({'r_id': self.round_id,
                               'r_name': self.round_name,
                               'r_matches_list': self.r_matches_list,
                               'start_datentime': self.start_date_time,
                               'end_datentime': self.end_date_time,
                               })

    # start_date_time DOIT ETRE "renseigné" A LA CREATION DE L'OBJET ROUND
    def start_round(self):
        """ generate date & time for the begining of a round"""
        start_date_time = str(datetime.now())
        return start_date_time

    # end_date_time A REVOIR
    def close_round(self, round_id):  # grandes lignes
        end_date_time = str(datetime.now())
        self.update_round_end_date_time(round_id, end_date_time)
        return end_date_time

    def read_round(self, round_id):
        self.rounds_db.get(doc_id=round_id)
        return Round()

    def update_round_end_date_time(self, round_id, end_date_time):
        self.rounds_db.update(
            {
                'end_datentime': end_date_time
            },
            doc_ids=[round_id]
        )

    def delete_round(self, round_id):
        self.rounds_db.remove(doc_id=round_id)


class Match:
    """ defines an object 'player' : (shape, characteristics)"""
    def __init__(self, match_id, match_player1, match_player2,
                 player1_score=0, player2_score=0):
        self.match_id = match_id
        self.match_player1 = match_player1
        self.match_player2 = match_player2
        self.player1_score = player1_score
        self.player2_score = player2_score

        """creation of a database for matches """
        self.db = TinyDB('db.json')
        self.matches_db = self.db.table('matches_db')

    def create_match(self, match_player1, match_player2):
        """ create (and save) a match"""
        self.matches_db.insert(
            {
                'match_id': self.match_id,
                'chess_player1': match_player1,
                'score_player1': self.player1_score,
                'chess_player2': match_player2,
                'score_player2': self.player2_score
            }
        )

    def read_match(self, match_id):
        self.matches_db.get(doc_id=match_id)
        return Match()

    def update_players_scores(self, match_id, player1_score, player2_score):
        self.matches_db.update({'score_player1': player1_score},
                               doc_ids=[match_id])
        self.matches_db.update({'score_player2': player2_score},
                               doc_ids=[match_id])

    def delete_match(self, match_id):
        self.matches_db.remove(doc_id=match_id)


class Player:
    """ defines an object 'player' : (shape, characteristics)"""
    def __init__(self, player_id, player_name, player_first_name,
                 player_birth_date, player_gender, player_ranking,
                 player_points_qty=0):
        self.player_id = player_id
        self.player_name = player_name
        self.player_first_name = player_first_name
        self.player_birth_date = player_birth_date
        self.player_gender = player_gender
        self.player_ranking = player_ranking
        # sum of a player's scores (calcul dans TOURNOI):
        self.player_points_qty = player_points_qty

        """creation of a database for players """
        self.db = TinyDB('db.json')
        self.players_db = self.db.table('players_db')

    def create_player(self):
        """ create (and save to a database) a player """
        self.players_db.insert(
            {
                'p_id': self.player_id,
                'p_name': self.player_name,
                'p_firstname': self.player_first_name,
                'p_birthdate': self.player_birth_date,
                'p_gender': self.player_gender,
                'p_rank': self.player_ranking,
                'p_total_points': self.player_points_qty
            }
        )

    def read_player(self, player_id):
        self.players_db.get(doc_id=player_id)
        # db renvoie un dictionnaire idem "create"
        return Player()

    def update_player_id(self, player_id):
        """ update player_id to be = doc_id """
        self.players_db.update({'p_id': self.player_id}, doc_ids=[player_id])

    @classmethod
    def update_player_ranking(cls, player_id, player_ranking):
        """ update a player rank in DB through its ID"""
        cls.players_db.update({'p_rank': player_ranking},
                              doc_ids=[player_id])

    def delete_player(self, player_id):
        """remove a player from DB through its ID"""
        self.players_db.remove(doc_id=player_id)
