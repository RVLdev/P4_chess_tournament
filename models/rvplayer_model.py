from tinydb import TinyDB, Query


class RvPlayer:
    """ defines an object 'player' : (shape, characteristics)"""
    def __init__(self, players_db, p_data=None):
        self.players_db = players_db
        if p_data:
            self.p_data = p_data
        else:
            self.p_data = {
                'p_id': None,
                'p_name': None,
                'p_firstname': None,
                'p_birthdate': None,
                'p_gender': None,
                'p_rank': None,
                'p_total_points': None
            }

        """creation of a database for players """
        db = TinyDB('db.json')
        # Player_q = Query()  # à revoir (User rebaptisé Player_q car ici il s'agit d'un joueur)
        players_db = db.table('players_db')

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
        self.p_data = self.players_db.get(doc_id=player_id)  # récup données "joueur" ds DB

        self.player = RvPlayer(self.players_db, self.p_data)
        return player()

    def load_player(self, player_id):  # pour charger le dico DB dans un nouvel objet "player" vide
        pass  # à faire ds CONTROLLER

    def update_player(self, player_id):
        pass

    def update_player_id(self, player_id):
        # update player's id (set at 'None' by default) with a new value
        self.players_db.update({'p_id': self.player_id}, doc_id=player_id)

    def update_player_ranking(self, player_id):
        """ update a player rank in DB through its ID"""
        self.players_db.update({'p_rank': self.player_ranking},
                               doc_id=player_id)

    def update_points_qty(self):  # cf controleur, A REDIGER
        """ add match score to player points qty
        (to be used to create next round's pairs of players)"""
        pass

    def delete_player(self, player_id):
        """remove a player from DB through its ID"""
        self.players_db.remove(doc_id=player_id)

    