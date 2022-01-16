from ..models.tournament_model import Tournament # model
from ..views.tournament_view import TournamentView
from player_controller import PlayerController
from rvinterface import Interface

class TournamentController:
    def __init__(self):
        self.tournament_view = TournamentView()

    def create_new_tournament(self):
        """create one tournament"""
        tournament = Tournament(
            self.ask_tournament_name(),
            self.ask_tournament_place(),
            self.ask_tournament_date(),
            self.get_tournament_players_list(),
            self.ask_tournament_description(),
            self.ask_time_control()
            )
        tournament.create_tournament() # enregistrement en BDD
        
        return tournament

    def update_tournament(self, id):
        """ update tournament's data in  database """
        tournament = Tournament()
        tournament.get_tournament(id)
        tournament.name = self.ask_tournament_name()
        tournament.place = self.ask_tournament_place()
        tournament.date = self.ask_tournament_date()
        tournament.players_list = self.get_tournament_players_list()
        tournament.description = self.ask_tournament_description()
        tournament.time_control = self.ask_time_control()
        tournament.update() # enregistrement en BDD
        return tournament

    def ask_tournament_name(self):
        TournamentView.ask_tournament_name()
        tournament_name = input()
		# vérifications !!!
        return tournament_name

    def ask_tournament_place(self):
        TournamentView.ask_tournament_place()
        tournament_place = input()
        return tournament_place

    def ask_tournament_date(self):
        TournamentView.ask_tournament_date()
        tournament_date = input()
        return tournament_date

    def add_player_to_tournament(self, newplayer):
        tournament_players_list = []
        tournament_players_list.append(newplayer)

    def get_tournament_players_list(self):
        """ get the 8 players of this tournament """
        PlayerController.create8player()
        tournament_players_list = []
        return tournament_players_list

	# si 8 nouveaux joueurs 
    def create8players(self):
        """ create a list of 8 new players"""
        tournament_players_list = []
        for t in range[:8]:
            player = PlayerController.create_player()
            tournament_players_list.append(player)
        return tournament_players_list


    def ask_tournament_description(self):
        TournamentView.ask_tournament_description()
        tournament_description = input()
        return tournament_description

    def ask_time_control(self):
        TournamentView.ask_time_control()
        time_control = input()
        return time_control
