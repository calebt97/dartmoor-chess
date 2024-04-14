import chess


class Model:

    def __init__(self):
        self.pieceValues = {
            "p": 1,
            "r": 5,
            "n": 3.2,
            "b": 3.3,
            "q": 9,
            "k": 200
        }

    # Each eval function pushes move, evaluates then pops move and returns value

    def evaluateMove(self, move: chess.Move):
        self.move = move
        move_quality = 0.0

        move_quality += self.__evaluate_checks()

        # If checkmate just return
        if move_quality >= 100.0:
            return 100.0

        move_quality += self.__evaluate_castling()
        move_quality += self.__takes_piece()
        move_quality += self.__move_back_rank_piece()
        move_quality += self.__evaluate_attacks_against()
        move_quality += self.__space_taken()
        move_quality += self.__evaluate_attackers_against_current_position()

        return move_quality

    def loadBoard(self, board: chess.Board):
        self.board = board
        self.turn_color = board.turn

    def __space_taken(self):
        current_piece = self.__get_current_piece()
        self.board.push(self.move)
        spaces_attacked = len(self.board.attacks(self.move.to_square))

        if current_piece == 'q':
            # It gets queen happy if it overvalues the space a queen takes
            spaces_attacked = spaces_attacked // 5

        self.board.pop()
        return spaces_attacked * .05

    def __evaluate_attackers_against_current_position(self):
        if self.__get_current_piece() != 'p':
            return 8 * len(self.board.attackers(not self.turn_color, self.move.from_square))
        return 0

    def __evaluate_attacks_against(self):

        current_piece = self.__get_current_piece()
        self.board.push(self.move)
        spaces_attacked_by = len(self.board.attackers(not self.turn_color, self.move.to_square))
        is_pinned = self.board.is_pinned(self.turn_color, self.move.to_square)
        self.board.pop()

        if current_piece == 'q' and spaces_attacked_by > 0:
            return -15.0

        eval = (spaces_attacked_by * 1) + (is_pinned * 3)

        return eval * -1

    def __takes_piece(self):
        eval = 0

        if self.board.is_capture(self.move):
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
                self.move.to_square) != self.__get_back_rank() and self.__get_current_piece() != 'k':
            eval += 1.6

        # If possible, move the king back
        if self.__is_headed_towards_back_rank() and self.__get_current_piece() == 'k':
            eval += 1.6

        # Avoiding moving king forward if possible
        elif not self.__is_headed_towards_back_rank() and self.__get_current_piece() == 'k':
            eval -= 1.6

        if self.board.is_zeroing(self.move):
            eval += .6

        return eval

    def __evaluate_castling(self):
        quality_eval = 0.0
        # Is this move a castle?
        if self.board.is_castling(self.move):
            quality_eval = 5

        self.board.push(self.move)
        # Does this move enable castling?
        if self.board.has_castling_rights(self.turn_color):
            quality_eval = 2.2

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
                if self.board.piece_at(square).symbol().lower() != 'p':
                    squares_attacked += 1

        return squares_attacked * 9

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
