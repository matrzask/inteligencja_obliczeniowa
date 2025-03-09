from easyAI import Negamax
from ClumsyConnectFour import ClumsyConnectFour 
from ConnectFour import ConnectFour
from Simulate import simulate_games
from NegamaxNoAlphaBeta import NegamaxNoAlphaBeta

num_games = 10
depths = [(4, 4), (4, 6), (6, 4), (6, 6)]

print("Deterministic Connect Four:")
for depth1, depth2 in depths:
    ai_algo1 = Negamax(depth1)
    ai_algo2 = NegamaxNoAlphaBeta(depth2)
    wins, avg_time_ai1, avg_time_ai2 = simulate_games(ConnectFour, ai_algo1, ai_algo2, num_games)
    print(f"Depth {depth1} (with alpha-beta) vs Depth {depth2} (without alpha-beta): Player 1 wins: {wins[0]}, Player 2 wins: {wins[1]}")
    print(f"Average time per move: Player 1: {avg_time_ai1:.4f}s, Player 2: {avg_time_ai2:.4f}s")

print("\nClumsy Connect Four:")
for depth1, depth2 in depths:
    ai_algo1 = Negamax(depth1)
    ai_algo2 = NegamaxNoAlphaBeta(depth2)
    wins, avg_time_ai1, avg_time_ai2 = simulate_games(ClumsyConnectFour, ai_algo1, ai_algo2, num_games)
    print(f"Depth {depth1} (with alpha-beta) vs Depth {depth2} (without alpha-beta): Player 1 wins: {wins[0]}, Player 2 wins: {wins[1]}")
    print(f"Average time per move: Player 1: {avg_time_ai1:.4f}s, Player 2: {avg_time_ai2:.4f}s")