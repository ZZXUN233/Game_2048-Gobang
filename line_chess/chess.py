from pygame.sprite import Sprite
import pygame


class Chess(Sprite):
    def __init__(self, screen, grids, color, pos):
        super(Chess, self).__init__()
        self.screen = screen
        self.color = color
        self.pos_x = pos[0]
        self.pos_y = pos[1]
        self.radius = int(grids.cell_width // 2.1)

    def down(self):
        pygame.draw.circle(self.screen, self.color, (int(self.pos_x), int(self.pos_y)), self.radius)
