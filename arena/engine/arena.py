import time

import pygame, chess

from State import State

pygame.init()
window = pygame.display.set_mode((1000, 1000))

clock = pygame.time.Clock()

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

# Fill up the state with the board engine and visual
state = State(chess.Board(), pygame.sprite.Group(), board_rect, window, gameBoard)

run = True
counter = 0
color = True
while run:
    state.drawGroup()
    pygame.display.flip()

    event = pygame.event.wait()

    if event.type == pygame.QUIT:
        run = False

    state.play_game( color)
    state.drawGroup()
    pygame.display.flip()
    color = not color
    counter += 1
    print(counter)

pygame.quit()
exit()

# while run:
#     blockedActions = [pygame.MOUSEMOTION, pygame.ACTIVEEVENT, pygame.WINDOWEXPOSED, pygame.WINDOWFOCUSGAINED,
#                       pygame.WINDOWFOCUSLOST]
#
#     pygame.event.set_blocked(blockedActions)
#
#     allowedActions = [pygame.QUIT, pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP]
#     pygame.event.set_allowed(allowedActions)
#     event = pygame.event.wait()
#
#     if event.type == pygame.QUIT:
#         run = False
#
#     state.updateHumanMove(event)
#     state.drawGroup()
#     pygame.display.flip()