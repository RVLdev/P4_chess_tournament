import time
import sys
from p4_ctrl2302_hors_interface import TournamentCtlr
from p4_ctrl2302_hors_interface import RoundController
from p4_ctrl2302_hors_interface import MatchController
from p4_ctrl2302_hors_interface import PlayerController
from p4_ctrl2302_hors_interface import ReportingController
from p4_ctrl2302_hors_interface import Save_and_load_Ctrl
from p4_models import Tournament
from p4_models import Round
from p4_models import Match
from p4_models import Player
from p4_models import Save_and_load
from p4_views2202 import InterfaceView
from p4_views2202 import TournamentView
from p4_views2202 import RoundView
from p4_views2202 import PlayerView
from p4_views2202 import MatchView
from p4_views2202 import ReportingView
from p4_views2202 import Save_and_load_View
from tinydb import TinyDB, where, Query
from datetime import datetime

def main():
    launch = InterfaceController()
    launch.t_launch()
    
class InterfaceController:
    def __init__(self):
        self.menu_list = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
        self.t_launch()

    def t_launch(self):
        """ launches the program's menu """
        InterfaceView.launch_tournament()
        self.choose_startmenu_options()
        
    def choose_startmenu_options(self):
        """ asks the user its choice """
        start_menu_choice = input('Entrez le numero correspondant : ')
        self.activate_startmenu_choice(start_menu_choice)

    def activate_startmenu_choice(self, start_menu_choice):
        """ executes user's choice and then sends him back to the start menu
        (for the next choice) """
        if start_menu_choice not in self.menu_list:
            InterfaceView.choice_unavailable(self)
            time.sleep(1.5)
            self.choose_startmenu_options()
        else:
            if start_menu_choice == '1':  # 1 TOURNOI : Créer un tournoi
                TournamentCtlr.create_new_tournament(self, tournament_id=0, tournament_rounds_qty=4)
                time.sleep(2)
                Save_and_load_View.ask_programm_saving(self)  # ********** propose SVG ***********
                prog_saving = input()
                if prog_saving == 'O':
                    Save_and_load_Ctrl.save_program(self)
                else:
                    pass
                self.choose_startmenu_options()
            
            elif start_menu_choice == '2':  # 2 JOUEURS : Enregistrer des joueurs
                PlayerController.create_new_player(self, player_id=0)
                time.sleep(2)
                Save_and_load_View.ask_programm_saving(self)  # ********** propose SVG ***********
                prog_saving = input()
                if prog_saving == 'O':
                    Save_and_load_Ctrl.save_program(self)
                else:
                    pass
                self.choose_startmenu_options()
            
            elif start_menu_choice == '3':  # 3 JOUEURS : Mettre à jour le classement d'un joueur
                PlayerController.update_players_ranking(self)
                time.sleep(2)
                Save_and_load_View.ask_programm_saving(self)  # ********** propose SVG ***********
                prog_saving = input()
                if prog_saving == 'O':
                    Save_and_load_Ctrl.save_program(self)
                else:
                    pass
                self.choose_startmenu_options()
            
            elif start_menu_choice == '4':  # 4 TOUR : Lancer un tour
                TournamentCtlr.create_a_tournament_round (self)
                time.sleep(2)
                Save_and_load_View.ask_programm_saving(self)  # ********** propose SVG ***********
                prog_saving = input()
                if prog_saving == 'O':
                    Save_and_load_Ctrl.save_program(self)
                else:
                    pass
                self.choose_startmenu_options()

            elif start_menu_choice == '5':  # 5 TOUR : Clôturer un tour
                TournamentCtlr.closing_a_round(self)
                time.sleep(2)
                Save_and_load_View.ask_programm_saving(self)  # ********** propose SVG ***********
                prog_saving = input()
                if prog_saving == 'O':
                    Save_and_load_Ctrl.save_program(self)
                else:
                    pass
                self.choose_startmenu_options()
                
            elif start_menu_choice == '6':  # 6 TOUR : Renseigner les scores
                TournamentCtlr.update_matches_scores_players_points(self)
                time.sleep(2)
                Save_and_load_View.ask_programm_saving(self)  # ********** propose SVG ***********
                prog_saving = input()
                if prog_saving == 'O':
                    Save_and_load_Ctrl.save_program(self)
                else:
                    pass
                self.choose_startmenu_options()
            
            elif start_menu_choice == '7':  # 7 Reporting
                InterfaceView.menu_reporting(self)
                reporting_choice = input()
                if reporting_choice == '1':  # 1 Liste de tous joueurs
                    ReportingController.display_all_players_reporting(self)
                elif reporting_choice == '2':  # 2 Liste de tous joueurs d'un tournoi
                    ReportingController.display_tournament_players(self)
                elif reporting_choice == '3':  # 3 Liste de tous les tournois
                    ReportingController.display_all_tournaments(self)
                elif reporting_choice == '4':  # 4 Liste des tours ('rounds') d'un tournoi
                    ReportingController.tournament_all_rounds(self)
                elif reporting_choice == '5':  # 5 Liste des matches d'un tournoi
                    ReportingController.tournament_all_matches(self)
                else:
                    self.choose_startmenu_options() 
            
            elif start_menu_choice == '8':  #8 Sauvegarder - Charger
                InterfaceView.save_or_load_menu(self)
                save_or_load_choice = input('Entrez le numero correspondant : ')
                if save_or_load_choice == '1':
                    Save_and_load_Ctrl.save_program(self)
                elif save_or_load_choice == '2':
                    Save_and_load_Ctrl.load_progam(self)
                else:
                    self.choose_startmenu_options()    
            
            elif start_menu_choice == '9':  #9 Quitter le programme
                InterfaceView.exit_programm(self)
                user_answer = input()
                if user_answer == 'O':
                    Save_and_load_Ctrl.save_program(self)
                    print('Au revoir')
                    sys.exit()
                else:
                    self.choose_startmenu_options()   
            else: 
                InterfaceView.exit_programm(self)
                user_answer = input()
                if user_answer == 'O':
                    Save_and_load_Ctrl.save_program(self)
                    print('Au revoir')
                    sys.exit()
                else:
                    self.choose_startmenu_options()
        return self.choose_startmenu_options()

