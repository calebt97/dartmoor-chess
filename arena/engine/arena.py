import random
import time
from pathlib import Path

import pygame, chess
import datetime

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
color = chess.WHITE
blackWins = 0
whiteWins = 0
draws = 0
total_games = 0
opening_fens = open("openings/opening_fen_list.txt", "r")
black_times = []
white_times = []
white_avgs = []
black_avgs = []
openings = opening_fens.readlines()
random.shuffle(openings)

while total_games < 10:
    total_games += 1
    state.initial_fen(openings[total_games])

    while run:
        start = time.time()
        state.drawGroup()
        pygame.display.flip()

        event = pygame.event.peek()

        if state.isDraw():
            print("draw")
            draws += 1
            print("\n------------\nwhite wins: " + str(whiteWins))
            print("\nblack wins: " + str(blackWins))
            print("\ndraws: " + str(draws))
            break

        state.play_game(color)
        if color == chess.BLACK:
            black_times.append(time.time() - start)
        else:
            white_times.append(time.time() - start)

        time.sleep(1)
        state.drawGroup()
        pygame.display.flip()
        color = not color
        if state.board.outcome():
            if state.board.outcome().winner == chess.WHITE:
                print("white won")
                whiteWins += 1
                print("\n------------\nwhite wins: " + str(whiteWins))
                print("\nblack wins: " + str(blackWins))
                print("\ndraws: " + str(draws))
                black_avg = sum(black_times) / len(black_times)
                white_avg = sum(white_times) / len(white_times)
                print("black avg: " + str(black_avg))
                print("white avg: " + str(white_avg))

                black_avgs.append(black_avg)
                white_avgs.append(white_avg)
                black_times.clear()
                white_times.clear()

                break

            if state.board.outcome().winner == chess.BLACK:
                print("black won")
                blackWins += 1
                print("\n------------\nwhite wins: " + str(whiteWins))
                print("\nblack wins: " + str(blackWins))
                print("\ndraws: " + str(draws))
                black_avg = sum(black_times) / len(black_times)
                white_avg = sum(white_times) / len(white_times)
                print("black avg: " + str(black_avg))
                print("white avg: " + str(white_avg))

                black_avgs.append(black_avg)
                white_avgs.append(white_avg)
                black_times.clear()
                white_times.clear()
                break


    state.reloadState()
    state.drawGroup()
    pygame.display.flip()

report_file_name = "results/" + state.get_matchup_name() + ".txt"
path = Path(report_file_name)
report = open(path, "a")
report.write("\n------------\nwhite wins: " + str(whiteWins))
report.write("\nblack wins: " + str(blackWins))
report.write("\ndraws: " + str(draws))
report.write("\ntimestamp: " + str(datetime.datetime.now()))
total_black_avg = sum(black_avgs) / len(black_avgs)
report.write("\nblack avg: " + str(total_black_avg))
total_white_avg = sum(white_avgs) / len(white_avgs)
report.write("\nwhite avg: " + str(total_white_avg))


report.close()

pygame.quit()
exit()
