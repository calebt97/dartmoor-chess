import chess, pygame, EngineUtils

from PieceSprite import PieceSprite


class State:

    def __init__(self, board: chess.Board, group: pygame.sprite.Group, board_rect: pygame.rect.Rect,
                 window: pygame.display, board_viz: pygame.Surface):
        self.gameBoardVis = board_viz
        self.board = board
        self.group = group
        self.board_rect = board_rect
        self.fromSquare = None
        self.toSquare = None
        self.window = window

    def updateEvent(self, event):

        isSecondMove = self.fromSquare is not None

        if event.type == pygame.MOUSEBUTTONDOWN and isSecondMove is False:
            self.fromSquare = EngineUtils.getMoveFromPos(event.dict['pos'])

        elif isSecondMove is True and event.type == pygame.MOUSEBUTTONDOWN:
            print("Called")
            print(self.fromSquare)
            self.toSquare = EngineUtils.getMoveFromPos(event.dict['pos'])

            # Construct a move once we have picked up the piece and dropped it
            move = chess.Move(from_square=self.fromSquare, to_square=self.toSquare)

            # If legal, make move
            if self.board.is_legal(move):
                self.board.push(move)
                self.drawGroup()

            # Regardless, clear out move set
            self.fromSquare = None
            self.toSquare = None

        self.group.update([event])
        self.window.blit(self.gameBoardVis, (0, 0))

    def drawGroup(self):

        piece_map = self.board.piece_map()
        figures = []

        self.group = pygame.sprite.Group()

        for val, key in enumerate(piece_map):
            figures.append(EngineUtils.getPieceFrom(key, str(piece_map.get(key))))

        for i, figure in enumerate(figures):
            self.group.add(PieceSprite(self.board_rect, figure.x, figure.y, figure.draw()))

        return self.group.draw(self.window)
