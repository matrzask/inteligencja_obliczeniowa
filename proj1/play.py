from easyAI import AI_Player, Human_Player
from ConnectFour import ConnectFour
from NegamaxNoAlphaBeta import NegamaxNoAlphaBeta

ai = NegamaxNoAlphaBeta(4)
game = ConnectFour([Human_Player(), AI_Player(ai)])
game.play()