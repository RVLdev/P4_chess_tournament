from tinydb import TinyDB, where, Query



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

    def dis_bonjour_r_model(self):  #TEST INITIAL - A SUPPRIMER*****************************
        print ('Bonjour de la classe Round - fichier roundmodel')

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

    def read_round(self, tournament_id, round_id):
        # display a round
        db = TinyDB('db'+str(tournament_id)+'.json')
        Round.rounds_db = db.table('rounds_db')
        Round.rounds_db.get(doc_id=round_id)
        return Round()

    def update_round_end_date_time(self, tournament_id,
                                   round_id, end_date_time):
        """ update a round end date & time"""
        db = TinyDB('db'+str(tournament_id)+'.json')
        Round.rounds_db = db.table('rounds_db')
        Round.rounds_db.update({
                'end_datentime': end_date_time}, doc_ids=[round_id])

    def delete_round(self, tournament_id, round_id):
        # delete a round from tournament's DB
        db = TinyDB('db'+str(tournament_id)+'.json')
        Round.rounds_db = db.table('rounds_db')
        Round.rounds_db.remove(doc_id=round_id)
