import chess

from dartmoor_model import Model


class Parser:

    def __init__(self):
        self.model = Model.Model()
        
    def get_bot_name(self):
        return "hk-alpha.0.1"

    def find_move(self, board: chess.Board):

        self.model.loadBoard(board)

        best_move_value = -1.0
        best_move: chess.Move
        possible_moves = board.legal_moves

        # 100 equals checkmate
        for potential in possible_moves:

            move_eval = self.model.evaluateMove(potential)

            if move_eval > best_move_value:
                best_move_value = move_eval
                best_move = potential

        if best_move is not None:
            print("ideal move " + str(best_move))
            print("ideal eval value " + str(best_move_value))

        return best_move
