import engine.piece_tile.piece_tile as piece_tile


class Bishop(piece_tile.Piece):
    def __init__(self, tile, is_white, is_first_move=True):
        super().__init__(piece_tile.Piece.BISHOP, tile, is_white, is_first_move)

    def __str__(self):
        return 'B'

    def calculate_moves(self, board):
        import engine.move.move

        row = self.tile.row
        col = self.tile.col

        possible_moves = []
        down_right = row+1 < 8 and col+1 < 8
        up_left = row-1 >= 0 and col-1 >= 0
        down_left = row+1 < 8 and col-1 >= 0
        up_right = row-1 >= 0 and col+1 < 8
        for k in range(1, 8):
            if down_right and row+k < 8 and col+k < 8:
                possible_moves.append(engine.move.move.Move(board, self, board[row+k][col+k]))
                if not board[row+k][col+k].is_empty(): down_right = False
            if up_left and row-k >= 0 and col-k >= 0:
                possible_moves.append(engine.move.move.Move(board, self, board[row-k][col-k]))
                if not board[row-k][col-k].is_empty(): up_left = False
            if down_left and row+k < 8 and col-k >= 0:
                possible_moves.append(engine.move.move.Move(board, self, board[row+k][col-k]))
                if not board[row+k][col-k].is_empty(): down_left = False
            if up_right and row-k >= 0 and col+k < 8:
                possible_moves.append(engine.move.move.Move(board, self, board[row-k][col+k]))
                if not board[row-k][col+k].is_empty(): up_right = False

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
        return Bishop(move.target, self.is_white, False)
