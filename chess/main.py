""" TODO:
        PAWN PROMOTION CHOICE
        FOR ATTACK MOVES, CONTINUE SEARCHING UNTIL NO LONGER LEADS TO ATTACK MOVE
        SORT MOVES ACCORDING TO https://www.youtube.com/watch?v=U4ogK0MIzqk
        END GAMES
        ITERATIVE DEEPENING
"""

import gui.table
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

table = gui.table.Table()
