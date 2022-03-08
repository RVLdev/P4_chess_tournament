from tinydb import TinyDB
from models.playermodel import Player
from models.matchmodel import Match
from models.roundmodel import Round
from models.tournamentmodel import Tournament


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
            db = TinyDB('db' + str(tournament_id) + '.json')

            Tournament.tournaments_db = db.table('tournaments_db')
            Round.rounds_db = db.table('rounds_db')
            Match.matches_db = db.table('matches_db')
            Player.players_db = db.table('players_db')

            self.db_backup = TinyDB('db_backup' + str(tournament_id) + '.json')
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
            db = TinyDB('db' + str(tournament_id) + '.json')

            Tournament.tournaments_db = db.table('tournaments_db')
            Round.rounds_db = db.table('rounds_db')
            Match.matches_db = db.table('matches_db')
            Player.players_db = db.table('players_db')

            self.db_backup = TinyDB('db_backup' + str(tournament_id) + '.json')
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
