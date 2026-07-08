class FenUtilities:
    def __init__(self):
        raise RuntimeError("Cannot be instantiated!")

    def create_game_from_fen(self, fen_string: str):
        return None

    def create_fen_from_game(self, board) -> str:
        return self.calculate_board_text(board) + ' ' + \
               self.calculate_current_player_text(board) + ' ' + \
               self.calculate_castle_text(board) + ' ' + \
               self.calculate_en_passant_square(board) + ' ' + \
               '0 1'

    @staticmethod
    def calculate_board_text(board) -> str:
        result = ''
        for r in range(8):
            for c in range(8):
                if board[r][c].is_occupied():
                    result += str(board[r][c].piece)
                    if board[r][c].piece.is_black:
                        result = result.lower()
                else:
                    result += '-'
            result += '/'
        result = result[:-1]  # remove extra '/'

        result = result.replace('--------', '8')
        result = result.replace('-------', '7')
        result = result.replace('------', '6')
        result = result.replace('-----', '5')
        result = result.replace('----', '4')
        result = result.replace('---', '3')
        result = result.replace('--', '2')
        result = result.replace('-', '1')

        return result

    @staticmethod
    def calculate_current_player_text(board) -> str:
        return str(board.current_player)[0].lower()

    @staticmethod
    def calculate_castle_text(board) -> str:
        result = ''
        if board.white_player.can_king_side_castle():
            result += 'K'
        if board.white_player.can_queen_side_castle():
            result += 'Q'
        if board.black_player.can_king_side_castle():
            result += 'k'
        if board.black_player.can_queen_side_castle():
            result += 'q'

        return '-' if len(result) == 0 else result

    @staticmethod
    def calculate_en_passant_square(board):
        en_passant_pawn = board.en_passant_pawn
        if en_passant_pawn is not None:
            if en_passant_pawn.is_white:
                return str(board[en_passant_pawn.tile.row+1][en_passant_pawn.tile.col])
            else:
                return str(board[en_passant_pawn.tile.row-1][en_passant_pawn.tile.col])
        return '-'
