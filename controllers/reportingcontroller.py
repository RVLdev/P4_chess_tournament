from models.matchmodel import Match
from models.playermodel import Player
from models.roundmodel import Round
from models.tournamentmodel import Tournament
from views.reportingviews import ReportingViews
from tinydb import TinyDB, where, Query
from controllers.tournamentcontroller import TournamentCtrlr
import time


class ReportingCtrlr:
    def __init__(self):
        db = TinyDB('db.json')
        Tournament.tournaments_db = db.table('tournaments_db')
        Round.rounds_db = db.table('rounds_db')
        Match.matches_db = db.table('matches_db')
        Player.players_db = db.table('players_db')

    def dis_bonjour_report_ctrl(self):    #TEST INITIAL - A SUPPRIMER
        print ('Bonjour de la classe ReportingCtrlr - fichier reportingcontroller')


    """ List of all participants
    1/ by alphabetical order
    2/ by ranking
    """
    def display_all_players_reporting(self):
        db_all_t = TinyDB('db_all_t.json')
        Player.Theplayer = Query()
        Player.all_players_db = db_all_t.table('all_players_db')

        all_players_list = []
        for pl in Player.all_players_db:
            all_players_list.append(pl)

        ReportingViews.display_all_players_reporting()
        sorting_choice = input()

        if sorting_choice == '1':
            ReportingViews.display_all_players_alphabetical_order()
            """Liste de tous les acteurs triés par ordre alphabétique"""
            pl_list = (len(all_players_list))
            players_name_list = []
            for i in range(0, pl_list):
                players_name_list.append(all_players_list[i]['p_name'])
            players_name_list.sort
            print(players_name_list)
            time.sleep(2)

            # details :
            ReportingViews.display_all_players_alphabetical_order_details()
            for p in players_name_list:
                print(Player.all_players_db.search(where('p_name') == p))
            time.sleep(5)

        else:
            ReportingViews.display_all_players_by_rank()
            rank_sorted_all_players_list = sorted(all_players_list,
                                                  key=lambda k: k['p_rank'])

            pl_list = (len(rank_sorted_all_players_list))
            pl_id_list = []
            for pl in rank_sorted_all_players_list:
                pl_id_list.append(pl['p_id'])
            
            for id in pl_id_list:
                pl_name = (Player.all_players_db.get(doc_id=id))['p_name']
                pl_firstname = (Player.all_players_db.get(
                    doc_id=id))['p_firstname']
                pl_rk = (Player.all_players_db.get(doc_id=id))['p_rank']
                print(pl_name+' '+pl_firstname+'- classement: '+str(pl_rk))      
        time.sleep(5)
        ReportingViews.separator()

    """ List of all players of ONE tournament
    1/ by alphabetical order
    2/ by ranking
    """
    def display_tournament_players(self):
        ReportingViews.one_tournament_players_list()
        ReportingViews.display_tournaments_list()
        tournament_id = TournamentCtrlr.request_tournament_id(self)
        db = TinyDB('db'+str(tournament_id)+'.json')
        Tournament.tournaments_db = db.table('tournaments_db')
        Player.players_db = db.table('players_db')

        tournament_requested = (Tournament.tournaments_db.get(
            doc_id=tournament_id))

        tournament_pl_id_list = []
        for t in (tournament_requested['t_players_list']):
            tournament_pl_id_list.append(t)

        tournament_players_list = []
        for pl_id in tournament_pl_id_list:
            tournament_pl = Player.players_db.get(doc_id=pl_id)
            tournament_players_list.append(tournament_pl)

        ReportingViews.display_chosen_tournament_players()
        sorting_choice = input()
        if sorting_choice == '1':
            ReportingViews.display_all_players_alphabetical_order()
            players_name_list = []
            for i in range(0, len(tournament_players_list)):
                players_name_list.append(tournament_players_list[i]['p_name'])
            players_name_list.sort
            print(players_name_list)
            time.sleep(5)
            # details :
            ReportingViews.display_all_players_alphabetical_order_details()
            for p in players_name_list:
                print(Player.players_db.search(where('p_name') == p))
            time.sleep(5)

        else:
            ReportingViews.display_all_players_by_rank()
            rank_sorted_tournament_players_list = sorted(
                tournament_players_list, key=lambda k: k['p_rank'])

            pl_list = (len(rank_sorted_tournament_players_list))
            players_name_list = []
            for j in range(0, pl_list):
                players_name_list.append(
                    rank_sorted_tournament_players_list[j]['p_name'])
            print(players_name_list)
            time.sleep(5)
            ReportingViews.display_all_players_by_rank_details()
            for j in rank_sorted_tournament_players_list:
                print(j)
            time.sleep(5)
        ReportingViews.separator()

    """ List of all tournaments """
    def display_all_tournaments(self):
        db_all_t = TinyDB('db_all_t.json')
        Tournament.all_tournaments_db = db_all_t.table('all_tournaments_db')

        ReportingViews.all_tournaments_list()
        ReportingViews.display_tournaments_list()
        for t in Tournament.all_tournaments_db:
            print(t['t_name'])
        time.sleep(2)

        ReportingViews.display_tournaments_list_details()
        tournaments_id_list = []
        for tournament in Tournament.all_tournaments_db:
            tournaments_id_list.append(tournament.doc_id)

            tournament_id = tournament.doc_id

            db = TinyDB('db'+str(tournament_id)+'.json')
            Tournament.tournaments_db = db.table('tournaments_db')
            t_details = Tournament.tournaments_db.get(doc_id=tournament_id)
            print(t_details)
        time.sleep(5)
        ReportingViews.separator()

    """ List of all rounds of ONE tournament """
    def tournament_all_rounds(self):
        ReportingViews.one_tournament_rounds_list()
        tournament_id = TournamentCtrlr.request_tournament_id(self)
        db = TinyDB('db'+str(tournament_id)+'.json')
        Tournament.tournaments_db = db.table('tournaments_db')
        Round.rounds_db = db.table('rounds_db')

        chosen_tournament = (Tournament.tournaments_db.get(
            doc_id=tournament_id))

        ReportingViews.chosen_t_rounds_names_list()
        t_rounds_list = []
        t_round_id_list = (chosen_tournament['t_rounds_list'])
        for rd_id in (t_round_id_list):
            t_round = Round.rounds_db.get(doc_id=rd_id)
            t_rounds_list.append(t_round)
            print(t_round['r_name'])
        time.sleep(2)

        ReportingViews.chosen_t_rounds_details()
        for t in (t_rounds_list):
            print(t)
        time.sleep(5)
        ReportingViews.separator()
        
    """ List of all matches of ONE tournament """
    def tournament_all_matches(self):
        ReportingViews.one_tournament_matches_list()
        tournament_id = TournamentCtrlr.request_tournament_id(self)
        db = TinyDB('db'+str(tournament_id)+'.json')
        Tournament.tournaments_db = db.table('tournaments_db')
        Round.rounds_db = db.table('rounds_db')
        Match.matches_db = db.table('matches_db')
        Player.players_db = db.table('players_db')

        chosen_tournament = (Tournament.tournaments_db.get(
            doc_id=tournament_id))
        matches_id_list = []
        t_rounds_id_list = (chosen_tournament['t_rounds_list'])  # doc_id

        if len(t_rounds_id_list) < 1:
            print("Aucun tour n'a été lancé pour ce tournoi")
            pass
        else:
            for rd_id in t_rounds_id_list:
                one_round_matches_id = ((Round.rounds_db.get(
                    doc_id=rd_id))['rnd_matches_list'])

                for m_id in one_round_matches_id:
                    matches_id_list.append(m_id)

            ReportingViews.chosen_round_matches_list()
            matches_list = []
            for m in matches_id_list:
                a_match = Match.matches_db.get(doc_id=m)
                matches_list.append(a_match)

                chess_player1 = Match.matches_db.get(
                    doc_id=m)['chess_player1']
                name_pl1 = Player.players_db.get(
                    doc_id=chess_player1)['p_name']
                score_pl1 = Match.matches_db.get(doc_id=m)['score_player1']

                chess_player2 = Match.matches_db.get(
                    doc_id=m)['chess_player2']
                name_pl2 = Player.players_db.get(
                    doc_id=chess_player2)['p_name']
                score_pl2 = Match.matches_db.get(doc_id=m)['score_player1']
                print('match id ' + str(m)
                      + ' ' + str(name_pl1)
                      + ' score: ' + str(score_pl1)
                      + ' contre ' + str(name_pl2)
                      + ' score: ' + str(score_pl2))
        time.sleep(5)
        ReportingViews.separator()
