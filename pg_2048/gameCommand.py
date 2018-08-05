import sys
import numpy as np
import random
import pygame

# 初始化矩阵
# 在空位置生成随机2或4
# 在判断矩阵的可以消除方向
# 特定的消除方向上的消除

MaList = np.zeros((4, 4))
nowMatrix = np.empty((4, 4))
SCORE = 0
game_history = []


def newGame():
    global MaList, nowMatrix, SCORE, game_history
    MaList = np.zeros((4, 4))
    nowMatrix = np.empty((4, 4))
    SCORE = 0
    game_history = []
    newNum()
    newNum()


# 在空位随机生成2或4
def newNum():
    global MaList, game_history
    global nowMatrix
    seed = 4 if random.random() > 0.9 else 2
    # 找到这个系列中所有0的位置
    for line in MaList.reshape(1, 16):
        tempList = line
    zero_pos = [i for i, v in enumerate(tempList) if v == 0]
    if len(zero_pos) > 0 and (nowMatrix - MaList).any():
        pos = random.choice(zero_pos)
        tempList[pos] = seed
        MaList = np.array(tempList, np.int).reshape(4, 4)
        if len(game_history) < 10:
            game_history.append(MaList)
        else:
            game_history = game_history[1:]
            game_history.append(MaList)
        return True
    else:
        return False


def checkLine(line):
    Len = len(line)
    for index in range(Len - 1):
        if line[index] == line[index + 1]:
            return True
    return False


def moveZeroRight(line):
    newLine = [i for i in line if i != 0]
    zeroNum = len(line) - len(newLine)
    newLine.extend([0] * zeroNum)
    return newLine


def moveZeroLeft(line):
    newLine = [i for i in line if i != 0]
    zeros = [0] * (len(line) - len(newLine))
    newLine = zeros + newLine
    return newLine


def moveLineLeft(line):
    global SCORE
    newLine = moveZeroRight(line)  # 先移动0
    # 把相邻的不是0的数相加
    for index in range(len(newLine) - 1):
        if newLine[index] != 0 and newLine[index] == newLine[index + 1]:
            newLine[index] += newLine[index + 1]
            SCORE += newLine[index]
            newLine[index + 1] = 0
    newLine = moveZeroRight(newLine)
    return newLine


def moveLineRight(line):
    global SCORE
    newLine = moveZeroLeft(line)  # 先移动0
    # 把相邻的不是0的数相加
    for index in [3, 2, 1]:
        if newLine[index] != 0 and newLine[index] == newLine[index - 1]:
            newLine[index] += newLine[index - 1]
            SCORE += newLine[index]
            newLine[index - 1] = 0
    newLine = moveZeroLeft(newLine)
    return newLine


# 判断各个方向是否可移动,不可移动时游戏结束
def canMove():
    rows = MaList  # 将原本的16个数变换为矩阵
    cols = rows.transpose()  # 转置后的每一行就是列
    if not rows.all():  # 只要有元素为空就可以消除
        return True
    else:
        # 逐行判断是否有相邻可消除
        for row in rows:
            if checkLine(row):
                return True

        # 逐列判断是否有相邻可消除
        for col in cols:
            if checkLine(col):
                return True

        return False


# 进行移动操作
def moveLeft():
    if canMove():
        for index in range(4):
            MaList[index] = moveLineLeft(MaList[index])
        return True
    else:
        return False


def moveRight():
    if canMove():
        for index in range(4):
            MaList[index] = moveLineRight(MaList[index])
        return True
    else:
        return False

    # 上下移动的时候先转置矩阵
    # 在进行同左右移动的操作
    # 再次转置矩阵


def moveUp():
    if canMove():
        global MaList
        MaList = MaList.transpose()
        moveLeft()
        MaList = MaList.transpose()
        return True
    else:
        return False


def moveDown():
    if canMove():
        global MaList
        MaList = MaList.transpose()
        moveRight()
        MaList = MaList.transpose()
        return True
    else:
        return False


def checkEvent():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.type == pygame.K_a:
                if moveLeft():
                    newNum()
            elif event.type == pygame.K_d:
                if moveRight():
                    newNum()
            elif event.type == pygame.K_w:
                if moveUp():
                    newNum()
            elif event.type == pygame.K_s:
                if moveDown():
                    newNum()


def Main():
    global nowMatrix
    newNum()
    print(MaList)
    str1 = ""
    while True:
        if not canMove():  # 不能再滑动了
            print("游戏结束！")
            print(MaList)
            break
        else:
            nowMatrix = MaList.copy()
        str1 = input("输入移动的方向：（q退出！）")
        if str1 == "w":
            if moveUp():
                newNum()
        elif str1 == "s":
            if moveDown():
                newNum()
        elif str1 == "a":
            if moveLeft():
                newNum()
        elif str1 == "d":
            if moveRight():
                newNum()
        elif str1 == "q":
            print(MaList)
            break
            # 打印查看状态
        else:
            pass
        print(MaList)


if __name__ == '__main__':
    Main()
