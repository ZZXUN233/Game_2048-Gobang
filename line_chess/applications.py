from line_chess.grids import Grids
from line_chess.settings import Settings
from line_chess.chess import Chess
from line_chess.button import Button

from pygame.sprite import Group
import pygame
import sys
import numpy as np

BLACK = (0, 0, 0)
WHITE = (250, 250, 250)
game_status = {}
black_turn = True
me_list = []
ai_list = []
my_scores = {}
ai_scores = {}


def ai_chess(Matrix, game_status):
    rows = Matrix.shape[0]
    cols = Matrix.shape[1]
    all_wins, count, myWins, aiWins, my_score, ai_score = game_status.values()
    maxScore = 0
    ai_x, ai_y = 0, 0
    for row in range(rows):
        for col in range(cols):
            if Matrix[row][col] == 0:
                for k in range(count):
                    if k in all_wins[row][col].keys():
                        if myWins[k] == 1:
                            my_score[row][col] += 200
                        elif myWins[k] == 2:
                            my_score[row][col] += 400
                        elif myWins[k] == 3:
                            my_score[row][col] += 2000
                        elif myWins[k] == 4:
                            my_score[row][col] += 10000
                        # ai 落子
                        if aiWins[k] == 1:
                            ai_score[row][col] += 200
                        elif aiWins[k] == 2:
                            ai_score[row][col] += 400
                        elif aiWins[k] == 3:
                            ai_score[row][col] += 2000
                        elif aiWins[k] == 4:
                            ai_score[row][col] += 10000

                # 我方下棋
                if my_score[row][col] > maxScore:
                    maxScore = my_score[row][col]
                    ai_x = row
                    ai_y = col
                elif my_score[row][col] == maxScore:
                    if ai_score[row][col] > ai_score[ai_x][ai_y]:
                        ai_x = row
                        ai_y = col

                # ai开始下棋
                if ai_score[row][col] > maxScore:
                    maxScore = ai_score[row][col]
                    ai_x = row
                    ai_y = col
                elif ai_score[row][col] == maxScore:
                    if my_score[row][col] > my_score[ai_x][ai_y]:
                        ai_x = row
                        ai_y = col

    print((ai_x, ai_y))
    for k in range(count):
        if k in all_wins[ai_x][ai_y].keys():
            aiWins[k] += 1  # 此处一旦落子，ai在此处对饮的赢法中就加一个权重
            myWins[k] = 6  # 计算机一旦下子，此处人就不能赢了
            if not black_turn and Matrix[ai_x][ai_y] == 0:
                Matrix[ai_x][ai_y] = 1
            if aiWins[k] == 5:
                print("计算机赢了！")
    return (ai_x, ai_y)


def get_game_status(Matrix):
    count = 0
    rows = Matrix.shape[0]
    cols = Matrix.shape[1]
    all_wins = [[{} for _ in range(cols)] for _ in range(rows)]
    for row in range(rows):
        for col in range(cols - 4):
            for k in range(5):
                all_wins[row][col + k][count] = True
            count += 1
    # 记录竖线赢法
    for col in range(cols):
        for row in range(rows - 4):
            for k in range(5):
                all_wins[row + k][col][count] = True
            count += 1
    # 记录斜线赢法
    for row in range(rows - 4):
        for col in range(cols - 4):
            for k in range(5):
                all_wins[row + k][col + k][count] = True
            count += 1
    # 记录反斜线赢法
    for row in range(rows - 4):
        for col in reversed(range(4, cols)):
            for k in range(5):
                all_wins[row + k][col - k][count] = True
            count += 1
    print(count)
    # 用于记录在当前赢法下落了几颗子
    my_wins = [0 for _ in range(count)]
    ai_wins = [0 for _ in range(count)]
    my_score = np.zeros((rows, cols))
    ai_score = np.zeros((rows, cols))
    return {
        "all_wins": all_wins,
        "count": count,
        "my_wins": my_wins,
        "ai_wins": ai_wins,
        "my_score": my_score,
        "ai_score": ai_score}


def on_step(p_x, p_y, game_status):
    all_wins, count, myWins, aiWins, my_score, ai_score = game_status.values()
    for k in range(count):
        if k in all_wins[p_x][p_y].keys():
            myWins[k] += 1
            aiWins[k] = 0
            if myWins[k] == 5:
                print("你赢了！")
    return


def chess_event(screen, grids, Matrix, chess_group, button_group, game_status):
    global black_turn
    global me_list, ai_list, my_scores, ai_scores
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:  # 点击菜单的动作
            p_x, p_y = pygame.mouse.get_pos()
            if p_y > 800:
                for button in button_group:
                    if button.img.collidepoint(p_x, p_y):
                        if button.msg_str == "New Game":
                            # 全部置零
                            Matrix = np.zeros_like(Matrix)
                            chess_group.empty()
                        elif button.msg_str == "Back OneStep":
                            chess_group = chess_group[:len(chess_group) - 1]
                        elif button.msg_str == "Settings":
                            print("setting")
                        elif button.msg_str == "Exit Game":
                            sys.exit()

            else:  #
                p_x, p_y = round((p_x - grids.border) / grids.cell_width), round(
                    (p_y - grids.border) / grids.cell_width)
                if black_turn and Matrix[p_x][p_y] != 1:
                    Matrix[p_x][p_y] = 1
                    ####
                    me_list += list(game_status["all_wins"][p_x][p_y].keys())
                    for me_step in me_list:
                        my_scores[me_step] = game_status["my_wins"][me_step]
                        if me_step in ai_list:
                            print("ai此处不能胜%d" % me_step)
                            ai_list.remove(me_step)
                    print("我方落子后的可胜种类：%d" % len(me_list))
                    me_list.sort()
                    print(me_list)
                    ####
                    on_step(p_x, p_y, game_status)
                    chess_group.add(
                        Chess(screen, grids, BLACK,
                              (p_x * grids.cell_width + grids.border, p_y * grids.cell_width + grids.border)))
                    black_turn = not black_turn
                    (ai_x, ai_y) = ai_chess(Matrix, game_status)
                    ####
                    ai_list += list(game_status["all_wins"][ai_x][ai_y].keys())
                    for ai_step in ai_list:
                        ai_scores[ai_step] = game_status["ai_wins"][ai_step]
                        if ai_step in me_list:
                            print("我方此处不能胜：%d" % ai_step)
                            me_list.remove(ai_step)
                    ai_list.sort()
                    print("ai的可胜种类：%d" % len(ai_list))
                    print(ai_list)
                    ####
                    chess_group.add(
                        Chess(screen, grids, WHITE,
                              (ai_x * grids.cell_width + grids.border, ai_y * grids.cell_width + grids.border)))
                    black_turn = not black_turn



def get_button(screen):
    button_group = Group()
    button_group.add(Button(screen,
                            50, 800, (63, 63, 63), 100, 50, "New Game", (255, 255, 255)))
    button_group.add(Button(screen,
                            200, 800, (63, 63, 63), 100, 50, "Back OneStep", (255, 255, 255)))
    button_group.add(Button(screen,
                            400, 800, (63, 63, 63), 100, 50, "Settings", (255, 255, 255)))
    button_group.add(Button(screen,
                            600, 800, (63, 63, 63), 100, 50, "Exit Game", (255, 255, 255)))
    return button_group


def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 850))
    pygame.display.set_caption("Grid Games")
    bg_color = (191, 191, 191)
    settings = Settings()
    new_grid = Grids(screen, settings)
    Matrix = np.zeros((new_grid.rows + 1, new_grid.cols + 1))  # 记录每个位置是否已经落子
    chess_group = Group()
    button_group = get_button(screen)
    global game_status
    game_status = get_game_status(Matrix)
    while True:
        screen.fill(bg_color)
        new_grid.draw()
        for button in button_group:
            button.draw()
        for chess in chess_group:
            chess.down()
        chess_event(screen, new_grid, Matrix, chess_group, button_group, game_status)
        pygame.display.flip()


if __name__ == '__main__':
    main()
