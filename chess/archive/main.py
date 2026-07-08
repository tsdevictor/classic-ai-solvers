from tile import Tile
from piece import Piece
import pygame

WHITE = [255, 206, 158]
BLACK = [209, 139, 71]
GRAY = [105, 113, 125]
FONT_BLACK = [0, 0, 0]
TILE_SIZE = 60
BOARD_SIZE = TILE_SIZE * 8
AI_COLOR = False


def create_board(tiles_setup):
    for rr in range(8):
        tiles_setup.append([Tile(rr, 0), Tile(rr, 1), Tile(rr, 2), Tile(rr, 3),
                            Tile(rr, 4), Tile(rr, 5), Tile(rr, 6), Tile(rr, 7)])


def set_pieces(piece_setup):
    for rr in range(8):
        piece_setup.append([None, None, None, None, None, None, None, None])
        for cc in range(8):
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
    choice = input("Enter a number between 1 and 4:\n1. Queen\n2. Rook\n3. Bishop\n4. Knight")
    while not (choice == "1" or choice == "2" or choice == "3" or choice == "4"):
        choice = input("Not a valid choice. Please try again.")
    return Piece(6 - int(choice), is_white)


def draw_board(tile_setup, piece_setup, display, is_white_turn):
    for rr in range(8):
        for cc in range(8):
            if tile_setup[rr][cc].is_active():
                if piece_setup[rr][cc].is_empty():
                    pygame.draw.circle(display, GRAY, ((cc + 0.5) * TILE_SIZE, (rr + 0.5) * TILE_SIZE), TILE_SIZE / 5)
                else:
                    pygame.draw.rect(display, GRAY, (cc * TILE_SIZE, rr * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            elif rr % 2 == cc % 2:
                pygame.draw.rect(display, WHITE, (cc * TILE_SIZE, rr * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            else:
                pygame.draw.rect(display, BLACK, (cc * TILE_SIZE, rr * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            if not piece_setup[rr][cc].is_empty():
                display.blit(pygame.transform.scale(piece_setup[rr][cc].get_image(), (TILE_SIZE, TILE_SIZE)),
                             (cc * TILE_SIZE, rr * TILE_SIZE))
    for rr in range(8):
        for cc in range(8):
            if piece_setup[rr][cc].is_king() and piece_setup[rr][cc].is_white() == is_white_turn:
                game_state = piece_setup[rr][cc].checkmate(piece_setup, Tile(rr, cc), is_white_turn)
                if game_state[1] != 0:
                    message = pygame.font.Font("Fonts/Lato-Light.ttf", 60).render(game_state[0], False, FONT_BLACK)
                    display.blit(message, [BOARD_SIZE / 2 - message.get_rect().width / 2,
                                           BOARD_SIZE / 2 - message.get_rect().height / 2])
                return game_state
    return -1


def make_move(piece_setup, sr, sc, tr, tc, is_white_turn):
    # for en passant
    was_empty = piece_setup[tr][tc].is_empty()

    # move the move
    piece_setup[tr][tc] = piece_setup[sr][sc]
    piece_setup[sr][sc] = Piece(0, True)

    # castling
    piece_setup[tr][tc].move()
    if piece_setup[tr][tc].is_king() and abs(tc - sc) == 2:
        if sc + 2 == tc:
            piece_setup[tr][5] = piece_setup[tr][7]
            piece_setup[tr][7] = Piece(0, True)
        else:
            piece_setup[tr][3] = piece_setup[tr][0]
            piece_setup[tr][0] = Piece(0, True)

    if piece_setup[tr][tc].is_pawn():
        # pawn promotion
        if tr == 0 or tr == 7:
            piece_setup[tr][tc] = get_pawn_choice(is_white_turn)
        # en passant
        if was_empty and abs(sr - tr) == 1 and abs(sc - tc) == 1:
            piece_setup[sr][tc] = Piece(0, True)
        piece_setup[tr][tc].set_adv_two(abs(sr - tr) == 2 and tc == sc)


def eval_board(piece_setup, is_white):
    white_value = 0
    black_value = 0
    for rr in range(8):
        for cc in range(8):
            if piece_setup[rr][cc].is_white():
                white_value += piece_setup[rr][cc].get_value()
            else:
                black_value += piece_setup[rr][cc].get_value()
    if is_white:
        return white_value - black_value
    else:
        return black_value - white_value


def get_king_pos(piece_setup, is_white):
    for rr in range(8):
        for cc in range(8):
            if piece_setup[rr][cc].is_king() and piece_setup[rr][cc].is_white() == is_white:
                return Tile(rr, cc)
    return None


def get_all_moves(piece_setup, tile_setup, player_color):
    all_moves = []
    for rr in range(8):
        for cc in range(8):
            if piece_setup[rr][cc].is_white() == player_color and not piece_setup[rr][cc].is_empty():
                all_moves += piece_setup[rr][cc].get_moves(piece_setup, tile_setup, rr, cc, player_color)
    return all_moves


def eval_board_after_move(piece_setup, moves, player_color):
    copy_setup = []
    for rr in range(8):
        copy_setup.append([None, None, None, None, None, None, None, None])
        for cc in range(8):
            copy_setup[rr][cc] = piece_setup[rr][cc]
    make_move(copy_setup, moves.get_sr(), moves.get_sc(), moves.get_tr(), moves.get_tc(), white_turn)
    return eval_board(copy_setup, player_color), copy_setup


def minimax(depth, piece_setup, tile_setup, is_maximizer):
    game_state = piece_setup[0][0].checkmate(piece_setup, get_king_pos(piece_setup, is_maximizer), is_maximizer)
    if game_state[1] != 0 or depth > 2:
        return eval_board(piece_setup, AI_COLOR)

    if is_maximizer:
        all_moves = get_all_moves(piece_setup, tile_setup, AI_COLOR)
        max_eval = -1000000
        for moves in all_moves:
            # basically the same as make move without having to undo after
            new_setup = eval_board_after_move(piece_setup, moves, AI_COLOR)[1]
            current_eval = minimax(depth + 1, new_setup, tile_setup, False)
            if current_eval > max_eval:
                max_eval = current_eval
                best_move = moves
        if depth == 0:
            return best_move
        return max_eval
    else:
        all_moves = get_all_moves(piece_setup, tile_setup, AI_COLOR)
        min_eval = 1000000
        for moves in all_moves:
            new_setup = eval_board_after_move(piece_setup, moves, AI_COLOR)[1]
            current_eval = minimax(depth + 1, new_setup, tile_setup, True)
            min_eval = min(min_eval, current_eval)
        return min_eval

    # noinspection PyUnreachableCode
    """all_moves = get_all_moves(piece_setup, tile_setup, AI_COLOR)
            best_move = all_moves[random.randint(0, len(all_moves) - 1)]
            best_eval = -10000
            for moves in all_moves:
                current_setup = eval_board_after_move(piece_setup, moves, AI_COLOR)
                current_eval = current_setup[0]
                if current_eval > best_eval:
                    best_eval = current_eval
                    best_move = moves
        return best_move"""


tiles = []
create_board(tiles)
piece_layout = []
set_pieces(piece_layout)

pygame.init()
game_display = pygame.display.set_mode([BOARD_SIZE, BOARD_SIZE])
pygame.display.set_caption("Chess")
pygame.display.set_icon(Piece(6, False).get_image())

s_row = -1
s_col = -1
white_turn = True
running = True
while running:
    pygame.display.ai_move()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and white_turn:
            m_pos = pygame.mouse.get_pos()
            t_row = m_pos[1] // TILE_SIZE
            t_col = m_pos[0] // TILE_SIZE
            sp = piece_layout[s_row][s_col]
            tp = piece_layout[t_row][t_col]

            # move a move
            if tiles[t_row][t_col].is_active() and not sp.is_empty() and sp.is_white() == white_turn:
                make_move(piece_layout, s_row, s_col, t_row, t_col, white_turn)
                white_turn = not white_turn
                for r in range(8):
                    for c in range(8):
                        tiles[r][c].set_active(False)

            # show valid moves
            elif not tp.is_empty() and tp.is_white() == white_turn:
                possible_moves = piece_layout[t_row][t_col].get_moves(piece_layout, tiles, t_row, t_col, white_turn)
                for move in possible_moves:
                    tiles[move.get_row()][move.get_col()].set_active(True)

            s_row = t_row
            s_col = t_col

    pygame.display.ai_move()
    game_status = draw_board(tiles, piece_layout, game_display, white_turn)

    if not white_turn and game_status[1] == 0:
        ai_move = minimax(0, piece_layout, tiles, True)
        make_move(piece_layout, ai_move.get_sr(), ai_move.get_sc(), ai_move.get_tr(), ai_move.get_tc(), white_turn)
        white_turn = not white_turn
