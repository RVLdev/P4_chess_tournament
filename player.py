class Player:
    """ defines an object 'player' : its caracteristics and actions"""
    def __init__(self, player_name, player_first_name, player_birth_date,
                 player_gender, player_ranking, player_points_qty):
        self.player_name = player_name
        self.player_first_name = player_first_name
        self.player_birth_date = player_birth_date
        self.player_gender = player_gender
        self.player_ranking = player_ranking
        self.player_points_qty = player_points_qty

    def create_player(self):
        """ pour test inerface"""
        print(" ==> Joueur créé")

    def create_eight_players(self, a_player):
        """Creates a list filled eight times by """
        players_list = []
        for i in range(8):
            self.create_player_model(self)
            self.get_player_data(a_player)
            players_list.append(a_player)
        return players_list

    def create_player_model(self):
        """Create a model for any player"""
        a_player = {'player_name': None,
                    'player_first_name': None,
                    'player_birth_date': None,
                    'player_gender': None,
                    'player_ranking': None,
                    'player_points_qty': None
                    }
        return a_player
        

    def get_player_data(self, a_player):
        """Ask the user for player's data"""
        return {
            a_player["player_name"]: input('Entrez le nom du joueur : '),
            a_player["player_first_name"]:
                input('Entrez le prenom du joueur : '),
            a_player["player_birth_date"]:
                input('Entrez sa date de naissance (JJ/MM/AAAA) : '),
            a_player["player_gender"]:
                input('Indiquez le sexe du joueur (H/F): '),
            a_player["player_ranking"]: input('Entrez son classement : '),
            a_player["player_points_qty"]: 0
            }

 
    def modify_player_rank(self):
        """ From start menu ; modify the ranking of a player"""
        print('==> mise à jour du classement du joueur')
