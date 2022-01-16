from ..views.player_view import PlayerView
from player_model import Player
from tinydb import where

# TEST PLAYER_CONTROLLER


def create_player(player_id=0):
    """create one player"""
    player = Player(
        player_id,
        ask_player_name(),
        ask_player_first_name(),
        ask_player_birth_date(),
        ask_player_gender(),
        ask_player_ranking(),
        player_points_qty=0
        )
    player.create_player()  # renvoie vers enregistrement en BDD (Model)
    return player


def ask_player_name():
    """ get player_name from User through player_view """
    PlayerView.ask_player_name()  # cf @classmethod
    player_name = input()
    # vérifications !!!
    return player_name


def ask_player_first_name():
    """ get player_first_name from User through player_view """
    PlayerView.ask_player_first_name()
    player_first_name = input()
    return player_first_name


def ask_player_birth_date():
    """ get player_birth_date from User through player_view """
    PlayerView.ask_player_birth_date()
    player_birth_date = input()
    return player_birth_date


def ask_player_gender():
    """ get player_gender from User through player_view """
    PlayerView.ask_player_gender()
    player_gender = input()
    return player_gender


def ask_player_ranking():
    """ get player_ranking from User through player_view """
    PlayerView.ask_player_ranking()
    player_ranking = input()
    return player_ranking


ask_player_name()
