import engine.players.ai.board_evaluator as be
import engine.players.ai.book.book_moves as bm
import time


class OpenerMinimax:
    BIG_NUMBER = 10000000

    def __init__(self, search_depth: int):
        self.board_evaluator = be.BoardEvaluator()
        self.current_value = 0
        self.search_depth = search_depth
        self.opener = bm.BookMove()

    def __str__(self):
        return 'Minimax'

    def execute(self, board, previous_move, num_moves):  # -> Move
        if num_moves < 16:
            try:
                return self.opener.get_next_move(board.current_player.legal_moves, previous_move)
            except RuntimeError:
                pass

        if len(board.white_pieces + board.black_pieces) < 5:
            self.search_depth = 10

        start = time.time()

        best_move = None
        best_white_value = -OpenerMinimax.BIG_NUMBER
        best_black_value = OpenerMinimax.BIG_NUMBER
        self.current_value = 0
        print(str(board.current_player) + ' analyzing next move with depth ' + str(self.search_depth))

        num_moves = 1
        for move in board.current_player.legal_moves:
            print('Evaluating move ' + str(num_moves) + '/' + str(len(board.current_player.legal_moves)))
            num_moves += 1
            move_transition = board.current_player.make_move(move)
            if move_transition.get_move_status().is_done():
                self.current_value = self.minimax(move_transition.get_transition_board(),
                                                  self.search_depth - 1,
                                                  -OpenerMinimax.BIG_NUMBER, OpenerMinimax.BIG_NUMBER,
                                                  not board.current_player.is_white)
                if board.current_player.is_white and self.current_value > best_white_value:
                    best_white_value = self.current_value
                    best_move = move
                elif board.current_player.is_black and self.current_value < best_black_value:
                    best_black_value = self.current_value
                    best_move = move

        print('Analysis took ' + str(time.time() - start) + ' seconds: ' +
              'best move is ' + str(best_move) + ' with board evaluation score ' +
              str(best_black_value if board.current_player.is_black else best_white_value) + '\n')

        return best_move

    def minimax(self, board, depth: int, alpha: int, beta: int, is_maximizer: bool):
        if depth == 0 or board.current_player.is_in_checkmate() or board.current_player.is_in_stalemate():
            return self.board_evaluator.evaluate(board, depth)

        if is_maximizer:
            max_eval = -OpenerMinimax.BIG_NUMBER
            for move in board.current_player.legal_moves:
                move_transition = board.current_player.make_move(move)
                if move_transition.get_move_status().is_done():
                    evaluation = self.minimax(move_transition.get_transition_board(), depth - 1, alpha, beta, False)
                    max_eval = max(max_eval, evaluation)
                    alpha = max(alpha, evaluation)
                    if beta <= alpha:
                        break
            return max_eval
        else:
            min_eval = OpenerMinimax.BIG_NUMBER
            for move in board.current_player.legal_moves:
                move_transition = board.current_player.make_move(move)
                if move_transition.get_move_status().is_done():
                    evaluation = self.minimax(move_transition.get_transition_board(), depth - 1, alpha, beta, True)
                    min_eval = min(min_eval, evaluation)
                    beta = min(beta, evaluation)
                    if beta <= alpha:
                        break
            return min_eval
