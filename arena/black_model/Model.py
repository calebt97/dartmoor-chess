from random import randrange

import chess
import chess.polyglot
from . import value_maps


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
        self.opening_reader = chess.polyglot.open_reader("openings/human.bin")
        self.maps = value_maps.value_maps()

    def eval_board(self, board: chess.Board):
        score = 0
        if len(board.move_stack) < 10 and self.opening_reader.get(board) is not None:
            score += self.opening_move(board)

        score += self.castling(board)
        score += self.score_knights(board)
        score += self.score_pawns(board)
        score += self.score_queen(board)
        score += self.score_king(board)
        score += self.score_rooks(board)
        score += self.score_bishops(board)
        score += self.sum_board(board)

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
            whiteAttacked += len(board.attackers(chess.BLACK, square))
            total_white_score += self.maps.queen_table[square] // 22

        for square in black_queen:
            blackAttacks -= len(board.attacks(square))
            blackAttacked -= len(board.attackers(chess.BLACK, square))
            total_black_score -= (-1 * (self.maps.queen_table[square] // 22))

        return sum([whiteAttacked, whiteAttacks, blackAttacked, blackAttacks, total_white_score, total_black_score])

    def score_king(self, board: chess.Board):

        black_king = board.pieces(chess.KING, chess.BLACK).pop()
        white_king = board.pieces(chess.KING, chess.WHITE).pop()

        total_black_score = -1 * self.maps.king_table[black_king] // 10
        total_white_score = self.maps.king_table[white_king] // 10
        
        # if len(board.piece_map()) < 8:
        #     total_white_score *= -1
        #     total_black_score *= -1
        if chess.square_rank(black_king) == 7 and len(board.piece_map()) > 8:
            total_black_score -= 4

        if chess.square_rank(white_king) == 0 and len(board.piece_map()) > 8:
            total_white_score += 4

        return sum([total_white_score, total_black_score])

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
            total_white_score += self.maps.knight_table[square] // 17

        for square in black_knights:
            blackAttacks -= len(board.attacks(square))
            blackAttacked -= len(board.attackers(chess.BLACK, square))
            total_black_score -= (-1 * (self.maps.knight_table[square] // 17))

        return sum([whiteAttacked, whiteAttacks, blackAttacked, blackAttacks, total_white_score, total_black_score])

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
            total_white_score += self.maps.rook_table[square] // 20

        for square in black_rooks:
            blackAttacks -= len(board.attacks(square))
            blackAttacked -= len(board.attackers(chess.BLACK, square))
            total_black_score -= (-1 * (self.maps.rook_table[square] // 20))

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

        for square in black_bishops:
            blackAttacks -= len(board.attacks(square))
            blackAttacked -= len(board.attackers(chess.BLACK, square))
            total_black_score -= (-1 * (self.maps.bishop_table[square] // 18))

        return sum([whiteAttacked, whiteAttacks, blackAttacked, blackAttacks, total_white_score, total_black_score])

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

        # We want attacks to be scarier than attacked for pawns
        blackAttacked *= .5
        whiteAttacked *= .5

        return sum([whiteAttacked, whiteAttacks, blackAttacked, blackAttacks, total_white_score, total_black_score])

    def castling(self, board):
        score = 0

        if board.has_castling_rights(chess.WHITE):
            score += 2
        if board.has_castling_rights(chess.BLACK):
            score -= 2

        prev_move = board.pop()

        if board.is_castling(prev_move):
            score = 6

        if board.turn == chess.BLACK:
            score *= -1

        board.push(prev_move)
        return score

    #
    def sum_board(self, board):
        score = 0

        # score += 9 * (len(board.pieces(chess.QUEEN, chess.WHITE)) - len(board.pieces(chess.QUEEN, chess.BLACK)))
        # score += 3.3 * (len(board.pieces(chess.BISHOP, chess.WHITE)) - len(board.pieces(chess.BISHOP, chess.BLACK)))
        # score += 3.2 * (len(board.pieces(chess.KNIGHT, chess.WHITE)) - len(board.pieces(chess.KNIGHT, chess.BLACK)))
        # score += 5 * (len(board.pieces(chess.ROOK, chess.WHITE)) - len(board.pieces(chess.ROOK, chess.BLACK)))
        # score += (len(board.pieces(chess.PAWN, chess.WHITE)) - len(board.pieces(chess.PAWN, chess.BLACK)))

        score /= 10

        return score
