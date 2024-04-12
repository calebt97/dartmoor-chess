import chess, random

from dartmoor_model import Model


class Parser:

    def __init__(self):
        self.model = Model.Model()

    def move(self, board: chess.Board):
        self.model.test()

        if (board.legal_moves.count()) == 0:
            print("Checkmate!!!")
            exit(0)

        random_move_index = random.randrange(board.legal_moves.count())

        move = list(board.legal_moves)[random_move_index]

        return move
