from ..views.player_view import PlayerView # vue
from ..models.player_model import Player # model
from ..models.rvplayer_model import RvPlayer # modèle avec "p_data"
from tournament_controller import TournamentController


class PlayerController:
	def __init__(self):
		self.player_view = PlayerView()

	def create_player(self):
		"""create one player"""
		player_points_qty = 0 # à gérer ds tournoi
		player = Player(
			self.ask_player_name(),
			self.ask_player_first_name(),
			self.ask_player_birth_date(),
			self.ask_player_gender(),
			self.ask_player_ranking(),
			player_points_qty
			)
		player.create_player() # renvoie vers enregistrement en BDD (Model)
		return player

	# inutile ! A SUPPR
	def save_player(self):
		""" send to player-model for DB saving"""
		Player.save_player()

	# à gérer ds Tournoi
	def create8players(self):
		""" create a list of 8 new players"""
		TournamentController.tournament_players_list = []
		player1 = self.create_player()
		TournamentController.tournament_players_list.append(player1)
		player2 = self.create_player()
		TournamentController.tournament_players_list.append(player2)
		player3 = self.create_player()
		TournamentController.tournament_players_list.append(player3)
		player4 = self.create_player()
		TournamentController.tournament_players_list.append(player4)
		player5 = self.create_player()
		TournamentController.tournament_players_list.append(player5)
		player6 = self.create_player()
		TournamentController.tournament_players_list.append(player6)
		player7 = self.create_player()
		TournamentController.tournament_players_list.append(player7)
		player8 = self.create_player()
		TournamentController.tournament_players_list.append(player8)
		return TournamentController.tournament_players_list

	# exemple d'update
	def update_player(self, id):
		""" update player's data in  database """
		player = Player()
		player.get_player(id)
		player.name = self.ask_player_name()
		player.first_name = self.ask_player_first_name()
		player.birth_date = self.ask_player_birth_date()
		player.gender = self.ask_player_gender()
		player.ranking = self.ask_player_ranking()
		player.points_qty = self.ask_player_points_qty()
		player.update() # enregistrement en BDD
		return player

	def load_player(self, p_data):  # si model = rvplayer_model
		player = RvPlayer()
		player.p_id = p_data['p_id']
		player.p_name = p_data['p_name']
		player.p_firstname = p_data['p_firstname']
		player.p_birthdate = p_data['p_birthdate']
		player.p_gender = p_data['p_gender']
		player.p_rank = p_data['p_rank']
		player.p_total_points = p_data['p_total_points']
		player.update() # enregistrement en BDD
		return player 
     

	def update_player_rank_by_id(self, id):
		pass # cf ci_dessous :

   	# L'utilisateur connaît nom et prénom du joueur pas l'ID => ma suggestion :
	def update_player_rank(self):
		""" get update information and send it to player-model for DB saving"""
		player_name = self.ask_player_name()
		player_first_name = self.ask_player_first_name()
		player_ranking = self.ask_player_ranking()
		self.Player.update_player_ranking()

	def ask_player_name(self):
		""" get player_name from User through player_view """
		PlayerView.ask_player_name() # cf @classmethod
		player_name = input()
		# vérifications !!!
		return player_name

	def ask_player_first_name(self):
		""" get player_first_name from User through player_view """
		PlayerView.ask_player_first_name()
		player_first_name = input()
		return player_first_name

	def ask_player_birth_date(self):
		""" get player_birth_date from User through player_view """
		PlayerView.ask_player_birth_date()
		player_birth_date = input()
		return player_birth_date

	def ask_player_gender(self):
		""" get player_gender from User through player_view """
		PlayerView.ask_player_gender()
		player_gender = input()
		return player_gender

	def ask_player_ranking(self):
		""" get player_ranking from User through player_view """
		PlayerView.ask_player_ranking()
		player_ranking = input()
		return player_ranking

	def update_player_points_qty(self):  # A GERER DS TOURNOI
		# à la fin d'un tour et pour chaque joueur
		# for item in players_list:
		#     player_points_qty = player_points_qty + Match.playerscore
		"""
        add match score to player points qty
        (to be used to create next round's pairs of players)"""
		pass
