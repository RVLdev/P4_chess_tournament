from tinydb import TinyDB, where, Query
from models.playermodel import Player
from views.playerviews import PlayerViews
from models.tournamentmodel import Tournament


class PlayerCtrlr:
    def __init__(self):
        self.player_view = PlayerViews()

    def dis_bonjour_p_ctrl(self):  #TEST INITIAL - A SUPPRIMER
        print ('Bonjour de la classe PlayerCtrlr - fichier playercontroller')

    def create_new_player(self, tournament_id, player_id=0):
        """create one player"""
        player = Player(
            player_id,
            PlayerCtrlr.ask_player_name(self),
            PlayerCtrlr.ask_player_first_name(self),
            PlayerCtrlr.ask_player_birth_date(self),
            PlayerCtrlr.ask_player_gender(self),
            PlayerCtrlr.ask_player_ranking(self),
            player_points_qty=0
        )
        player.create_player()
        new_player_id = Player.update_player_id(self)
        new_player = Player.all_players_db.get(doc_id=new_player_id)

        db = TinyDB('db'+str(tournament_id)+'.json')
        Player.players_db = db.table('players_db')
        Player.players_db.insert(new_player)

        return new_player

    def create_new_player_in_db_all(self, player_id=0):
        """create one player in global DB"""
        player = Player(
            player_id,
            PlayerCtrlr.ask_player_name(self),
            PlayerCtrlr.ask_player_first_name(self),
            PlayerCtrlr.ask_player_birth_date(self),
            PlayerCtrlr.ask_player_gender(self),
            PlayerCtrlr.ask_player_ranking(self),
            player_points_qty=0
        )
        player.create_player()
        Player.update_player_id(self)

    def ask_player_name(self):
        """ get player_name from User through player_view """
        PlayerViews.ask_player_name()
        player_name = input()
        return player_name

    def ask_player_first_name(self):
        """ get player_first_name from User through player_view """
        PlayerViews.ask_player_first_name()
        player_first_name = input()
        return player_first_name

    def ask_player_birth_date(self):
        """ get player_birth_date from User through player_view """
        PlayerViews.ask_player_birth_date()
        player_birth_date = input()
        return player_birth_date

    def ask_player_gender(self):
        """ get player_gender from User through player_view """
        PlayerViews.ask_player_gender()
        player_gender = input()
        return player_gender

    def display_points_sorted_tournament_players(self, tournament_id):   
        """display, at a tournament's end its players sorted by points"""
 
        db = TinyDB('db'+str(tournament_id)+'.json')
        Tournament.tournaments_db = db.table('tournaments_db')
        Player.players_db = db.table('players_db')

        tournament_requested = (Tournament.tournaments_db.get(
            doc_id=tournament_id))

        tournament_pl_id_list = []  # tournament players'id list
        for t in (tournament_requested['t_players_list']):
            tournament_pl_id_list.append(t)

        tournament_players_list = []
        for pl_id in tournament_pl_id_list:
            tournament_pl = Player.players_db.get(doc_id=pl_id)
            tournament_players_list.append(tournament_pl)  # tourney's players
            
        # players sorted by descending points and by rank
        rank_sorted_p_list = sorted(tournament_players_list,
                                key=lambda k: k['p_rank'])
        points_n_rank_sorted_all_players_list = sorted(
            rank_sorted_p_list, key=lambda k: k['p_total_points'],
            reverse=True)

        # display players name, first name, points quantity, rank 
        PlayerViews.display_points_n_rank_sorted_tournament_players()
        pl_qty = (len(points_n_rank_sorted_all_players_list))
        for pl in range(0, pl_qty):
            pl_name = points_n_rank_sorted_all_players_list[pl]['p_name']
            pl_firstname = points_n_rank_sorted_all_players_list[pl]['p_firstname']
            pl_points = points_n_rank_sorted_all_players_list[pl]['p_total_points']
            pl_rank = points_n_rank_sorted_all_players_list[pl]['p_rank']
            
            print(str(pl_name)+' '+str(pl_firstname)
                  +', nombre de points : '+str(pl_points)
                  +', classement : '+str(pl_rank)) 

    def update_players_points_in_db_all(self):
        """for each player, get its total_points in each tournament,
        sum all these points and update player's total points in db_all"""

        db_all_t = TinyDB('db_all_t.json')
        Player.all_players_db = db_all_t.table('all_players_db')
        Tournament.all_tournaments_db = db_all_t.table('all_tournaments_db')
        length_tournaments_list = len(Tournament.all_tournaments_db )
        oneplayer_points_list = []

        for pl in Player.all_players_db:
            pl_name = pl['p_name']
            pl_firstname = pl['p_firstname']
            pl_doc_id = pl['p_id']
            #print(pl_name)
            
            # get one player's points in all tournaments
            for t in range(1, (length_tournaments_list+1)):
                db = TinyDB('db'+str(t)+'.json')
                Theplayer = Query()
                Player.players_db = db.table('players_db')

                one_player = (Player.players_db.get(
                    (
                        Theplayer.p_name == pl_name
                    ) & (
                        Theplayer.p_firstname == pl_firstname
                        )
                    ))
                if one_player is None:
                    # print('Joueur '+pl_name+' : aucun match du tournoi '+str(t))
                    pass
                else:
                    one_player_points = one_player['p_total_points']
                    oneplayer_points_list.append(one_player_points)
            #print(oneplayer_points_list)

            # sum all tournaments player's points and update in global DB.
            player_points_in_all_t = sum(oneplayer_points_list)
            #print(player_points_in_all_t)
            Player.all_players_db.update({
                'p_total_points': player_points_in_all_t}, 
                                         doc_ids=[pl_doc_id])
            oneplayer_points_list.clear()

    def display_all_players_sorted_by_points(self):
        db_all_t = TinyDB('db_all_t.json')
        Player.all_players_db = db_all_t.table('all_players_db')
        all_tournaments_players_list = []

        for each_player in Player.all_players_db:
            all_tournaments_players_list.append(each_player)
        # players sorted by descending points and by rank
        rank_sorted_p_list = sorted(all_tournaments_players_list,
                                key=lambda k: k['p_rank'])
        points_n_rank_sorted_all_players_list = sorted(
            rank_sorted_p_list, key=lambda k: k['p_total_points'],
            reverse=True)
        
        # display players name, first name, points quantity, rank 
        PlayerViews.display_points_n_rank_sorted_tournament_players()
        pl_qty = (len(points_n_rank_sorted_all_players_list))
        for pl in range(0, pl_qty):
            pl_name = points_n_rank_sorted_all_players_list[pl]['p_name']
            pl_firstname = points_n_rank_sorted_all_players_list[pl]['p_firstname']
            pl_points = points_n_rank_sorted_all_players_list[pl]['p_total_points']
            pl_rank = points_n_rank_sorted_all_players_list[pl]['p_rank']
            
            print(str(pl_name)+' '+str(pl_firstname)
                    +', nombre de points : '+str(pl_points)
                    +', classement : '+str(pl_rank))

    def ask_player_ranking(self):
        """ get player_ranking from User through player_view """
        PlayerViews.ask_player_ranking()
        player_rank = int(input())
        return player_rank

    def update_global_ranking(self):
        """Update global ranking with User's information"""
        PlayerCtrlr.display_all_players_sorted_by_points(self)
        PlayerViews.ask_player_to_update_rank()
        player_id = PlayerCtrlr.request_player(self)
        if player_id is None:
                pass
        else:
            PlayerViews.ask_player_ranking()
            player_rank = int(input())
            new_player_rank = Player.update_playr_rank(self, player_id,
                                                       player_rank)
            return new_player_rank

    #TRANSFERE DANS TOURNAMENT CONTROLLER*********************
    """def update_players_ranking(self):  
        # update player rank with User's information
        tournament_id = TournamentCtrlr.request_tournament_id(self)
        PlayerCtrlr.display_points_sorted_tournament_players(
            self, tournament_id)
        PlayerViews.ask_player_to_update_rank()
        player_id = PlayerCtrlr.request_tournament_player(self,
                                                               tournament_id)
        if player_id is None:
            pass
        else:
            PlayerViews.ask_player_ranking()
            player_rank = int(input())
            new_player_rank = Player.update_t_player_rank(self, 
                                                          tournament_id,
                                                          player_id,
                                                          player_rank)
            return new_player_rank"""

    def request_player(self):
        """search a player (by his name & firstname) into db"""
        db_all_t = TinyDB('db_all_t.json')
        Player.all_players_db = db_all_t.table('all_players_db')

        search_p_name = PlayerCtrlr.ask_player_name(self)
        search_p_first_name = PlayerCtrlr.ask_player_first_name(self)
        Theplayer = Query()
        searched_player = Player.all_players_db.get(
            (
                Theplayer.p_name == search_p_name
            ) & (
                Theplayer.p_firstname == search_p_first_name
                )
            )
        print(searched_player)
        if searched_player is None:
            PlayerViews.display_absent_player()
            return searched_player
        else:
            return searched_player.doc_id

    def request_tournament_player(self, tournament_id):
        """search a player (by his name & firstname) into db"""
        db = TinyDB('db'+str(tournament_id)+'.json')
        Player.players_db = db.table('players_db')

        search_p_name = PlayerCtrlr.ask_player_name(self)
        search_p_first_name = PlayerCtrlr.ask_player_first_name(self)
        Theplayer = Query()
        searched_player = Player.players_db.get(
            (
                Theplayer.p_name == search_p_name
            ) & (
                Theplayer.p_firstname == search_p_first_name
                )
            )
        print(searched_player)
        if searched_player is None:
            PlayerViews.display_absent_player()
            return searched_player
        else:
            return searched_player.doc_id
