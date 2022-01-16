from views.player_view import PlayerView
from models.player_model import Player
# from ..models.rvplayer_model import Player # modèle avec "p_data"
# from tournament_controller import TournamentController
from tinydb import where


class PlayerController:
    def __init__(self):
        self.player_view = PlayerView()

    def create_player(self, player_id=0):
        """create one player"""
        player = Player(
            player_id,
            self.ask_player_name(),
            self.ask_player_first_name(),
            self.ask_player_birth_date(),
            self.ask_player_gender(),
            self.ask_player_ranking(),
            player_points_qty=0
        )
        player.create_player()  # renvoie vers enregistrement en BDD (Model)
        return player

    # exemple d'update - ds quel cas ?
    def update_player(self, id):
        """ update player's data in  database """
        player = Player()
        player.get_player(id)
        player.name = self.ask_player_name()
        player.first_name = self.ask_player_first_name()
        player.birth_date = self.ask_player_birth_date()
        player.gender = self.ask_player_gender()
        player.ranking = self.ask_player_ranking()
        player.points_qty = self.ask_player_points_qty()  # cf Tournoi
        player.update()  # enregistrement en BDD
        return player

    def update_player2(self, id):  # update ou load ? ds quel cas ?
        player = Player()
        player.p_id = self.ask_player_id()
        player.name = self.ask_player_name()
        player.first_name = self.ask_player_first_name()
        player.birth_date = self.ask_player_birth_date()
        player.gender = self.ask_player_gender()
        player.ranking = self.ask_player_ranking()
        player.points_qty = self.ask_player_points_qty()  # cf Tournoi
        player.update()  # enregistrement en BDD
        return player

    def update_player_rank_by_id(self, player_id, player_ranking):
        """ modify player_rank through player-model for DB saving"""
        Player.update_player_ranking(player_id, player_ranking)
        check_update = Player.read_player(player_id)
        print(check_update)

    def ask_player_name(self):
        """ get player_name from User through player_view """
        PlayerView.ask_player_name()  # cf @classmethod
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

    def choose_menu_add_tournament_player(self):
        PlayerView.ask_choice_menu_add_t_player()

    def resquest_player(self):
        search_p_name = self.ask_player_name()
        search_p_firstname = self.ask_player_first_name()
        requested_player = Player.players_db.search
        (
            where('p_name') == search_p_name
        ) & (
            where('p_firstname') == search_p_firstname
            )
        print(requested_player.__dict__)
        return requested_player
