import chess

class State:

    def __init__(self, board: chess.Board):
        self.board = board

    def display(self):
        print(self.board)

    def getPieceMap(self):
        return self.board.piece_map()

    def getBoard(self):
        return self.board