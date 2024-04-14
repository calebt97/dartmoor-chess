import sys, chess, pygame, EngineUtils
import time

sys.path.insert(0, '../')

from PieceSprite import PieceSprite

from white_parser.Parser import Parser as WhiteParser
from black_parser.Parser import Parser as BlackParser


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
        self.white_parser = WhiteParser()
        self.black_parser = BlackParser()

    # def updateComputerMove(self):
    #
    #     move = self.white_parser.find_move(self.board)
    #     self.board.push(move)
    #     self.drawGroup()
    #     self.window.blit(self.gameBoardVis, (0, 0))
    #
    #     time.sleep(1)
    #     move = self.black_parser.find_move(self.board)
    #     self.board.push(move)
    #     self.drawGroup()

    # self.window.blit(self.gameBoardVis, (0, 0))

    def play_game(self, event, color):
        self.window.blit(self.gameBoardVis, (0, 0))

        time.sleep(1)
        if color == chess.WHITE:
            move = self.white_parser.find_move(self.board)

            self.board.push(move)
            self.drawGroup()
            # time.sleep(2)
            self.window.blit(self.gameBoardVis, (0, 0))

        if color == chess.BLACK:
            move = self.black_parser.find_move(self.board)
            self.board.push(move)
            # self.group.update([event])
            self.drawGroup()
            print(str(self.gameBoardVis))
            self.window.blit(self.gameBoardVis, (0, 0))

        if self.board.is_checkmate():
            print("Checkmate!")
            exit(0)

    def drawGroup(self):

        piece_map = self.board.piece_map()
        figures = []

        self.group = pygame.sprite.Group()

        for val, key in enumerate(piece_map):
            figures.append(EngineUtils.getPieceFrom(key, str(piece_map.get(key))))

        for i, figure in enumerate(figures):
            self.group.add(PieceSprite(self.board_rect, figure.x, figure.y, figure.draw()))

        return self.group.draw(self.window)

    def getTurnColor(self):
        return self.board.turn

    def get_promotion(self):
        pawns = ["P", "p"]

        if chess.square_rank(self.toSquare) == 7 and self.board.piece_at(self.fromSquare).symbol() in pawns:
            print("promotion!")
            return chess.QUEEN

        return None

    # def play_game(self):
    #
    #     is_second_move = self.fromSquare is not None
    #
    #     if event.type == pygame.MOUSEBUTTONDOWN and is_second_move is False:
    #         self.fromSquare = EngineUtils.getMoveFromPos(event.dict['pos'])
    #
    #     elif is_second_move is True and event.type == pygame.MOUSEBUTTONDOWN:
    #         self.toSquare = EngineUtils.getMoveFromPos(event.dict['pos'])
    #         promotion = self.get_promotion()
    #
    #         # Construct a move including potential promotion
    #         move = chess.Move(from_square=self.fromSquare, to_square=self.toSquare, promotion=promotion)
    #
    #         # If legal, make move
    #         if self.board.is_legal(move):
    #             self.board.push(move)
    #             self.drawGroup()
    #             self.updateComputerMove(event)
    #
    #         else:
    #             print("illegal move!")
    #
    #         # Regardless, clear out move set
    #         self.fromSquare = None
    #         self.toSquare = None
    #
    #     self.group.update([event])
    #     self.window.blit(self.gameBoardVis, (0, 0))
    #
    #     if self.board.is_checkmate():
    #         print("Checkmate!")
    #         exit(0)
