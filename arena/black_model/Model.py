from random import randrange

import chess
import chess.polyglot
from . import value_maps


class Model:

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
        self.opening_reader = chess.polyglot.open_reader("openings/human.bin")
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
            score = 5 + randrange(-1, 1)

        if board.turn == chess.BLACK:
            return score * -1

        return score

    def score_queen(self, board: chess.Board):
        whiteAttacks = 0
        whiteAttacked = 0
        blackAttacks = 0
        blackAttacked = 0
        total_white_score = 0
        total_black_score = 0

        white_queen = board.pieces(chess.QUEEN, chess.WHITE)
        black_queen = board.pieces(chess.QUEEN, chess.BLACK)
        for square in white_queen:
            whiteAttacks += len(board.attacks(square))
            whiteAttacked -= len(board.attackers(chess.BLACK, square))
            total_white_score += self.maps.queen_table[square] // 22

        for square in black_queen:
            blackAttacks -= len(board.attacks(square))
            blackAttacked += len(board.attackers(chess.BLACK, square))
            total_black_score -= (-1 * (self.maps.queen_table[square] // 22))

        blackAttacked *= 4
        whiteAttacked *= 4

        return sum([whiteAttacked, whiteAttacks, blackAttacked, blackAttacks, total_white_score, total_black_score]) * 5

    def score_king(self, board: chess.Board):

        black_king = board.pieces(chess.KING, chess.BLACK).pop()
        white_king = board.pieces(chess.KING, chess.WHITE).pop()

        total_black_score = -1 * self.maps.king_table[black_king] // 10
        total_white_score = self.maps.king_table[white_king] // 10

        if chess.square_rank(black_king) == 7 and len(board.piece_map()) > 8:
            total_black_score -= 4

        if chess.square_rank(white_king) == 0 and len(board.piece_map()) > 8:
            total_white_score += 4

        # Aggressive king when the board starts to simplify
        if len(board.piece_map()) < 10:
            total_white_score *= -1
            total_black_score *= -1

        whiteAttacked = 5 * len(board.attackers(chess.BLACK, white_king))
        blackAttacked = -5 * len(board.attackers(chess.BLACK, black_king))

        return sum([total_white_score, total_black_score, whiteAttacked, blackAttacked])

    def score_knights(self, board: chess.Board):
        whiteAttacks = 0
        whiteAttacked = 0
        blackAttacks = 0
        blackAttacked = 0
        total_white_score = 0
        total_black_score = 0

        white_knights = board.pieces(chess.KNIGHT, chess.WHITE)
        black_knights = board.pieces(chess.KNIGHT, chess.BLACK)
        for square in white_knights:
            whiteAttacks += len(board.attacks(square))
            whiteAttacked += len(board.attackers(chess.BLACK, square))
            total_white_score += self.maps.knight_table[square] // 20

            if chess.square_rank(square) == 0:
                total_white_score -= 1

        for square in black_knights:
            blackAttacks -= len(board.attacks(square))
            blackAttacked -= len(board.attackers(chess.BLACK, square))
            total_black_score -= (-1 * (self.maps.knight_table[square] // 20))

            if chess.square_rank(square) == 7:
                total_black_score += 1

        blackAttacks *= .4
        whiteAttacks *= .4

        return sum(
            [whiteAttacked, whiteAttacks, blackAttacked, blackAttacks, total_white_score, total_black_score]) * 3.2

    def score_rooks(self, board: chess.Board):
        whiteAttacks = 0
        whiteAttacked = 0
        blackAttacks = 0
        blackAttacked = 0
        total_white_score = 0
        total_black_score = 0

        white_rooks = board.pieces(chess.ROOK, chess.WHITE)
        black_rooks = board.pieces(chess.ROOK, chess.BLACK)
        for square in white_rooks:
            whiteAttacks += len(board.attacks(square))
            whiteAttacked += len(board.attackers(chess.BLACK, square))
            total_white_score += self.maps.rook_table[square] // 16

        for square in black_rooks:
            blackAttacks -= len(board.attacks(square))
            blackAttacked -= len(board.attackers(chess.BLACK, square))
            total_black_score -= (-1 * (self.maps.rook_table[square] // 16))

        whiteAttacks *= 1.5
        blackAttacks *= 1.5

        return sum([whiteAttacked, whiteAttacks, blackAttacked, blackAttacks, total_white_score, total_black_score])

    def score_bishops(self, board: chess.Board):
        whiteAttacks = 0
        whiteAttacked = 0
        blackAttacks = 0
        blackAttacked = 0
        total_white_score = 0
        total_black_score = 0

        white_bishops = board.pieces(chess.BISHOP, chess.WHITE)
        black_bishops = board.pieces(chess.BISHOP, chess.BLACK)

        for square in white_bishops:
            whiteAttacks += len(board.attacks(square))
            whiteAttacked += len(board.attackers(chess.BLACK, square))
            total_white_score += self.maps.bishop_table[square] // 18

            # Penalty for not developing
            if chess.square_rank(square) == 0:
                total_white_score -= 1

        for square in black_bishops:
            blackAttacks -= len(board.attacks(square))
            blackAttacked -= len(board.attackers(chess.BLACK, square))
            total_black_score -= (-1 * (self.maps.bishop_table[square] // 18))
            # Penalty for not developing
            if chess.square_rank(square) == 7:
                total_black_score += 1

        blackAttacks *= .4
        whiteAttacks *= .4

        return sum(
            [whiteAttacked, whiteAttacks, blackAttacked, blackAttacks, total_white_score, total_black_score]) * 3.3

    def score_pawns(self, board: chess.Board):
        whiteAttacks = 0
        whiteAttacked = 0
        blackAttacks = 0
        blackAttacked = 0
        total_white_score = 0
        total_black_score = 0

        white_pawns = board.pieces(chess.PAWN, chess.WHITE)
        black_pawns = board.pieces(chess.PAWN, chess.BLACK)
        for square in white_pawns:
            whiteAttacks += len(board.attacks(square))
            whiteAttacked -= len(board.attackers(chess.BLACK, square))
            total_white_score += self.maps.pawn_table[square] // 18

        for square in black_pawns:
            blackAttacks -= len(board.attacks(square))
            blackAttacked += len(board.attackers(chess.BLACK, square))
            total_black_score -= (-1 * (self.maps.pawn_table[square] // 18))

        if len(board.piece_map()) < 15:
            total_black_score *= 1.5
            total_white_score *= 1.5

        return sum([whiteAttacked, whiteAttacks, blackAttacked, blackAttacks, total_white_score, total_black_score])

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

