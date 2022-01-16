from tinydb import TinyDB, Query


class Match:
    """ defines an object 'player' : (shape, characteristics)"""
    def __init__(self, match_id, player1, player2, player1_score=0,
                 player2_score=0):
        self.match_id = match_id
        self.player1 = player1
        self.player2 = player2
        self.player1_score = player1_score
        self.player2_score = player2_score
        self.sorted_players_list = []

        """creation of a database for matches """
        self.db = TinyDB('db.json')
        User = Query()  # à revoir
        self.matches_db = self.db.table('matches_db')

    def create_match(self, match_id, player1, player2, player1_score,
                     player2_score):
        """ create (and save) a match"""
        self.matches_db.insert(
            {
                'match_id': match_id
            },
            {
                'chess_player1': player1,  # player_id
                'score_player1': player1_score
            },
            {
                'chess_player2': player2,  # player_id
                'score_player2': player2_score
            }
        )

    def read_match(self, match_id):
        self.matches_db.get(doc_id=match_id)
        return Match()

    def update_match_id(self, match_id):
        self.matches_db.update({'match_id': self.match_id}, doc_id=match_id)

    def update_match_scores(self, match_id):
        self.matches_db.update({'score_player1': self.player1_score},
                               doc_id=match_id)
        self.matches_db.update({'score_player2': self.player2_score},
                               doc_id=match_id)

    def delete_match(self, match_id):
        self.matches_db.remove(doc_id=match_id)

# def read_match(self, id) ['read' équivaut à 'get'] # doit retourner un objet MATCH !!!
# def update_match(self, id, player1, player2, player1_score, player2_score)
# def delete_match(self, id)
