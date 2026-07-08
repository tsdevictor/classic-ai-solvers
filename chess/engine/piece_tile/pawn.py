import engine.piece_tile.piece_tile as piece_tile
import engine.piece_tile.queen

class Pawn(piece_tile.Piece):
    def __init__(self, tile, is_white, is_first_move=True):
        super().__init__(piece_tile.Piece.PAWN, tile, is_white, is_first_move)
        self.popup_menu = None
        self.promotion_choice = None

    def __str__(self):
        return 'P'

    def calculate_moves(self, board):
        import engine.move.move

        row = self.tile.row
        col = self.tile.col

        direction = -1 if self.is_white else 1

        legal_moves = []

        if not (0 <= row + direction < 8):
            return legal_moves

        if not board[row + direction][col].is_occupied():  # move up 1
            if self.is_pawn_promotion_square(board[row + direction][col]):  # pawn promotion square?
                legal_moves.append(engine.move.move.PawnPromotion
                                   (engine.move.move.PawnMove(board, self, board[row + direction][col])))
            else:
                legal_moves.append(engine.move.move.
                                   PawnMove(board, self, board[row + direction][col]))
            if self.is_first_move and not board[row + 2*direction][col].is_occupied():  # move up 2
                legal_moves.append(engine.move.move.
                                   PawnJump(board, self, board[row + 2*direction][col]))

        if col < 7:
            up_right = board[row + direction][col + 1]  # take the piece forward to the right
            if up_right.is_occupied() and up_right.get_piece().diff_color(self):
                if self.is_pawn_promotion_square(board[row + direction][col]):  # pawn promotion square?
                    legal_moves.append(engine.move.move.PawnPromotion
                                       (engine.move.move.PawnAttackMove(board, self, up_right, up_right.piece)))
                else:
                    legal_moves.append(engine.move.move.
                                       PawnAttackMove(board, self, up_right, up_right.piece))
            en_passant_pawn = board.get_en_passant_pawn()
            if en_passant_pawn is not None:
                if en_passant_pawn.tile == board[row][col+1] and en_passant_pawn.diff_color(self) and up_right.is_empty():
                    legal_moves.append(engine.move.move.
                                       PawnEnPassantAttackMove(board, self, up_right, en_passant_pawn))

        if col > 0:
            up_left = board[row + direction][col - 1]  # take the piece forward to the left
            if up_left.is_occupied() and up_left.get_piece().diff_color(self):
                if self.is_pawn_promotion_square(board[row + direction][col]):  # pawn promotion square?
                    legal_moves.append(engine.move.move.PawnPromotion
                                       (engine.move.move.PawnAttackMove(board, self, up_left, up_left.piece)))
                else:
                    legal_moves.append(engine.move.move.
                                       PawnAttackMove(board, self, up_left, up_left.piece))
            en_passant_pawn = board.get_en_passant_pawn()
            if en_passant_pawn is not None:
                if en_passant_pawn.tile == board[row][col-1] and en_passant_pawn.diff_color(self) and up_left.is_empty():
                    legal_moves.append(engine.move.move.
                                       PawnEnPassantAttackMove(board, self, up_left, en_passant_pawn))

        return legal_moves

    def move_piece(self, move):
        return Pawn(move.target, self.is_white, False)

    def get_promotion_piece(self):
        return engine.piece_tile.queen.Queen(self.tile, self.is_white, False)
    """
     TODO:
        return correct promotion choice (currently returns none before choice can even be made bc thread continues)

        self.popup()
        return self.do_popup()

    def popup(self):
        import gui.table
        self.popup_menu = gui.table.Menu(gui.table.Table.board_panel, tearoff=0)

        self.popup_menu.add_command(label="Queen", command=lambda: self.assign_choice(piece_tile.Piece.QUEEN))
        self.popup_menu.add_command(label="Rook", command=lambda: self.assign_choice(piece_tile.Piece.ROOK))
        self.popup_menu.add_command(label="Bishop", command=lambda: self.assign_choice(piece_tile.Piece.BISHOP))
        self.popup_menu.add_command(label="Knight", command=lambda: self.assign_choice(piece_tile.Piece.KNIGHT))

    def do_popup(self):
        import gui.table
        try:
            self.popup_menu.tk_popup(gui.table.Table.game_frame.winfo_x() + self.tile.col * 50,
                                     gui.table.Table.game_frame.winfo_y() + self.tile.row * 50)
        finally:
            self.popup_menu.grab_release()

    def assign_choice(self, piece_type):
        if piece_type == piece_tile.Piece.KNIGHT:
            self.promotion_choice = engine.piece_tile.knight.Knight(self.tile, self.is_white, False)
        if piece_type == piece_tile.Piece.BISHOP:
            self.promotion_choice = engine.piece_tile.bishop.Bishop(self.tile, self.is_white, False)
        if piece_type == piece_tile.Piece.ROOK:
            self.promotion_choice = engine.piece_tile.rook.Rook(self.tile, self.is_white, False)
        if piece_type == piece_tile.Piece.QUEEN:
            self.promotion_choice = engine.piece_tile.queen.Queen(self.tile, self.is_white, False)
        else:
            raise RuntimeError("Pawn promotion error")
    """
