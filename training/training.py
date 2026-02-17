import torch
import torch.nn as nn
from random import randint
import chess

from training.get_games import get_games

piece_to_plane = {
    chess.PAWN: 0,
    chess.KNIGHT: 1,
    chess.BISHOP: 2,
    chess.ROOK: 3,
    chess.QUEEN : 4,
    chess.KING: 5
}

def train_loop(model):
    # Get positions
    positions = get_games(1000)

    # Training loop
    loss_fn = nn.MSELoss()

    for pos in positions["positions"]:
        tensor = torch.zeros(12, 8, 8)
        board = chess.Board(pos["fen"])

        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece == None:
                continue
            row = 7 - chess.square_rank(square)
            col = chess.square_file(square)

            plane = piece_to_plane[piece.piece_type]
            if piece.color == chess.BLACK:
                plane+=6
            tensor[plane, row, col] = 1
        
        tensor = tensor.unsqueeze(0)
        optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
        target_value = pos["evaluation"]
        target = torch.tensor([[target_value]])

        for step in range(100):
            optimizer.zero_grad()
            output = model(tensor)
            loss = loss_fn(output, target)
            loss.backward()
            optimizer.step()
            if step == 99:
                print(f"Output: {output.item():.4f} Loss: {loss.item():.4f} Target: {target_value}")
