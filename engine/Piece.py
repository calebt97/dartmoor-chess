import pygame

class Piece:
    def __init__(self, color, x, y, piece_type):
        self.color = color
        self.x = x
        self.y = y
        self.type = piece_type

    def draw(self):
        return pygame.image.load(f"pieces-basic-png/{self.color}-{self.type}.png")
        # surface.blit(img, (self.x*108, self.y*108))