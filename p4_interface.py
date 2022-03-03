import time
import sys
from p4_controllers import TournamentCtlr
from p4_controllers import PlayerController
from p4_controllers import ReportingController
from p4_controllers import Save_and_load_Ctrl
from p4_views import InterfaceView
from p4_views import Save_and_load_View


def main():
    launch = InterfaceController()
    launch.t_launch()


class InterfaceController:
    def __init__(self):
        self.menu_list = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11']
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
            InterfaceView.choice_unavailable()
            time.sleep(1.5)
            self.t_launch()
        else:
            if start_menu_choice == '1':  # 1 : Create a tournament
                tourney_id = TournamentCtlr.create_new_tournament(
                    self, tournament_id=0, tournament_rounds_qty=4)
                Save_and_load_View.ask_programm_saving()
                prog_saving = input()
                if prog_saving == 'O':
                    Save_and_load_Ctrl.save_program(self)
                else:
                    pass
                InterfaceView.ask_for_players_inclusion()
                adding_players = input()
                if adding_players == 'O':
                    tournament_id = tourney_id
                    TournamentCtlr.create_tournament_players_id_list(
                        self, tournament_id)
                    Save_and_load_View.ask_programm_saving()
                    prog_saving = input()
                    if prog_saving == 'O':
                        Save_and_load_Ctrl.save_program(self)
                    else:
                        pass
                    InterfaceView.ask_for_first_round_launch()
                    first_r_launch = input()
                    if first_r_launch == 'O':
                        round_id = TournamentCtlr.create_first_round(
                            self, tournament_id)
                        Save_and_load_View.ask_programm_saving()
                        prog_saving = input()
                        if prog_saving == 'O':
                            Save_and_load_Ctrl.save_program(self)
                        else:
                            pass
                        InterfaceView.this_round_closing()
                        closing_r = input()
                        if closing_r == 'O':
                            TournamentCtlr.closing_this_round(
                                self,tournament_id, round_id)
                            Save_and_load_View.ask_programm_saving()
                            prog_saving = input()
                            if prog_saving == 'O':
                                Save_and_load_Ctrl.save_program(self)
                            else:
                                pass
                            InterfaceView.update_scores()
                            scores_updating = input()
                            if scores_updating == 'O':
                                TournamentCtlr.updating_this_r_scores(
                                    self, tournament_id, round_id)
                                Save_and_load_View.ask_programm_saving()
                                prog_saving = input()
                                if prog_saving == 'O':
                                    Save_and_load_Ctrl.save_program(self)
                                else:
                                    pass
                                for r_nb in range(0, 3):
                                    InterfaceView.launch_round()
                                    launch_rd = input()
                                    if launch_rd == 'O':
                                        round_id = TournamentCtlr.create_next_round(
                                            self, tournament_id)
                                        Save_and_load_View.ask_programm_saving()
                                        prog_saving = input()
                                        if prog_saving == 'O':
                                            Save_and_load_Ctrl.save_program(
                                                self)
                                        else:
                                            pass
                                        InterfaceView.this_round_closing()
                                        closing_r = input()
                                        if closing_r == 'O':
                                            TournamentCtlr.closing_this_round(
                                                self, tournament_id, round_id)
                                            Save_and_load_View.ask_programm_saving()
                                            prog_saving = input()
                                            if prog_saving == 'O':
                                                Save_and_load_Ctrl.save_program(self)
                                            else:
                                                pass
                                            InterfaceView.update_scores()
                                            scores_updating = input()
                                            if scores_updating == 'O':
                                                TournamentCtlr.updating_this_r_scores(
                                                    self, tournament_id, round_id)
                                                Save_and_load_View.ask_programm_saving()
                                                prog_saving = input()
                                                if prog_saving == 'O':
                                                    Save_and_load_Ctrl.save_program(self)
                                                else:
                                                    pass
                                            else:
                                                pass
                                        else:
                                            print('Vous devez clore un tour,')
                                            print("avant de pouvoir en lancer un autre.")
                                            pass
                                    else:
                                        pass
                                InterfaceView.request_ranking_update()
                                rk_update_choice = input()
                                if rk_update_choice == '1':
                                    PlayerController.update_players_ranking(self)
                                    time.sleep(2)
                                elif rk_update_choice == '1':
                                    PlayerController.update_global_ranking(self)
                                else:
                                    self.t_launch()
                                Save_and_load_View.ask_programm_saving()
                                prog_saving = input()
                                if prog_saving == 'O':
                                    Save_and_load_Ctrl.save_program(self)
                                else:
                                    pass
                            else:
                                pass
                        else:
                            print('Vous devez terminer un tour,')
                            print('avant de pouvoir en lancer un autre.')
                            return self.t_launch()
                    else:
                        pass
                else:
                    pass

            elif start_menu_choice == '2':  # 2 Display a tournament
                TournamentCtlr.read_a_tournament(self)
                time.sleep(2)
                Save_and_load_View.ask_programm_saving()
                prog_saving = input()
                if prog_saving == 'O':
                    Save_and_load_Ctrl.save_program(self)
                else:
                    pass

            elif start_menu_choice == '3':  # 3 Create new player
                PlayerController.create_new_player_in_db_all(self, player_id=0)
                time.sleep(2)
                Save_and_load_View.ask_programm_saving()
                prog_saving = input()
                if prog_saving == 'O':
                    Save_and_load_Ctrl.save_program(self)
                else:
                    pass

            elif start_menu_choice == '4':  # 4 : add a tournament 1 player
                InterfaceView.ask_add_one_player()
                add_one_players = input()
                if add_one_players == 'O':
                    TournamentCtlr.add_a_player_to_a_tournament(self)
                    Save_and_load_View.ask_programm_saving()
                    prog_saving = input()
                    if prog_saving == 'O':
                        Save_and_load_Ctrl.save_program(self)
                    else:
                        pass
                else:
                    pass

            elif start_menu_choice == '5':  # 5 : updating a player rank
                InterfaceView.request_ranking_update()
                rk_update_choice = input()
                if rk_update_choice == '1':
                    PlayerController.update_players_ranking(self)
                    time.sleep(2)
                else:
                    PlayerController.update_global_ranking(self)
                Save_and_load_View.ask_programm_saving()
                prog_saving = input()
                if prog_saving == 'O':
                    Save_and_load_Ctrl.save_program(self)
                else:
                    pass

            elif start_menu_choice == '6':  # 6 : Launching a round
                TournamentCtlr.create_a_tournament_round(self)
                Save_and_load_View.ask_programm_saving()
                prog_saving = input()
                if prog_saving == 'O':
                    Save_and_load_Ctrl.save_program(self)
                else:
                    pass

            elif start_menu_choice == '7':  # 7 : Ending a tournament
                TournamentCtlr.closing_a_round(self)
                time.sleep(2)
                Save_and_load_View.ask_programm_saving()
                prog_saving = input()
                if prog_saving == 'O':
                    Save_and_load_Ctrl.save_program(self)
                else:
                    pass

            elif start_menu_choice == '8':  # 8 : Enter scores
                TournamentCtlr.update_matches_scores_players_points(self)
                time.sleep(2)
                Save_and_load_View.ask_programm_saving()
                prog_saving = input()
                if prog_saving == 'O':
                    Save_and_load_Ctrl.save_program(self)
                else:
                    pass

            elif start_menu_choice == '9':  # 9 Reporting
                InterfaceView.menu_reporting()
                reporting_choice = input()
                if reporting_choice == '1':  # 1 All players
                    ReportingController.display_all_players_reporting(self)
                elif reporting_choice == '2':  # 2 One tournament's players
                    ReportingController.display_tournament_players(self)
                elif reporting_choice == '3':  # 3 All tournaments
                    ReportingController.display_all_tournaments(self)
                elif reporting_choice == '4':  # 4 One tournament's rounds
                    ReportingController.tournament_all_rounds(self)
                elif reporting_choice == '5':  # 5 One tournament's matches
                    ReportingController.tournament_all_matches(self)
                else:
                    pass

            elif start_menu_choice == '10':  # 10 Save - Load backup
                InterfaceView.save_or_load_menu()
                save_or_load_choice = input(
                    'Entrez le numero correspondant : ')
                if save_or_load_choice == '1':
                    Save_and_load_Ctrl.save_program(self)
                    time.sleep(2)
                    InterfaceView.program_saved()
                    time.sleep(5)
                elif save_or_load_choice == '2':
                    Save_and_load_Ctrl.load_progam(self)
                    InterfaceView.backup_loaded()
                    time.sleep(5)
                else:
                    pass

            elif start_menu_choice == '11':  # 11 Program exit
                InterfaceView.exit_programm()
                user_answer = input()
                if user_answer == 'O':
                    PlayerController.update_players_points_in_db_all(self)
                    Save_and_load_Ctrl.save_program(self)
                    print('Au revoir')
                    sys.exit()
                else:
                    pass
            else:
                InterfaceView.exit_programm()
                user_answer = input()
                if user_answer == 'O':
                    PlayerController.update_players_points_in_db_all(self)
                    Save_and_load_Ctrl.save_program(self)
                    print('Au revoir')
                    sys.exit()
                else:
                    pass
        return self.t_launch()


main()
