from tile import Tile
import pygame


class Piece:
    def __init__(self, t, w):
        self.my_type = t
        self.am_white = w
        self.first_move = True
        self.adv_two = False

    def move(self):
        self.first_move = False

    def set_adv_two(self, a):
        self.adv_two = a

    def get_adv_two(self):
        return self.adv_two

    def is_white(self):
        return self.am_white

    def is_first_move(self):
        return self.first_move

    def get_type(self):
        return self.my_type

    def is_empty(self):
        return self.my_type == 0

    def is_pawn(self):
        return self.my_type == 1

    def is_knight(self):
        return self.my_type == 2

    def is_bishop(self):
        return self.my_type == 3

    def is_rook(self):
        return self.my_type == 4

    def is_queen(self):
        return self.my_type == 5

    def is_king(self):
        return self.my_type == 6

    def get_image(self):
        if self.is_white():
            color = "White"
        else:
            color = "Black"
        if self.my_type == 1:
            return pygame.image.load("Images/" + color + "Pawn.png")
        elif self.my_type == 2:
            return pygame.image.load("Images/" + color + "Knight.png")
        elif self.my_type == 3:
            return pygame.image.load("Images/" + color + "Bishop.png")
        elif self.my_type == 4:
            return pygame.image.load("Images/" + color + "Rook.png")
        elif self.my_type == 5:
            return pygame.image.load("Images/" + color + "Queen.png")
        elif self.my_type == 6:
            return pygame.image.load("Images/" + color + "King.png")

    def pawn_possible_moves(self, piece_layout, row, col):
        possible_moves = []

        if self.is_white():
            one = -1
            two = -2
            pawn_first_move = row == 6
        else:
            one = 1
            two = 2
            pawn_first_move = row == 1

        if pawn_first_move and piece_layout[row + two][col].is_empty() and piece_layout[row + one][col].is_empty():
            possible_moves.append(Tile(row + two, col))
        if row != 0 and row != 7:
            if piece_layout[row + one][col].is_empty():
                possible_moves.append(Tile(row + one, col))
            if col != 0:
                diagonal_piece = piece_layout[row + one][col - 1]
                if diagonal_piece.is_white() != self.is_white() and not diagonal_piece.is_empty():
                    possible_moves.append(Tile(row + one, col - 1))
            if col != 7:
                diagonal_piece = piece_layout[row + one][col + 1]
                if diagonal_piece.is_white() != self.is_white() and not diagonal_piece.is_empty():
                    possible_moves.append(Tile(row + one, col + 1))

        # En passant
        if (self.is_white() and row == 3) or (not self.is_white() and row == 4):
            for k in range(-1, 2, 2):  # for(int k = -1; k <= 1; k += 2)
                if 0 <= col + k <= 7:
                    adj = piece_layout[row][col + k]
                    if piece_layout[row + one][col + k].is_empty() and adj.is_pawn() and adj.get_adv_two() and adj.is_white() != self.is_white():
                        possible_moves.append(Tile(row + one, col + k))

        return possible_moves

    @staticmethod
    def knight_possible_moves(row, col):
        possible_moves = [Tile(row + 2, col + 1),
                          Tile(row + 2, col - 1),
                          Tile(row - 2, col + 1),
                          Tile(row - 2, col - 1),
                          Tile(row + 1, col + 2),
                          Tile(row + 1, col - 2),
                          Tile(row - 1, col + 2),
                          Tile(row - 1, col - 2)]

        return possible_moves

    @staticmethod
    def bishop_possible_moves(piece_layout, row, col):
        possible_moves = []

        # diagonal down right
        r = row + 1
        c = col + 1
        while r < 8 and c < 8:
            possible_moves.append(Tile(r, c))
            if not piece_layout[r][c].is_empty():
                break
            r += 1
            c += 1

        # diagonal up left
        r = row - 1
        c = col - 1
        while r >= 0 and c >= 0:
            possible_moves.append(Tile(r, c))
            if not piece_layout[r][c].is_empty():
                break
            r -= 1
            c -= 1

        # diagonal down left
        r = row + 1
        c = col - 1
        while r < 8 and c >= 0:
            possible_moves.append(Tile(r, c))
            if not piece_layout[r][c].is_empty():
                break
            r += 1
            c -= 1

        # diagonal up right
        r = row - 1
        c = col + 1
        while r >= 0 and c < 8:
            possible_moves.append(Tile(r, c))
            if not piece_layout[r][c].is_empty():
                break
            r -= 1
            c += 1

        return possible_moves

    @staticmethod
    def rook_possible_moves(piece_layout, row, col):
        possible_moves = []

        # column below
        for r in range(row + 1, 8):
            possible_moves.append(Tile(r, col))
            if not piece_layout[r][col].is_empty():
                break

        # column above
        for r in range(row - 1, -1, -1):
            possible_moves.append(Tile(r, col))
            if not piece_layout[r][col].is_empty():
                break

        # row right
        for c in range(col + 1, 8):
            possible_moves.append(Tile(row, c))
            if not piece_layout[row][c].is_empty():
                break

        # row left
        for c in range(col - 1, -1, -1):
            possible_moves.append(Tile(row, c))
            if not piece_layout[row][c].is_empty():
                break

        return possible_moves

    def queen_possible_moves(self, piece_layout, row, col):
        return self.bishop_possible_moves(piece_layout, row, col) + self.rook_possible_moves(piece_layout, row, col)

    @staticmethod
    def king_possible_moves(row, col):
        possible_moves = [Tile(row + 1, col + 1),
                          Tile(row + 1, col - 1),
                          Tile(row - 1, col + 1),
                          Tile(row - 1, col - 1),
                          Tile(row + 1, col),
                          Tile(row - 1, col),
                          Tile(row, col + 1),
                          Tile(row, col - 1)]

        return possible_moves

    def castle(self, possible_moves, piece_layout, king_pos):
        pr = king_pos.get_row()
        pc = king_pos.get_col()
        king_color = piece_layout[pr][pc].is_white()

        one = 1
        if piece_layout[pr][pc].is_white():
            one = -1

        if not piece_layout[pr][pc].in_check(piece_layout, Tile(pr, pc), king_color):
            if piece_layout[pr][pc].is_king() and piece_layout[pr][pc].is_first_move():
                if piece_layout[pr][0].is_rook() and piece_layout[pr][0].is_first_move():
                    blocking = False
                    for c in range(1, 4):
                        if self.in_check(piece_layout, Tile(pr, c), king_color) or not piece_layout[pr][c].is_empty():
                            blocking = True
                    for c in range(1, 5):
                        if piece_layout[pr+one][c].is_pawn() and piece_layout[pr+one][c].is_white() != piece_layout[pr][pc].is_white():
                            blocking = True
                    if not blocking:
                        possible_moves.append(Tile(pr, 2))

                if piece_layout[pr][7].is_rook() and piece_layout[pr][7].is_first_move():
                    blocking = False
                    for c in range(5, 7):
                        if self.in_check(piece_layout, Tile(pr, c), king_color) or not piece_layout[pr][c].is_empty():
                            blocking = True
                    for c in range(4, 8):
                        if piece_layout[pr+one][c].is_pawn() and piece_layout[pr+one][c].is_white() != piece_layout[pr][pc].is_white():
                            blocking = True
                    if not blocking:
                        possible_moves.append(Tile(pr, 6))

    def possible_moves(self, piece_layout, piece_pos):
        row = piece_pos.get_row()
        col = piece_pos.get_col()
        moving_piece = piece_layout[row][col]

        if moving_piece.is_empty():
            return []
        elif moving_piece.is_pawn():
            possible_moves = self.pawn_possible_moves(piece_layout, row, col)
        elif moving_piece.is_knight():
            possible_moves = self.knight_possible_moves(row, col)
        elif moving_piece.is_bishop():
            possible_moves = self.bishop_possible_moves(piece_layout, row, col)
        elif moving_piece.is_rook():
            possible_moves = self.rook_possible_moves(piece_layout, row, col)
        elif moving_piece.is_queen():
            possible_moves = self.queen_possible_moves(piece_layout, row, col)
        else:  # moving_piece.is_king():
            possible_moves = self.king_possible_moves(row, col)

        k = 0
        while k < len(possible_moves):
            r = possible_moves[k].get_row()
            c = possible_moves[k].get_col()
            if r > 7 or r < 0 or c > 7 or c < 0 or (
                    not piece_layout[r][c].is_empty() and piece_layout[r][c].is_white() == self.is_white()):
                possible_moves.remove(possible_moves[k])
                k -= 1
            k += 1

        return possible_moves

    @staticmethod
    def in_check(piece_layout, king_pos, king_color):
        row = king_pos.get_row()
        col = king_pos.get_col()
        for r in range(8):
            for c in range(8):
                current_piece = piece_layout[r][c]
                if not current_piece.is_empty() and current_piece.is_white() != king_color:
                    possible_moves = current_piece.possible_moves(piece_layout, Tile(r, c))
                    for k in range(len(possible_moves)):
                        if possible_moves[k].get_row() == row and possible_moves[k].get_col() == col:
                            return True
        return False

    def remove_check_moves(self, possible_moves, piece_layout, piece_pos, king_pos):
        pr = piece_pos.get_row()
        pc = piece_pos.get_col()
        king_color = piece_layout[king_pos.get_row()][king_pos.get_col()].is_white()

        # to make sure king can't move to block path of move that puts it in check
        piece_is_king = piece_layout[pr][pc].is_king()

        if piece_is_king:
            self.castle(possible_moves, piece_layout, king_pos)

        k = 0
        while k < len(possible_moves):
            tr = possible_moves[k].get_row()
            tc = possible_moves[k].get_col()

            can_en_passant = piece_layout[pr][pc].is_pawn() and tc != pc and piece_layout[tr][tc].is_empty()
            en_passant_piece = None
            if can_en_passant:
                en_passant_piece = piece_layout[pr][tc]
                piece_layout[pr][tc] = Piece(0, True)

            piece_at_target = piece_layout[tr][tc]
            piece_layout[tr][tc] = piece_layout[pr][pc]
            piece_layout[pr][pc] = Piece(0, True)

            if piece_is_king:
                king_pos = Tile(tr, tc)

            if self.in_check(piece_layout, king_pos, king_color):
                possible_moves.remove(possible_moves[k])
                k -= 1

            piece_layout[pr][pc] = piece_layout[tr][tc]
            piece_layout[tr][tc] = piece_at_target
            if can_en_passant:
                piece_layout[pr][tc] = en_passant_piece

            k += 1

    @staticmethod
    def get_moves(piece_layout, tiles, s_row, s_col, white_turn):
        possible_moves = piece_layout[s_row][s_col].possible_moves(piece_layout, Tile(s_row, s_col))
        for r in range(8):
            for c in range(8):
                tiles[r][c].set_active(False)
                piece_layout[r][c].set_adv_two(False)
                if piece_layout[r][c].is_king() and piece_layout[r][c].is_white() == white_turn:
                    piece_layout[r][c].remove_check_moves(possible_moves, piece_layout, Tile(s_row, s_col), Tile(r, c))
        for k in range(len(possible_moves)):
            possible_moves[k] = Move(s_row, s_col, possible_moves[k].get_row(), possible_moves[k].get_col())
        return possible_moves

    def checkmate(self, piece_layout, king_pos, white_turn):
        no_moves = True
        for r in range(8):
            for c in range(8):
                if piece_layout[r][c].is_white() == white_turn and not piece_layout[r][c].is_empty():
                    possible_moves = piece_layout[r][c].possible_moves(piece_layout, Tile(r, c))
                    piece_layout[r][c].remove_check_moves(possible_moves, piece_layout, Tile(r, c), king_pos)
                    if len(possible_moves) > len([]):
                        no_moves = False
        if self.in_check(piece_layout, king_pos, white_turn) and no_moves:
            if white_turn:
                return "Black wins!", 1
            return "White wins!", 2
        if no_moves:
            return "Draw!", 3
        return "Chess", 0

    def get_value(self):
        if self.my_type == 0:
            return 0
        elif self.my_type == 1:
            return 10
        elif self.my_type == 2:
            return 30
        elif self.my_type == 3:
            return 30
        elif self.my_type == 4:
            return 50
        elif self.my_type == 5:
            return 90
        elif self.my_type == 6:
            return 900


class Move:
    def __init__(self, sr, sc, tr, tc):
        self.start_row = sr
        self.start_col = sc
        self.start_pos = Tile(sr, sc)
        self.target_row = tr
        self.target_col = tc
        self.target_pos = Tile(tr, tc)

    def get_start(self):
        return self.start_pos

    def get_end(self):
        return self.target_pos

    def get_row(self):
        return self.target_row

    def get_col(self):
        return self.target_col

    def get_sr(self):
        return self.start_row

    def get_sc(self):
        return self.start_col

    def get_tr(self):
        return self.target_row

    def get_tc(self):
        return self.target_col

    def to_string(self):
        return str(self.start_row) + ", " + str(self.start_col) + ", " + str(self.target_row) + ", " + str(self.target_col)
