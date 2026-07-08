import engine.piece_tile.piece_tile as piece_tile


class Knight(piece_tile.Piece):
    def __init__(self, tile, is_white, is_first_move=True):
        super().__init__(piece_tile.Piece.KNIGHT, tile, is_white, is_first_move)

    def __str__(self):
        return 'N'

    def calculate_moves(self, board):
        import engine.move.move

        row = self.tile.row
        col = self.tile.col

        possible_moves = []
        if piece_tile.Tile.is_in_bounds(row + 2, col + 1):
            possible_moves.append(engine.move.move.Move(board, self, board[row + 2][col + 1]))
        if piece_tile.Tile.is_in_bounds(row + 2, col - 1):
            possible_moves.append(engine.move.move.Move(board, self, board[row + 2][col - 1]))
        if piece_tile.Tile.is_in_bounds(row - 2, col + 1):
            possible_moves.append(engine.move.move.Move(board, self, board[row - 2][col + 1]))
        if piece_tile.Tile.is_in_bounds(row - 2, col - 1):
            possible_moves.append(engine.move.move.Move(board, self, board[row - 2][col - 1]))
        if piece_tile.Tile.is_in_bounds(row + 1, col + 2):
            possible_moves.append(engine.move.move.Move(board, self, board[row + 1][col + 2]))
        if piece_tile.Tile.is_in_bounds(row + 1, col - 2):
            possible_moves.append(engine.move.move.Move(board, self, board[row + 1][col - 2]))
        if piece_tile.Tile.is_in_bounds(row - 1, col + 2):
            possible_moves.append(engine.move.move.Move(board, self, board[row - 1][col + 2]))
        if piece_tile.Tile.is_in_bounds(row - 1, col - 2):
            possible_moves.append(engine.move.move.Move(board, self, board[row - 1][col - 2]))

        legal_moves = []
        for move in possible_moves:
            if move.target is not None and move.target.piece != self:
                if move.target.is_occupied():
                    if move.target.piece.diff_color(self):
                        legal_moves.append(engine.move.move.
                                           MajorAttackMove(move.board, move.piece, move.target, move.target.piece))
                else:
                    legal_moves.append(engine.move.move.
                                       MajorMove(move.board, move.piece, move.target))

        return legal_moves

    def move_piece(self, move):
        return Knight(move.target, self.is_white, False)
