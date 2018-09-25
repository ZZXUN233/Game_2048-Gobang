import math

# 最大最小搜索
BLACK = True
WHITE = False


# 判断起手方函数
def MinMax(depth, player):
    """
    根据起手方调用的深度搜索函数。
    :param depth: 向前搜索的深度
            player: 用于判断当前优先落子的身份
    :return: Max_search(depth)或Min_search(depth)
    """
    if player == WHITE:  # 白方是最大者
        return Max_search(depth)
    else:
        return Min_search(depth)


def Max_search(depth):
    best = -float("inf")
    if depth <= 0:
        return Evaluate()
    GenerateLegalMoves()
    while movesLeft():
        MakeNextMove()
        val = Min_search(depth - 1)
        UnMakeMove()
        if val > best:
            best = val
    return best


def Min_search(depth):
    best = float('inf')
    if depth <= 0:
        return Evaluate()    #直接根据当前局面做判断并执行操作
    GenerateLegalMoves()    # 判断出后续的可能移动情况
    while MovesLeft():      #
        MakeNextMove()
        val = Max_search(depth - 1)
        UnMakeMove()
        if val < best:
            best = val
    return best
