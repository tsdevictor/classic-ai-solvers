import engine.piece_tile

# for a move to be valid:
#    target must not be None
#    piece at target must not be different color than moving piece
#

class Move:
    def __init__(self, board,
                 piece: engine.piece_tile.piece_tile.Piece,
                 target: engine.piece_tile.piece_tile.Tile):
        self.piece = piece
        self.current = None if self.piece is None else piece.tile
        self.target = target
        self.board = board
        self.is_first_move = False if self.piece is None else piece.is_first_move

    def __str__(self):
        letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        return str(self.piece) + ' from ' + letters[self.current.col] + str(8-self.current.row)\
            + ' to ' + letters[self.target.col] + str(8-self.target.row)

    def __eq__(self, other):
        if not isinstance(other, Move):
            return False
        return self.piece == other.piece and self.current == other.current and self.target == other.target

    @staticmethod
    def is_attack() -> bool:
        return False

    @staticmethod
    def is_castling_move() -> bool:
        return False

    @staticmethod
    def get_attacked_piece():
        return None

    def execute(self):  # -> engine.board.board.Board:
        import engine.board.board
        builder = engine.board.board.Board.Builder(self.board.current_player.color())
        for piece in self.board.current_player.get_active_pieces():
            if not (self.piece == piece):
                builder.set_piece(piece)

        for piece in self.board.current_player.get_opponent().get_active_pieces():
            builder.set_piece(piece)

        builder.set_piece(self.piece.move_piece(self))
        builder.switch_move_maker()

        return builder.build()


class AttackMove(Move):
    def __init__(self, board, piece, target, attacked):
        super().__init__(board, piece, target)
        self.attacked_piece = attacked

    def __str__(self):
        return super().__str__()

    def __eq__(self, other):
        if not isinstance(other, AttackMove):
            return False
        return super() == other and self.attacked_piece == other.attacked_piece

    @staticmethod
    def is_attack() -> bool:
        return True

    def get_attacked_piece(self) -> engine.piece_tile.piece_tile.Piece:
        return self.attacked_piece


class MajorMove(Move):
    def __init__(self, board, piece, target):
        super().__init__(board, piece, target)

    def __str__(self):
        return str(self.piece) + str(self.target)

    def __eq__(self, other):
        return isinstance(other, MajorMove) and super() == other


class MajorAttackMove(AttackMove):
    def __init__(self, board, piece, target, attacked):
        super().__init__(board, piece, target, attacked)

    def __str__(self):
        return str(self.piece) + str(self.target)

    def __eq__(self, other):
        return isinstance(other, MajorAttackMove) and super() == other


class PawnMove(Move):
    def __init__(self, board, piece, target):
        super().__init__(board, piece, target)

    def __str__(self):
        return str(self.target)

    def __eq__(self, other):
        return isinstance(other, PawnMove) and super == other

class PawnAttackMove(AttackMove):
    def __init__(self, board, piece, target, attacked):
        super().__init__(board, piece, target, attacked)

    def __str__(self):
        return str(self.piece.tile)[0] + 'x' + str(self.target)

    def __eq__(self, other):
        return isinstance(other, PawnAttackMove) and super() == other

class PawnEnPassantAttackMove(PawnAttackMove):
    def __init__(self, board, piece, target, attacked):
        super().__init__(board, piece, target, attacked)

    def __str__(self):
        return super().__str__()

    def __eq__(self, other):
        return isinstance(other, PawnAttackMove) and super() == other

    def execute(self):
        import engine.board.board
        builder = engine.board.board.Board.Builder(self.board.current_player.color())
        for piece in self.board.current_player.get_active_pieces():
            if not (self.piece == piece):
                builder.set_piece(piece)

        for piece in self.board.current_player.get_opponent().get_active_pieces():
            if not (piece == self.attacked_piece):
                builder.set_piece(piece)

        builder.set_piece(self.piece.move_piece(self))
        builder.switch_move_maker()

        return builder.build()

class PawnPromotion(Move):
    def __init__(self, decorated_move):
        super().__init__(decorated_move.board, decorated_move.piece, decorated_move.target)
        self.decorated_move = decorated_move
        self.promoted_pawn = decorated_move.piece

    def __str__(self):
        return str(self.decorated_move.target) + '=Q'

    def __eq__(self, other):
        return isinstance(other, PawnPromotion) and super() == other

    def is_attack(self) -> bool:
        return self.decorated_move.is_attack()

    def get_attacked_piece(self):
        return self.decorated_move.get_attacked_piece()

    def execute(self):
        import engine.board.board

        pawn_moved_board = self.decorated_move.execute()
        builder = engine.board.board.Board.Builder(self.board.current_player.color())
        for piece in pawn_moved_board.current_player.get_active_pieces():
            if not (self.promoted_pawn == piece):
                builder.set_piece(piece)

        for piece in pawn_moved_board.current_player.get_opponent().get_active_pieces():
            builder.set_piece(piece)

        builder.set_piece(self.promoted_pawn.get_promotion_piece().move_piece(self))
        builder.switch_move_maker()

        return builder.build()

class PawnJump(Move):
    def __init__(self, board, piece, target):
        super().__init__(board, piece, target)

    def __str__(self):
        return str(self.target)

    def execute(self):  # -> engine.board.board.Board:
        import engine.board.board
        builder = engine.board.board.Board.Builder(self.board.current_player.color())
        for piece in self.board.current_player.get_active_pieces():
            if not (self.piece == piece):
                builder.set_piece(piece)

        for piece in self.board.current_player.get_opponent().get_active_pieces():
            builder.set_piece(piece)

        moved_pawn = self.piece.move_piece(self)
        builder.set_piece(moved_pawn)
        builder.en_passant_pawn = moved_pawn
        builder.switch_move_maker()

        return builder.build()


class CastleMove(Move):
    def __init__(self, board,
                 king: engine.piece_tile.piece_tile.Piece,
                 target: engine.piece_tile.piece_tile.Tile,
                 rook,  # rook object
                 rook_start: engine.piece_tile.piece_tile.Tile,
                 rook_target: engine.piece_tile.piece_tile.Tile):
        super().__init__(board, king, target)
        self.king = king
        self.rook = rook
        self.rook_start = rook_start
        self.rook_target = rook_target

    def __str__(self):
        return super().__str__()

    def __eq__(self, other):
        if not isinstance(other, CastleMove):
            return False
        return super() == other and self.rook == other.rook

    @staticmethod
    def is_castling_move() -> bool:
        return True

    def execute(self):  # -> engine.board.board.Board:
        import engine.board.board
        builder = engine.board.board.Board.Builder(self.board.current_player.color())
        for piece in self.board.current_player.get_active_pieces():
            if not (self.king == piece) and not (self.rook == piece):
                builder.set_piece(piece)

        for piece in self.board.current_player.get_opponent().get_active_pieces():
            builder.set_piece(piece)

        builder.set_piece(self.king.move_piece(self))
        builder.set_piece(self.rook.move_piece(Move(self.board, self.rook, self.rook_target)))
        builder.switch_move_maker()

        board = builder.build()
        board.current_player.get_opponent().is_castled = True

        return board

class KingSideCastleMove(CastleMove):
    def __init__(self, board, king, target, rook, rook_start, rook_target):
        super().__init__(board, king, target, rook, rook_start, rook_target)

    def __str__(self):
        return 'O-O'

    def __eq__(self, other):
        return isinstance(other, KingSideCastleMove) and super() == other

class QueenSideCastleMove(CastleMove):
    def __init__(self, board, king, target, rook, rook_start, rook_target):
        super().__init__(board, king, target, rook, rook_start, rook_target)

    def __str__(self):
        return 'O-O-O'

    def __eq__(self, other):
        return isinstance(other, QueenSideCastleMove) and super() == other


class NullMove(Move):
    def __init__(self):
        # noinspection PyTypeChecker
        super().__init__(None, None, None)

    def __str__(self):
        return 'NULL MOVE'

    def execute(self):  # -> engine.board.board.Board:
        raise RuntimeError("Cannot execute a null move!")


class MoveFactory:
    def __init__(self):
        raise RuntimeError("Cannot be instantiated!")

    @staticmethod
    def create_move(board,
                    current_tile: engine.piece_tile.piece_tile.Tile,
                    target_tile: engine.piece_tile.piece_tile.Tile) -> Move:
        legal_moves = board.current_player.legal_moves
        for move in legal_moves:
            if move.current == current_tile and move.target == target_tile:
                return move
        return NullMove()


class MoveStatus:
    ILLEGAL_MOVE = 0
    LEAVES_IN_CHECK = 0
    DONE = 1

    def __init__(self, status: int):
        self.status = status

    def is_done(self) -> bool:
        return self.status == 1


class MoveTransition:
    def __init__(self, transition_board,
                 move: Move,
                 move_status: int):
        self.transition_board = transition_board
        self.move = move
        self.move_status = move_status

    def print(self):
        print(self.transition_board)
        print(self.move)
        print(self.move_status)

    def get_move_status(self) -> MoveStatus:
        return MoveStatus(self.move_status)

    def get_transition_board(self):
        return self.transition_board
