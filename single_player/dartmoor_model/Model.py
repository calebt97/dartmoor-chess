from random import randrange

import chess


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

        # Each eval function pushes move, evaluates then pops move and returns value

    def eval_board(self, board: chess.Board):
        score = 0

        piece_map = board.piece_map()
        for key in piece_map:
            if piece_map[key].symbol().islower():
                score -= self.pieceValues[piece_map[key].symbol()]
            else:
                score += self.pieceValues[piece_map[key].symbol().lower()]
        #
        # if board.is_checkmate() and board.turn is False:
        #     return -10
        #
        # if board.is_checkmate() and board.turn:
        #     return 10


        score /= 10

        return score

    def evaluateMove(self, move: chess.Move):
        self.move = move
        move_quality = 0.0

        move_quality += self.__evaluate_checks()

        # If checkmate just return
        if move_quality >= 100.0:
            return 100.0

        if self.__get_current_piece() == 'k':
            move_quality -= 10

        if self.__get_current_piece() == 'r':
            move_quality -= 5

        if self.__get_current_piece() == 'p':
            move_quality += 1.2

        move_quality += self.__evaluate_castling()
        move_quality += self.__takes_piece()
        move_quality += self.__move_back_rank_piece()
        move_quality += self.__evaluate_attacks_against()
        move_quality += self.__space_taken()
        move_quality += self.__evaluate_attackers_against_current_position()
        move_quality += self.__avoid_repitition()

        return move_quality

    def loadBoard(self, board: chess.Board):
        self.board = board
        self.turn_color = board.turn

    def __space_taken(self):
        current_piece = self.__get_current_piece()
        self.board.push(self.move)
        spaces_attacked = len(self.board.attacks(self.move.to_square))

        # if current_piece == 'q':
        #     # It gets queen happy if it overvalues the space a queen takes
        #     spaces_attacked = spaces_attacked // 2

        self.board.pop()
        return spaces_attacked * .04

    def __evaluate_attackers_against_current_position(self):
        if self.__get_current_piece() != 'p':
            return 12 * len(self.board.attackers(not self.turn_color, self.move.from_square))
        return 0

    def __evaluate_attacks_against(self):

        current_piece = self.__get_current_piece()
        eval = 0
        self.board.push(self.move)
        spaces_attacked_by = len(self.board.attackers(not self.turn_color, self.move.to_square))
        is_pinned = self.board.is_pinned(self.turn_color, self.move.to_square)
        self.board.pop()

        if current_piece == 'q' and spaces_attacked_by > 0:
            return -15.0

        for attacker in self.board.attackers(not self.turn_color, self.move.to_square):
            piece = self.board.piece_at(attacker).symbol().lower()
            if self.pieceValues[piece] < self.pieceValues[current_piece]:
                eval += 6

        eval += is_pinned * 3

        return eval * -1

    def __takes_piece(self):
        eval = 0

        if self.board.is_capture(self.move) and self.board.piece_at(self.move.to_square):
            piece_taken = self.board.piece_at(self.move.to_square).symbol().lower()
            eval += self.pieceValues[piece_taken]

            # Fuck them pawns
            if self.__get_current_piece() != 'p' and self.pieceValues[self.__get_current_piece()] > self.pieceValues[
                self.board.piece_at(self.move.to_square).symbol().lower()]:
                eval -= 2.0

            eval += self.__save_another_piece()

        return eval

    def __move_back_rank_piece(self):
        eval = 0

        # Deploy pieces that aren't the king on the back rank
        if chess.square_rank(self.move.from_square) == self.__get_back_rank() and chess.square_rank(
                self.move.to_square) != self.__get_back_rank() and self.__get_current_piece() not in ['k', 'r']:
            eval += 3.6

        # If possible, move the king back
        if self.__is_headed_towards_back_rank() and self.__get_current_piece() == 'k':
            eval += 6.6

        # Avoiding moving king forward if possible
        elif not self.__is_headed_towards_back_rank() and self.__get_current_piece() in ['k']:
            eval -= 6.6

        return eval

    def __evaluate_castling(self):
        quality_eval = 0.0
        # Is this move a castle?
        if self.board.is_castling(self.move):
            quality_eval = 25

        self.board.push(self.move)
        # Does this move enable castling?
        if self.board.has_castling_rights(self.turn_color):
            quality_eval = 5.2

        self.board.pop()

        return quality_eval

    def __evaluate_checks(self):
        quality_eval = 0

        self.board.push(self.move)
        if self.board.is_check():
            quality_eval = 1.4

        if self.board.is_checkmate():
            quality_eval = 100.0

        self.board.pop()

        return quality_eval

    def __save_another_piece(self):
        squares_attacked = 0
        square_set = list(self.board.attacks(self.move.to_square))
        for square in square_set:
            if self.board.piece_at(square) is not None:
                piece = self.board.piece_at(square).symbol().lower()
                if piece != 'p' and self.pieceValues[piece] >= self.pieceValues[self.__get_current_piece()]:
                    squares_attacked += 1

        return squares_attacked * 9

    def __avoid_repitition(self):
        self.board.push(self.move)
        if self.board.is_fivefold_repetition():
            self.board.pop()
            return -10
        self.board.pop()
        return 0

    def __get_current_piece(self):
        return self.board.piece_at(self.move.from_square).symbol().lower()

    def __get_back_rank(self):
        # If white, back rank is 0
        if self.turn_color:
            return 0
        return 7

    def __is_headed_towards_back_rank(self):
        if self.turn_color:
            return chess.square_rank(self.move.from_square) > chess.square_rank(
                self.move.to_square)
        return chess.square_rank(self.move.from_square) < chess.square_rank(
            self.move.to_square)
