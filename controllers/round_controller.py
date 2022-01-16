from ..models.round_model import Round
from ..views.round_view import RoundView

class RoundController: 
    def __init__(self):
        pass
    
    def create_round(self):
        pass
    
    def save_round(self):
        """ send to round-model for DB saving"""
        self.Round.save_round()
        

    def ask_round_name(self):
        """ get or ask round name"""
        pass
    
    def end_round(self):
        Round.close_round()
        
        