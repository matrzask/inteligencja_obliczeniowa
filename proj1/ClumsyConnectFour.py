from easyAI import TwoPlayerGame
import random

class ClumsyConnectFour(TwoPlayerGame):
    def __init__(self, players):
        self.players = players
        self.current_player = 1
        self.board = [ [0 for row in range(7)] for col in range(6)]
    
    def possible_moves(self):
        return [ i for i in range(7) if (self.board[0][i] == 0)]

    def random_moves(self, move):
        moves = [move]
        if move > 0 and self.board[0][move - 1] == 0:
            moves.append(move-1)
        if move < 6 and self.board[0][move + 1] == 0:
            moves.append(move+1)
        return moves

    def make_move(self, move):
        column = random.choice(self.random_moves(move))

        for i in range(5, -1, -1):
            if self.board[i][column] == 0:
                self.board[i][column] = self.current_player
                break
    
    def force_move(self, move):
        for i in range(5, -1, -1):
            if self.board[i][move] == 0:
                self.board[i][move] = self.current_player
                break

    def undo_forced_move(self, move):
        for i in range(6):
            if self.board[i][move] != 0:
                self.board[i][move] = 0
                break
    
    def lose(self):
        for row in range(6):
            for col in range(7):
                if self.board[row][col] == 3 - self.current_player:
                    for direction in [(0,1), (1,0), (1,1), (1,-1)]:
                        dx, dy = direction
                        for length in range(1, 4):
                            if 0 <= row + length * dy < 6 and 0 <= col + length * dx < 7 and self.board[row + length * dy][col + length * dx] == 3 - self.current_player:
                                if length == 3:
                                    return True
                            else:
                                break
        return False

    def is_over(self):
        return (self.possible_moves() == []) or self.lose()

    def scoring(self):
        return -100 if self.lose() else 0

    def show(self):
        for row in range(6):
            print(' '.join(['.' if self.board[row][col] == 0 else 'X' if self.board[row][col] == 1 else 'O' for col in range(7)]))
        print()