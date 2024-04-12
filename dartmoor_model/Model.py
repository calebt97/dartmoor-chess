import chess


class Model:

    def __init__(self):
        self.blah = "blah"
        self.board = None

    def evaluateMove(self):
        print("hello world!")

    def loadBoard(self, board: chess.Board):
        self.board = board
