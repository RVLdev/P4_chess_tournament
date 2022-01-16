from datetime import datetime
from tinydb import TinyDB, Query

db = TinyDB('db.json')
User = Query()
rounds_db = db.table('rounds_db')


class Round:
    def __init__(self, round_id, round_name, match1, match2, match3, match4,
                 start_date_time, end_date_time):
        self.round_id = round_id
        self.round_name = round_name
        self.start_date_time = start_date_time
        self.end_date_time = end_date_time
        self.match1 = match1
        self.match2 = match2
        self.match3 = match3
        self.match4 = match4

        """creation of a database for rounds """
        self.db = TinyDB('db.json')
        User = Query()  # à revoir
        self.rounds_db = self.db.table('rounds_db')

    def create_round(self):
        # enregistrement en BDD ==> code A VERIFIER
        rounds_db.insert({'r_id': self.round_name,
                          'r_name': self.round_name,
                          'match_1': self.match1,
                          'match_2': self.match2,
                          'match_3': self.match3,
                          'match_4': self.match4,
                          'start_datentime': self.start_date_time,
                          'end_datentime': self.end_date_time})

    def read_round(self, round_id):
        self.rounds_db.get(doc_id=round_id)
        return Round()

    def update_round(self, id):
        pass

    def update_round_id(self, round_id):
        self.rounds_db.update({'r_id': self.round_id}, doc_id=round_id)

    def update_round_end_date_time(self, round_id):
        self.rounds_db.update(
            {
                'end_datentime': self.end_date_time
            },
            doc_id=round_id
        )

    def delete_round(self, round_id):
        self.rounds_db.remove(doc_id=round_id)

    # start_date_time DOIT ETRE "renseigné" A LA CREATION DE L'OBJET ROUND
    def start_round(self):
        """ generate date & time for the begining of a round"""
        start_date_time = str(datetime.now())
        return start_date_time

    # end_date_time A REVOIR
    def close_round(self, round_id):  # grandes lignes
        ask_round_name()
        get_round(round_name)
        end_date_time = str(datetime.now())
        self.update_round_end_date_time(round_id)
        return end_date_time

# def Create / Read(get) / Update / Delete
