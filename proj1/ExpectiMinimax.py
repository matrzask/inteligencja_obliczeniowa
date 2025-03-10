inf = float('infinity')
L = -100
U = 100

def expectiminimax(game, depth, origDepth, alpha, beta, move, scoring):
    current_player = game.current_player

    if (depth == 0) or game.is_over():
        if current_player == 1:
            return scoring(game) * (1 - 0.001 * depth)
        else:
            return -scoring(game) * (1 - 0.001 * depth)

    if move is not None: # chance node
        moves = game.random_moves(move)
        N = len(moves)
        a = N * (alpha - U) + U
        b = N * (beta - L) + L
        sum = 0
        for move in moves:
            AX = max(a, L)
            BX = min(b, U)

            game.force_move(move)
            game.switch_player()
            eval = expectiminimax(game, depth - 1, origDepth, AX, BX, None, scoring)
            game.undo_forced_move(move)
            game.switch_player()

            if eval <= a:
                return alpha
            if eval >= b:
                return beta
            
            sum += eval
            a += U - eval
            b += L - eval
        return sum / N
    elif current_player == 1: # maximizing player
        maxEval = -inf
        for move in game.possible_moves():
            eval = expectiminimax(game, depth, origDepth, alpha, beta, move, scoring)
            if eval > maxEval:
                maxEval = eval
                if depth == origDepth:
                    game.ai_move = move
        return maxEval
    else: # minimizing player
        minEval = inf
        for move in game.possible_moves():
            eval = expectiminimax(game, depth, origDepth, alpha, beta, move, scoring)
            if eval < minEval:
                minEval = eval
                if depth == origDepth:
                    game.ai_move = move
        return minEval


class ExpectiMinimax:
    def __init__(self, depth, scoring=None):
        self.depth = depth
        self.scoring = scoring

    def __call__(self, game):
        """
        Returns the AI's best move given the current state of the game.
        """

        scoring = (
            self.scoring if self.scoring else (lambda g: g.scoring())
        )

        self.alpha = expectiminimax(
            game,
            self.depth,
            self.depth,
            -inf,
            inf,
            None,
            scoring
        )
        return game.ai_move