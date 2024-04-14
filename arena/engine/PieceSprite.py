from DragOperator import DragOperator
import pygame


class PieceSprite(pygame.sprite.Sprite):
    def __init__(self, board_rect, i, j, image):
        super().__init__()
        self.board = board_rect
        self.image = image
        self.set_pos(i, j)
        self.drag = DragOperator(self)

    def set_pos(self, i, j):
        x = self.board.left + self.board.width // 8 * i + self.board.width // 16
        y = self.board.left + self.board.height // 8 * (7 - j) + self.board.height // 16
        self.rect = self.image.get_rect(center=(x, y))

    def update(self, event_list):
        self.drag.update(event_list)
        if not self.drag.dragging:
            i = max(0, min(7, (self.rect.centerx - self.board.left) // (self.board.width // 8)))
            j = 7 - max(0, min(7, (self.rect.centery - self.board.top) // (self.board.height // 8)))
            self.set_pos(i, j)
