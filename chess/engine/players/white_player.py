import engine.piece_tile.piece_tile
import engine.players.player
import engine.board.board

class WhitePlayer(engine.players.player.Player):
    def __init__(self, board: engine.board.board.Board, legal_moves, opponent_moves):
        super().__init__(board, legal_moves, opponent_moves, True)

    def get_active_pieces(self) -> [engine.piece_tile.piece_tile.Piece]:
        white_pieces = []
        for r in range(8):
            for c in range(8):
                if self.board[r][c].is_occupied():
                    if self.board[r][c].get_piece().is_white:
                        white_pieces.append(self.board[r][c].get_piece())
        return white_pieces

    def get_opponent(self) -> engine.players.player.Player:
        return self.board.black_player

    def color(self) -> int:
        return engine.board.board.Board.WHITE
