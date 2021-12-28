""" 1 to create new tournament = instance of class Tournament"""
from player import Player


class Tournament:
    def __init__(self, tournament_name, place, date, rounds_qty, rounds_list,
                 tournament_players_list, tournament_description, time_control):
        self.tournament_name = tournament_name
        self.place = place
        self.date = date
        self.rounds_qty = rounds_qty
        self.rounds_list = rounds_list
        self.tournament_players_list = tournament_players_list
        self.tournament_description = tournament_description
        self.time_control = time_control

    def create_new_tournament(self):
        """ pour test interface"""
        self.tournament_name = input ('Entrez le nom du nouveau tournoi : ')
        self.place = input ('Entrez le lieu du tournoi : ')
        self.date = input ('Entrez la date du tournoi au format JJ/MM/AAAA :') 
        self.round_qty = 4 
        self.rounds_list = ['round1', 'round2', 'round3', 'round4']
        self.tournament_description = input('Saisissez les commentaires : ')
        self.time_control = input ('choisissez entre bullet, blitz ou coup rapide :  ')
        print("Merci pour vos informations")
    
    def get_tournament_data(self): 
        self.tournament_name = input ('Entrez le nom du nouveau tournoi : ')
        self.place = input ('Entrez le lieu du tournoi : ')
        self.date = input ('Entrez la date du tournoi au format AAAA/MM/JJ :') 
        # vérifier gestion des dates (format) ds Python
        self.round_qty = 4 # dans quels cas != 4 ?
        self.rounds_list = ['round1', 'round2', 'round3', 'round4']
        # évolue si round_qty != 4  '= instances de la classe Tour'
        tournament_players_list = []
        tournament_players_list = tournament_players_list.append(Player.players_list)
        # se met à jour qd joueurs sont ajoutés
        # indices correspondant aux instances du joueur stockées en mémoire = pas clair
        self.tournament_description = input('Saisissez les commentaires de la Direction')
        # prévoir cas où saisie != bullet, blitz ou coup rapide
        self.time_control = input ('saisissez : bullet, blitz ou coup rapide')
        
        print("Nouveau tournoi créé")

    """ A DEPLACER/CORRIGER : LES METHODES CI-DESSOUS N APPARTIENNENT PAS TOUTES A CETTE CLASSE"""

    """def update_rounds_qty(self):
        # modifie valeur de rounds_qty qd !=4
        rounds_qty_default_value = input('Nombre de tours = 4. Oui ou Non ? ')
        if rounds_qty_default_value =="Non":
            rounds_qty = input('Saisissez le nombre de tours ')
        else: rounds_qty = 4
        return rounds_qty"""

    def add_players(self):
        # ajoute 8 joueurs : si nouveau joueur, l'ajouter à la base puis le "rechercher" pour j'ajouter à liste de joueurs
        # si déjà ds base,  le "rechercher" pour j'ajouter à liste de joueurs
        pass

    def generate_firstround_pairs(self):
        # generate pairs of players for the 1st round
        pass

    def update_points(self):
        # saisit, à la fin d'un tour, le nb de points de chq match (points des joueurs)
        pass

    def generate_players_pairs(self):
        # generate pairs of players for rounds >1
        pass

    def update_ranking(self):
        # met à jour le classement des joueurs
        pass

    """ Si vous avez le choix entre la manipulation de dictionnaires ou d'instances de classe, 
    choisissez toujours des instances de classe. """
    # Alors créer des classes pour : 
    # name, place, date, rounds_qty, rounds_list, players_list'?', tournament_description, time_control ?

    """ ou
        # version dictionnaire :
        def __init__(self, datas)
            self.datas = {
                "name": None,
                "place": None,
                "date": None,
                "rounds_qty": None,
                "rounds_list": None, 
                "players_list": None,
                "tournament_description": None,
                "time_control": None
            }
    """
