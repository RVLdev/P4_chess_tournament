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
        self.menu_list = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
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
            if start_menu_choice == '1':  # 1 TOURNOI : Créer un tournoi
                tourney_id = TournamentCtlr.create_new_tournament(
                    self, tournament_id=0, tournament_rounds_qty=4)
                Save_and_load_View.ask_programm_saving(self)  # ******* SVG **
                prog_saving = input()
                if prog_saving == 'O':
                    Save_and_load_Ctrl.save_program(self)
                else:
                    pass
                InterfaceView.ask_for_players_inclusion()  # ajouer 8 joueurs ?
                adding_players = input()
                if adding_players == 'O':
                    tournament_id = tourney_id
                    TournamentCtlr.create_tournament_players_id_list(
                        self, tournament_id)
                    Save_and_load_View.ask_programm_saving(self)  # ******* SVG **
                    prog_saving = input()
                    if prog_saving == 'O':
                        Save_and_load_Ctrl.save_program(self)
                    else:
                        pass
                    InterfaceView.ask_for_first_round_launch()  # lancer 1er tour ?
                    first_r_launch = input()
                    if first_r_launch == 'O':
                        round_id = TournamentCtlr.create_first_round(
                            self, tournament_id)
                        Save_and_load_View.ask_programm_saving(self)  # ******* SVG **
                        prog_saving = input()
                        if prog_saving == 'O':
                            Save_and_load_Ctrl.save_program(self)
                        else:
                            pass
                        InterfaceView.this_round_closing()  # terminer CE tour ?
                        closing_r = input()
                        if closing_r == 'O':
                            TournamentCtlr.closing_this_round(self, round_id)
                            Save_and_load_View.ask_programm_saving(self)  # ******* SVG **
                            prog_saving = input()
                            if prog_saving == 'O':
                                Save_and_load_Ctrl.save_program(self)
                            else:
                                pass
                            InterfaceView.update_scores()  # màj scores ?
                            scores_updating = input()
                            if scores_updating == 'O':
                                TournamentCtlr.updating_this_r_scores(
                                    self, round_id)
                                Save_and_load_View.ask_programm_saving(self)  # ******* SVG **
                                prog_saving = input()
                                if prog_saving == 'O':
                                    Save_and_load_Ctrl.save_program(self)
                                else:
                                    pass
                                """ VERIFIER de quel tournoi est issue la val de .tournament_rounds_id_list"""
                                for r_nb in range(0, 3):
                                    InterfaceView.launch_round()  # lancer tour suivant
                                    launch_rd = input()
                                    if launch_rd == 'O':
                                        round_id = TournamentCtlr.create_next_round(self, tournament_id)
                                        Save_and_load_View.ask_programm_saving(self)  # ******* SVG **
                                        prog_saving = input()
                                        if prog_saving == 'O':
                                            Save_and_load_Ctrl.save_program(
                                                self)
                                        else:
                                            pass
                                        InterfaceView.this_round_closing()  # terminer CE tour ?
                                        closing_r = input()
                                        if closing_r == 'O':
                                            TournamentCtlr.closing_this_round(
                                                self, round_id)
                                            Save_and_load_View.ask_programm_saving(self)  # ******* SVG **
                                            prog_saving = input()
                                            if prog_saving == 'O':
                                                Save_and_load_Ctrl.save_program(self)
                                            else:
                                                pass
                                            InterfaceView.update_scores()  # màj scores ?
                                            scores_updating = input()
                                            if scores_updating == 'O':
                                                TournamentCtlr.updating_this_r_scores(self, round_id)
                                                Save_and_load_View.ask_programm_saving(self)  # ******* SVG **
                                                prog_saving = input()
                                                if prog_saving == 'O':
                                                    Save_and_load_Ctrl.save_program(self)
                                                else:
                                                    pass
                                            else:
                                                pass  # self.t_launch()
                                        else:
                                            print('Vous devez clore un tour,')
                                            print("avant de pouvoir en lancer un autre.")
                                            pass  # self.t_launch()
                                    else:
                                        pass  # self.t_launch()
                                InterfaceView.request_rank_update()  # màj rank ?
                                updating_rank = input()
                                if updating_rank == 'O':
                                    PlayerController.update_players_ranking(
                                        self)
                                    Save_and_load_View.ask_programm_saving(
                                        self)  # ******* SVG **
                                    prog_saving = input()
                                    if prog_saving == 'O':
                                        Save_and_load_Ctrl.save_program(self)
                                    else:
                                        pass
                                else:
                                    pass  # self.t_launch()

                            else:
                                pass  # self.t_launch()
                        else:
                            print('Vous devez terminer un tour,')
                            print('avant de pouvoir en lancer un autre.')
                            return self.t_launch()
                    else:
                        pass  # self.t_launch()
                else:
                    pass  # self.t_launch()

            elif start_menu_choice == '2':  # 2 JOUEURS : Enregistrer joueurs
                PlayerController.create_new_player(self, player_id=0)
                time.sleep(2)
                Save_and_load_View.ask_programm_saving(self)  # ******* SVG **
                prog_saving = input()
                if prog_saving == 'O':
                    Save_and_load_Ctrl.save_program(self)
                else:
                    pass  # self.t_launch()

            elif start_menu_choice == '3':  # 3 J : + un joueur à 1 tournoi'
                TournamentCtlr.add_a_player_to_a_tournament(self)
                Save_and_load_View.ask_programm_saving(self)  # ******* SVG **
                prog_saving = input()
                if prog_saving == 'O':
                    Save_and_load_Ctrl.save_program(self)
                else:
                    pass  # self.t_launch()

            elif start_menu_choice == '4':  # 4 JOUEURS : màj classmnt joueur
                PlayerController.update_players_ranking(self)
                time.sleep(2)
                Save_and_load_View.ask_programm_saving(self)  # ******* SVG **
                prog_saving = input()
                if prog_saving == 'O':
                    Save_and_load_Ctrl.save_program(self)
                else:
                    pass  # self.t_launch()

            elif start_menu_choice == '5':  # 5 TOUR : Lancer un tour
                TournamentCtlr.create_a_tournament_round(self)
                Save_and_load_View.ask_programm_saving(self)  # ******* SVG **
                prog_saving = input()
                if prog_saving == 'O':
                    Save_and_load_Ctrl.save_program(self)
                else:
                    pass  # self.t_launch()

            elif start_menu_choice == '6':  # 6 TOUR : Clôturer un tour
                TournamentCtlr.closing_a_round(self)
                time.sleep(2)
                Save_and_load_View.ask_programm_saving(self)  # ******* SVG **
                prog_saving = input()
                if prog_saving == 'O':
                    Save_and_load_Ctrl.save_program(self)
                else:
                    pass  # self.t_launch()

            elif start_menu_choice == '7':  # 7 TOUR : Renseigner les scores
                TournamentCtlr.update_matches_scores_players_points(self)
                time.sleep(2)
                Save_and_load_View.ask_programm_saving(self)  # ******* SVG **
                prog_saving = input()
                if prog_saving == 'O':
                    Save_and_load_Ctrl.save_program(self)
                else:
                    pass  # self.t_launch()

            elif start_menu_choice == '8':  # 8 Reporting
                InterfaceView.menu_reporting()
                reporting_choice = input()
                if reporting_choice == '1':  # 1 Liste de tous joueurs
                    ReportingController.display_all_players_reporting(self)
                elif reporting_choice == '2':  # 2 Liste joueurs d'un tournoi
                    ReportingController.display_tournament_players(self)
                elif reporting_choice == '3':  # 3 Liste de tous les tournois
                    ReportingController.display_all_tournaments(self)
                elif reporting_choice == '4':  # 4 Liste tours d'un tournoi
                    ReportingController.tournament_all_rounds(self)
                elif reporting_choice == '5':  # 5 Liste matches d'un tournoi
                    ReportingController.tournament_all_matches(self)
                else:
                    pass  # self.t_launch()

            elif start_menu_choice == '9':  # 8 Sauvegarder - Charger
                InterfaceView.save_or_load_menu()
                save_or_load_choice = input(
                    'Entrez le numero correspondant : ')
                if save_or_load_choice == '1':
                    Save_and_load_Ctrl.save_program(self)
                elif save_or_load_choice == '2':
                    Save_and_load_Ctrl.load_progam(self)
                else:
                    pass  # self.t_launch()

            elif start_menu_choice == '0':  # 0 Quitter le programme
                InterfaceView.exit_programm()
                user_answer = input()
                if user_answer == 'O':
                    Save_and_load_Ctrl.save_program(self)
                    print('Au revoir')
                    sys.exit()
                else:
                    pass  # self.t_launch()
            else:
                InterfaceView.exit_programm()
                user_answer = input()
                if user_answer == 'O':
                    Save_and_load_Ctrl.save_program(self)
                    print('Au revoir')
                    sys.exit()
                else:
                    pass  # self.t_launch()
        return self.t_launch()


main()
