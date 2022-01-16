from tinydb import TinyDB


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
        self.player_points_qty = player_points_qty  # sum of a player's scores (calcul dans TOURNOI)

        """creation of a database for players """
        self.db = TinyDB('db.json')
        self.players_db = self.db.table('players_db')

        # self.create_player()  # lance automatiquement cette méthode

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

    def read_player(self, player_id):  # 'read' équivaut à 'get' + doit retourner un objet PLAYER (pas uniqmt ID)
        self.players_db.get(doc_id=player_id)
            #db renvoie un dictionnaire idem "create"    
        return Player()

    def load_player(self, player_id):  # pour charger un joueur de DB (dico -->p_data = None)
        # charger un joueur : lequel / selon quel critère ?(son nom, son ranking...)
        pass  # à faire ds CONTROLLER

    def db_players_list(self): # pour faire quoi ? VERIFIER UTILITE
        """ get list of name+family name+ id of all saved players"""

    def update_player(self, player_id):
        pass  # si utile, db.update_multiple([...])
    
    def update_player_id(self, player_id):
        """ update player's id (set at 'None' by default) with a new value """
        self.players_db.update({'p_id': self.player_id}, doc_id=player_id)

    def update_p_total_points(self, player_id, player_points_qty):  # calcul de p_total_points dans tournament_model
        """ update player's points (sum of matches' scores) """
        self.players_db.update({'p_total_points': player_points_qty},
                               doc_id=player_id)

    def update_player_ranking(self, player_id, player_ranking):
        """ update a player rank in DB through its ID"""
        self.players_db.update({'p_rank': player_ranking},
                               doc_ids=[player_id])

    def delete_player(self, player_id):
        """remove a player from DB through its ID"""
        self.players_db.remove(doc_id=player_id)

"""if __name__ == "__main__":
    p = Player()
    print(p.read_player(player_id=2))"""