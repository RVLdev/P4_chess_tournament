from tinydb import TinyDB, where, Query


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

    def dis_bonjour_p_model(self):  #TEST INITIAL - A SUPPRIMER*****************************
        print ('Bonjour de la classe Player - fichier playermodel')

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
    
