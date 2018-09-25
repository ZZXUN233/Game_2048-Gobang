import pygame as pg
import math
import random
from settings import Settings
from pygame.sprite import Sprite


class Grid(Sprite):
    def __init__(self, screen, settings, grid_info):
        super(Grid, self).__init__()
        self.screen = screen
        self.width = settings.gridWidth - 4
        self.settings = settings
        self.value = 0
        # 随机位置与数值
        self.rect = pg.Rect(0, 0, self.width, self.width)
        # self._randPut(settings)
        self.font = pg.font.SysFont(None, int(80))

        # self.updateGrid()

        self.move = [0, 0, 0, 0]
        self.speed = settings.grid_speed

        self.newGrid(grid_info[0], grid_info[1], grid_info[2])
        self.color = settings.gridColor.update(self.value)
        print(self.color)

    def newGrid(self, p_x, p_y, seed):
        self.value = seed
        self.rect.centerx = p_x * self.settings.gridWidth + self.settings.gridWidth / 2
        self.rect.top = p_y * self.settings.gridWidth + 2
        # 生成新格后绘制它
        self.updateGrid()

    def updateGrid(self):
        print(self.value)
        try:
            self.font = pg.font.SysFont(None, int(80 - 2 * math.log2(self.value)))
        except Exception as e:
            print(str(e))
        self.text_color = (0, 0, 0)
        self.msg_image = self.font.render(str(self.value), True, self.text_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_grid(self):
        self.screen.fill(self.color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
        # pg.draw.rect(self.screen, self.color, self.rect)

    def move_in(self, direction):
        while True:
            if direction == 0:  # left
                self.rect.centerx -= self.speed
                self.msg_image_rect.center = self.rect.center
                if self.rect.centerx <= 75:
                    break
            elif direction == 1:  # up
                self.rect.top -= self.speed
                self.msg_image_rect.center = self.rect.center
                if self.rect.top <= 2:
                    break
            elif direction == 2:  # right
                self.rect.centerx += self.speed
                self.msg_image_rect.center = self.rect.center
                if self.rect.centerx >= 525:
                    break
            elif direction == 3:
                self.rect.top += self.speed
                self.msg_image_rect.center = self.rect.center
                if self.rect.top >= 452:
                    break
            else:
                pass
