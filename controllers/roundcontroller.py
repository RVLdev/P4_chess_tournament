from datetime import datetime
from models.roundmodel import Round
from models.tournamentmodel import Tournament


class RoundCtrlr:
    def __init__(self, r_matches_id_list):
        self.r_matches_id_list = r_matches_id_list

    def create_new_round(self, tournament_id, r_matches_id_list, round_id=0,
                         end_date_time=0, start_date_time=0):
        """ create a round """
        round = Round(round_id,
                      RoundCtrlr.give_round_name(self, tournament_id),
                      r_matches_id_list,
                      start_date_time,
                      end_date_time)
        round.create_round(tournament_id)
        self.round_id = Round.update_round_id(self, tournament_id)

        return round

    def give_round_name(self, tournament_id):
        """ get or ask round name"""
        this_tourney = Tournament.tournaments_db.get(doc_id=tournament_id)
        round_number = len(this_tourney['t_rounds_list'])
        round_name = f'{"Round"}{round_number+1}'
        return round_name

    def start_round(self):
        """generate date & time for the begining of a round"""
        start_date_and_time = str(datetime.now())
        return start_date_and_time

    def update_start_date_and_time(self, tournament_id,
                                   start_date_time, round_id):
        """ update round start date_and_time in database """
        Round.update_start_date_time(self, tournament_id,
                                     start_date_time, round_id)

    def close_round(self):
        """set end date and time"""
        end_date_time = str(datetime.now())
        return end_date_time

    def update_round_end_date_time(self, round_id, end_date_time):
        """ update round end date_and_time in database """
        Round.update_round_end_date_time(self, round_id, end_date_time)
