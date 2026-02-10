import requests

players = ["ya10be", "hikaru", "magnuscarlsen", "gothamchess"]

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

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


    for game in data["games"]:
        pgn = game["pgn"]
        
get_games(100, 0, 2026, 1)
