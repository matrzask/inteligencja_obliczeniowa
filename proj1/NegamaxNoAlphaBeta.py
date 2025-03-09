inf = float("infinity")

def negamax(game, depth, origDepth, scoring):
    if (depth == 0) or game.is_over():
        return scoring(game) * (1 + 0.001 * depth)

    possible_moves = game.possible_moves()

    state = game
    if depth == origDepth:
        state.ai_move = possible_moves[0]
    
    bestValue = -inf
    unmake_move = hasattr(state, "unmake_move")

    for move in possible_moves:

        if not unmake_move:
            game = state.copy()  # re-initialize move

        game.make_move(move)
        game.switch_player()

        move_alpha = -negamax(game, depth - 1, origDepth, scoring)

        if unmake_move:
            game.switch_player()
            game.unmake_move(move)

        if bestValue < move_alpha:
            bestValue = move_alpha
            if depth == origDepth:
                state.ai_move = move
    
    return bestValue


class NegamaxNoAlphaBeta:
    def __init__(self, depth, scoring=None, win_score=+inf):
        self.scoring = scoring
        self.depth = depth
        self.win_score = win_score

    def __call__(self, game):
        """
        Returns the AI's best move given the current state of the game.
        """

        scoring = (
            self.scoring if self.scoring else (lambda g: g.scoring())
        )

        self.alpha = negamax(
            game,
            self.depth,
            self.depth,
            scoring
        )
        return game.ai_move