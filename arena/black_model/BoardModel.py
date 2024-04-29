from random import randrange

import chess
import chess.polyglot
from . import value_maps


class BoardModel:

    def __init__(self):
        self.pieceValues = {
            "p": 1,
            "r": 6,
            "n": 3.2,
            "b": 3.3,
            "q": 9,
            "k": 0
        }
        self.count = 0
        self.opening_reader = chess.polyglot.open_reader("openings/baron30.bin")
        self.maps = value_maps.value_maps()

    def eval_board(self, board: chess.Board):
        score = 0
        if board.fullmove_number < 12 and self.opening_reader.get(board) is not None:
            score += self.opening_move(board)

        score += self.castling(board)
        score += self.score_knights(board)
        score += self.score_pawns(board)
        score += self.score_queen(board)
        score += self.score_king(board)
        score += self.score_rooks(board)
        score += self.score_bishops(board)
        score += self.checking(board)

        return score

    def opening_move(self, board: chess.Board):
        score = 0
        if self.opening_reader.get(board) is not None:
            score = 15 + randrange(-1, 1)

        if board.turn == chess.BLACK:
            return score * -1

        return score

    def score_queen(self, board: chess.Board):
        total_white_score = 0
        total_black_score = 0

        white_queen = board.pieces(chess.QUEEN, chess.WHITE)
        black_queen = board.pieces(chess.QUEEN, chess.BLACK)
        total_white_score += len(white_queen) * 10
        total_black_score -= len(black_queen) * 10

        for square in white_queen:
            total_white_score += len(board.attacks(square))
            total_white_score += len(board.attackers(chess.WHITE, square))
            total_white_score += self.maps.queen_table[square]
            total_black_score -= len(board.attackers(chess.BLACK, square))

        for square in black_queen:
            total_black_score -= len(board.attacks(square))
            total_black_score -= len(board.attackers(chess.BLACK, square))
            total_black_score -= self.maps.knight_table[square]
            total_white_score += len(board.attackers(chess.WHITE, square))

        return sum([total_white_score, total_black_score]) * 7

    def score_king(self, board: chess.Board):

        black_king = board.pieces(chess.KING, chess.BLACK).pop()
        white_king = board.pieces(chess.KING, chess.WHITE).pop()

        total_black_score = -1 * self.maps.king_table[black_king] // 10
        total_white_score = self.maps.king_table[white_king] // 10

        # Aggressive king when the board starts to simplify
        if len(board.piece_map()) < 10:
            total_white_score *= -1
            total_black_score *= -1

        whiteAttacked = 5 * len(board.attackers(chess.BLACK, white_king))
        blackAttacked = -5 * len(board.attackers(chess.BLACK, black_king))

        return sum([total_white_score, total_black_score, whiteAttacked, blackAttacked])

    def score_knights(self, board: chess.Board):
        total_white_score = 0
        total_black_score = 0

        white_knights = board.pieces(chess.KNIGHT, chess.WHITE)
        black_knights = board.pieces(chess.KNIGHT, chess.BLACK)
        total_white_score += len(white_knights) * 3.3
        total_black_score -= len(black_knights) * 3.3

        for square in white_knights:
            total_white_score += len(board.attacks(square))
            total_white_score += len(board.attackers(chess.WHITE, square))
            total_white_score += self.maps.knight_table[square]
            total_black_score -= len(board.attackers(chess.BLACK, square))

        for square in black_knights:
            total_black_score -= len(board.attacks(square))
            total_black_score -= len(board.attackers(chess.BLACK, square))
            total_black_score -= self.maps.knight_table[square]
            total_white_score += len(board.attackers(chess.WHITE, square))

        return sum([total_white_score, total_black_score]) * 3.2

    def score_rooks(self, board: chess.Board):
        total_white_score = 0
        total_black_score = 0

        white_rooks = board.pieces(chess.ROOK, chess.WHITE)
        black_rooks = board.pieces(chess.ROOK, chess.BLACK)
        total_white_score += len(white_rooks) * 7
        total_black_score -= len(black_rooks) * 7

        for square in white_rooks:
            total_white_score += len(board.attacks(square))
            total_white_score += len(board.attackers(chess.WHITE, square))
            total_white_score += self.maps.rook_table[square] / 2
            total_black_score -= len(board.attackers(chess.BLACK, square))

        for square in black_rooks:
            total_black_score -= len(board.attacks(square))
            total_black_score -= len(board.attackers(chess.BLACK, square))
            total_black_score -= self.maps.rook_table[chess.square_mirror(square)] / 2
            total_white_score += len(board.attackers(chess.WHITE, square))


        return sum([total_white_score, total_black_score]) * 5

    def score_bishops(self, board: chess.Board):
        total_white_score = 0
        total_black_score = 0

        white_bishops = board.pieces(chess.BISHOP, chess.WHITE)
        black_bishops = board.pieces(chess.BISHOP, chess.BLACK)
        total_white_score += len(white_bishops) * 4
        total_black_score -= len(black_bishops) * 4

        for square in white_bishops:
            total_white_score += len(board.attacks(square))
            total_white_score += len(board.attackers(chess.WHITE, square))
            total_white_score += self.maps.bishop_table[square] / 2
            total_black_score -= len(board.attackers(chess.BLACK, square))

        for square in black_bishops:
            total_black_score -= len(board.attacks(square))
            total_black_score -= len(board.attackers(chess.BLACK, square))
            total_black_score -= self.maps.bishop_table[chess.square_mirror(square)] / 2
            total_white_score += len(board.attackers(chess.WHITE, square))

        # Bonus for bishop pair
        if len(white_bishops) == 2:
            total_white_score += 5

        if len(black_bishops) == 2:
            total_black_score -= 5

        return sum(
            [total_white_score, total_black_score]) * 3.3

    def score_pawns(self, board: chess.Board):
        total_white_score = 0
        total_black_score = 0

        white_pawns = board.pieces(chess.PAWN, chess.WHITE)
        black_pawns = board.pieces(chess.PAWN, chess.BLACK)
        total_white_score += len(white_pawns) * 2
        total_black_score -= len(black_pawns) * 2

        for square in white_pawns:
            total_white_score += len(board.attacks(square))
            total_white_score += len(board.attackers(chess.WHITE, square))
            total_white_score += self.maps.pawn_table[square] / 4
            total_black_score -= len(board.attackers(chess.BLACK, square))

        for square in black_pawns:
            total_black_score -= len(board.attacks(square))
            total_black_score -= len(board.attackers(chess.BLACK, square))
            total_black_score -= self.maps.pawn_table[chess.square_mirror(square)] / 4
            total_white_score += len(board.attackers(chess.WHITE, square))

        if len(board.piece_map()) < 15:
            total_black_score *= 1.5
            total_white_score *= 1.5

        return sum([total_white_score, total_black_score])

    def castling(self, board):
        score = 0

        if board.has_castling_rights(chess.WHITE):
            score += 2
        if board.has_castling_rights(chess.BLACK):
            score -= 2

        prev_move = board.pop()

        if board.is_castling(prev_move):
            score = 7

        if board.turn == chess.BLACK:
            score *= -1

        board.push(prev_move)

        return score

    def checking(self, board: chess.Board):
        num_attackers = 0

        color = board.turn

        if board.is_check():
            attacked_king = board.pieces(chess.KING, color).pop()
            num_attackers += len(board.attackers(not color, attacked_king))

        if color == chess.WHITE:
            num_attackers *= -1

        # More attackers on king the better
        return num_attackers * 2
