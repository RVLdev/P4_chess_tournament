from tinydb import Query, TinyDB


class Tournament:
    """ defines an object 'tournament' : (shape, characteristics)"""
    def __init__(self, tournament_id, tournament_name, tournament_place,
                 tournament_date, tournament_description,
                 tournament_time_control, tournament_rounds_qty,
                 tournament_rounds_id_list, tournament_players_id_list,):
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

        # tournament DB
        db = TinyDB('db' + str(tournament_id) + '.json')
        Tournament.tournaments_db = db.table('tournaments_db')

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
        db = TinyDB('db' + str(tournament_id) + '.json')
        Tournament.tournaments_db = db.table('tournaments_db')
        that_tournament = Tournament.tournaments_db.get(doc_id=tournament_id)
        print(that_tournament)
        return that_tournament

    def update_tournament_id(self):
        """ default new tournament id = 0
        Update tournament_id to become its doc_id value """
        db_all_t = TinyDB('db_all_t.json')
        Tournament.all_tournaments_db = db_all_t.table('all_tournaments_db')
        Thetournmt = Query()
        new_tournmt_id = Tournament.all_tournaments_db.get(
            Thetournmt.t_id == 0)
        tournament_id = new_tournmt_id.doc_id
        Tournament.all_tournaments_db.update({'t_id': tournament_id},
                                             doc_ids=[tournament_id])
        return tournament_id

    def update_tournament_rounds_qty(self,
                                     tournament_rounds_qty,
                                     tournament_id):
        """update rounds quantity of the tournament"""
        db = TinyDB('db' + str(tournament_id) + '.json')
        Tournament.tournaments_db = db.table('tournaments_db')
        Tournament.tournaments_db.update({
            't_round_qty': tournament_rounds_qty},
            doc_ids=[tournament_id]
        )

    def update_tournament_players_id_list(self, tournament_players_id_list,
                                          tournament_id):

        """ update the players id list of the tournament"""
        db = TinyDB('db' + str(tournament_id) + '.json')
        Tournament.tournaments_db = db.table('tournaments_db')
        Tournament.tournaments_db.update({
            't_players_list': tournament_players_id_list},
            doc_ids=[tournament_id]
        )

    def update_tournament_rounds_id_list(self, tournament_rounds_id_list,
                                         tournament_id):
        """ update the rounds id list of the tournament"""
        db = TinyDB('db' + str(tournament_id) + '.json')
        Tournament.tournaments_db = db.table('tournaments_db')
        Tournament.tournaments_db.update({
            't_rounds_list': tournament_rounds_id_list},
            doc_ids=[tournament_id]
        )

    def delete_tournament(self, tournament_id):
        # delete a tournament from its DB
        db = TinyDB('db' + str(tournament_id) + '.json')
        Tournament.tournaments_db = db.table('tournaments_db')
        Tournament.tournaments_db.remove(doc_id=tournament_id)
