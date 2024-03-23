import pygame, time
from PieceSprite import PieceSprite
import EngineUtils
import chess
from State import State

pygame.init()
window = pygame.display.set_mode((1000, 1000))

clock = pygame.time.Clock()
state = State(chess.Board())

gameBoard = pygame.Surface(window.get_size())

gameBoard.fill((255, 255, 255))
size = (min(window.get_size()) - 20) // 8
start = (window.get_width() - size * 8) // 2, (window.get_height() - size * 8) // 2
board_rect = pygame.Rect(*start, size * 8, size * 8)
ts, w, h, c1, c2 = 50, *window.get_size(), (128, 128, 128), (64, 64, 64)

for y in range(8):
    for x in range(8):
        color = (192, 192, 164) if (x + y) % 2 == 0 else (96, 64, 32)
        pygame.draw.rect(gameBoard, color, (start[0] + x * size, start[1] + y * size, size, size))

# Get initial board setup
group = pygame.sprite.Group()
# figures = EngineUtils.getInitialPieces()

pieceMap = state.getPieceMap()
figures = []
for val, key in enumerate(pieceMap):
    figures.append(EngineUtils.getPieceFrom(key, str(pieceMap.get(key))))

for i, figure in enumerate(figures):
    group.add(PieceSprite(board_rect, figure.x, figure.y, figure.draw()))

# TODO: Board needs to get pulled from State
# TODO: Board actions need to affect State
# TODO: Board needs to be aware of moves
# TODO: Moves need to follow rules set by State
board = state.getBoard()


run = True
while run:
    clock.tick(60)
    event = pygame.event.wait()
    event_list = [event]

    print(event_list)
    for event in event_list:
        if event.type == pygame.QUIT:
            run = False

    group.update(event_list)

    window.blit(gameBoard, (0, 0))
    group.draw(window)
    pygame.display.flip()

pygame.quit()
exit()

# # https://en.wikipedia.org/wiki/Chess_symbols_in_Unicode
# white_figures = {'king': '♔', 'queen': '♕', 'rook': '♖', 'bishop': '♗', 'knight': '♘', 'pawn': '♙'}
# black_figures = {'king': '♚', 'queen': '♛', 'rook': '♜', 'bishop': '♝', 'knight': '♞', 'pawn': '♟'}
#
# seguisy = pygame.font.SysFont("segoeuisymbol", size - 4)
# white_images = {k: seguisy.render(c, True, (255, 255, 255)) for k, c in white_figures.items()}
# black_images = {k: seguisy.render(c, True, (0, 0, 0)) for k, c in black_figures.items()}
