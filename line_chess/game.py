from line_chess.grids import Grids
from line_chess.settings import Settings
from line_chess.chess import Chess
from line_chess.button import Button

from pygame.sprite import Group
import pygame
import sys
import numpy as np


class Game:
    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode(self.settings.screen_size)
        self.bg_color = (191, 191, 191)
        self.grid = Grids(self.screen, self.settings)
        self.chess_group = Group()
        self.button_group = Group()
        self.game_status = {}

        self.Matrix = np.zeros((self.grid.rows + 1, self.grid.cols + 1))
        self.black_turn = True  # 黑子优先
        self.win_types = 0
        self.all_wins = [[{} for _ in range(self.Matrix.shape[1])] for _ in range(self.Matrix.shape[1])]
        self.my_score = np.zeros_like(self.Matrix)
        self.ai_score = np.zeros_like(self.Matrix)
        self.my_wins = [0 for _ in range(self.win_types)]
        self.ai_wins = [0 for _ in range(self.win_types)]

        self.my_win_list = []
        self.ai_win_list = []

    def get_game_status(self):
        rows = self.Matrix.shape[0]
        cols = self.Matrix.shape[1]
        for row in range(rows):
            for col in range(cols - 4):
                for k in range(5):
                    self.all_wins[row][col + k][self.win_types] = True
                self.win_types += 1
        for col in range(cols):
            for row in range(rows - 4):
                for k in range(5):
                    self.all_wins[row + k][col][self.win_types] = True
                self.win_types += 1
        # 记录斜线赢法
        for row in range(rows - 4):
            for col in range(cols - 4):
                for k in range(5):
                    self.all_wins[row + k][col + k][self.win_types] = True
                self.win_types += 1
        # 记录反斜线赢法
        for row in range(rows - 4):
            for col in reversed(range(4, cols)):
                for k in range(5):
                    self.all_wins[row + k][col - k][self.win_types] = True
                self.win_types += 1
        self.my_wins = [0 for _ in range(self.win_types)]
        self.ai_wins = [0 for _ in range(self.win_types)]

    def get_button(self):
        self.button_group.add(Button(self.screen,
                                     50, 800, (63, 63, 63), 100, 50, "New Game", (255, 255, 255)))
        self.button_group.add(Button(self.screen,
                                     200, 800, (63, 63, 63), 100, 50, "Back OneStep", (255, 255, 255)))
        self.button_group.add(Button(self.screen,
                                     400, 800, (63, 63, 63), 100, 50, "Settings", (255, 255, 255)))
        self.button_group.add(Button(self.screen,
                                     600, 800, (63, 63, 63), 100, 50, "Exit Game", (255, 255, 255)))

    def new_game(self):
        self.Matrix = np.zeros((self.grid.rows + 1, self.grid.cols + 1))
        self.chess_group.empty()
        self.my_score = np.zeros_like(self.Matrix)
        self.my_wins = [0 for _ in range(self.win_types)]
        self.ai_score = np.zeros_like(self.Matrix)
        self.ai_wins = [0 for _ in range(self.win_types)]

        self.my_win_list = []
        self.ai_win_list = []

    def update_info(self, p_x, p_y):
        if self.black_turn:
            self.my_win_list += list(self.all_wins[p_x][p_y].keys())
            for my_step in self.my_win_list:
                if my_step in self.ai_win_list:
                    self.ai_win_list.remove(my_step)
        else:
            self.ai_win_list += list(self.all_wins[p_x][p_y].keys())
            for ai_step in self.ai_win_list:
                if ai_step in self.my_win_list:
                    self.my_win_list.remove(ai_step)

    def check_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                p_x, p_y = pygame.mouse.get_pos()
                if p_y > 800:
                    for button in self.button_group:
                        if button.img.collidepoint(p_x, p_y):
                            if button.msg_str == "New Game":
                                self.new_game()
                            elif button.msg_str == "Back OneStep":
                                print("回撤一步")
                            elif button.msg_str == "Settings":
                                print("Settings")
                            elif button.msg_str == "Exit Game":
                                sys.exit()
                else:
                    p_x, p_y = round((p_x - self.grid.border) / self.grid.cell_width), round(
                        (p_y - self.grid.border) / self.grid.cell_width)
                    if self.black_turn and self.Matrix[p_x][p_y] != 1:
                        self.update_info(p_x, p_y)
                        self.my_step(p_x, p_y)
                        self.draw_chessman(p_x, p_y)

                        self.black_turn = not self.black_turn
                        (ai_x, ai_y) = self.ai_step()
                        self.draw_chessman(ai_x, ai_y)
                        self.update_info(ai_x, ai_y)
                        self.black_turn = not self.black_turn

    def draw_chessman(self, p_x, p_y):
        if self.black_turn:
            self.chess_group.add(Chess(self.screen, self.grid, (1, 1, 1),
                                       (p_x * self.grid.cell_width + self.grid.border,
                                        p_y * self.grid.cell_width + self.grid.border)))
        else:
            self.chess_group.add(Chess(self.screen, self.grid, (255, 255, 255),
                                       (p_x * self.grid.cell_width + self.grid.border,
                                        p_y * self.grid.cell_width + self.grid.border)))

    def my_step(self, p_x, p_y):
        self.Matrix[p_x][p_y] = 1
        for k in range(self.win_types):
            if k in self.all_wins[p_x][p_y].keys():
                self.my_wins[k] += 1
                self.ai_wins[k] = 6
                if self.my_wins[k] == 5:
                    print("你赢了！")

    def ai_step(self):
        max_score = 0
        ai_x, ai_y = 0, 0
        for row in range(self.Matrix.shape[0]):
            for col in range(self.Matrix.shape[1]):
                if self.Matrix[row][col] == 0:
                    for k in range(self.win_types):
                        if k in self.all_wins[row][col].keys():
                            if self.my_wins[k] == 1:
                                self.my_score[row][col] += 200
                            elif self.my_wins[k] == 2:
                                self.my_score[row][col] += 400
                            elif self.my_wins[k] == 2:
                                self.my_score[row][col] += 2000
                            elif self.my_wins[k] == 2:
                                self.my_score[row][col] += 10000

                            if self.ai_wins[k] == 1:
                                self.ai_score[row][col] += 200
                            elif self.ai_wins[k] == 2:
                                self.ai_score[row][col] += 400
                            elif self.ai_wins[k] == 3:
                                self.ai_score[row][col] += 2000
                            elif self.ai_wins[k] == 4:
                                self.ai_score[row][col] += 10000
                    if self.my_score[row][col] > max_score:
                        max_score = self.my_score[row][col]
                        ai_x = row
                        ai_y = col
                    elif self.my_score[row][col] == max_score:
                        if self.ai_score[row][col] > self.ai_score[ai_x][ai_y]:
                            ai_x = row
                            ai_y = col
                    if self.ai_score[row][col] > max_score:
                        max_score = self.ai_score[row][col]
                        ai_x = row
                        ai_y = col
                    elif self.ai_score[row][col] == max_score:
                        if self.my_score[row][col] > self.my_score[ai_x][ai_y]:
                            ai_x = row
                            ai_y = col
        print((ai_x, ai_y))
        for k in range(self.win_types):
            if k in self.all_wins[ai_x][ai_y].keys():
                self.ai_wins[k] += 1
                self.my_wins[k] = 6
                if not self.black_turn and self.Matrix[ai_x][ai_y] == 0:
                    self.Matrix[ai_x][ai_y] = 1
                if self.ai_wins[k] == 5:
                    print("计算机胜利！")
        return (ai_x, ai_y)

    def run(self):
        self.get_button()
        self.get_game_status()
        print(self.win_types)
        while True:
            self.screen.fill(self.bg_color)
            self.grid.draw()
            for button in self.button_group:
                button.draw()
            for chess in self.chess_group:
                chess.down()
            self.check_event()
            pygame.display.flip()
