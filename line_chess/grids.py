import pygame
from pygame.sprite import Sprite


class Grids(Sprite):
    def __init__(self, screen, settings):
        super(Grids, self).__init__()
        self.screen = screen
        self.width = settings.gridWidth
        self.height = settings.gridWidth
        self.color = (0, 0, 0)
        self.rows = settings.rows
        self.cols = settings.cols
        self.cell_width = self.width / (self.cols + 1)
        self.border = self.cell_width / 2

    def set_color(self, new_color):
        self.color = new_color

    def draw(self):
        for col in range(0, self.cols + 1):  # 绘制列的竖线
            pygame.draw.line(self.screen, self.color, (col * self.cell_width + self.border, self.border),
                             (col * self.cell_width + self.border, self.width - self.border))
        for row in range(0, self.cols + 1):
            pygame.draw.line(self.screen, self.color, (self.border, row * self.cell_width + self.border),
                             (self.width - self.border, row * self.cell_width + self.border))
