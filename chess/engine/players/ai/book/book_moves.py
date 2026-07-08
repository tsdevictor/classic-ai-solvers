from random import randint
import os

PATH = os.path.dirname(__file__)


class BookMove:
    def __init__(self):
        self.next_move = None
        self.openings = self.get_all_openings()

    def get_next_move(self, legal_moves, previous_move):
        if previous_move is None:
            index = randint(0, len(self.openings) - 1)
            self.next_move = self.openings[index][0]
            for move in legal_moves:
                if str(move) == self.next_move:
                    return move
            raise RuntimeError('Could not find valid book move')

        candidate_continuations = []
        for opening in self.openings:
            if opening[0] == str(previous_move):
                candidate_continuations.append(opening[1:])

        if len(candidate_continuations) == 0:
            raise RuntimeError('Could not find valid book move')

        self.openings = candidate_continuations
        index = randint(0, len(self.openings)-1)
        self.next_move = self.openings[index][0]

        for move in legal_moves:
            if str(move) == self.next_move:
                return move
        raise RuntimeError('Could not find valid book move')

    @staticmethod
    def get_all_openings() -> [[]]:
        f = open(os.path.join(PATH, 'openings2.txt'), 'r')

        all_games = []
        for game in f.readlines():
            all_games.append(BookMove.game_move_list(game))

        f.close()
        return all_games

    @staticmethod
    def game_move_list(game: str) -> []:
        moves = []

        for move in game.strip().split(' '):
            joe = move[(move.find('.')+1):]
            moves.append(move[(move.find('.')+1):])

        return moves
