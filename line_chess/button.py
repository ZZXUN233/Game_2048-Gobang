from pygame.sprite import Sprite
import math
import pygame


class Button(Sprite):
    def __init__(self, screen, p_x, p_y, rect_color, width, length, msg, msg_color):
        super(Button, self).__init__()
        self.screen = screen
        self.img = pygame.Rect(0, 0, width, length)
        self.img.centerx = p_x + width / 2
        self.img.top = p_y
        self.img_color = rect_color
        self.msg_str = msg
        self.msg_size = 30
        self.msg_color = msg_color
        self.font = pygame.font.SysFont(None, int(self.msg_size))
        self.msg_img = self.font.render(self.msg_str, True, self.msg_color)
        self.msg_rect = self.msg_img.get_rect()
        self.img.width = self.msg_rect.width
        self.msg_rect.center = self.img.center

    def draw(self):
        self.screen.fill(self.img_color, self.img)
        self.screen.blit(self.msg_img, self.msg_rect)
