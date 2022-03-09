from tinydb import TinyDB, Query
from models.playermodel import Player
from views.playerviews import PlayerViews
from models.tournamentmodel import Tournament


class PlayerCtrlr:
    def __init__(self):
        self.player_view = PlayerViews()

    def create_new_player(self, tournament_id):
        """Create one player, store it in databases and
        return its identifier.
        """
        new_player_id = PlayerCtrlr.create_new_player_in_db_all(self,
                                                                player_id=0)
        new_player = Player.all_players_db.get(doc_id=new_player_id)
        db = TinyDB('db' + str(tournament_id) + '.json')
        Player.players_db = db.table('players_db')
        Player.players_db.insert(new_player)

        return new_player_id

    def create_new_player_in_db_all(self, player_id=0):
        """Create one player in global database."""
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
        return new_player_id

    def ask_player_name(self):
        """Get player_name from User through player_view."""
        PlayerViews.ask_player_name()
        player_name = input()
        return player_name

    def ask_player_first_name(self):
        """Get player_first_name from User through player_view."""
        PlayerViews.ask_player_first_name()
        player_first_name = input()
        return player_first_name

    def ask_player_birth_date(self):
        """Get player_birth_date from User through player_view."""
        PlayerViews.ask_player_birth_date()
        player_birth_date = input()
        return player_birth_date

    def ask_player_gender(self):
        """Get player_gender from User through player_view."""
        PlayerViews.ask_player_gender()
        player_gender = input()
        return player_gender

    def get_points_sorted_tournament_players(self, tournament_id):
        """Get tournament players sorted by points."""
        tournament_players_list = PlayerCtrlr.get_tournament_players_list(
            self, tournament_id)
        # players sorted by descending points and by rank
        players_list = tournament_players_list
        pts_n_rank_sorted_players_list = PlayerCtrlr.sort_players_by_points(
            self, players_list)
        PlayerCtrlr.display_points_n_rank_sorted_tournament_players(
            self, pts_n_rank_sorted_players_list)

    def get_tournament_players_list(self, tournament_id):
        """Get the tournament's players list."""
        db = TinyDB('db' + str(tournament_id) + '.json')
        Tournament.tournaments_db = db.table('tournaments_db')
        Player.players_db = db.table('players_db')
        tournament_players_list = []

        tournament_pl_id_list = (Tournament.tournaments_db.get(
            doc_id=tournament_id))['t_players_list']
        for pl_id in tournament_pl_id_list:
            tournament_pl = Player.players_db.get(doc_id=pl_id)
            tournament_players_list.append(tournament_pl)
        return tournament_players_list

    def display_points_n_rank_sorted_tournament_players(self,
                                                        pts_n_rank_sorted_players_list):
        """Display tournament players sorted by points and rank."""
        PlayerViews.display_points_n_rank_sorted_tournament_players()
        pl_qty = (len(pts_n_rank_sorted_players_list))
        for pl in range(0, pl_qty):
            pl_name = pts_n_rank_sorted_players_list[pl]['p_name']
            pl_firstname = pts_n_rank_sorted_players_list[pl]['p_firstname']
            pl_points = pts_n_rank_sorted_players_list[pl]['p_total_points']
            pl_rank = pts_n_rank_sorted_players_list[pl]['p_rank']
            print(
                str(pl_name) + ' ' + str(
                    pl_firstname) + ', nombre de points : ' + str(
                        pl_points) + ', classement : ' + str(pl_rank)
            )

    def update_players_points_in_db_all(self):
        """For each player, get its total_points in each tournament,
        sum all these points and update player's total points in db_all.
        """
        db_all_t = TinyDB('db_all_t.json')
        Player.all_players_db = db_all_t.table('all_players_db')
        Tournament.all_tournaments_db = db_all_t.table('all_tournaments_db')
        length_tournaments_list = len(Tournament.all_tournaments_db)
        oneplayer_pts_list = []

        for pl in Player.all_players_db:
            pl_name = pl['p_name']
            pl_firstname = pl['p_firstname']
            pl_doc_id = pl['p_id']

            oneplayer_pts_list = PlayerCtrlr.get_all_tournaments_player_points(
                self, length_tournaments_list, pl_name, pl_firstname,
                oneplayer_pts_list
            )

            player_points_in_all_t = sum(oneplayer_pts_list)
            Player.all_players_db.update({
                'p_total_points': player_points_in_all_t},
                doc_ids=[pl_doc_id]
            )
            oneplayer_pts_list.clear()

    def get_all_tournaments_player_points(self, length_tournaments_list,
                                          pl_name, pl_firstname,
                                          oneplayer_pts_list):
        """Get one player's points in all tournaments"""
        for tourn in range(1, (length_tournaments_list + 1)):
            db = TinyDB('db' + str(tourn) + '.json')
            Theplayer = Query()
            Player.players_db = db.table('players_db')
            one_player = (Player.players_db.get(
                (Theplayer.p_name == pl_name
                 ) & (
                    Theplayer.p_firstname == pl_firstname))
            )
            if one_player is None:
                pass
            else:
                one_player_points = one_player['p_total_points']
                oneplayer_pts_list.append(one_player_points)
        return oneplayer_pts_list

    def display_all_players_sorted_by_points(self):
        """Display all players from global database, sorted by points."""
        db_all_t = TinyDB('db_all_t.json')
        Player.all_players_db = db_all_t.table('all_players_db')
        all_tournaments_players_list = []

        for each_player in Player.all_players_db:
            all_tournaments_players_list.append(each_player)

        players_list = all_tournaments_players_list
        pts_n_rank_sorted_players_list = PlayerCtrlr.sort_players_by_points(
            self, players_list)
        PlayerCtrlr.display_points_n_rank_sorted_tournament_players(
            self, pts_n_rank_sorted_players_list)

    def sort_players_by_points(self, players_list):
        """Sort players by descending points and by rank."""
        rank_sorted_p_list = sorted(players_list,
                                    key=lambda k: k['p_rank'])
        pts_n_rank_sorted_players_list = sorted(
            rank_sorted_p_list, key=lambda k: k['p_total_points'],
            reverse=True)
        return pts_n_rank_sorted_players_list

    def ask_player_ranking(self):
        """Get player_ranking from User through player_view."""
        PlayerViews.ask_player_ranking()
        player_rank = int(input())
        return player_rank

    def update_global_ranking(self):
        """Update global ranking with User's information."""
        PlayerCtrlr.update_players_points_in_db_all(self)
        PlayerCtrlr.display_all_players_sorted_by_points(self)
        PlayerViews.ask_player_to_update_rank()
        player_id = PlayerCtrlr.request_player(self)
        if player_id is None:
            PlayerViews.display_absent_player()
        else:
            PlayerViews.ask_player_ranking()
            player_rank = int(input())
            new_player_rank = Player.update_playr_rank(self, player_id,
                                                       player_rank)
            return new_player_rank

    def request_player(self):
        """Search any player (by his name & firstname) into database."""
        db_all_t = TinyDB('db_all_t.json')
        Player.all_players_db = db_all_t.table('all_players_db')

        search_p_name = PlayerCtrlr.ask_player_name(self)
        search_p_first_name = PlayerCtrlr.ask_player_first_name(self)
        Theplayer = Query()
        searched_player = Player.all_players_db.get(
            (Theplayer.p_name == search_p_name
             ) & (
                 Theplayer.p_firstname == search_p_first_name)
        )
        print(searched_player)
        if searched_player is None:
            PlayerViews.display_absent_player()
            return searched_player
        else:
            return searched_player.doc_id

    def request_tournament_player(self, tournament_id):
        """Search a player of a specific tournament, by his name & firstname,
        into tournament database.
        """
        db = TinyDB('db' + str(tournament_id) + '.json')
        Player.players_db = db.table('players_db')

        search_p_name = PlayerCtrlr.ask_player_name(self)
        search_p_first_name = PlayerCtrlr.ask_player_first_name(self)
        Theplayer = Query()
        searched_player = Player.players_db.get(
            (Theplayer.p_name == search_p_name
             ) & (
                 Theplayer.p_firstname == search_p_first_name)
        )
        print(searched_player)
        if searched_player is None:
            PlayerViews.display_absent_player()
            return searched_player
        else:
            return searched_player.doc_id
