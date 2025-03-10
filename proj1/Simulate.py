from easyAI import AI_Player
import time

def play_game(game_class, ai_algo1, ai_algo2, start_player):
    players = [AI_Player(ai_algo1), AI_Player(ai_algo2)]
    game = game_class(players)
    game.current_player = start_player

    p1_avg_time = 0
    p1_moves = 0
    p2_avg_time = 0
    p2_moves = 0
    while not game.is_over():
        #game.show()
        start_time = time.time()
        move = game.get_move()
        end_time = time.time()
        if game.current_player == 1:
            p1_avg_time += end_time - start_time
            p1_moves += 1
        else:
            p2_avg_time += end_time - start_time
            p2_moves += 1
        game.play_move(move)
    p1_avg_time /= p1_moves
    p2_avg_time /= p2_moves
    return 3 - game.current_player, p1_avg_time, p2_avg_time

def simulate_games(game_class, ai_algo1, ai_algo2, num_games):
    wins = [0, 0]
    p1_avg_time = 0
    p2_avg_time = 0
    for i in range(num_games):
        start_player = 1
        winner, p1_avg_game_time, p2_avg_game_time = play_game(game_class, ai_algo1, ai_algo2, start_player)
        p1_avg_time += p1_avg_game_time
        p2_avg_time += p2_avg_game_time
        wins[winner - 1] += 1
    p1_avg_time /= num_games
    p2_avg_time /= num_games
    return wins, p1_avg_time, p2_avg_time