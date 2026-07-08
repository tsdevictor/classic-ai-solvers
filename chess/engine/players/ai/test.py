import engine.piece_tile.piece_tile
import engine.piece_tile.bishop
import engine.piece_tile.king
import engine.piece_tile.knight
import engine.piece_tile.pawn
import engine.piece_tile.rook
import engine.piece_tile.queen
import engine.players.player
import engine.players.white_player
import engine.players.black_player
from engine.board.board import Board
from engine.move.move import MoveFactory
from engine.players.ai.minimax import Minimax


board = Board.create_standard_board()
t1 = board.current_player.make_move(MoveFactory.create_move(board, board.get_tile('f2'), board.get_tile('f3')))

board = t1.transition_board
t2 = board.current_player.make_move(MoveFactory.create_move(board, board.get_tile('e7'), board.get_tile('e5')))

board = t2.transition_board
t3 = board.current_player.make_move(MoveFactory.create_move(board, board.get_tile('g2'), board.get_tile('g4')))
print(t3.transition_board)

strategy = Minimax(3)
ai_move = strategy.execute(t3.transition_board)
print(ai_move)

"""board = Board.create_standard_board()
t1 = board.current_player.make_move(MoveFactory.create_move(board, board.get_tile('e2'), board.get_tile('e4')))

board = t1.transition_board
t2 = board.current_player.make_move(MoveFactory.create_move(board, board.get_tile('d7'), board.get_tile('d5')))

board = t2.transition_board
t3 = board.current_player.make_move(MoveFactory.create_move(board, board.get_tile('d1'), board.get_tile('g4')))
print(t3.transition_board)

strategy = Minimax(4)
ai_move = strategy.execute(t3.transition_board)

print(ai_move)"""
