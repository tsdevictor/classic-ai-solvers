class Piece:
    PAWN = 1
    ROOK = 2
    KNIGHT = 3
    BISHOP = 4
    QUEEN = 5
    KING = 6

    def __init__(self, piece_type, tile, is_white, is_first_move):
        self.piece_type = piece_type
        self.tile = tile
        self.is_white = is_white
        self.is_black = not is_white
        self.is_first_move = is_first_move

    def __eq__(self, other):
        return isinstance(other, Piece) and self.piece_type == other.piece_type and self.same_color(other) \
            and self.tile == other.tile

    def get_piece_value(self):
        if self.piece_type == self.PAWN:
            return 100
        elif self.piece_type == self.KNIGHT:
            return 320
        elif self.piece_type == self.BISHOP:
            return 330
        elif self.piece_type == self.ROOK:
            return 500
        elif self.piece_type == self.QUEEN:
            return 900
        elif self.piece_type == self.KING:
            return 20000

    def calculate_moves(self, board) -> []:
        return []

    def same_color(self, other) -> bool:
        return self.is_white == other.is_white

    def diff_color(self, other) -> bool:
        return self.is_white != other.is_white

    def move_piece(self, move):
        return

    def get_row(self) -> int:
        return self.tile.row

    def get_col(self) -> int:
        return self.tile.col

    def is_pawn_promotion_square(self, tile) -> bool:
        return (tile.row == 0 and self.is_white) or (tile.row == 7 and self.is_black)

    def is_pawn(self) -> bool:
        return self.piece_type == Piece.PAWN

    def is_knight(self) -> bool:
        return self.piece_type == Piece.KNIGHT

    def is_bishop(self) -> bool:
        return self.piece_type == Piece.BISHOP

    def is_rook(self) -> bool:
        return self.piece_type == Piece.ROOK

    def is_queen(self) -> bool:
        return self.piece_type == Piece.QUEEN

    def is_king(self) -> bool:
        return self.piece_type == Piece.KING


class Tile:
    def __init__(self, r: int, c: int, p: Piece = None):
        if not Tile.is_in_bounds(r, c):
            raise ValueError("Tile out of bounds")
        self.row = r
        self.col = c
        self.piece = p

    def __str__(self):
        return ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'][self.col] + str(8 - self.row)

    def __eq__(self, other):
        return isinstance(other, Tile) and self.row == other.row and self.col == other.col

    def is_occupied(self) -> bool:
        return self.piece is not None

    def is_empty(self) -> bool:
        return self.piece is None

    def get_piece(self) -> Piece:
        return self.piece

    def get_row(self) -> int:
        return self.row

    def get_col(self) -> int:
        return self.col

    def is_at(self, r: int, c: int) -> bool:
        return self.row == r and self.col == c

    @staticmethod
    def is_in_bounds(r, c) -> bool:
        return 0 <= r < 8 and 0 <= c < 8
