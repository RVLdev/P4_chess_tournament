import time
from tournament import Tournament
from round import Round
from player import Player
from match import Match

""" REMINDER  : User interface - actions 
 1 create_new_tournament
    # 2 (create and) add 8 players (auto_fill Tournoi/players_list)
    # 3 generate_first_round_players (and create 1st round matches)
    # 4 open/create_round (and add matches to a list + fill Tournoi/"tournées")
    # 5 close/end-round
    # 6 record_matchs_points (pts des matchs à chq round)
    # 7 START LOOP :
    #  generate_next_players_pair & matches (2nd 3rd 4th rounds)
    #  open/create_round
    #  close/end-round
    #  record_matchs_points
    # x3 => END OF LOOP
    # 8 update_players_ranking (fin du tournoi et à la dde)
    # save (et any time)
    # display reports (+ export option)"""

""" Tournaments manager MENU """


class Interface:
    def __init__(self):
        self.menu_list = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
        self.launch()

    def launch(self):
        """ launches the program's menu """
        print("Bonjour, bienvenue dans le gestionnaire de tournois d'echecs")
        time.sleep(1)
        self.display_startmenu()

    def display_startmenu(self):
        """ displays the menu """
        print('\nMENU :')
        print('1 Creer un tournoi\n2 Ajouter un(des) joueur(s)')
        print('3 Generer des paires de joueurs\n4 Lancer un tour')
        print('5 Cloturer un tour\n6 Renseigner les scores')
        print('7 Modifier le classement\n8 lancer une sauvegarde\n9 Quitter')
        print('Que souhaitez-vous faire ?')
        self.choose_startmenu_options()

    def choose_startmenu_options(self):
        """ asks the user its choice """
        start_menu_choice = input('Entrez le numero correspondant : ')
        self.activate_startmenu_choice(start_menu_choice)

    def activate_startmenu_choice(self, start_menu_choice):
        """ executes user's choice and then sends him back to the start menu
        (for the next choice) """
        if start_menu_choice not in self.menu_list:
            print('*** Désolé, choix non disponible\n')
            time.sleep(1.5)
            self.display_startmenu()
        else:
            if start_menu_choice == '1':
                Tournament.create_new_tournament(self)
                time.sleep(2)
                self.display_startmenu()
            elif start_menu_choice == '2':
                Player.create_player(self)
                time.sleep(1)
                self.display_startmenu()
            elif start_menu_choice == '3':
                print('\nMenu 3 Generer des paires de joueurs, choisissez : ')
                print("1 paires de joueurs du premier tour")
                print("2 paires de joueurs d'un autre tour\n")
                pairs_round = input('Entrez le numero correspondant : ')
                if pairs_round == '1':
                    Match.generate_firstround_pairs(self)
                    time.sleep(1.5)
                    self.display_startmenu()
                elif pairs_round == '2':
                    Match.generate_players_pairs(self)
                    time.sleep(1.5)
                    self.display_startmenu()
                else:
                    print('*** Désolé, choix non disponible\n')
                    time.sleep(1.5)
                    self.display_startmenu()

            elif start_menu_choice == '4':
                Round.launch_round(self)
                time.sleep(1.5)
                self.display_startmenu()
            elif start_menu_choice == '5':
                Round.end_round(self)
                time.sleep(1.5)
                self.display_startmenu()
            elif start_menu_choice == '6':
                Match.enter_scores(self)
                time.sleep(1.5)
                self.display_startmenu()
            elif start_menu_choice == '7':
                Player.modify_player_rank(self)
                time.sleep(1.5)
                self.display_startmenu()
            elif start_menu_choice == '8':
                print('==> Sauvegarde : Fonctionnalité à mettre en place')
                time.sleep(2)
                self.display_startmenu()
            else:
                print('Au revoir')


linterface = Interface()
