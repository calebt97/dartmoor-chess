import time
from random import randrange

import chess

from black_model import Model, MoveModel


class Parser:

    def __init__(self):
        self.board_model = Model.Model()
        self.move_model = MoveModel.MoveModel()
        self.max_depth = 3
        self.test_list = None
        board = chess.Board()
        self.previous_evals = {board.fen(): 0.0}
        self.white_check_mate, self.black_checkmate = 10000, -10000
        self.horizon_threshold = 200
        self.skipped_counts = 0

    def get_bot_name(self):
        return "hk-alpha.0.3"

    def find_move(self, board: chess.Board):

        self.move_model.loadBoard(board)

        moves = self.get_ordered_list_of_moves(board)
        return self.get_best_move(board, moves)

    def get_ordered_list_of_moves(self, board: chess.Board):
        possible_moves = board.legal_moves
        sorted_moves = sorted(possible_moves, key=lambda move: self.move_model.evaluateMove(move))

        if board.turn == chess.BLACK:
            sorted_moves.reverse()

        return sorted_moves

    def get_best_move(self, board: chess, moves):
        best_move = None
        self.best_value = 10000
        start = time.time()

        if board.turn == chess.WHITE:
            # If white, best move should start at -10000
            self.best_value *= -1

        for move in moves:
            # move hasn't been made yet, so we need to look at not current board turn
            eval = self.minimax(0, board, not board.turn, alpha=-10000, beta=10000)

            # White wants the highest eval
            if board.turn == chess.WHITE and eval > self.best_value:

                if eval == self.white_check_mate:
                    print("white checkmate!!! " + str(move))
                    return move

                best_move = move
                self.best_value = eval
                # print("best move update "+str(move))
                # print("best score update "+str(best_value))

            # Black wants the lowest eval
            if board.turn == chess.BLACK and eval < self.best_value:
                if eval == self.black_checkmate:
                    print("black checkmate!!! " + str(move))
                    return move

                best_move = move
                self.best_value = eval
                # print("best move update "+str(move))
                # print("best score update "+str(best_value))

        print("black best move " + str(best_move))
        print("black best score " + str(self.best_value))
        print("Skipped counts "+str(self.skipped_counts))
        print("Time taken " + str(time.time() - start))
        return best_move

    def minimax(self, depth, board: chess.Board, maximizing_player,
                alpha, beta):

        MAX, MIN = 1000, -1000

        if board.is_checkmate() and board.turn == chess.WHITE:
            # Bias for checkmates that are fewer turns away
            return self.white_check_mate - (depth * 2)

        if board.is_checkmate() and board.turn == chess.BLACK:
            # Bias for checkmates that are fewer turns away
            return self.white_check_mate + (depth * 2)

        if board.is_fivefold_repetition():
            return 0

        legal_moves = board.legal_moves

        if depth == self.max_depth - 1:
            score = 0

            if self.previous_evals.get(board.fen()) is not None:
                score = self.previous_evals.get(board.fen())
            else:
                score = self.board_model.eval_board(board)
                self.previous_evals[board.fen()] = score

            if board.turn == chess.WHITE:
                if score < self.best_value - self.horizon_threshold and self.best_value != -10000:
                    self.skipped_counts += 1
                    return score
            if board.turn == chess.BLACK:
                if score > self.best_value + self.horizon_threshold and self.best_value != 10000:
                    self.skipped_counts += 1
                    return score

        # Terminating condition. i.e
        # leaf node is reached
        if depth == self.max_depth:

            if self.previous_evals.get(board.fen()) is not None:
                return self.previous_evals[board.fen()]

            eval = self.board_model.eval_board(board)

            self.previous_evals[board.fen()] = eval

            return eval

        if maximizing_player:

            best = MIN

            for move in legal_moves:
                board_copy = board.copy()
                board_copy.push(move)

                val = self.minimax(depth + 1, board_copy,
                                   False, alpha, beta)

                best = max(best, val)
                alpha = max(alpha, best)

                # Alpha Beta Pruning
                if beta <= alpha:
                    break

            return best

        else:
            best = MAX

            for move in legal_moves:
                board_copy = board.copy()
                board_copy.push(move)

                val = self.minimax(depth + 1, board,
                                   True, alpha, beta)
                best = min(best, val)
                beta = min(beta, best)

                # Alpha Beta Pruning
                if beta <= alpha:
                    break

            return best
