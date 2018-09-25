import pygame as pg
import random
import time
from pg_2048.settings import Settings
import math
import sys


def check_event(gameCommand, button_group):
    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_a or event.key == pg.K_LEFT:
                if gameCommand.moveLeft():
                    gameCommand.newNum()
            elif event.key == pg.K_w or event.key == pg.K_UP:
                if gameCommand.moveUp():
                    gameCommand.newNum()
            elif event.key == pg.K_d or event.key == pg.K_RIGHT:
                if gameCommand.moveRight():
                    gameCommand.newNum()
            elif event.key == pg.K_s or event.key == pg.K_DOWN:
                if gameCommand.moveDown():
                    gameCommand.newNum()
            elif event.key == pg.K_b:
                if len(gameCommand.game_history) > 0:
                    gameCommand.MaList = gameCommand.game_history.pop()
                # gameCommand.MaList = game_history.pop()
            elif event.key == pg.K_q:
                sys.exit()
        elif event.type == pg.MOUSEBUTTONDOWN:
            m_x, m_y = pg.mouse.get_pos()
            for button in button_group:
                if button.img.collidepoint(m_x, m_y):
                    if button.msg_str == " New Game":
                        gameCommand.newGame()
                    elif button.msg_str == "Auto Play":
                        print("auto play")
                    elif button.msg_str == " Setting ":
                        print("settings")
                    elif button.msg_str == "  Exit   ":
                        sys.exit()


def check_collide(Grids):
    copyGroup = Grids.copy()
    for grid1 in Grids:
        copyGroup.remove(grid1)
        for grid2 in copyGroup:
            distance = math.sqrt((grid1.rect.center[0] - grid2.rect.center[0]) ** 2 +
                                 (grid1.rect.center[1] - grid2.rect.center[1]) ** 2)
            if distance < grid1.width:
                if grid1.value == grid2.value:
                    grid1.value *= 2
                    Grids.update(grid1)
                    print(grid1.value)
                    Grids.remove(grid2)
                print("发生碰撞！")
        copyGroup.add(grid1)  # 每一块不与自身进行碰撞检测
