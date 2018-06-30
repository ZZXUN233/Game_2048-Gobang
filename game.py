import sys
import numpy as np
import random
import pygame

# 初始化矩阵
# 在空位置生成随机2或4
# 在判断矩阵的可以消除方向
# 特定的消除方向上的消除

MaList = np.zeros((4, 4))


# 在空位随机生成2或4
def newNum():
    global MaList
    seed = 4 if random.random() > 0.9 else 2
    # 找到这个系列中所有0的位置
    for line in MaList.reshape(1, 16):
        tempList = line
    zero_pos = [i for i, v in enumerate(tempList) if v == 0]
    if len(zero_pos) > 0:
        tempList[random.choice(zero_pos)] = seed
        MaList = np.array(tempList, np.int).reshape(4, 4)
        return True
    else:
        return False


def checkLine(line):
    Len = len(line)
    for index in range(Len - 1):
        if line[index] == line[index + 1]:
            return True
    return False


def moveZero(line):
    newLine = [i for i in line if i != 0]
    zeroNum = len(line) - len(newLine)
    newLine.extend([0] * zeroNum)
    return newLine


def moveLine(line):
    newLine = moveZero(line)  # 先移动0
    # 把相邻的不是0的数相加
    for index in range(len(newLine) - 1):
        if newLine[index] != 0 and newLine[index] == newLine[index + 1]:
            newLine[index] += newLine[index + 1]
            newLine[index + 1] = 0
    newLine = moveZero(newLine)
    return newLine


# 判断各个方向是否可移动,不可移动时游戏结束
def canMove():
    rows = MaList.reshape(4, 4).tolist  # 将原本的16个数变换为矩阵
    cols = rows.transpose().tolist  # 转置后的每一行就是列
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
    pass


def moveRight():
    pass


def moveUp():
    pass


def moveDown():
    pass


def checkEvent():
    try:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.type == pygame.K_a:
                    moveLeft()
                elif event.type == pygame.K_d:
                    moveRight()
                elif event.type == pygame.K_w:
                    moveUp()
                elif event.type == pygame.K_s:
                    moveDown()
    except:
        print("不合法的键盘输入！")


def Main():
    newNum()
    while True:
        if not canMove():  # 不能再滑动了
            print("游戏结束！")
            break
        else:
            checkEvent()
            # 打印查看状态
            print(MaList)


if __name__ == '__main__':
    for i in range(10):
        newNum()
    print(MaList)

    for i in [0,1,2,3]:
        MaList[i] = moveLine(MaList[i])
    print(MaList)
