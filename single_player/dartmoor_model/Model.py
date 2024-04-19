from random import randrange

import chess
import chess.polyglot


class Model:

    def __init__(self):
        self.pieceValues = {
            "p": 1,
            "r": 5,
            "n": 3.2,
            "b": 3.3,
            "q": 9,
            "k": 0
        }
        self.count = 0
        self.opening_reader = chess.polyglot.open_reader("../engine/openings/human.bin")

    def eval_board(self, board: chess.Board):
        score = 0
        if len(board.move_stack) < 8 and self.opening_reader.get(board) is not None:
            score += self.opening_move(board)

        score += self.sum_board(board)
        score += self.castling(board)

        return score

    def opening_move(self, board: chess.Board):
        score = 0
        if self.opening_reader.get(board) is not None:
            score = 2

        if board.turn == chess.BLACK:
            return score * -1

        return score

    def castling(self, board):
        prev_move = board.pop()

        if board.is_castling(prev_move) and board.turn == chess.WHITE:
            return 3

        if board.is_castling(prev_move) and board.turn == chess.BLACK:
            return -3

        board.push(prev_move)
        return 0

    def sum_board(self, board):
        score = 0

        score += 9 * (len(board.pieces(chess.QUEEN, chess.WHITE)) - len(board.pieces(chess.QUEEN, chess.BLACK)))
        score += 3.3 * (len(board.pieces(chess.BISHOP, chess.WHITE)) - len(board.pieces(chess.BISHOP, chess.BLACK)))
        score += 3.2 * (len(board.pieces(chess.KNIGHT, chess.WHITE)) - len(board.pieces(chess.KNIGHT, chess.BLACK)))
        score += 5 * (len(board.pieces(chess.ROOK, chess.WHITE)) - len(board.pieces(chess.ROOK, chess.BLACK)))
        score += (len(board.pieces(chess.PAWN, chess.WHITE)) - len(board.pieces(chess.PAWN, chess.BLACK)))

        score /= 10

        return score
