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
blackWins = 0
whiteWins = 0
draws = 0
total_games = 0
while total_games < 100:
    total_games += 1
    state.initial_random_moves(3)

    while run:
        state.drawGroup()
        pygame.display.flip()

        event = pygame.event.peek()

        winner = state.play_game(color)
        state.drawGroup()
        pygame.display.flip()
        color = not color
        if winner == chess.WHITE:
            print("white won")
            whiteWins += 1
            break

        if winner == chess.BLACK:
            print("black won")
            blackWins += 1
            break

        if state.isDraw():
            print("draw")
            draws += 1
            break

    state.reloadState()
    state.drawGroup()
    pygame.display.flip()


report_file_name = state.get_matchup_name() + ".txt"
report = open(report_file_name, "w")
report.write("\nwhite wins: "+str(whiteWins))
report.write("\nblack wins: "+str(blackWins))
report.write("\ndraws: "+str(draws))
report.close()

pygame.quit()
exit()
