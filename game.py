import pygame

pygame.init()

# set up the window
size = (1000, 1000)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Chess Game")

# set up the board
board = pygame.Surface((800, 800))
board.fill((215, 206, 158))

# draw the board
for x in range(0, 8, 2):
    for y in range(0, 8, 2):
        pygame.draw.rect(board, (210, 180, 140), (x*100, y*100, 100, 100))
        pygame.draw.rect(board, (210, 180, 140), ((x+1)*100, (y+1)*100, 100, 100))

class Piece:
    def __init__(self, color, x, y, piece_type):
        self.color = color
        self.x = x
        self.y = y
        self.type = piece_type

    def draw(self, surface):
        img = pygame.image.load(f"pieces-basic-png/{self.color}-{self.type}.png")
        surface.blit(img, (self.x*95, self.y*95))

# set up the pieces
pieces = []
for i in range(8):
    pieces.append(Piece("black", i, 1, "pawn"))
    pieces.append(Piece("white", i, 6, "pawn"))

# draw the pieces
for piece in pieces:
    piece.draw(board)

# add the board to the screen
screen.blit(board, (20, 20))

pygame.display.flip()

# main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()