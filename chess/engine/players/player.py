import engine.piece_tile.piece_tile
import engine.move.move
import engine.piece_tile.king

class Player:
    def __init__(self, board,
                 legal_moves: [engine.move.move.Move],
                 opponent_moves: [engine.move.move.Move],
                 is_white: bool):
        self.board = board
        self.is_white = is_white
        self.is_black = not is_white
        self.opponent_moves = opponent_moves
        self.king = self.establish_king()
        self.legal_moves = self.get_king_castles() + legal_moves
        self.is_castled = False

    def __str__(self):
        if self.is_white:
            return 'White'
        return 'Black'

    def color(self):
        return

    def establish_king(self) -> engine.piece_tile.piece_tile.Piece:
        for r in range(8):
            for c in range(8):
                if self.board[r][c].is_occupied() and \
                        isinstance(self.board[r][c].get_piece(), engine.piece_tile.king.King) \
                        and self.board[r][c].get_piece().is_white == self.is_white:
                    return self.board[r][c].get_piece()
        raise RuntimeError('No king found for ' + ('white' if self.is_white else 'black'))

    @staticmethod
    def attacks_on_tile(tile: engine.piece_tile.piece_tile.Tile, opponent_moves: [engine.move.move.Move])\
            -> [engine.move.move.Move]:
        moves = []
        for move in opponent_moves:
            if move.target == tile:
                moves.append(move)
        return moves

    def get_active_pieces(self) -> [engine.piece_tile.piece_tile.Piece]:
        return

    def get_opponent(self):
        return

    def is_move_legal(self, move) -> bool:
        return move in self.legal_moves

    def is_in_check(self) -> bool:
        return len(self.attacks_on_tile(self.king.tile, self.opponent_moves)) != 0

    def is_in_checkmate(self) -> bool:
        return self.is_in_check() and not self.can_escape()

    def is_in_stalemate(self) -> bool:
        return not self.is_in_check() and not self.can_escape()

    def can_escape(self) -> bool:
        for move in self.legal_moves:
            transition = self.make_move(move)
            if transition.get_move_status().is_done():
                return True
        return False

    def can_king_side_castle(self) -> bool:
        for castle in self.get_king_castles():
            if isinstance(castle, engine.move.move.KingSideCastleMove):
                return True
        return False

    def can_queen_side_castle(self) -> bool:
        for castle in self.get_king_castles():
            if isinstance(castle, engine.move.move.QueenSideCastleMove):
                return True
        return False

    def get_king_castles(self) -> [engine.move.move.Move]:
        king_castles = []

        if self.king.is_first_move and not self.is_in_check():
            king_row = self.king.tile.row
            if not self.board[king_row][5].is_occupied() and \
                    not self.board[king_row][6].is_occupied():
                if self.board[king_row][7].is_occupied() and self.board[king_row][7].piece.is_first_move:
                    if not Player.attacks_on_tile(self.board[king_row][5], self.opponent_moves) and \
                            not Player.attacks_on_tile(self.board[king_row][6], self.opponent_moves) and \
                            self.board[king_row][7].piece.piece_type == engine.piece_tile.piece_tile.Piece.ROOK:
                        king_castles.append(engine.move.move.
                                            KingSideCastleMove(self.board,
                                                               self.king,
                                                               self.board[king_row][6],        # king destination
                                                               self.board[king_row][7].piece,  # rook object
                                                               self.board[king_row][7],        # rook tile
                                                               self.board[king_row][5]))       # rook destination

            if not self.board[king_row][1].is_occupied() and \
                    not self.board[king_row][2].is_occupied() and \
                    not self.board[king_row][3].is_occupied():
                if self.board[king_row][0].is_occupied() and self.board[king_row][0].piece.is_first_move:
                    if not Player.attacks_on_tile(self.board[king_row][1], self.opponent_moves) and \
                            not Player.attacks_on_tile(self.board[king_row][2], self.opponent_moves) and \
                            not Player.attacks_on_tile(self.board[king_row][3], self.opponent_moves) and \
                            self.board[king_row][0].piece.piece_type == engine.piece_tile.piece_tile.Piece.ROOK:
                        king_castles.append(engine.move.move.
                                            QueenSideCastleMove(self.board, self.king,
                                                                self.board[king_row][2],        # king destination
                                                                self.board[king_row][0].piece,  # rook object
                                                                self.board[king_row][0],        # rook tile
                                                                self.board[king_row][3]))       # rook destination

        return king_castles

    def make_move(self, move: engine.move.move.Move) -> engine.move.move.MoveTransition:
        if not self.is_move_legal(move):
            return engine.move.move.MoveTransition(self.board, move, engine.move.move.MoveStatus.ILLEGAL_MOVE)

        transition_board = move.execute()
        if Player.attacks_on_tile(transition_board.current_player.get_opponent().king.tile,
                                  transition_board.current_player.legal_moves):
            return engine.move.move.MoveTransition(self.board, move, engine.move.move.MoveStatus.LEAVES_IN_CHECK)

        return engine.move.move.MoveTransition(transition_board, move, engine.move.move.MoveStatus.DONE)
