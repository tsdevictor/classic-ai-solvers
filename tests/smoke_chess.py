import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "chess"))

# Import explicit engine modules so the package structure initializes cleanly.
import engine.piece_tile.piece_tile
import engine.piece_tile.bishop
import engine.piece_tile.king
import engine.piece_tile.knight
import engine.piece_tile.pawn
import engine.piece_tile.rook
import engine.piece_tile.queen
import engine.players.player
import engine.players.white_player
import engine.players.black_player

from engine.board.board import Board

def main():
    board = Board.create_standard_board()

    checks = [
        (len(board.white_pieces) == 16, "expected 16 white pieces"),
        (len(board.black_pieces) == 16, "expected 16 black pieces"),
        (len(board.white_legal_moves) == 20, "expected 20 legal opening moves for white"),
        (len(board.black_legal_moves) == 20, "expected 20 legal opening moves for black"),
        (str(board.get_tile("e1").piece).lower() == "k", "expected white king on e1"),
        (str(board.get_tile("e8").piece).lower() == "k", "expected black king on e8"),
    ]

    failed = [message for ok, message in checks if not ok]

    if failed:
        print("Chess smoke test failed.")
        for message in failed:
            print(f"- {message}")
        print("\nBoard:")
        print(board)
        raise SystemExit(1)

    print("Chess smoke test passed.")
    print(f"White pieces: {len(board.white_pieces)}")
    print(f"Black pieces: {len(board.black_pieces)}")
    print(f"White legal moves: {len(board.white_legal_moves)}")
    print(f"Black legal moves: {len(board.black_legal_moves)}")

if __name__ == "__main__":
    main()
