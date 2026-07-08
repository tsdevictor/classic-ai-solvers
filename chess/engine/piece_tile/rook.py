import engine.piece_tile.piece_tile as piece_tile


class Rook(piece_tile.Piece):

    def __init__(self, tile, is_white, is_first_move=True):
        super().__init__(piece_tile.Piece.ROOK, tile, is_white, is_first_move)

    def __str__(self):
        return 'R'

    def calculate_moves(self, board):
        import engine.move.move

        row = self.tile.row
        col = self.tile.col
        possible_moves = []

        down = row+1 < 8
        up = row-1 >= 0
        right = col+1 < 8
        left = col-1 >= 0
        for k in range(1, 8):
            if down and row+k < 8:
                possible_moves.append(engine.move.move.Move(board, self, board[row + k][col]))
                if not board[row + k][col].is_empty(): down = False
            if up and row-k >= 0:
                possible_moves.append(engine.move.move.Move(board, self, board[row - k][col]))
                if not board[row - k][col].is_empty(): up = False
            if right and col+k < 8:
                possible_moves.append(engine.move.move.Move(board, self, board[row][col + k]))
                if not board[row][col + k].is_empty(): right = False
            if left and col-k >= 0:
                possible_moves.append(engine.move.move.Move(board, self, board[row][col - k]))
                if not board[row][col - k].is_empty(): left = False

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
        return Rook(move.target, self.is_white, False)
