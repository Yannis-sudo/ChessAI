import torch
import torch.nn as nn
from random import randint

from get_games import get_games, get_next_player_month, players, update_next_player_month

def train_loop(model):
    random_player_id = randint(0, len(players) - 1)
    next_player = get_next_player_month(players[random_player_id])
    positions = get_games(100, random_player_id, next_player["year"], next_player["month"])
    update_next_player_month(players[random_player_id])

    