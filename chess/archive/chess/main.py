from tile import Tile
from piece import Piece
import pygame


def create_board(tiles_setup):
    for k in range(0, 8):
        empty_row = [None, None, None, None, None, None, None, None]
        tiles_setup.append(empty_row)
    for rr in range(0, 8):
        for cc in range(0, 8):
            tiles_setup[rr][cc] = Tile(rr, cc)


def set_pieces(piece_setup):
    for k in range(0, 8):
        empty_row = [None, None, None, None, None, None, None, None]
        piece_setup.append(empty_row)
    for rr in range(0, 8):
        for cc in range(0, 8):
            if rr == 0 or rr == 7:
                if cc == 0 or cc == 7:
                    piece_setup[rr][cc] = Piece(4, rr == 7)
                elif cc == 1 or cc == 6:
                    piece_setup[rr][cc] = Piece(2, rr == 7)
                elif cc == 2 or cc == 5:
                    piece_setup[rr][cc] = Piece(3, rr == 7)
                elif cc == 3:
                    piece_setup[rr][cc] = Piece(5, rr == 7)
                else:
                    piece_setup[rr][cc] = Piece(6, rr == 7)
            elif rr == 1 or rr == 6:
                piece_setup[rr][cc] = Piece(1, rr == 6)
            else:
                piece_setup[rr][cc] = Piece(0, True)


def get_pawn_choice(is_white):
    choice = ""
    while not (choice == "1" or choice == "2" or choice == "3" or choice == "4"):
        choice = input("Enter a number between 1 and 4: \n1. Queen\n2. Rook \n3. Bishop \n4. Knight")
    return Piece(6 - int(choice), is_white)


WHITE = (255, 206, 158)
BLACK = (209, 139, 71)
GRAY = (105, 113, 125)

EMPTY = 0
PAWN = 1
KNIGHT = 2
BISHOP = 3
ROOK = 4
QUEEN = 5
KING = 6

TILE_SIZE = 60
BOARD_SIZE = TILE_SIZE * 8
image = []

piece_layout = []
tiles = []
create_board(tiles)
set_pieces(piece_layout)

pygame.init()
game_display = pygame.display.set_mode((BOARD_SIZE, BOARD_SIZE))
pygame.display.set_caption("Chess")
pygame.display.set_icon(pygame.image.load('BlackKing.png'))

pygame.font.init()
my_font = pygame.font.Font("Lato-Light.ttf", 60)
my_font.set_bold(True)
FONT_WHITE = [255, 255, 255]
FONT_BLACK = [0, 0, 0]

white_turn = True
prev_col = prev_row = -1

pygame.display.update()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for r in range(0, 8):
        image.append([None, None, None, None, None, None, None, None])
        for c in range(0, 8):
            if r % 2 == c % 2:
                pygame.draw.rect(game_display, WHITE, (c * TILE_SIZE, r * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            else:
                pygame.draw.rect(game_display, BLACK, (c * TILE_SIZE, r * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            if tiles[r][c].is_active():
                pygame.draw.rect(game_display, GRAY, (c * TILE_SIZE, r * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            if not piece_layout[r][c].is_empty():
                # noinspection PyTypeChecker
                image[r][c] = pygame.image.load(str(piece_layout[r][c].to_string()))
                game_display.blit(image[r][c], (c * TILE_SIZE, r * TILE_SIZE))

    # noinspection PyUnboundLocalVariable
    if event.type == pygame.MOUSEBUTTONDOWN:
        mouse = pygame.mouse.get_pos()
        col = mouse[0] // TILE_SIZE
        row = mouse[1] // TILE_SIZE

        if tiles[row][col].is_active() and piece_layout[prev_row][prev_col].is_white() == white_turn and \
                not piece_layout[prev_row][prev_col].is_empty():
            white_turn = not white_turn

            was_empty = piece_layout[row][col].is_empty()

            castle = False
            if piece_layout[prev_row][prev_col].is_king():
                if prev_col + 2 == col or prev_col - 2 == col:
                    castle = True

            piece_layout[row][col] = piece_layout[prev_row][prev_col]
            piece_layout[prev_row][prev_col] = Piece(0, True)

            if castle:
                if prev_col + 2 == col:
                    piece_layout[row][prev_col + 1] = piece_layout[row][7]
                    piece_layout[row][7] = Piece(0, True)
                else:
                    piece_layout[row][prev_col - 1] = piece_layout[row][0]
                    piece_layout[row][0] = Piece(0, True)

            if piece_layout[row][col].is_king() or piece_layout[row][col].is_rook():
                piece_layout[row][col].move()

            for r in range(8):
                for c in range(8):
                    tiles[r][c].make_inactive()

            for r in range(8):
                for c in range(8):
                    moving_piece = piece_layout[r][c]
                    if moving_piece.is_pawn() and not (r == row and c == col):
                        piece_layout[r][c].set_just_advanced_two(False)

            if piece_layout[row][col].is_pawn():
                if row == 0 or row == 7:
                    piece_layout[row][col] = get_pawn_choice(piece_layout[row][col].is_white())
                piece_layout[row][col].set_just_advanced_two(abs(row - prev_row) == 2 and col == prev_col)
                if was_empty and abs(prev_row - row) == 1 and abs(prev_col - col) == 1:
                    piece_layout[prev_row][col] = Piece(0, True)

        if piece_layout[row][col].is_white() == white_turn and not piece_layout[row][col].is_empty():
            possible_moves = piece_layout[row][col].possible_moves(piece_layout, Tile(row, col))

            for r in range(0, len(piece_layout)):
                for c in range(0, len(piece_layout)):
                    if piece_layout[r][c].is_king() and \
                            piece_layout[r][c].is_white() == piece_layout[row][col].is_white():
                        this = Tile(row, col)
                        king = Tile(r, c)
                        piece_layout[r][c].remove_invalid_moves_second(possible_moves, piece_layout, this, king)
                        break

            for r in range(8):
                for c in range(8):
                    tiles[r][c].make_inactive()

            for i in range(len(possible_moves)):
                tiles[possible_moves[i].get_row()][possible_moves[i].get_col()].make_active()

        prev_col = col
        prev_row = row

    for r in range(0, 8):
        for c in range(0, 8):
            if piece_layout[r][c].is_king():
                game_status = piece_layout[r][c].checkmate(piece_layout, Tile(r, c), white_turn)
                if game_status == 1:
                    text = my_font.render("Black wins!", False, FONT_BLACK)
                    game_display.blit(text, [BOARD_SIZE/2 - text.get_rect().width/2,
                                      BOARD_SIZE/2 - text.get_rect().height/2])
                elif game_status == 2:
                    text = my_font.render("White wins!", False, FONT_BLACK)
                    game_display.blit(text, [BOARD_SIZE / 2 - text.get_rect().width / 2,
                                      BOARD_SIZE / 2 - text.get_rect().height / 2])
                elif game_status == 3:
                    text = my_font.render("Draw by stalemate!", False, FONT_BLACK)
                    game_display.blit(text, [BOARD_SIZE / 2 - text.get_rect().width / 2,
                                      BOARD_SIZE / 2 - text.get_rect().height / 2])

    pygame.display.update()
