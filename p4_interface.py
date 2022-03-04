import sys

from controllers.tournamentcontroller import TournamentCtrlr
from controllers.roundcontroller import RoundCtrlr
from controllers.matchcontroller import MatchCtrlr
from controllers.playercontroller import PlayerCtrlr
from controllers.reportingcontroller import ReportingCtrlr
from controllers.save_n_loadcontroller import Save_and_load_Ctrlr
from models.save_n_loadmodel import Save_and_load
from models.playermodel import Player
from models.matchmodel import Match
from models.roundmodel import Round
from models.tournamentmodel import Tournament
from views.interfaceviews import InterfaceView
from views.tournamentviews import TournamentViews
from views.roundviews import RoundViews
from views.matchviews import MatchViews
from views.playerviews import PlayerViews
from views.reportingviews import ReportingViews
from views.save_n_loadviews import Save_and_load_Views


def main():
    launch = InterfaceMenu()
    launch.t_launch()


class InterfaceMenu:
    def __init__(self):
        self.menu_list = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10',
                          '11']
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
            self.exit_on_unavailable_choice()
        else:
            if start_menu_choice == '1':  # 1 : Create a tournament
                self.create_tournament()
            elif start_menu_choice == '2':  # 2 Display a tournament
                TournamentCtrlr.read_a_tournament(self)
            elif start_menu_choice == '3':  # 3 Create new player
                PlayerCtrlr.create_new_player_in_db_all(self,
                                                             player_id=0)
                self.suggest_saving()
            elif start_menu_choice == '4':  # 4 : add a tournament 1 player
                InterfaceView.display_add_one_player()
                TournamentCtrlr.add_a_player_to_a_tournament(self)
                self.suggest_saving()
            elif start_menu_choice == '5':  # 5 : updating a player rank
                self.update_ranking()
            elif start_menu_choice == '6':  # 6 : Launching a round
                TournamentCtrlr.create_a_tournament_round(self)
                self.suggest_saving()
            elif start_menu_choice == '7':  # 7 : Ending a tournament
                TournamentCtrlr.closing_a_round(self)
                self.suggest_saving()
            elif start_menu_choice == '8':  # 8 : Enter scores
                TournamentCtrlr.update_matches_scores_players_points(self)
                self.suggest_saving()
            elif start_menu_choice == '9':  # 9 Reporting
                InterfaceView.menu_reporting()
                reporting_choice = input()
                if reporting_choice == '1':  # 1 All players
                    ReportingCtrlr.display_all_players_reporting(self)
                elif reporting_choice == '2':  # 2 One tournament's players
                    ReportingCtrlr.display_tournament_players(self)
                elif reporting_choice == '3':  # 3 All tournaments
                    ReportingCtrlr.display_all_tournaments(self)
                elif reporting_choice == '4':  # 4 One tournament's rounds
                    ReportingCtrlr.tournament_all_rounds(self)
                elif reporting_choice == '5':  # 5 One tournament's matches
                    ReportingCtrlr.tournament_all_matches(self)
                else:
                    self.exit_on_unavailable_choice()
            elif start_menu_choice == '10':  # 10 Save - Load backup
                InterfaceView.save_or_load_menu()
                save_or_load_choice = input(
                    'Entrez le numero correspondant : ')
                if save_or_load_choice == '1':
                    Save_and_load_Ctrlr.save_program(self)
                    InterfaceView.program_saved()
                elif save_or_load_choice == '2':
                    Save_and_load_Ctrlr.load_progam(self)
                    InterfaceView.backup_loaded()
                else:
                    self.exit_on_unavailable_choice()
            elif start_menu_choice == '11':  # 11 Program exit
                InterfaceView.exit_programm()
                user_answer = input()
                if user_answer == 'O':
                    PlayerCtrlr.update_players_points_in_db_all(self)
                    Save_and_load_Ctrlr.save_program(self)
                    InterfaceView.display_goodbye()
                    sys.exit()
                else:
                    self.exit_on_unavailable_choice()
            else:
                InterfaceView.choice_unavailable()
                InterfaceView.exit_programm()
                user_answer = input()
                if user_answer == 'O':
                    PlayerCtrlr.update_players_points_in_db_all(self)
                    Save_and_load_Ctrlr.save_program(self)
                    InterfaceView.display_goodbye()
                    sys.exit()
                else:
                    self.exit_on_unavailable_choice()
        return self.t_launch()

    def create_tournament(self):
        tourney_id = TournamentCtrlr.create_new_tournament(
                    self, tournament_id=0, tournament_rounds_qty=4)
        self.suggest_saving()
        self.adding_t_players(tourney_id)
        tournament_id = tourney_id
        for r_nb in range(0, 3):
            self.launch_next_round(tournament_id)
        self.update_ranking()

    def adding_t_players(self, tourney_id):
        InterfaceView.ask_for_players_inclusion()
        adding_players = input()
        if adding_players == 'O':
            tournament_id = tourney_id
            TournamentCtrlr.create_tournament_players_id_list(self,
                                                             tournament_id)
            self.suggest_saving()
            self.launch_first_round(tournament_id)
        else:
            self.t_launch()

    def launch_first_round(self, tournament_id):
        InterfaceView.ask_for_first_round_launch()
        first_r_launch = input()
        if first_r_launch == 'O':
            round_id = TournamentCtrlr.create_first_round(self, tournament_id)
            self.suggest_saving()
            self.close_this_round(tournament_id, round_id)
        else:
            self.t_launch()

    def close_this_round(self, tournament_id, round_id):
        InterfaceView.this_round_closing()
        closing_r = input()
        if closing_r == 'O':
            TournamentCtrlr.closing_this_round(self, tournament_id, round_id)
            self.suggest_saving()
            self.update_this_rd_scores(tournament_id, round_id)
        else:
            self.t_launch()

    def update_this_rd_scores(self, tournament_id, round_id):
        InterfaceView.update_scores()
        scores_updating = input()
        if scores_updating == 'O':
            TournamentCtrlr.updating_this_r_scores(self, tournament_id,
                                                  round_id)
            self.suggest_saving()
            return tournament_id
        else:
            self.t_launch()

    def launch_next_round(self, tournament_id):
        InterfaceView.launch_round()
        launch_rd = input()
        if launch_rd == 'O':
            round_id = TournamentCtrlr.create_next_round(self, tournament_id)
            self.suggest_saving()
            self.close_this_round(tournament_id, round_id)
        else:
            self.t_launch()
 
    def close_this_round(self, tournament_id, round_id):
        InterfaceView.this_round_closing()
        closing_r = input()
        if closing_r == 'O':
            TournamentCtrlr.closing_this_round(self, tournament_id, round_id)
            self.suggest_saving()
            self.update_this_rd_scores(tournament_id, round_id)
        else:
             InterfaceView.end_round_before_start_new_one()
             self.t_launch()
 
    def update_ranking(self):
        InterfaceView.request_ranking_update()
        rk_update_choice = input()
        if rk_update_choice == '1':
            TournamentCtrlr.update_players_ranking(self)
        elif rk_update_choice == '2':
            PlayerCtrlr.update_global_ranking(self)
        else:
            self.t_launch()
        self.suggest_saving()
        return self.t_launch()

    def suggest_saving(self):
        Save_and_load_Views.ask_programm_saving()
        prog_saving = input()
        if prog_saving == 'O':
            Save_and_load_Ctrlr.save_program(self)
        else:
            pass

    def exit_on_unavailable_choice(self):
        InterfaceView.end_round_before_start_new_one()
        self.t_launch()
        
    
main()
