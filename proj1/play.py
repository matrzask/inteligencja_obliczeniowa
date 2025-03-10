from easyAI import AI_Player, Human_Player
from ClumsyConnectFour import ClumsyConnectFour
from ExpectiMinimax import ExpectiMinimax

ai = ExpectiMinimax(4)
game = ClumsyConnectFour([Human_Player(), AI_Player(ai)])
game.play()