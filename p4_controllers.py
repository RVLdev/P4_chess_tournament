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
        self.r_matches_list = []  # EMPLACEMENT A REVOIR
        self.first_round_matches = []
        self.rank_sorted_p_list = []
        self.points_sorted_p_list = []
        self.points_sorted_p_id_list = []
        self.m_list = []  # list of matches from DB
        self.previous_pairs_list = []  # list of previous matches pairs of players
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
        """create one tournament"""
        tournament = Tournament(
            self.tournament_id,
            self.ask_tournament_name(),
            self.ask_tournament_place(),
            self.ask_tournament_date(),
            self.ask_tournament_description(),
            self.ask_time_control(),
            self.tournament_rounds_qty,  # 4 par défaut
            self.tournament_players_id_list,  # doc_ids
            self.tournament_rounds_id_list  # rounds doc_ids list
            )
        tournament.create_tournament()
        self.tournament_id = Tournament.update_tournament_id(self)

        # VERIFICATION
        print('ETAPE create new tournament, update tournament id')
        for t in Tournament.tournaments_db:
            print(t)

        # add/update values : rounds_qty, players_id_list, rounds_id_list
        self.update_tourney_data(self.tournament_rounds_qty, self.tournament_id, self.r_matches_list)
        return tournament

    def ask_tournament_name(self):
        TournamentView.ask_tournament_name()
        tournament_name = input()
        return tournament_name

    def ask_tournament_place(self):
        TournamentView.ask_tournament_place()
        tournament_place = input()
        return tournament_place

    def ask_tournament_date(self):
        TournamentView.ask_tournament_date()
        tournament_date = input()
        return tournament_date

    def ask_tournament_description(self):
        """ get tournament description from User"""
        TournamentView.ask_tournament_description()
        tournament_description = input()
        return tournament_description

    def ask_time_control(self):
        """ Get time control information from User"""
        TournamentView.ask_time_control()
        time_control = input()
        return time_control

    def update_tourney_data(self, tournament_rounds_qty, tournament_id, r_matches_list):
        self.confirm_tournament_rounds_qty(tournament_id)
        # VERIFICATION
        print('L93 valeur confirmée de rounds_qty :')  # OK
        print((Tournament.tournaments_db.get(doc_id=tournament_id))['t_round_qty'])

        self.create_tournament_players_id_list(tournament_id)
        # VERIFICATION
        print('L98 Liste des doc_ids des joueurs du tournoi :')  # OK
        print((Tournament.tournaments_db.get(doc_id=tournament_id))['t_players_list'])

        self.create_tournament_rounds_id_list(tournament_rounds_qty, tournament_id, r_matches_list)
        # VERIFICATION
        print('L103 Liste des doc_ids des tours du tournoi :')  # en cours de deboggage
        print((Tournament.tournaments_db.get(doc_id=tournament_id))['t_rounds_list'])

        # SIMULATION DDE DE FERMETURE DU TOUR
        RoundView.ask_round_closing(self)
        r_closing = input()
        if r_closing == 'N':
            pass
        else:
            self.end_round()  # lance clôture round, puis màj scores & pts)

        # udate scores : automatique après dde de fermeture du tour par le User
        # VERIFICATION ds code 'def update_r_match_score()'

        # update players points qty : automatique, suit l'update des scores
        # VERIFICATION ds code def update_player_points_qty(self)
        
        # update players points qty lance automatiquement la demande de màj du classement des joueurs (L738)

    def confirm_tournament_rounds_qty(self, tournament_id):
        """ Get tournament_rounds_qty from User"""
        TournamentView.ask_tournament_rounds_qty()
        tournament_rounds_qty = int(input())
        # save 'tournament_rounds_qty' :
        Tournament.update_tournament_rounds_qty(self, tournament_rounds_qty, tournament_id)

    def create_tournament_players_id_list(self, tournament_id):  # ok  - players doc_ids
        """ create this tournament's list of 8 players"""
        while len(self.tournament_players_id_list) < 8:
            TournamentView.ask_for_player_inclusion()
            player_inclusion = input()
            if player_inclusion == 'N':

                print("L136 liste des joueurs INCOMPLETE enregistrée en l'état")
                pass  # PREVOIR UNE SORTIE DU TOURNOI VERS L INTERFACE
            else:
                self.add_player_to_tournament(tournament_id)
            # save 'tournament_players_id_list':
            Tournament.update_tournament_players_id_list(
                   self,
                   self.tournament_players_id_list,
                   tournament_id
                   )

        print('L147 liste des joueurs du tournoi complète')  # A AFFICHER DS INTERFACE (pas ici)
        return self.tournament_players_id_list

    def add_player_to_tournament(self, tournament_id):  # ok
        """ add player to tournament_players_id_list """
        # check if player in DB (get player's doc_id)
        requested_player = PlayerController.request_player(self)
        # if player not in DB, launch its creation and add it to list
        if requested_player is None:
            print('Merci de saisir à nouveau : ')
            new_player = PlayerController.create_new_player(self, player_id=0)
            Theplayer = Query()
            new_player_id = (Player.players_db.get(
                (
                 Theplayer.p_name == new_player.player_name
                ) & (
                 Theplayer.p_firstname == new_player.player_first_name
                )
            )).doc_id
            print(new_player_id)
            self.tournament_players_id_list.append(new_player_id)
            print(self.tournament_players_id_list)

        # if player in DB, add it to list
        else:
            self.tournament_players_id_list.append(requested_player)
            print(self.tournament_players_id_list)

        Tournament.update_tournament_players_id_list(
                   self,
                   self.tournament_players_id_list,
                   tournament_id
                   )
        return self.tournament_players_id_list

    # PREPARE tournament_ROUNDS_id_LIST - CODE 09/02
    def create_tournament_rounds_id_list(self, tournament_rounds_qty, tournament_id, r_matches_list):  # rounds doc_ids
        """ create this tournament's list of rounds_id"""
        for r in range(1, int(tournament_rounds_qty)):  # liste vide => PB pour len(liste vide)
            print('L 186 VERIF self.tournament_rounds_id_list :')  # VERIF
            print(self.tournament_rounds_id_list)  # VERIF
            RoundView.launch_round(self)
            launch_answ = input()
            if launch_answ == 'N':
                pass
            else:
                self.add_round_to_t_rounds_list(tournament_id, r_matches_list)   
            # save 'tournament_rounds_id_list'
            Tournament.update_tournament_rounds_id_list(self, self.tournament_rounds_id_list, tournament_id)
            self.update_r_match_score()  # pour lancer la màj des scores
        return self.tournament_rounds_id_list

    def add_round_to_t_rounds_list(self, tournament_id, r_matches_list):  # vérifier que l'on obtient bien doc_id du Round
        """add new round to round matches list"""
        # PRINCIPE : je crée un round et je l'ajoute à la liste
        new_round = RoundController.create_new_round(self, tournament_id,
                                                 r_matches_list,
                                                 round_id=0,
                                                 end_date_time=0,
                                                 start_date_time=0)
        print('L208 round_name :')  # VERIF
        print(new_round.round_name)  # VERIF
        Theround = Query()
        new_round_id = (Round.rounds_db.get(
            Theround.r_name == new_round.round_name
            )).doc_id
        print(new_round_id)
        # ATTENTION : CLOPTURER LE TOUR AVANT DE CREER LE SUIVANT
        self.tournament_rounds_id_list.append(new_round_id)  # 17/02 PB 'NoneType'
        print('L217 liste des doc_ids des rounds')
        print(self.tournament_rounds_id_list)
        round_id = new_round_id
        self.closing_this_round(round_id)
        return self.tournament_rounds_id_list

    """ CODE du 08 02 2022"""
    # ROUND / matches list
    # matchs contiennent doc_ids Joueurs:
    def create_r_matches_list(self, tournament_id, r_matches_list, round_id):
        matches_nb = (len(self.tournament_players_id_list))/2
        # r_matches_list = []
        while len(r_matches_list) < matches_nb:
            if len(self.tournament_rounds_id_list) >= 1:
                r_matches_list = self.create_next_round_matches_list(tournament_id)
                """for i_roundmatch in next_round_matches:
                    r_matches_list.append(i_roundmatch)
                    print('ajout i_roundmatch')  # VERIF"""
                print(r_matches_list)  # VERIF
            else:
                r_matches_list = self.create_first_rd_matches_list(tournament_id)  # variante self.create_first_round_matches_list
                print('AFFICHAGE r_matches_list de la METHODE def create_r_matches_list : ')  # VERIF
                print(r_matches_list)  # VERIF
            print(round_id)  # VERIF
            Round.update_r_matches_list(self, round_id, r_matches_list)
        return r_matches_list

    """ For rounds next to 1st round, matches players must be sorted
    by rank and total points. It is also  required to check that
    new pairs of players are different from previous matches pairs."""

    # MATCHS 1ST ROUND
    # TournamentCtlr L282 **** MODIFIE/original
    """ def create_first_round_matches_list(self, tournament_id):  # MATCHS ac doc_ids joueurs
        # create matches for first round
        rank_sorted_p_list = self.sort_tournament_players_list_by_rank(tournament_id)
        matches_qty = len(rank_sorted_p_list)/2
        first_round_matches = []
        for i in range(0, int(matches_qty)):  # ordre des paramères importants ou pas ?
            first_round_matches.append(Match(
                match_player1=rank_sorted_p_list[i]['p_id'],
                match_player2=rank_sorted_p_list[i+int(matches_qty)]['p_id'],
                match_id=0,
                player1_score=0,
                player2_score=0
                )
            )
        return first_round_matches"""

    # version 11/02/22
    """def create_first_round_matches_list(self, tournament_id):  # MATCHS ac doc_ids joueurs
        # create matches for first round
        rank_sorted_p_list = self.sort_tournament_players_list_by_rank(tournament_id)
        matches_qty = len(rank_sorted_p_list)/2
        # first_round_matches = []  # liste des matches 'entiers du 1er round

        for i in range(0, int(matches_qty)):
            print(" IMPRESSION rank_sorted_p_list[i]['p_id'] : ")
            print(rank_sorted_p_list[i]['p_id'])
            first_rd_match = Match(
                match_id=0,
                match_player1=rank_sorted_p_list[i]['p_id'],   # get id from full object 'player'
                player1_score=0,
                match_player2=rank_sorted_p_list[i+int(matches_qty)]['p_id'],
                player2_score=0
                )
            print(first_rd_match.__dict__)  # VERIF

            self.first_round_matches.append(first_rd_match)
            print("AFFICHAGE L273 : first_round_matches[i] MATCHS ENTIERS ")
            print(self.first_round_matches[i])
            print('**** ----****----****----****')

        print(self.first_round_matches)
        return self.first_round_matches"""

    # variante 14/02/2022 (+ réf L221)
    def create_first_rd_matches_list(self, tournament_id):  # MATCHS ac doc_ids joueurs
        """ create matches for first round """
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
            match.create_match()
            new_m_id = match.update_match_id()  # match.update_match_id() - renvoie match id
            self.r_matches_list.append(new_m_id)  # self.r_matches_list.append(match.match_id)
            print(self.r_matches_list)
        return self.r_matches_list

    def sort_tournament_players_list_by_rank(self, tournament_id):
        """sort by rank tournament players list"""
        # récupère la liste complète des éléments à trier
        self.tournament_players_id_list = self.create_tournament_players_id_list(tournament_id)
        print(len(self.tournament_players_id_list))  # VERIF : 8
        for pl_id in self.tournament_players_id_list:  # doc_ids
            t_full_player = Player.players_db.get(doc_id=pl_id)  # from doc_ids get full objects 'player'
            self.t_full_players_list.append(t_full_player)

        rank_sorted_p_list = sorted(self.t_full_players_list,
                                    key=lambda k: k['p_rank'])
        print('joueurs triés par classement')
        print(rank_sorted_p_list)  # contient des joueurs 'complets' (pas liste de doc_ids)'
        print('**********************************')
        return rank_sorted_p_list

    # MATCHS Next ROUND
    # TournamentCtlr
    def create_next_round_matches_list(self, tournament_id):  # MATCHS ac doc_ids joueurs
        """ create matches for round > 1 """
        next_round_p_pairs_list = self.compare_matches_p_pairs(tournament_id)
        matches_qty = len(next_round_p_pairs_list)
        for i in range(0, int(matches_qty)):  # ordre des paramères importants ou pas ?
            match_player1 = next_round_p_pairs_list[i]  # player1 doc_id
            match_player2 = next_round_p_pairs_list[i+1]
            match = MatchController.create_new_match(self,
                                                     match_player1,  # player1 doc_id
                                                     match_player2,  # i+1 = next player
                                                     match_id=0,
                                                     player1_score=0,
                                                     player2_score=0)
            match.create_match()
            new_m_id = match.update_match_id()  # match.update_match_id()
            self.r_matches_list.append(new_m_id)  # self.r_matches_list.append(match.match_id)
            print(self.r_matches_list)
        return self.r_matches_list

    def sort_t_players_id_list_by_points(self, tournament_id):
        """ get tournament players list sorted by rank and total points """
        rank_sorted_p_list = self.sort_tournament_players_list_by_rank(tournament_id)
        points_sorted_p_list = sorted(rank_sorted_p_list,
                                      key=lambda k: k['p_total_points'],
                                      reverse=True)
        # print(points_sorted_p_list)  # 'full' players (not only doc_ids)
        self.points_sorted_p_id_list = []
        for p in points_sorted_p_list:  # parenthèses ou crochets autour de "int"
            self.points_sorted_p_id_list.append(p['p_id'])
        print('liste des docs_id joueurs triés classement & points')
        print(self.points_sorted_p_id_list)
        return self.points_sorted_p_id_list  # players'doc_ids

    def create_test_players_pair(self, i, tournament_id):
        # create pair of players to be tested
        points_sorted_p_id_list = self.sort_t_players_id_list_by_points(self, tournament_id)
        test_pair = [points_sorted_p_id_list[0],
                     points_sorted_p_id_list[i]]
        return test_pair

    def create_prev_matches_players_id_list(self, tournament_id):  # A REVOIR (besoin : matchs précédents du même tournoi)
        # get list of previous matches pairs of players

        this_tournament = Tournament.tournaments_db.get(doc_id=tournament_id)
        tournmt_r_id_list = this_tournament['t_rounds_list']
        self.m_list = []
        for item in tournmt_r_id_list:
            prev_matches = Match.matches_db.get(doc_id=item)
            self.m_list.append(prev_matches)

        nb_prev_matchs = len(self.m_list)
        for n in range(0, nb_prev_matchs):
            self.previous_pairs_list.append([self.m_list[n]['chess_player1'],  # player's doc_id
                                            self.m_list[n]['chess_player2']])
        return self.previous_pairs_list

    def compare_matches_p_pairs(self, tournament_id):
        # check players pairs to get uniq players players (never compete in the same tournament)
        points_sorted_p_id_list = self.sort_t_players_id_list_by_points(self, tournament_id)
        next_round_p_pairs_list = []  # list of pairs of players for next matches
        i = 1

        while len(points_sorted_p_id_list) > 0:
            testing_pair = self.create_test_players_pair(i, tournament_id)
            if testing_pair in self.previous_pairs_list:
                # ALREADY PLAYED pair. New testing_pair :
                i += 1
                testing_pair = self.create_test_players_pair(i, tournament_id)
            else:
                # UNIQUE pair of players to be added to next round matches
                next_round_p_pairs_list.append(testing_pair)
                # update points_sorted_p_id_list (to avoid testing twice the same players)
                del points_sorted_p_id_list[0]
                del points_sorted_p_id_list[i-1]

                if len(points_sorted_p_id_list) > 0:
                    # new testing_pair:
                    i = 1
                    testing_pair = self.create_test_players_pair(i, tournament_id)
                else:
                    return next_round_p_pairs_list
        print('liste des paires pour prochain round')
        print(next_round_p_pairs_list)
        return next_round_p_pairs_list

    def closing_this_round(self, round_id):
        RoundView.ask_round_closing(self)
        r_closing = input()
        if r_closing == 'N':
            print('REFUS USER de cloturer le tour en cours') # NE PAS LANCER DE NOUVEAU TOUR
        else:
            end_date_time = Round.close_round(self, round_id)  # lance clôture round, puis màj scores & pts
            Round.update_round_end_date_time(self, round_id, end_date_time)
            print(' AFFICHE Round.end_date_time :')
            print(end_date_time)
          

    # END ANY ROUND - CODE màj v 09/02
    def end_round(self):  # A LA DEMANDE DU USER
        """ give closing date & time of a round """
        # quel round de quel tournoi ?
        RoundView.close_a_round()
        round_id = self.request_round_id() # identifie le round à clore
        RoundController.close_round(round_id)  # lance la clôture du round choisi (dont 'date_time_end')
        self.update_r_match_score(self)  # pour lancer la màj des scores

    def request_round_id(self):
        # liste des tournois :
        print('liste des tournois:')
        for t in Tournament.tournaments_db:
            print(t['t_name'])
        RoundView.ask_tournament_name(self)
        tournament_name = input()
        Thetournmt = Query()
        rounds_id_list = Tournament.tournaments_db.get(
            Thetournmt.t_name == tournament_name)['t_rounds_list']
        # liste des rounds
        print('Liste des rounds du tournoi :')
        print(rounds_id_list)  # VERIF
        for rd_id in rounds_id_list:
            round_name = (Round.rounds_db.get(doc_id=rd_id))['r_name']
            print(round_name)
        RoundView.ask_round_name(self)
        round_name_req = input()
        Theround = Query()
        round_id = (Round.rounds_db.get(Theround.r_name == round_name_req))['r_id']
        return round_id

    # SCORES 09/02/2022
    # update scores in r_matches_list AND matches_db
    def update_r_match_score(self):  # ancien code ds RoundController
        """ update round matches players'score"""
        MatchView.update_scores()
        round_id = self.request_round_id()  # récupère Tournoi et Round concernés
        matches_list = (Round.rounds_db.get(doc_id=round_id))['rnd_matches_list']

        # VERIFICATION intermédiaire
        print('liste des matchs pour màj des scores')
        print(matches_list)  # ok

        nbr_matches = len(matches_list)
        for i in range(0, nbr_matches):
            # VERIFICATION 1/2 - SCORES avant màj
            print('pr vérif, Id Match: ')
            print(self.r_matches_list[i])
            print('player1_score AVANT update :')  # VERIF - ok
            init_score_pl1 = (Match.matches_db.get(doc_id = self.r_matches_list[i]))['score_player1']
            print(init_score_pl1)
            print('player2_score AVANT update')  # VERIF
            init_score_pl2 = (Match.matches_db.get(doc_id = self.r_matches_list[i]))['score_player2']
            print(init_score_pl2)

            player1_score = self.ask_player1_score(i, matches_list)
            player2_score = self.ask_player2_score(i, matches_list)

            # update r_matches_list
            RoundController.r_matches_list[i]['score_player1'] = player1_score
            RoundController.r_matches_list[i]['score_player2'] = player2_score

            # VERIFICATION : comparaison visuelle 1/2 et 2/2
            print('player1_score APRES update')  # VERIF
            print(RoundController.r_matches_list[i]['score_player1'])  # VERIF
            print('player2_score APRES update')  # VERIF
            print(RoundController.r_matches_list[i]['score_player2'])  # VERIF

            # update matches_db
            match_id = i
            Match.update_players_scores(match_id, player1_score, player2_score)

        self.update_player_points_qty()

    def ask_player1_score(self, i, matches_list):
        """ get player1 's score"""
        # print "match PLAYER1-NAME / PLAYER2-NAME"
        print('match ' + matches_list[i]['chess_player1']['p_name']
                       + " / "
                       + matches_list[i]['chess_player2']['p_name'])

        # print "joueur 1 : PLAYER1-NAME"
        print('joueur1: ' + matches_list[i]['chess_player1']['p_name'])

        MatchView.ask_score_player()
        player1_score = int(input('saisissez son score (0 ou 0.5 ou 1) : '))
        print('joueur1 : ' + matches_list[i]['chess_player1']['p_name']
                           + ' score = ' + player1_score)

        return player1_score

    def ask_player2_score(self, i, matches_list):
        """ get player2 's score"""
        # print "match PLAYER1-NAME / PLAYER2-NAME"
        print('match ' + matches_list[i]['chess_player1']['p_name']
                       + " / "
                       + matches_list[i]['chess_player2']['p_name'])

        # print "joueur 2 : PLAYER2-NAME"
        print('joueur2 : '+matches_list[i]['chess_player2']['p_name'])

        MatchView.ask_score_player()
        player2_score = int(input('saisissez son score (0 ou 0.5 ou 1) : '))
        print('joueur2 : ' + matches_list[i]['chess_player2']['p_name']
                           + ' score = ' + player2_score)
        return player2_score

    # PLAYERS TOTAL POINTS
    # UPDATE POINTS QTY - AFTER ROUND IS FINISHED
    def update_player_points_qty(self):
        """ calculate and update players total points"""
        nbr_players = len(self.tournament_players_id_list)

        for j in range(0, nbr_players/2):
            # Get match 1st player's doc_id and points nb before match (previous_points_pl1)
            match_pl1_doc_id = RoundController.r_matches_list[j]['chess_player1']
            player1 = Player.players_db.get(doc_id=match_pl1_doc_id)  # ou doc_ids=[]
            previous_points_pl1 = player1['p_total_points']

            print('points précédents Joueur 1')  # VERIF
            print(previous_points_pl1)  # VERIF

            # Get match 1st player's new points (match score)
            new_points_pl1 = RoundController.r_matches_list[j]['score_player1']

            print('nouveaux points Joueur 1')  # VERIF
            print(new_points_pl1)  # VERIF

            # calculate match 1st player's new total of points & update its points in DB
            new_total_points_pl1 = new_points_pl1 + previous_points_pl1
            Player.players_db.update({'p_total_points': new_total_points_pl1},
                                     doc_ids=[match_pl1_doc_id])

            print('nouveau total de points Joueur 1')  # VERIF
            print(new_total_points_pl1)  # VERIF
            print('Vérif màj POINTS Joueur 1 : ')  # VERIF
            print(Player.players_db.get(doc_id=match_pl1_doc_id))  # VERIF

            # do the same with match 2nd player
            match_pl2_doc_id = RoundController.r_matches_list[j]['chess_player2']
            player2 = Player.players_db.get(doc_id=match_pl2_doc_id)  # ou doc_ids=[]
            previous_points_pl2 = player2['p_total_points']

            print('points précédents Joueur 2')  # VERIF
            print(previous_points_pl2)  # VERIF

            new_points_pl2 = RoundController.r_matches_list[j]['score_player2']

            print('nouveaux points Joueur 2')  # VERIF
            print(new_points_pl2)  # VERIF

            new_total_points_pl2 = new_points_pl2 + previous_points_pl2
            Player.players_db.update({'p_total_points': new_total_points_pl2},
                                     doc_ids=[match_pl2_doc_id])

            print('nouveau total de points Joueur 2')  # VERIF
            print(new_total_points_pl2)  # VERIF
            print('Vérif màj POINTS Joueur 2 : ')  # VERIF
            print(Player.players_db.get(doc_id=match_pl2_doc_id))  # VERIF

        PlayerController.update_players_ranking()


class RoundController:
    def __init__(self):
        pass

    # c'est l'utilisateur qui "crée" le tour => def ask_user_round_launch()
    """ CODE du 08 02 2022"""
    def create_new_round(self, tournament_id, r_matches_list, round_id=0,
                         end_date_time=0, start_date_time=0):
        """ create a round """
        round = Round(round_id,
                      RoundController.give_round_name(self),
                      r_matches_list,
                      start_date_time,
                      end_date_time)
        round.create_round()
        self.round_id = Round.update_round_id(self)
        print('L579 round_id = ')  # VERIF
        print(self.round_id)  # VERIF
        self.r_matches_list = TournamentCtlr.create_r_matches_list(self,
                                                                   tournament_id,
                                                                   self.r_matches_list,
                                                                   self.round_id)
        self.start_date_time = RoundController.start_round(self)
        RoundController.update_start_date_and_time(self, self.start_date_time,
                                                   self.round_id)
        # update end_date_time (def end_round) A LA DEMANDE DE CLOTURE DU TOUR
        return round

    def give_round_name(self):  # ancien code ok 08/02
        """ get or ask round name"""
        round_nbr = len(Round.rounds_db)
        round_name = f'{"Round"}{round_nbr+1}'
        return round_name

    def start_round(self):
        """ generate date & time for the begining of a round"""
        start_date_and_time = str(datetime.now())
        return start_date_and_time

    def update_start_date_and_time(self, start_date_time, round_id):
        Round.update_start_date_time(self, start_date_time, round_id)
    
    def close_round(self, round_id):
        end_date_time = str(datetime.now())
        self.update_round_end_date_time(round_id, end_date_time)
        return end_date_time

    def update_round_end_date_time(self, round_id, end_date_time):
        Round.update_round_end_date_time(self, round_id, end_date_time)
    

    # ANCIEN CODE - remplacé par CODE du 08/02 ds TournamentCtlr
    """def create_r_matches_list(self):
        # launch creation of the round's matches'list
        TournamentCtlr.rank_sorted_p_list = (
            TournamentCtlr.sort_tournament_players_list_by_rank(self)
            )
        TournamentCtlr.points_sorted_p_list = (
            TournamentCtlr.sort_t_players_id_list_by_points(
                (self, TournamentCtlr.rank_sorted_p_list)
                )
            )
        r_matches_list = TournamentCtlr.add_match_to_r_matches_list(
                TournamentCtlr.rank_sorted_p_list,
                TournamentCtlr.points_sorted_p_list)
        return r_matches_list
    """

    # SCORES - ANCIEN CODE remplacé par CODE du 09/02
    # update scores in r_matches_list AND matches_db
    """def update_r_match_score(self):
        # update round matches players'score
        MatchView.update_scores()

        nbr_matches = len(self.r_matches_list)
        for i in range(0, nbr_matches):
            player1_score = self.ask_player1_score(i, self.r_matches_list)
            player2_score = self.ask_player2_score(i, self.r_matches_list)

            # update r_matches_list
            self.r_matches_list[i]['score_player1'] = player1_score
            self.r_matches_list[i]['score_player2'] = player2_score
            # update matches_db
            match_id = i
            Match.update_players_scores(match_id, player1_score, player2_score)

    def ask_player1_score(self, i):
        # get player1 's score
        # print "match PLAYER1-NAME / PLAYER2-NAME"
        print('match ' + self.r_matches_list[i]['chess_player1']['p_name']
                       + " / "
                       + self.r_matches_list[i]['chess_player2']['p_name'])

        # print "joueur 1 : PLAYER1-NAME"
        print('joueur1: ' + self.r_matches_list[i]['chess_player1']['p_name'])

        MatchView.ask_score_player()
        player1_score = input('saisissez son score (0 ou 0.5 ou 1) : ')

        # dico qui associe player doc_id et new points
        pl_doc_id = self.r_matches_list[i]['chess_player1']
        new_points_player1 = {'pl_doc_id': pl_doc_id,
                              'newpoints': player1_score}

        print('joueur1 : ' + self.r_matches_list[i]['chess_player1']['p_name']
                           + ' score = ' + player1_score)

        return player1_score

    def ask_player2_score(self, i):
        # get player2 's score
        # print "match PLAYER1-NAME / PLAYER2-NAME"
        print('match ' + self.r_matches_list[i]['chess_player1']['p_name']
                       + " / "
                       + self.r_matches_list[i]['chess_player2']['p_name'])

        # print "joueur 2 : PLAYER2-NAME"
        print('joueur2 : '+self.r_matches_list[i]['chess_player2']['p_name'])

        MatchView.ask_score_player()
        player2_score = input('saisissez son score (0 ou 0.5 ou 1) : ')
        print('joueur2 : ' + self.r_matches_list[i]['chess_player2']['p_name']
                           + ' score = ' + player2_score)
        return player2_score"""


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
        self.match_id = Match.update_match_id(self)
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
        player_rank = int(input())
        return player_rank

    def update_players_ranking(self):
        player_req_id = self.request_player()
        PlayerView.ask_player_ranking()
        player_rank = int(input())
        new_player_rank = Player.update_playr_rank(player_req_id, player_rank)
        return new_player_rank

    def request_player(self):
        """search a player (by his name & firstname) into db"""
        search_p_name = PlayerController.ask_player_name(self)
        search_p_first_name = PlayerController.ask_player_first_name(self)
        Theplayer = Query()
        searched_player = Player.players_db.get(
            (
                Theplayer.p_name == search_p_name  # sensible aux MAJ/minuscules
            ) & (
                Theplayer.p_firstname == search_p_first_name
                )
            )
        # Search donne [{}] (liste contenant joueur),
        # mais 'get' donne directement le joueur {}
        print(searched_player)
        if searched_player is None:
            print('Joueur absent de la base de données.')
            return searched_player
        else:
            print(searched_player.doc_id)  # player's DOC_ID
            return searched_player.doc_id
