import requests
import io
import chess
import chess.pgn
import sqlite3
from pathlib import Path
import json

players = ["ya10be", "hikaru", "magnuscarlsen", "gothamchess"]

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

def update_next_player_month(player):
    current_file = Path(__file__)
    json_path = current_file.parent.parent / "db" / "next_game.json"
    with open(json_path, "r") as json_file:
        data = json.load(json_file)
    if data["player"][player]["month"] - 1 == 0:
        data["player"][player]["month"] = 12
        data["player"][player]["year"] = data["player"][player]["year"] - 1
    with open(json_path, "w") as json_file_w:
        json.dump(data, json_file_w, indent=4)

def get_next_player_month(player):
    # DB path
    current_file = Path(__file__)
    db_path = current_file.parent.parent / "db" / "games_downloaded.db"
    db = sqlite3.connect(db_path)
    cursor = db.cursor()
    
    # JSOn file
    json_path = current_file.parent.parent / "db" / "next_game.json"
    with open(json_path, "r") as json_file:
        data = json.load(json_file)
    year = data["player"][player]["year"]
    month = data["player"][player]["month"]

    return_data = {
        "year": year,
        "month": month,
        "player": player
    }

    month_for_sql = str(month)
    if (month < 10): 
        month_for_sql = "0" + str(month)
    cursor.execute("INSERT INTO games_downloaded (user, month) VALUES (?, ?)", (player, f"{str(year)}-{month_for_sql}", ))
    db.commit()

    return return_data

def get_games(max_games=100, player=0, year=2026, month=1):
    if player >= len(players):
        print("Player index out of range")
        player = 0

    api_url = f"https://api.chess.com/pub/player/{players[player]}/games/{year}/{month:02d}"
    res = requests.get(api_url, headers=headers)

    
    if res.status_code != 200:
        print(f"Fehler beim Abrufen: {res.status_code}")
        return
    
    data = res.json()
    
    if "games" not in data:
        print("Keine Spiele gefunden")
        return

    positions = []

    for game in data["games"]:
        try:
            pgn = game["pgn"]
            pgn_io = io.StringIO(pgn)
            game_position = chess.pgn.read_game(pgn_io)
            board = game_position.board()
            for move in game_position.mainline_moves():
                board.push(move)
                positions.append(board.fen)
        except:
            continue
    return positions