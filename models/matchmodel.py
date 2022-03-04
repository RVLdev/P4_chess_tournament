from tinydb import TinyDB, where, Query


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

    def dis_bonjour_m_model(self):  #TEST INITIAL - A SUPPRIMER*****************************
        print ('Bonjour de la classe Match - fichier matchmodel')


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
