class BoardEvaluator:
    CHECK_BONUS = 50
    CHECKMATE_BONUS = 100000
    DEPTH_BONUS = 100
    CASTLE_BONUS = 60

    @staticmethod
    def evaluate(board, depth: int) -> int:
        return BoardEvaluator.score_player(board, board.white_player, depth) - \
               BoardEvaluator.score_player(board, board.black_player, depth)

    @staticmethod
    def score_player(board, player, depth) -> int:
        return BoardEvaluator.piece_value(player) + \
               BoardEvaluator.checkmate(player, depth) + \
               BoardEvaluator.mobility(player) + \
               BoardEvaluator.check(player) + \
               BoardEvaluator.castled(player) + \
               BoardEvaluator.positioning(player, board)

    @staticmethod
    def piece_value(player) -> int:
        piece_value_score = 0
        for piece in player.get_active_pieces():
            piece_value_score += piece.get_piece_value()
        return piece_value_score

    @staticmethod
    def mobility(player) -> int:
        return len(player.legal_moves)

    @staticmethod
    def check(player) -> int:
        return BoardEvaluator.CHECK_BONUS if player.get_opponent().is_in_check() else 0

    @staticmethod
    def checkmate(player, depth: int) -> int:
        def depth_bonus() -> int:
            return 1 if depth == 0 else (BoardEvaluator.DEPTH_BONUS * depth)

        return (BoardEvaluator.CHECKMATE_BONUS * depth_bonus()) \
            if player.get_opponent().is_in_checkmate() else 0

    @staticmethod
    def castled(player) -> int:
        return BoardEvaluator.CASTLE_BONUS if player.is_castled else 0

    @staticmethod
    def positioning(player, board) -> int:
        def pawn_position_bonus(pawn) -> int:
            bonus = [0, 0, 0, 0, 0, 0, 0, 0,
                     50, 50, 50, 50, 50, 50, 50, 50,
                     10, 10, 20, 30, 30, 20, 10, 10,
                     5, 5, 10, 25, 25, 10, 5, 5,
                     0, 0, 0, 20, 20, 0, 0, 0,
                     5, -5, -10, 0, 0, -10, -5, 5,
                     5, 10, 10, -20, -20, 10, 10, 5,
                     0, 0, 0, 0, 0, 0, 0, 0]
            if pawn.is_black:
                bonus.reverse()
            return bonus[pawn.tile.row * 8 + pawn.tile.col]

        def knight_position_bonus(knight):
            bonus = [-50, -40, -30, -30, -30, -30, -40, -50,
                     -40, -20, 0, 0, 0, 0, -20, -40,
                     -30, 0, 10, 15, 15, 10, 0, -30,
                     -30, 5, 15, 20, 20, 15, 5, -30,
                     -30, 0, 15, 20, 20, 15, 0, -30,
                     -30, 5, 10, 15, 15, 10, 5, -30,
                     -40, -20, 0, 5, 5, 0, -20, -40,
                     -50, -40, -30, -30, -30, -30, -40, -50]
            if knight.is_black:
                bonus.reverse()
            return bonus[knight.tile.row * 8 + knight.tile.col]

        def bishop_position_bonus(bishop):
            bonus = [-20, -10, -10, -10, -10, -10, -10, -20,
                     -10, 0, 0, 0, 0, 0, 0, -10,
                     -10, 0, 5, 10, 10, 5, 0, -10,
                     -10, 5, 5, 10, 10, 5, 5, -10,
                     -10, 0, 10, 10, 10, 10, 0, -10,
                     -10, 10, 10, 10, 10, 10, 10, -10,
                     -10, 5, 0, 0, 0, 0, 5, -10,
                     -20, -10, -10, -10, -10, -10, -10, -20]
            if bishop.is_black:
                bonus.reverse()
            return bonus[bishop.tile.row * 8 + bishop.tile.col]

        def rook_position_bonus(rook):
            bonus = [0, 0, 0, 0, 0, 0, 0, 0,
                     5, 10, 10, 10, 10, 10, 10, 5,
                     -5, 0, 0, 0, 0, 0, 0, -5,
                     -5, 0, 0, 0, 0, 0, 0, -5,
                     -5, 0, 0, 0, 0, 0, 0, -5,
                     -5, 0, 0, 0, 0, 0, 0, -5,
                     -5, 0, 0, 0, 0, 0, 0, -5,
                     0, 0, 0, 5, 5, 0, 0, 0]
            if rook.is_black:
                bonus.reverse()
            return bonus[rook.tile.row * 8 + rook.tile.col]

        def queen_position_bonus(queen):
            bonus = [-20, -10, -10, -5, -5, -10, -10, -20,
                     -10, 0, 0, 0, 0, 0, 0, -10,
                     -10, 0, 5, 5, 5, 5, 0, -10,
                     -5, 0, 5, 5, 5, 5, 0, -5,
                     0, 0, 5, 5, 5, 5, 0, -5,
                     -10, 5, 5, 5, 5, 5, 0, -10,
                     -10, 0, 5, 0, 0, 0, 0, -10,
                     -20, -10, -10, -5, -5, -10, -10, -20]
            if queen.is_black:
                bonus.reverse()
            return bonus[queen.tile.row * 8 + queen.tile.col]

        def king_position_bonus(king):
            bonus = [-30, -40, -40, -50, -50, -40, -40, -30,
                     -30, -40, -40, -50, -50, -40, -40, -30,
                     -30, -40, -40, -50, -50, -40, -40, -30,
                     -30, -40, -40, -50, -50, -40, -40, -30,
                     -20, -30, -30, -40, -40, -30, -30, -20,
                     -10, -20, -20, -20, -20, -20, -20, -10,
                     20, 20, 0, 0, 0, 0, 20, 20,
                     20, 30, 10, 0, 0, 10, 30, 20]
            # endgame board
            no_queens = True
            for pieces in (board.white_pieces + board.black_pieces):
                if pieces.is_queen():
                    no_queens = False
                    break
            if no_queens or len(board.white_pieces + board.black_pieces) < 6:
                bonus = [-50, -40, -30, -20, -20, -30, -40, -50,
                         -30, -20, -10, 0, 0, -10, -20, -30,
                         -30, -10, 20, 30, 30, 20, -10, -30,
                         -30, -10, 30, 40, 40, 30, -10, -30,
                         -30, -10, 30, 40, 40, 30, -10, -30,
                         -30, -10, 20, 30, 30, 20, -10, -30,
                         -30, -30, 0, 0, 0, 0, -30, -30,
                         -50, -30, -30, -30, -30, -30, -30, -50]
            if king.is_black:
                bonus.reverse()
            return bonus[king.tile.row * 8 + king.tile.col]

        piece_value_score = 0
        for piece in player.get_active_pieces():
            if piece.is_pawn():
                piece_value_score += pawn_position_bonus(piece)
            elif piece.is_knight():
                piece_value_score += knight_position_bonus(piece)
            elif piece.is_bishop():
                piece_value_score += bishop_position_bonus(piece)
            elif piece.is_rook():
                piece_value_score += rook_position_bonus(piece)
            elif piece.is_queen():
                piece_value_score += queen_position_bonus(piece)
            elif piece.is_king():
                piece_value_score += king_position_bonus(piece)

        return piece_value_score
