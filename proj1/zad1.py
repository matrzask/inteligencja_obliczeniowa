from easyAI import Negamax
from ClumsyConnectFour import ClumsyConnectFour 
from ConnectFour import ConnectFour
from Simulate import simulate_games

num_games = 10
depths = [(4, 4), (4, 8), (8, 8)]

print("Deterministic Connect Four:")
for depth1, depth2 in depths:
    ai_algo1 = Negamax(depth1)
    ai_algo2 = Negamax(depth2)
    wins, _, _ = simulate_games(ConnectFour, ai_algo1, ai_algo2, num_games)
    print(f"Depth {depth1} vs Depth {depth2}: Player 1 wins: {wins[0]}, Player 2 wins: {wins[1]}")

print("\nClumsy Connect Four:")
for depth1, depth2 in depths:
    ai_algo1 = Negamax(depth1)
    ai_algo2 = Negamax(depth2)
    wins, _, _ = simulate_games(ClumsyConnectFour, ai_algo1, ai_algo2, num_games)
    print(f"Depth {depth1} vs Depth {depth2}: Player 1 wins: {wins[0]}, Player 2 wins: {wins[1]}")