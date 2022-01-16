from tinydb import TinyDB, Query
# from ..controllers.tournament_controller import TournamentController
from player_model import Player


class Tournament:
    """ defines an object 'tournament' : (shape, characteristics)"""
    def __init__(self, tournament_id, tournament_name, tournament_place,
                 tournament_date, tournament_players_list,
                 tournament_description,
                 tournament_time_control,
                 tournament_rounds_list=['round1', 'round2', 'round3',
                                         'round4'],
                 tournament_rounds_qty=4,):

        self.tournament_id = tournament_id
        self.tournament_name = tournament_name
        self.tournament_place = tournament_place
        self.tournament_date = tournament_date
        self.tournament_rounds_list = tournament_rounds_list
        self.tournament_players_list = tournament_players_list
        self.tournament_description = tournament_description
        self.tournament_time_control = tournament_time_control
        self.tournament_rounds_qty = tournament_rounds_qty

        tournament_rounds_list = ['round1', 'round2', 'round3', 'round4']
        # tournament_players_list = [player_id, p_rank]

        """creation of a database for tournaments """
        self.db = TinyDB('db.json')
        User = Query()  # à revoir (User à rebaptiser  ici c'est un tournoi)
        self.tournaments_db = self.db.table('tournaments_db')

    def create_tournament(self):
        # enregistrement en BDD ==> code A VERIFIER
        self.tournaments_db.insert(
            {
                't_id': self.tournament_id,
                't_name': self.tournament_name,
                't_place': self.tournament_place,
                't_date': self.tournament_date,
                't_players_list': self.tournament_players_list,
                't_description': self.tournament_description,
                't_time_control': self.tournament_time_control,
                't_rounds_list': self.tournament_rounds_list,
                't_round_qty': self.tournament_rounds_qty
            }
            )

    def read_tournament(self, tournament_id):
        self.tournaments_db.get(doc_id=tournament_id)
        return Tournament()

    def update_tournament(self, id):
        # MAJ en BDD (exple : liste des joueurs)
        pass

    def update_tournament_id(self, tournament_id):
        self.tournaments_db.update({'p_id': self.tournament_id},
                                   doc_id=tournament_id)

    def sort_tournament_players_list_by_rank(self):
        sorted(self.tournament_players_list, key=lambda player: Player.player_ranking)
        return self.tournament_players_list

    def calculate_p_total_points(self, player_id):
        # somme des scores des matchs d'un joueur
        return Player.player_points_qty

    def sort_tournament_players_list_by_points(self):
        sorted(self.tournament_players_list, key=lambda player: Player.player_points_qty)
        return self.tournament_players_list

    def update_tournament_players_list(self, tournament_id):
        self.tournaments_db.update(
            {
                't_players_list': self.tournament_players_list
            },
            doc_id=tournament_id
        )

    def update_tournament_rounds_list(self, tournament_id):
        self.tournaments_db.update(
            {
                't_rounds_list': self.tournament_rounds_list
            },
            doc_id=tournament_id
        )

    def delete_tournament(self, tournament_id):
        self.tournaments_db.remove(doc_id=tournament_id)

    def add_players(self, player_id):
        tournament_players_list = []
        player = Player
        
        tournament_players_list.append(player_id)
        """  PROVISOIRE ajoute 8 joueurs :
        * si nouveau joueur, l'ajouter à la base puis le "rechercher" pour
          l'ajouter à liste de joueurs,
          
        * si déjà ds base,  le "rechercher" pour j'ajouter à liste de joueurs
        tournament_players_list = []
        tournament_players_list = tournament_players_list.append(PlayerController.player1) + ATTENTION TROP LONG !!!
        """

    def read_all_players(self, tournament_players_list):
        # tournament_players_list = liste des id des joueurs du tournoi
        """ get list of tournament players"""
        for i in tournament_players_list:
            Player.players_db.get(doc_id=i)
