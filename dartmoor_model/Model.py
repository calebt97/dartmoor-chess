import chess


class Model:

    def __init__(self):
        self.pieceValues = {
            "p": 100,
            "r": 500,
            "n": 320,
            "b": 330,
            "q": 900,
            "k": 20000
        }

    # Max value is 10.0
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
        move_quality += self.__evaluate_attacks()

        # TODO: Incentivize protected checks
        # TODO: Will put your piece at risk

        return move_quality

    def loadBoard(self, board: chess.Board):
        self.board = board
        self.turn_color = board.turn

    def __evaluate_attacks_against(self):
        return 0

    def __evaluate_attacks(self):
        return 0

    def __takes_piece(self):

        if self.board.is_capture(self.move):
            piece_taken = self.board.piece_at(self.move.to_square).symbol().lower()
            return self.pieceValues[piece_taken] / 200.0

        if self.board.is_zeroing(self.move):
            return .5

        return 0

    def __move_back_rank_piece(self):
        if chess.square_rank(self.move.from_square) == 7 and chess.square_rank(
                self.move.to_square) != 7 and self.__get_current_piece() != 'k':
            return 1.6

        return 0

    def __evaluate_castling(self):
        quality_eval = 0.0
        # Is this move a castle?
        if self.board.is_castling(self.move):
            quality_eval = 1.9

        self.board.push(self.move)
        # Does this move enable castling?
        if self.board.has_castling_rights(self.turn_color):
            quality_eval = 1.0

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

    def __get_current_piece(self):
        return self.board.piece_at(self.move.from_square).symbol().lower()