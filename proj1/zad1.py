from easyAI import AI_Player, Negamax
from ClumsyConnectFour import ClumsyConnectFour
from ConnectFour import ConnectFour

def play_game(game_class, depth1, depth2, start_player):
    ai_algo1 = Negamax(depth1)
    ai_algo2 = Negamax(depth2)
    players = [AI_Player(ai_algo1), AI_Player(ai_algo2)]
    game = game_class(players)
    game.current_player = start_player
    game.play(verbose=False)
    return 3 - game.current_player

def simulate_games(game_class, depth1, depth2, num_games):
    wins = [0, 0]
    for i in range(num_games):
        start_player = i % 2 + 1
        winner = play_game(game_class, depth1, depth2, start_player)
        wins[winner - 1] += 1
    return wins

num_games = 100
depths = [(2, 2), (2, 4), (4, 4)]

print("Deterministic Connect Four:")
for depth1, depth2 in depths:
    wins = simulate_games(ConnectFour, depth1, depth2, num_games)
    print(f"Depth {depth1} vs Depth {depth2}: Player 1 wins: {wins[0]}, Player 2 wins: {wins[1]}")

print("\nClumsy Connect Four:")
for depth1, depth2 in depths:
    wins = simulate_games(ClumsyConnectFour, depth1, depth2, num_games)
    print(f"Depth {depth1} vs Depth {depth2}: Player 1 wins: {wins[0]}, Player 2 wins: {wins[1]}")