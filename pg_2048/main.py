import math
import pygame as pg
import threading
from pygame.sprite import Group

import pg_2048.gameCommand as gameCommand
from pg_2048.settings import Settings
import pg_2048.game_func as game_func
from pg_2048.button import Button

GridWidth = 150
Timer = 0
failed = False
button_group = Group()

COLORDIR = {
    0: (200, 200, 200),
    2: (239, 226, 216),
    4: (240, 224, 200),
    8: (240, 175, 120),
    16: (245, 150, 100),
    32: (250, 125, 90),
    64: (245, 95, 60),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 204, 97),
    1024: (237, 197, 63),
    2048: (237, 194, 46)
}


def timer():
    global Timer, Clock
    Timer += 1
    Clock = threading.Timer(1, timer)
    Clock.start()


def showNum(Matrix, screen):
    for x in range(4):
        for y in range(4):
            grid_rect = pg.Rect(0, 0, GridWidth - 4, GridWidth - 4)
            grid_rect.center = ((x + 1) * GridWidth - GridWidth / 2, (y + 1) * GridWidth - GridWidth / 2)
            value = Matrix[x][y]
            grid_color = COLORDIR[value]
            text_color = (4, 4, 4)
            fontSize = 80 - 2 * math.log2(value) if value >= 2 else 0
            font = pg.font.SysFont(None, int(fontSize))
            text_img = font.render(str(int(value)), True, text_color)
            text_img_rect = text_img.get_rect()
            text_img_rect.center = grid_rect.center
            screen.fill(grid_color, grid_rect)
            if value != 0:
                screen.blit(text_img, text_img_rect)


def create_button(screen, p_x, p_y, rect_color, width, lenght, msg, msg_color):
    button_img = pg.Rect(0, 0, width, lenght)
    button_img.centerx = p_x + width / 2
    button_img.top = p_y
    button_color = rect_color
    msg_str = msg
    msg_size = 80 - 4 * len(msg_str)
    msg_color = msg_color
    font = pg.font.SysFont(None, int(msg_size))
    msg_img = font.render(msg_str, True, msg_color)
    msg_rect = msg_img.get_rect()
    msg_rect.center = button_img.center

    screen.fill(button_color, button_img)
    screen.blit(msg_img, msg_rect)
    return button_img


def show_menu(screen, score, if_end, now_time):
    score_button = Button(screen, 600, 100, (255, 255, 255), 200, 80, str(score), (220, 20, 60))
    time_button = Button(screen, 600, 260, (255, 255, 255), 200, 80, str(now_time), (240, 20, 100))

    score_button.draw()
    time_button.draw()
    if not if_end:
        game_over = Button(screen, 0, 0, (240, 230, 140), 600, 600, "Game Over", (165, 42, 42))
        game_over.draw()


def game_init():
    pg.init()
    ai_settings = Settings()
    screen = pg.display.set_mode((ai_settings.ScreenWidth, ai_settings.ScreenHeight))
    pg.display.set_caption("Game 2048")
    button_group.add(Button(screen, 600, 0, (127, 127, 127), 200, 100, "Score:", (0, 0, 0)))
    button_group.add(Button(screen, 600, 180, (127, 127, 127), 200, 80, "Time Used:", (0, 0, 0)))
    button_group.add(Button(screen, 600, 340, (31, 31, 31), 200, 60, " New Game", (240, 240, 240)))
    button_group.add(Button(screen, 600, 405, (31, 31, 31), 200, 60, "Auto Play", (240, 240, 240)))
    button_group.add(Button(screen, 600, 470, (31, 31, 31), 200, 60, " Setting ", (240, 240, 240)))
    button_group.add(Button(screen, 600, 535, (31, 31, 31), 200, 60, "  Exit   ", (240, 240, 240)))
    return (screen, ai_settings)


def run_game():
    screen, ai_settings = game_init()
    clock = pg.time.Clock()
    now_time = 0
    game_start = False
    gameCommand.newNum()
    gameCommand.newNum()
    start_time = pg.time.get_ticks()
    while True:
        screen.fill((230, 230, 230))
        Matrix = gameCommand.MaList.transpose()
        SCORE = gameCommand.SCORE
        IfEnd = gameCommand.canMove()
        showNum(Matrix, screen)
        show_menu(screen, SCORE, IfEnd, now_time)
        for button in button_group:
            button.draw()
        game_func.check_event(gameCommand, button_group)
        now_time = (pg.time.get_ticks() - start_time) // 1000  # 计时器
        pg.display.flip()
        clock.tick(30)


if __name__ == '__main__':
    run_game()
