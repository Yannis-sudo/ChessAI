import requests
import io
import chess
import chess.pgn
import sqlite3
from pathlib import Path
import json
import io
import chess
import chess.pgn
import sqlite3
from pathlib import Path
import json
import os

def get_games(max_games=100):
    with open("/home/yannis/dev/ChessAI/db/api_url.txt", "r") as f:
        url = f.read()
    res = requests.get(url + "/get_games/1000")
    if res.status_code != 200:
        return

    data = res.json()
    return data