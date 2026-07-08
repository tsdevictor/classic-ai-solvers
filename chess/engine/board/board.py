import engine.piece_tile as pt
import engine

class Board:
    WHITE = 1
    BLACK = -1

    class Builder:
        def __init__(self, next_move_maker):
            self.board_config = []              # matrix of pieces
            for r in range(8):
                self.board_config.append([])
                for c in range(8):
                    self.board_config[r].append(None)
            self.next_move_maker = next_move_maker  # whose turn is it?
            self.en_passant_pawn = None

        def set_piece(self, piece):
            self.board_config[piece.get_row()][piece.get_col()] = piece
            return self

        @staticmethod
        def instantiate_piece(piece_type, tile, is_white, is_first_move=True):
            if piece_type == pt.piece_tile.Piece.PAWN:
                return pt.pawn.Pawn(tile, is_white, is_first_move)
            elif piece_type == pt.piece_tile.Piece.ROOK:
                return pt.rook.Rook(tile, is_white, is_first_move)
            elif piece_type == pt.piece_tile.Piece.KNIGHT:
                return pt.knight.Knight(tile, is_white, is_first_move)
            elif piece_type == pt.piece_tile.Piece.BISHOP:
                return pt.bishop.Bishop(tile, is_white, is_first_move)
            elif piece_type == pt.piece_tile.Piece.KING:
                return pt.king.King(tile, is_white, is_first_move)
            elif piece_type == pt.piece_tile.Piece.QUEEN:
                return pt.queen.Queen(tile, is_white, is_first_move)

        def switch_move_maker(self):
            self.next_move_maker *= -1

        def build(self):  # -> Board:
            return Board(self)

    def __init__(self, builder: Builder):
        self.game_board = Board.create_game_board(builder)  # matrix of tiles

        self.en_passant_pawn = builder.en_passant_pawn

        self.white_pieces = self.get_active_pieces(self.game_board, True)
        self.black_pieces = self.get_active_pieces(self.game_board, False)

        self.white_legal_moves = self.get_legal_moves(self.white_pieces)
        self.black_legal_moves = self.get_legal_moves(self.black_pieces)

        self.white_player = engine.players.white_player.WhitePlayer(self, self.white_legal_moves, self.black_legal_moves)
        self.black_player = engine.players.black_player.BlackPlayer(self, self.black_legal_moves, self.white_legal_moves)
        if builder.next_move_maker == Board.WHITE:
            self.current_player = self.white_player
        else:
            self.current_player = self.black_player

    def __str__(self):
        string = ''
        for row in self.game_board:
            for tile in row:
                if tile.is_occupied():
                    string += str(tile.piece) + ' '
                else:
                    string += '- '
            string += '\n'
        return string

    def __getitem__(self, r: int) -> [pt.piece_tile.Tile]:
        if not 0 <= r < 8:
            raise ValueError("Accessing out-of-bounds tile")
        return self.game_board[r]

    def get_tile(self, coordinate: str):
        if coordinate[0] == 'a':
            return self.__getitem__(8-int(coordinate[1]))[0]
        if coordinate[0] == 'b':
            return self.__getitem__(8-int(coordinate[1]))[1]
        if coordinate[0] == 'c':
            return self.__getitem__(8-int(coordinate[1]))[2]
        if coordinate[0] == 'd':
            return self.__getitem__(8-int(coordinate[1]))[3]
        if coordinate[0] == 'e':
            return self.__getitem__(8-int(coordinate[1]))[4]
        if coordinate[0] == 'f':
            return self.__getitem__(8-int(coordinate[1]))[5]
        if coordinate[0] == 'g':
            return self.__getitem__(8-int(coordinate[1]))[6]
        if coordinate[0] == 'h':
            return self.__getitem__(8-int(coordinate[1]))[7]

    def get_en_passant_pawn(self):
        return self.en_passant_pawn

    def get_legal_moves(self, pieces):  # -> [Move]:
        moves = []
        for piece in pieces:
            moves += piece.calculate_moves(self)
            # for move in piece.calculate_moves(self):  # to optimize alpha-beta pruning
            #   if move.is_attack():
            #       moves.insert(0, move)
            #   else:
            #       moves.append(move)
        return moves

    def get_all_legal_moves(self):  # -> [Move]:
        return self.white_player.legal_moves + self.black_player.legal_moves

    @staticmethod
    def create_game_board(builder: Builder) -> [[pt.piece_tile.Tile]]:
        tiles = []
        for r in range(8):
            tiles.append([])
            for c in range(8):
                tiles[r].append(pt.piece_tile.Tile(r, c, builder.board_config[r][c]))
        return tiles

    @staticmethod
    def get_active_pieces(board: [[]], is_white) -> [pt.piece_tile.Piece]:
        pieces = []
        for r in range(8):
            for c in range(8):
                if board[r][c].is_occupied():
                    if board[r][c].piece.is_white == is_white:
                        if board[r][c].piece.is_queen():
                            pieces.insert(0, board[r][c].piece)
                        else:
                            pieces.append(board[r][c].piece)
        return pieces

    @staticmethod
    def create_standard_board():  # -> Board:
        builder = Board.Builder(Board.WHITE)

        builder.set_piece(builder.instantiate_piece(pt.piece_tile.Piece.ROOK, pt.piece_tile.Tile(0, 0), False))
        builder.set_piece(builder.instantiate_piece(pt.piece_tile.Piece.KNIGHT, pt.piece_tile.Tile(0, 1), False))
        builder.set_piece(builder.instantiate_piece(pt.piece_tile.Piece.BISHOP, pt.piece_tile.Tile(0, 2), False))
        builder.set_piece(builder.instantiate_piece(pt.piece_tile.Piece.QUEEN, pt.piece_tile.Tile(0, 3), False))
        builder.set_piece(builder.instantiate_piece(pt.piece_tile.Piece.KING, pt.piece_tile.Tile(0, 4), False))
        builder.set_piece(builder.instantiate_piece(pt.piece_tile.Piece.BISHOP, pt.piece_tile.Tile(0, 5), False))
        builder.set_piece(builder.instantiate_piece(pt.piece_tile.Piece.KNIGHT, pt.piece_tile.Tile(0, 6), False))
        builder.set_piece(builder.instantiate_piece(pt.piece_tile.Piece.ROOK, pt.piece_tile.Tile(0, 7), False))
        builder.set_piece(builder.instantiate_piece(pt.piece_tile.Piece.PAWN, pt.piece_tile.Tile(1, 0), False))
        builder.set_piece(builder.instantiate_piece(pt.piece_tile.Piece.PAWN, pt.piece_tile.Tile(1, 1), False))
        builder.set_piece(builder.instantiate_piece(pt.piece_tile.Piece.PAWN, pt.piece_tile.Tile(1, 2), False))
        builder.set_piece(builder.instantiate_piece(pt.piece_tile.Piece.PAWN, pt.piece_tile.Tile(1, 3), False))
        builder.set_piece(builder.instantiate_piece(pt.piece_tile.Piece.PAWN, pt.piece_tile.Tile(1, 4), False))
        builder.set_piece(builder.instantiate_piece(pt.piece_tile.Piece.PAWN, pt.piece_tile.Tile(1, 5), False))
        builder.set_piece(builder.instantiate_piece(pt.piece_tile.Piece.PAWN, pt.piece_tile.Tile(1, 6), False))
        builder.set_piece(builder.instantiate_piece(pt.piece_tile.Piece.PAWN, pt.piece_tile.Tile(1, 7), False))

        builder.set_piece(builder.instantiate_piece(pt.piece_tile.Piece.PAWN, pt.piece_tile.Tile(6, 0), True))
        builder.set_piece(builder.instantiate_piece(pt.piece_tile.Piece.PAWN, pt.piece_tile.Tile(6, 1), True))
        builder.set_piece(builder.instantiate_piece(pt.piece_tile.Piece.PAWN, pt.piece_tile.Tile(6, 2), True))
        builder.set_piece(builder.instantiate_piece(pt.piece_tile.Piece.PAWN, pt.piece_tile.Tile(6, 3), True))
        builder.set_piece(builder.instantiate_piece(pt.piece_tile.Piece.PAWN, pt.piece_tile.Tile(6, 4), True))
        builder.set_piece(builder.instantiate_piece(pt.piece_tile.Piece.PAWN, pt.piece_tile.Tile(6, 5), True))
        builder.set_piece(builder.instantiate_piece(pt.piece_tile.Piece.PAWN, pt.piece_tile.Tile(6, 6), True))
        builder.set_piece(builder.instantiate_piece(pt.piece_tile.Piece.PAWN, pt.piece_tile.Tile(6, 7), True))
        builder.set_piece(builder.instantiate_piece(pt.piece_tile.Piece.ROOK, pt.piece_tile.Tile(7, 0), True))
        builder.set_piece(builder.instantiate_piece(pt.piece_tile.Piece.KNIGHT, pt.piece_tile.Tile(7, 1), True))
        builder.set_piece(builder.instantiate_piece(pt.piece_tile.Piece.BISHOP, pt.piece_tile.Tile(7, 2), True))
        builder.set_piece(builder.instantiate_piece(pt.piece_tile.Piece.QUEEN, pt.piece_tile.Tile(7, 3), True))
        builder.set_piece(builder.instantiate_piece(pt.piece_tile.Piece.KING, pt.piece_tile.Tile(7, 4), True))
        builder.set_piece(builder.instantiate_piece(pt.piece_tile.Piece.BISHOP, pt.piece_tile.Tile(7, 5), True))
        builder.set_piece(builder.instantiate_piece(pt.piece_tile.Piece.KNIGHT, pt.piece_tile.Tile(7, 6), True))
        builder.set_piece(builder.instantiate_piece(pt.piece_tile.Piece.ROOK, pt.piece_tile.Tile(7, 7), True))

        return builder.build()
