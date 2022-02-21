import time
from p4_models import Tournament
from p4_models import Round
from p4_models import Match
from p4_models import Player
from p4_views import TournamentView
from p4_views import RoundView
from p4_views import PlayerView
from p4_views import MatchView
from tinydb import TinyDB, where, Query
from datetime import datetime


class TournamentCtlr:
    def __init__(self):
        self.tournament_view = TournamentView()
        self.tournament_id = 0
        self.tournament_rounds_qty = 4
        self.tournament_players_id_list = []
        self.tournament_rounds_id_list = []
        self.t_full_players_list = []
        self.r_matches_id_list = []  # EMPLACEMENT A REVOIR
        self.first_round_matches = []
        self.rank_sorted_p_list = []
        self.points_sorted_p_list = []
        self.points_sorted_p_id_list = []
        self.m_list = []  # list of matches from DB
        self.previous_pairs_list = []  # previous matches pairs of players
        self.db = TinyDB('db.json')
        self.Thetournmt = Query()
        self.tournaments_db = self.db.table('tournaments_db')
        self.Theplayer = Query()
        self.players_db = self.db.table('players_db')
        self.Theround = Query()
        self.rounds_db = self.db.table('rounds_db')
        self.Thematch = Query()
        self.matches_db = self.db.table('matches_db')
    
    def create_new_tournament(self):
        #create one tournament
        tournament = Tournament(
            self.tournament_id,
            self.ask_tournament_name(),
            self.ask_tournament_place(),
            self.ask_tournament_date(),
            self.ask_tournament_description(),
            self.ask_time_control(),
            self.tournament_rounds_qty,  # 4 by default
            self.tournament_players_id_list,  # doc_ids
            self.tournament_rounds_id_list   # doc_ids
            )
        tournament.create_tournament()
        self.tournament_id = Tournament.update_tournament_id(self)

        # VERIFICATION
        print('Nouveau tournoi créé')
        # Complete tournament object with rounds_qty, players_id_list, rounds_id_list
        self.complete_tourney_data(self.tournament_id)
        return tournament

    def ask_tournament_name(self):
        # ask User tournament name 
        TournamentView.ask_tournament_name()
        tournament_name = input()
        return tournament_name

    def ask_tournament_place(self):
        # ask User tournament place
        TournamentView.ask_tournament_place()
        tournament_place = input()
        return tournament_place

    def ask_tournament_date(self):
        # ask User tournament date(s)
        TournamentView.ask_tournament_date()
        tournament_date = input()
        return tournament_date

    def ask_tournament_description(self):
        # ask User tournament description and comments
        TournamentView.ask_tournament_description()
        tournament_description = input()
        return tournament_description

    def ask_time_control(self):
        # ask User time control
        TournamentView.ask_time_control()
        time_control = input()
        return time_control
    
    def complete_tourney_data(self, tournament_id):
        # complete tournament with rounds_qty, players_id_list, rounds_id_list
        self.confirm_tournament_rounds_qty(tournament_id)
        self.create_tournament_players_id_list(tournament_id)
        self.create_tournament_rounds_id(tournament_id)
        TournamentView.end_tournament()
        PlayerController.suggest_ranking_update(self)

    def confirm_tournament_rounds_qty(self, tournament_id):
        # Get tournament_rounds_qty confirmation from User
        TournamentView.ask_tournament_rounds_qty()
        tournament_rounds_qty = int(input())
        # load tournament_rounds_qty update into DB
        Tournament.update_tournament_rounds_qty(self, tournament_rounds_qty,
                                                tournament_id)
        return tournament_rounds_qty

    def create_tournament_players_id_list(self, tournament_id):  # doc_ids
        # create this tournament's list of 8 players
        while len(self.tournament_players_id_list) < 8:
            TournamentView.ask_for_player_inclusion()
            self.add_player_to_tournament(tournament_id)
            # load tournament_players_id_list into DB
            Tournament.update_tournament_players_id_list(
                   self,
                   self.tournament_players_id_list,
                   tournament_id
                   )
        print('Liste des joueurs du tournoi complète')  # A AFFICHER DS INTERFACE (pas ici)
        return self.tournament_players_id_list

    def add_player_to_tournament(self, tournament_id):
        # add player to tournament_players_id_list 
        # check if player in DB (get player's doc_id)
        requested_player = PlayerController.request_player(self)
        # if player not in DB, launch its creation and add it to list
        if requested_player is None:
            print("Pour l'ajouter, merci de saisir à nouveau : ")
            new_player = PlayerController.create_new_player(self, player_id=0)
            Theplayer = Query()
            new_player_id = (Player.players_db.get(
                (
                 Theplayer.p_name == new_player.player_name
                ) & (
                 Theplayer.p_firstname == new_player.player_first_name
                )
            )).doc_id

            self.tournament_players_id_list.append(new_player_id)
        # if player in DB, add it to list
        else:
            self.tournament_players_id_list.append(requested_player)
            print(self.tournament_players_id_list)
        # load tournament_players_id_list into DB
        Tournament.update_tournament_players_id_list(
                   self,
                   self.tournament_players_id_list,
                   tournament_id
                   )
        return self.tournament_players_id_list
    
    def create_tournament_rounds_id(self, tournament_id):
        # create tournament's rounds
        self.create_first_round(tournament_id)
        self.create_next_rounds(tournament_id)

    def update_tournament_rd_id_list(self, tournament_rounds_id_list,
                                     tournament_id):
        # load tournament_rounds_id_list update into DB
        Tournament.update_tournament_rounds_id_list(self,
                                                    tournament_rounds_id_list,
                                                    tournament_id)
   
    def create_first_round(self, tournament_id):
        # create and load first round into DB 
        new_round = RoundController.create_new_round(self,
                                                     tournament_id,
                                                     self.r_matches_id_list,
                                                     round_id=0,
                                                     end_date_time=0,
                                                     start_date_time=0,
                                                     )
        print(new_round.round_name + ' créé')

        # get new_round id
        Theround = Query()
        new_round_id = (Round.rounds_db.get(
            Theround.r_name == new_round.round_name
            )).doc_id
        self.tournament_rounds_id_list.append(new_round_id)
        # load tournament_rd_id_list into DB
        self.update_tournament_rd_id_list(self.tournament_rounds_id_list,
                                          tournament_id)
        
        round_id = new_round_id
        
        # fill 1st round matches_list and load it into DB
        r_matches_id_list = self.create_first_r_matches_list(tournament_id, round_id)
        Round.update_r_matches_list(self, round_id, r_matches_id_list)
        
        # start 1st round and load start_date_and_time into DB
        self.start_date_time = RoundController.start_round(self)
        RoundController.update_start_date_and_time(self, self.start_date_time,
                                                   round_id)
        print(self.start_date_time)

        # end 1st round
        self.closing_a_round(round_id)

        # update players scores and points
        self.update_matches_scores_players_points()

        r_matches_id_list.clear()

    def create_next_rounds(self, tournament_id):
        matches_nb = (len(self.tournament_players_id_list))/2
        for rd in range (1, int(matches_nb)):
            new_round = RoundController.create_new_round(self,
                                                     tournament_id,
                                                     self.r_matches_id_list,
                                                     round_id=0,
                                                     end_date_time=0,
                                                     start_date_time=0,
                                                     )

            print(new_round.round_name + 'créé')
            Theround = Query()
            new_round_id = (Round.rounds_db.get(
                Theround.r_name == new_round.round_name
                )).doc_id

            self.tournament_rounds_id_list.append(new_round_id)
            self.update_tournament_rd_id_list(self.tournament_rounds_id_list,
                                            tournament_id)

            round_id = new_round_id

            # fill matches_list
            r_matches_id_list = self.create_next_round_matches_list(tournament_id, round_id)
            Round.update_r_matches_list(self, round_id, r_matches_id_list)
            
            # start round
            self.start_date_time = RoundController.start_round(self)
            RoundController.update_start_date_and_time(self, 
                                                       self.start_date_time,
                                                       round_id)
            print(self.start_date_time)

            # end round
            self.closing_a_round(round_id)
            # update scores and points
            self.update_matches_scores_players_points()
            
            r_matches_id_list.clear()
            
    def create_first_r_matches_list(self, tournament_id, round_id):      
        # create matches for first round
        rank_sorted_p_list = self.sort_tournament_players_list_by_rank(tournament_id)

        matches_qty = len(rank_sorted_p_list)/2
        for i in range(0, int(matches_qty)):
            match_player1 = rank_sorted_p_list[i]['p_id']
            match_player2 = rank_sorted_p_list[i+int(matches_qty)]['p_id']
            match = MatchController.create_new_match(self, match_player1,
                                                     match_player2,
                                                     match_id=0,
                                                     player1_score=0,
                                                     player2_score=0)
            new_m_id = match.update_match_id()  # get new match 'id'
            self.r_matches_id_list.append(new_m_id)
            
            Round.update_r_matches_list(self, round_id, self.r_matches_id_list)
            time.sleep(5)
        print('Matchs du 1er tour créés')
        rank_sorted_p_list.clear()
        return self.r_matches_id_list
    
    def sort_tournament_players_list_by_rank(self, tournament_id):
        """sort by rank tournament players list"""
        self.tournament_players_id_list = (Tournament.tournaments_db.get(
            doc_id = tournament_id))['t_players_list']

        t_full_players_list = []
        for pl_id in self.tournament_players_id_list:  # doc_ids
            t_full_player = Player.players_db.get(doc_id=pl_id)
            t_full_players_list.append(t_full_player)

        rank_sorted_p_list = sorted(t_full_players_list,
                                    key=lambda k: k['p_rank'])
        t_full_players_list.clear()
        return rank_sorted_p_list

    def create_next_round_matches_list(self, tournament_id, round_id):
        """ create matches for round > 1 """
        next_round_p_pairs_list = self.compare_matches_p_pairs(tournament_id)
        
        matches_qty = len(next_round_p_pairs_list)
        for i in range(0, int(matches_qty)):
            match_player1 = next_round_p_pairs_list[i][0]  # player1 doc_id
            match_player2 = next_round_p_pairs_list[i][1]
            match = MatchController.create_new_match(self,
                                                     match_player1,
                                                     match_player2,
                                                     match_id=0,
                                                     player1_score=0,
                                                     player2_score=0)
            new_m_id = match.update_match_id()
            self.r_matches_id_list.append(new_m_id)
            Round.update_r_matches_list(self, round_id, self.r_matches_id_list)
        
        print('Matchs de ce tour créés')    
        next_round_p_pairs_list.clear() 
       
        #time.sleep(3)
           
        return self.r_matches_id_list

    def sort_t_players_id_list_by_points(self, tournament_id):
        """ get tournament players list sorted by rank and total points """ 
        rank_sorted_p_list = self.sort_tournament_players_list_by_rank(tournament_id)
        points_sorted_p_list = sorted(rank_sorted_p_list,
                                      key=lambda k: k['p_total_points'],
                                      reverse=True)

        time.sleep(3)
        
        for p in points_sorted_p_list:  # parenthèses ou crochets autour de "int"
            self.points_sorted_p_id_list.append(p['p_id'])
        print('Joueurs triés pour le prochain tour')
        # print(self.points_sorted_p_id_list)
        rank_sorted_p_list.clear()
        
        time.sleep(5)
        
        return self.points_sorted_p_id_list  # players'doc_ids

    def create_test_players_pair(self, i, points_sorted_p_id_list):
        # create pair of players to be tested
        test_pair = [points_sorted_p_id_list[0],
                     points_sorted_p_id_list[i]]
        return test_pair

    def create_prev_matches_players_id_list(self, tournament_id):
        # get list of previous matches pairs of players
        this_tournament = Tournament.tournaments_db.get(doc_id=tournament_id)
        tournmt_r_id_list = this_tournament['t_rounds_list']

        rd_match_id_list = []
        for item in tournmt_r_id_list:
            rd_match_id = (Round.rounds_db.get(doc_id=item))['rnd_matches_list']
            rd_match_id_list.append(rd_match_id)
        del rd_match_id_list[-1] # del empty list from current round

        i = len(rd_match_id_list)
        id_matches_list = []
        for j in range (0, i):
            for k in rd_match_id_list[j]:
                id_matches_list.append(k)

        m_list = []
        for m in id_matches_list:
            prev_matches = Match.matches_db.get(doc_id=m)
            m_list.append(prev_matches)  # full matches

        nb_prev_matchs = len(m_list)
        previous_pairs_list = []
        for n in range(0, nb_prev_matchs):
            previous_pairs_list.append([m_list[n]['chess_player1'],
                                        m_list[n]['chess_player2']])
        return previous_pairs_list

    def compare_matches_p_pairs(self, tournament_id):
        # check players pairs to get uniq players players
        points_sorted_p_id_list = self.sort_t_players_id_list_by_points(tournament_id)
        next_round_p_pairs_list = []  # list of pairs of players for next matches
        previous_pairs_list = self.create_prev_matches_players_id_list(tournament_id)
        i = 1

        while len(points_sorted_p_id_list) > 0:
            testing_pair = self.create_test_players_pair(i, points_sorted_p_id_list)
            
            if testing_pair in previous_pairs_list:
                # ALREADY PLAYED pair
                if len(points_sorted_p_id_list) < 4:
                    next_round_p_pairs_list.append(testing_pair)
                    return next_round_p_pairs_list    
                else:
                    i += 1
                    testing_pair = self.create_test_players_pair(i,points_sorted_p_id_list)

            else:
                # UNIQUE pair of players to be added to next round matches
                print('L446 UNIQUE pair')
                next_round_p_pairs_list.append(testing_pair)
                
                # update points_sorted_p_id_list (avoid testing same players)
                del points_sorted_p_id_list[0]
                del points_sorted_p_id_list[i-1]

                if len(points_sorted_p_id_list) > 0:
                    # new testing_pair:
                    i = 1
                    testing_pair = self.create_test_players_pair(i, points_sorted_p_id_list) 
                else:
                    return next_round_p_pairs_list
        print('L462 next_round_p_pairs_list')
        print(next_round_p_pairs_list)
        
        self.previous_pairs_list.clear()
        points_sorted_p_id_list.clear()
        
        return next_round_p_pairs_list

    def closing_a_round(self, round_id):
        # Close round by adding round_end_date_time
        RoundView.ask_round_closing(self)
        r_closing = input()
        if r_closing == 'N':
            print('Tour non terminé')
            # + RETOUR AU MENU !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        else:
            end_date_time = Round.close_round(self, round_id)
            # load round_end_date_time into DB
            Round.update_round_end_date_time(self, round_id, end_date_time)
            print('Date et heure de FIN du tour:')
            print(end_date_time)
        return end_date_time

    def update_matches_scores_players_points(self):
        """ update round matches players'score and players'total points"""
        MatchView.update_scores()  # print 'Saisie des scores'
        
        round_id = self.request_round_id()  # get relevant Tournament & Round
        r_matches_id_list = (Round.rounds_db.get(doc_id=round_id)
                        )['rnd_matches_list']

        # VERIFICATION intermédiaire
        print('Liste des matchs pour màj des scores')
        print(r_matches_id_list)

        nbr_matches = len(r_matches_id_list)
        for i in range(0, nbr_matches):
            # players doc_ids
            player1_id = (Match.matches_db.get(doc_id=r_matches_id_list[i])
                          )['chess_player1']
            player2_id = (Match.matches_db.get(doc_id=r_matches_id_list[i])
                          )['chess_player2']

            player1_score = self.ask_player1_score(player1_id, player2_id)
            player2_score = self.ask_player2_score(player1_id, player2_id)

            self.update_player_points_qty(player1_id, player2_id,
                                          player1_score, player2_score)

            # update matches_db
            match_id = r_matches_id_list[i]
            Match.update_players_scores(self, match_id, player1_score,
                                        player2_score)

    def request_round_id(self):
        # liste des tournois :
        print('Liste des tournois:')
        for t in Tournament.tournaments_db:
            print(t['t_name'])
        RoundView.ask_tournament_name(self)
        tournament_name = input()
        Thetournmt = Query()
        rounds_id_list = (Tournament.tournaments_db.get(
            Thetournmt.t_name == tournament_name))['t_rounds_list']
        # liste des rounds
        print('Liste des tours du tournoi :')
        #print(rounds_id_list)  # VERIF
        for rd_id in rounds_id_list:
            round_name = (Round.rounds_db.get(doc_id=rd_id))['r_name']
            print(round_name)
        RoundView.ask_round_name(self)
        round_name_req = input()
        Theround = Query()
        round_id = (Round.rounds_db.get(Theround.r_name == round_name_req)
                    )['r_id']
        return round_id

    def ask_player1_score(self, player1_id, player2_id):
        """ get player1 's score"""
        # get chess_players names
        name_pl1 = Player.players_db.get(doc_id=player1_id)['p_name']
        name_pl2 = Player.players_db.get(doc_id=player2_id)['p_name']
        
        print('Match ' + name_pl1 + " contre " + name_pl2)
        print('1er joueur : ' + name_pl1)
        player1_score = float(input('Saisissez son score (0 ou 0.5 ou 1) : '))
        return player1_score

    def ask_player2_score(self, player1_id, player2_id):
        """ get player2 's score"""
        # get chess_players names
        name_pl1 = Player.players_db.get(doc_id=player1_id)['p_name']
        name_pl2 = Player.players_db.get(doc_id=player2_id)['p_name']
        
        print('Match ' + name_pl1 + " contre " + name_pl2)
        print('2eme joueur : ' + name_pl2)
        player2_score = float(input('Saisissez son score (0 ou 0.5 ou 1) : '))
        return player2_score

    def update_player_points_qty(self, player1_id, player2_id, player1_score,
                                 player2_score):
        pl1_points = (Player.players_db.get(doc_id=player1_id)
                      )['p_total_points']

        pl2_points = (Player.players_db.get(doc_id=player2_id)
                      )['p_total_points']

        pl1_new_points = pl1_points + player1_score
        Player.players_db.update({'p_total_points': pl1_new_points},
                                 doc_ids=[player1_id])

        pl2_new_points = pl2_points + player2_score
        Player.players_db.update({'p_total_points': pl2_new_points},
                                 doc_ids=[player2_id])
        print('new total points JOUEUR 1:')  # VERIF
        print(pl1_new_points)
        print('new total points JOUEUR 2:')  # VERIF
        print(pl2_new_points)


class RoundController:
    def __init__(self, r_matches_id_list):
        self.r_matches_id_list = r_matches_id_list

    def create_new_round(self, tournament_id, r_matches_id_list, round_id=0,
                         end_date_time=0, start_date_time=0):
        """ create a round """
        round = Round(round_id,
                      RoundController.give_round_name(self, tournament_id),
                      r_matches_id_list,
                      start_date_time,
                      end_date_time)
        round.create_round()
        self.round_id = Round.update_round_id(self)
        return round

    def give_round_name(self, tournament_id):
        """ get or ask round name"""
        this_tourney = Tournament.tournaments_db.get(doc_id = tournament_id)
        round_nbr = len(this_tourney['t_rounds_list'])
        
        # round_nbr = len(Round.rounds_db)
        round_name = f'{"Round"}{round_nbr+1}'
        return round_name

    def start_round(self):
        """ generate date & time for the begining of a round"""
        start_date_and_time = str(datetime.now())
        return start_date_and_time

    def update_start_date_and_time(self, start_date_time, round_id):
        """ update round start date_and_time in DB """
        Round.update_start_date_time(self, start_date_time, round_id)

    def close_round(self, round_id):
        """ set end date and time """
        end_date_time = str(datetime.now())
        self.update_round_end_date_time(round_id, end_date_time)
        return end_date_time

    def update_round_end_date_time(self, round_id, end_date_time):
        """ update round end date_and_time in DB """
        Round.update_round_end_date_time(self, round_id, end_date_time)


class MatchController:
    def __init__(self, match_player1, match_player2):
        self.match_player1 = match_player1
        self.match_player2 = match_player2

    def create_new_match(self, match_player1, match_player2, match_id=0,
                         player1_score=0, player2_score=0):
        """create one match"""
        match = Match(match_id,
                      match_player1,  # player's doc_id
                      match_player2,
                      player1_score,  # player's doc_id
                      player2_score)
        match.create_match()
        return match


class PlayerController:
    def __init__(self):
        self.player_view = PlayerView()

    def create_new_player(self, player_id=0):
        """create one player"""
        player = Player(
            player_id,
            PlayerController.ask_player_name(self),
            PlayerController.ask_player_first_name(self),
            PlayerController.ask_player_birth_date(self),
            PlayerController.ask_player_gender(self),
            PlayerController.ask_player_ranking(self),
            player_points_qty=0
        )
        player.create_player()
        Player.update_player_id(self)
        return player

    def ask_player_name(self):
        """ get player_name from User through player_view """
        PlayerView.ask_player_name()
        player_name = input()
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
        player_rank = int(input())
        return player_rank

    def suggest_ranking_update(self):
        """ suggest rank updating to User"""
        PlayerView.request_rank_update()
        answ = input()
        if answ == 'O':
            PlayerController.update_players_ranking(self)
        else:
            print('Classement non mis à jour')

    def update_players_ranking(self):
        player_id = PlayerController.request_player(self)
        print('L652')
        PlayerView.ask_player_ranking()
        player_rank = int(input())
        new_player_rank = Player.update_playr_rank(self, player_id, player_rank)
        return new_player_rank

    def request_player(self):
        """search a player (by his name & firstname) into db"""
        search_p_name = PlayerController.ask_player_name(self)
        search_p_first_name = PlayerController.ask_player_first_name(self)
        Theplayer = Query()
        searched_player = Player.players_db.get(
            (
                Theplayer.p_name == search_p_name  # sensitive to CAPITAL letters
            ) & (
                Theplayer.p_firstname == search_p_first_name
                )
            )
        print(searched_player)
        if searched_player is None:
            print('Joueur absent de la base de données.')
            time.sleep(1)
            return searched_player
        else:
            time.sleep(1)
            return searched_player.doc_id

class Reporting:
    def __init__(self):
        pass
    
    """ Liste de tous les acteurs
    1/ par ordre alphabétique
    2/ par classement
    """
    def display_all_players_reporting(self):
        all_players_list =[]
        for pl in Player.players_db:
            all_players_list.append(pl)

        print('Liste de tous les acteurs triés :')
        print('1 par ordre alphabétique')
        print('2 par classement')
        sorting_choice = input('Saisissez 1 ou 2 selon votre choix : ')

        if sorting_choice == '1':
            print('Liste de tous les acteurs triés par ordre alphabétique')
            pl_list = (len(all_players_list))
            players_name_list=[]
            for i in range(0, pl_list):
                players_name_list.append(all_players_list[i]['p_name'])
            players_name_list.sort
            print(players_name_list)

            # détail :
            print('En details : ')
            print('----------')
            for p in players_name_list:
                print(Player.players_db.search(where('p_name') == p))

        else:
            print('Liste de tous les acteurs triés par classement')

            rank_sorted_all_players_list = sorted(all_players_list,
                                                key=lambda k: k['p_rank'])

            pl_list = (len(rank_sorted_all_players_list))
            players_name_list=[]
            for j in range(0, pl_list):
                players_name_list.append(rank_sorted_all_players_list[j]['p_name'])
            print(players_name_list)

            print('En details : ')
            print('----------')
            for j in rank_sorted_all_players_list:
                print(j)


    """ Liste de tous les joueurs d'un tournoi
    1/ par ordre alphabétique
    2/ par classement
    """

    def display_tournament_players(self):
        tournament_players_list =[]
        print("Liste des tournois : ")
        for t in Tournament.tournaments_db:
                print(t['t_name'])
        tournament_name = TournamentCtlr.ask_tournament_name(self)
        tournament_requested = (Tournament.tournaments_db.get(
            where('t_name') == tournament_name))
        
        tournament_pl_id_list = []
        for t in (tournament_requested['t_players_list']):
            tournament_pl_id_list.append(t)   
        
        for pl_id in tournament_pl_id_list:
            tournament_pl = Player.players_db.get(doc_id = pl_id)
            tournament_players_list.append(tournament_pl)
        
        print('Liste de tous les joueurs du tournoi choisi :')
        print('1 par ordre alphabétique')
        print('2 par classement')
        sorting_choice = input('Saisissez 1 ou 2 selon votre choix')
        if sorting_choice == '1':
            print('Liste de tous les acteurs triés par ordre alphabétique')
            pl_list = (len(tournament_players_list))
            players_name_list=[]
            for i in range(0, pl_list):
                players_name_list.append(tournament_players_list[i]['p_name'])
            players_name_list.sort
            print(players_name_list)

            # détail :
            print('En details : ')
            print('----------')
            for p in players_name_list:
                print(Player.players_db.search(where('p_name') == p))
                
        else:
            print('Liste de tous les acteurs triés par classement')
            rank_sorted_tournament_players_list = sorted(tournament_players_list,
                                                key=lambda k: k['p_rank'])

            pl_list = (len(rank_sorted_tournament_players_list))
            players_name_list=[]
            for j in range(0, pl_list):
                players_name_list.append(rank_sorted_tournament_players_list[j]['p_name'])
            print(players_name_list)

            print('En details : ')
            print('----------')
            for j in rank_sorted_tournament_players_list:
                print(j)


    """ Liste de tous les tournois """

    def display_all_tournaments(self):      
        print("Liste des tournois : ")
        for t in Tournament.tournaments_db:
                print(t['t_name'])
        
        print('En détails')
        print('----------')
        tournaments_list = []
        for tournament in Tournament.tournaments_db:
            tournaments_list.append(tournament)
        for t in tournaments_list:
            print(t)
        
        
    """ Liste de tous les tours (rounds) d'un tournoi """

    def tournament_all_rounds(self):
        print("Liste des tournois : ")
        for t in Tournament.tournaments_db:
                print(t['t_name'])
        tournament_name = TournamentCtlr.ask_tournament_name(self)
        chosen_tournament = Tournament.tournaments_db.get(
            where('t_name') == tournament_name)

        print('Nom des tours du tournoi choisi :')
        t_rounds_list = []
        t_round_id_list = (chosen_tournament['t_rounds_list']) # doc_id
        for rd_id in (t_round_id_list):
            t_round = Round.rounds_db.get(doc_id = rd_id)
            t_rounds_list.append(t_round)
            print(t_round['r_name'])
        print('En détails')
        print('----------')
        for t in (t_rounds_list):
            print(t) 

    """ Liste de tous les matchs d'un tournoi """

    def tournament_all_matches(self):
        print("Liste des tournois : ")
        for t in Tournament.tournaments_db:
                print(t['t_name'])
        tournament_name = TournamentCtlr.ask_tournament_name(self)
        chosen_tournament = Tournament.tournaments_db.get(
            where('t_name') == tournament_name)
        
        matches_id_list = []
        t_rounds_id_list = (chosen_tournament['t_rounds_list']) # doc_id des 4 rounds
        
        # récup liste de rounds entiers (à partir de liste id)
        for rd_id in t_rounds_id_list:
            one_round_matches_id = ((Round.rounds_db.get(doc_id = rd_id))['rnd_matches_list'])

            for m_id in one_round_matches_id:
                matches_id_list.append(m_id)

        matches_list = []
        for m in matches_id_list:
            a_match = Match.matches_db.get(doc_id=m)
            matches_list.append(a_match)
            
            chess_player1 = Match.matches_db.get(doc_id=m)['chess_player1']
            name_pl1 = Player.players_db.get(doc_id=chess_player1)['p_name']
            score_pl1 = Match.matches_db.get(doc_id=m)['score_player1']
            
            chess_player2 = Match.matches_db.get(doc_id=m)['chess_player2']
            name_pl2 = Player.players_db.get(doc_id=chess_player2)['p_name']
            score_pl2 = Match.matches_db.get(doc_id=m)['score_player1']
            print('match id ' + str(m) + ' ' + str(name_pl1) + ' score: ' + str(score_pl1) 
                  + ' contre ' + str(name_pl2) + ' score: ' + str(score_pl2))
        
        


