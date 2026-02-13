import chess
import chess.engine

path_to_engine = "/home/yannis/dev/stockfish/stockfish-ubuntu-x86-64-avx2"
engine = chess.engine.SimpleEngine.popen_uci(path_to_engine)

def eval_position(board):
    info = engine.analyse(board, chess.engine.Limit(time=3.0))
    score = info["score"].relative
    if score.is_mate():
        return 1000000 - score.mate()
    else:
        return score.score() / 100