import sys, chess, pygame, EngineUtils
import time
from random import randrange

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

    def play_game(self, color):
        self.window.blit(self.gameBoardVis, (0, 0))

        # time.sleep(.5)
        if color == chess.WHITE:
            move = self.white_parser.find_move(self.board)

            self.board.push(move)

            self.drawGroup()
            self.window.blit(self.gameBoardVis, (0, 0))
            if self.board.is_checkmate():
                return chess.WHITE

        if color == chess.BLACK:
            move = self.black_parser.find_move(self.board)

            self.board.push(move)

            self.drawGroup()
            self.window.blit(self.gameBoardVis, (0, 0))

            if self.board.is_checkmate():
                return chess.BLACK

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

    def isDraw(self):
        return self.board.fullmove_number > 100 or self.board.is_stalemate() or self.board.is_fivefold_repetition()

    def reloadState(self):
        self.board.reset()

    def get_matchup_name(self):
        return self.white_parser.get_bot_name() + "_v_" + self.black_parser.get_bot_name()

    def initial_random_moves(self, num_moves):
        for x in range(num_moves):
            listomoves_white = list(self.board.legal_moves)
            random = randrange(len(listomoves_white))

            self.board.push(listomoves_white[random])
            listomoves_black = list(self.board.legal_moves)
            random = randrange(len(listomoves_black))

            self.board.push(listomoves_black[random])
