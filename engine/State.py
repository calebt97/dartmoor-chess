import chess, pygame, EngineUtils

from PieceSprite import PieceSprite


class State:

    def __init__(self, board: chess.Board, group: pygame.sprite.Group, board_rect: pygame.rect.Rect, window: pygame.display):
        self.board = board
        self.group = group
        self.board_rect = board_rect
        self.fromSquare = None
        self.toSquare = None
        self.window = window

    def display(self):
        print(self.board)

    def getPieceMap(self):
        return self.board.piece_map()

    def getBoard(self):
        return self.board

    def updateBoard(self, event):
        print("something")

    def updateEvent(self, event):

        if event.type == pygame.MOUSEBUTTONDOWN:
            self.fromSquare = EngineUtils.getMoveFromPos(event.dict['pos'])

        if event.type == pygame.MOUSEBUTTONUP:
            self.toSquare = EngineUtils.getMoveFromPos(event.dict['pos'])

            ##Construct a move once we have picked up the piece and dropped it
            move = chess.Move(from_square=self.fromSquare, to_square=self.toSquare)

            if self.board.is_legal(move):
                self.board.push(move)
                self.drawGroup()

        self.group.update([event])


    def getGroup(self):
        return self.group

    def drawGroup(self):
        pieceMap = self.board.piece_map()
        figures = []

        for val, key in enumerate(pieceMap):
            figures.append(EngineUtils.getPieceFrom(key, str(pieceMap.get(key))))

        for i, figure in enumerate(figures):
            self.group.add(PieceSprite(self.board_rect, figure.x, figure.y, figure.draw()))

        return self.group.draw(self.window)

    def setupBoard(self):
        pieceMap = self.board.piece_map()
        figures = []
        for val, key in enumerate(pieceMap):
            figures.append(EngineUtils.getPieceFrom(key, str(pieceMap.get(key))))

        for i, figure in enumerate(figures):
            self.group.add(PieceSprite(self.board_rect, figure.x, figure.y, figure.draw()))
