import numpy as np
import random
from grid import Grid


class Status():
    def __init__(self, settings):
        self.Matrix = np.zeros((settings.gridNumLine, settings.gridNumLine))  # 记录每个格子的数值矩阵
        self.nowMatrix = np.empty((settings.gridNumLine, settings.gridNumLine))  # 记录当前每个格子的数值
        self.maxNum = 0
        self.score = 0
        self.degree = settings.gridNumLine

    def update(self, tempMatrix):
        self.nowMatrix = tempMatrix

    def newNum(self):
        seed = 4 if random.random() > 0.9 else 2
        for line in self.Matrix.reshape(1, 16):
            templist = line
        zero_pos = [i for i, v in enumerate(templist) if v == 0]
        if len(zero_pos) > 0 and (self.nowMatrix - self.Matrix).any():
            pos = random.choice(zero_pos)
            templist[pos] = seed
            return (pos // 4, pos % 4, seed)
        else:
            return (-1, -1, -1)

    def getScore(self):
        pass

    # 检查行间是否有相等元素
    def checkLine(self, line):
        Len = len(line)
        for index in range(Len - 1):
            if line[index] == line[index + 1]:
                return True
        return False

    # 判断整体是否还有可移动方向
    def ifCanMove(self):
        rows = self.Matrix
        cols = self.Matrix.transpose()

        if not rows.all():
            return True
        else:
            for row in rows:
                if self.checkLine(row):
                    return True

    def moveZeroRight(self, line):
        tempLine = [i for i in line if i != 0]
        zeroNum = len(line) - len(tempLine)
        tempLine.extend([0] * zeroNum)
        return tempLine

    def moveZeroLeft(self, line):
        newLine = [i for i in line if i != 0]
        zeros = [0] * (len(line) - len(newLine))
        newLine = zeros + newLine
        return newLine

    def moveLineLeft(self, line):
        newLine = self.moveZeroRight(line)  # 先移动0
        # 把相邻的不是0的数相加
        for index in range(len(newLine) - 1):
            if newLine[index] != 0 and newLine[index] == newLine[index + 1]:
                newLine[index] += newLine[index + 1]
                newLine[index + 1] = 0
        newLine = self.moveZeroRight(newLine)
        return newLine

    def moveLineRight(self, line):
        newLine = self.moveZeroLeft(line)  # 先移动0
        # 把相邻的不是0的数相加
        for index in [3, 2, 1]:
            if newLine[index] != 0 and newLine[index] == newLine[index - 1]:
                newLine[index] += newLine[index - 1]
                newLine[index - 1] = 0
        newLine = self.moveZeroLeft(newLine)
        return newLine

    def moveLeft(self):
        if self.ifCanMove():
            for index in range(self.degree):
                self.Matrix[index] = self.moveLineLeft(self.Matrix[index])
            return True
        else:
            return False

    def moveRight(self):
        if self.ifCanMove():
            for index in range(self.degree):
                self.Matrix[index] = self.moveLineRight(self.Matrix[index])
            return True
        else:
            return False

    def moveUp(self):
        if self.ifCanMove():
            self.Matrix = self.Matrix.transpose()
            self.moveLeft()
            self.Matrix = self.Matrix.transpose()
            return True
        else:
            return False

    def moveDowm(self):
        if self.ifCanMove():
            self.Matrix = self.Matrix.transpose()
            self.moveRight()
            self.Matrix = self.Matrix.transpose()
            return True
        else:
            return False
