class NegamaxNoAlphaBeta:
    def __init__(self, depth):
        self.depth = depth

    def __call__(self, game):
        return self.negamax(game, self.depth)

    def negamax(self, game, depth):
        if game.is_over() or depth == 0:
            return game.scoring()
        best_score = -float('inf')
        possible_moves = game.possible_moves()
        state = game
        unmake_move = hasattr(state, "unmake_move")
        for move in possible_moves:
            if not unmake_move:
                game = state.copy()  # re-initialize move
            game.make_move(move)
            score = -self.negamax(game, depth - 1)
            if unmake_move:
                game.unmake_move(move)
            if score > best_score:
                best_score = score
        return best_score