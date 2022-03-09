import sys
from controllers.tournamentcontroller import TournamentCtrlr
from controllers.playercontroller import PlayerCtrlr
from controllers.reportingcontroller import ReportingCtrlr
from controllers.roundcontroller import RoundCtrlr
from controllers.save_n_loadcontroller import Save_and_load_Ctrlr
from views.interfaceviews import InterfaceView
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
        """Launches the program's menu."""
        InterfaceView.launch_tournament()
        self.choose_startmenu_options()

    def choose_startmenu_options(self):
        """Asks the user its choice."""
        start_menu_choice = input('Entrez le numero correspondant : ')
        self.activate_startmenu_choice(start_menu_choice)

    def activate_startmenu_choice(self, start_menu_choice):
        """Executes user's choice and then sends him back to the start menu
        (for the next choice).
        """
        if start_menu_choice not in self.menu_list:
            self.exit_option_on_unavailable_choice()
        else:
            if start_menu_choice == '1':
                self.create_tournament()
            elif start_menu_choice == '2':  # Display a tournament
                TournamentCtrlr.read_a_tournament(self)
            elif start_menu_choice == '3':
                PlayerCtrlr.create_new_player_in_db_all(self,
                                                        player_id=0)
                self.suggest_saving()
            elif start_menu_choice == '4':
                InterfaceView.display_add_one_player()
                TournamentCtrlr.add_player_to_any_tournament(self)
                self.suggest_saving()
            elif start_menu_choice == '5':
                self.update_ranking()
            elif start_menu_choice == '6':
                TournamentCtrlr.create_any_tournament_round(self)
                self.suggest_saving()
            elif start_menu_choice == '7':
                TournamentCtrlr.closing_a_tournament_round(self)
                self.suggest_saving()
            elif start_menu_choice == '8':
                TournamentCtrlr.log_a_round_scores(self)
                self.suggest_saving()
            elif start_menu_choice == '9':
                self.choose_reporting()
            elif start_menu_choice == '10':
                self.choose_saving_or_loading_backup()
            elif start_menu_choice == '11':
                self.exit_program()
            else:
                self.suggest_saving()
                self.exit_option_on_unavailable_choice()
        return self.t_launch()

    def create_tournament(self):
        """Create a tournament : its administrative data, players, rounds, new ranking."""
        tourney_id = TournamentCtrlr.create_new_tournament(
            self, tournament_id=0, tournament_rounds_qty=4)
        self.suggest_saving()
        self.adding_t_players(tourney_id)
        tournament_id = tourney_id
        for round_nb in range(0, 3):
            self.launch_next_round(tournament_id)
        self.update_ranking()

    def adding_t_players(self, tourney_id):
        """Add 8 players to current tournament."""
        InterfaceView.ask_for_players_inclusion()
        adding_players = input()
        if adding_players == 'OUI':
            tournament_id = tourney_id
            TournamentCtrlr.create_tournament_players_id_list(self,
                                                              tournament_id)
            self.suggest_saving()
            self.launch_first_round(tournament_id)
        else:
            self.t_launch()

    def launch_first_round(self, tournament_id):
        """Launches current tournament's first round."""
        InterfaceView.ask_for_first_round_launch()
        first_r_launch = input()
        if first_r_launch == 'OUI':
            round_id = TournamentCtrlr.create_first_round(self, tournament_id)
            self.suggest_saving()
            self.close_this_round(tournament_id, round_id)
        else:
            self.t_launch()

    def close_this_round(self, tournament_id, round_id):
        """ Closes current round by adding end date and time."""
        InterfaceView.this_round_closing()
        closing_r = input()
        if closing_r == 'OUI':
            RoundCtrlr.closing_this_round(self, tournament_id, round_id)
            self.suggest_saving()
            self.log_this_rd_scores(tournament_id, round_id)
        else:
            InterfaceView.end_round_before_start_new_one()
            self.t_launch()

    def log_this_rd_scores(self, tournament_id, round_id):
        """Saves matches scores of previously closed round."""
        InterfaceView.update_scores()
        scores_updating = input()
        if scores_updating == 'OUI':
            TournamentCtrlr.loging_this_r_scores(self, tournament_id,
                                                 round_id)
            self.suggest_saving()
            return tournament_id
        else:
            self.t_launch()

    def launch_next_round(self, tournament_id):
        """launches any round after a first round."""
        InterfaceView.launch_round()
        launch_rd = input()
        if launch_rd == 'OUI':
            round_id = TournamentCtrlr.create_next_round(self, tournament_id)
            self.suggest_saving()
            self.close_this_round(tournament_id, round_id)
        else:
            self.t_launch()

    def update_ranking(self):
        """Updates ranking at the end of one tournament or at the end of
        all tournaments (global ranking).
        """
        InterfaceView.request_ranking_update()
        rk_update_choice = input()
        if rk_update_choice == '1':
            TournamentCtrlr.update_tournament_player_ranking(self)
        elif rk_update_choice == '2':
            PlayerCtrlr.update_global_ranking(self)
        else:
            self.t_launch()
        self.suggest_saving()
        return self.t_launch()

    def choose_reporting(self):
        """Lists available reportings"""
        InterfaceView.menu_reporting()
        reporting_choice = input()
        if reporting_choice == '1':
            ReportingCtrlr.display_all_players_reporting(self)
        elif reporting_choice == '2':
            ReportingCtrlr.display_tournament_players(self)
        elif reporting_choice == '3':
            ReportingCtrlr.display_all_tournaments(self)
        elif reporting_choice == '4':  # One tournament's rounds
            ReportingCtrlr.tournament_all_rounds(self)
        elif reporting_choice == '5':  # One tournament's matches
            ReportingCtrlr.tournament_all_matches(self)
        else:
            self.exit_option_on_unavailable_choice()

    def suggest_saving(self):
        """Suggest the User to save the program."""
        Save_and_load_Views.ask_programm_saving()
        prog_saving = input()
        if prog_saving == 'OUI':
            Save_and_load_Ctrlr.save_program(self)
        else:
            pass

    def choose_saving_or_loading_backup(self):
        """Give options to save the program or to load a backup."""
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
            self.exit_option_on_unavailable_choice()

    def exit_option_on_unavailable_choice(self):
        """Displays a message on User's wrong choice and sends him
        back to the menu.
        """
        InterfaceView.choice_unavailable()
        self.t_launch()

    def exit_program(self):
        """ Exit the program on the User's choice."""
        InterfaceView.exit_programm()
        user_answer = input()
        if user_answer == 'OUI':
            PlayerCtrlr.update_players_points_in_db_all(self)
            Save_and_load_Ctrlr.save_program(self)
            InterfaceView.display_goodbye()
            sys.exit()
        else:
            self.exit_option_on_unavailable_choice()


main()
