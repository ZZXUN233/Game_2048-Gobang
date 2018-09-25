def AlphBeta(depth, alpha, beta):
    if depth == 0:
        return Evaluate()
    GenerateLegalMoves()
    while MoveLeft():
        MakeNextMove()
        val = -AlphBeta(depth - 1, -beta, -alpha)
        UnmakeMove()
        if val >= beta:
            return beta
        if val > alpha:
            alpha = val
    return alpha
