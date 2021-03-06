from models.matchmodel import Match


class MatchCtrlr:
    def __init__(self, match_player1, match_player2):
        self.match_player1 = match_player1
        self.match_player2 = match_player2

    def create_new_match(self, tournament_id, match_player1, match_player2,
                         match_id=0, player1_score=0, player2_score=0):
        """Create one match."""
        match = Match(match_id,
                      match_player1,  # player's doc_id
                      match_player2,
                      player1_score,
                      player2_score)
        match.create_match(tournament_id)
        self.match_id = Match.update_match_id(self, tournament_id)
        return self.match_id
