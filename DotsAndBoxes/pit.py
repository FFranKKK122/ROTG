import Arena
from MCTS import MCTS
from DotsAndBoxes.DotsAndBoxesGame import DotsAndBoxesGame
from DotsAndBoxes.DotsAndBoxesPlayers import *
from pretrained_models.gann5.keras.NNet import NNetWrapper as NNet1
from pretrained_models.gann2.keras.NNet import NNetWrapper as NNet2


import numpy as np
from utils import *

"""
use this script to play any two agents against each other, or play manually with
any agent.
"""

human_vs_cpu = True


g = DotsAndBoxesGame(3)

# all players
rp = RandomPlayer(g).play
hp = HumanPlayer(g).play



# nnet players
n1 = NNet1(g)
n1.load_checkpoint('./pretrained_models/gann5/','checkpoint_2.pth.tar')
args1 = dotdict({'numMCTSSims': 200, 'cpuct':2.5})
mcts1 = MCTS(g, n1, args1)
n1p = lambda x: np.argmax(mcts1.getActionProb(x, temp=0))
if human_vs_cpu:
    player2 = rp
else:
    n2 = NNet2(g)
    n2.load_checkpoint('./pretrained_models/gann2/','checkpoint_19.pth.tar')
    args2 = dotdict({'numMCTSSims': 200, 'cpuct': 3.75})
    mcts2 = MCTS(g, n2, args2)
    n2p = lambda x: np.argmax(mcts2.getActionProb(x, temp=0))
    player2 = n2p  # Player 2 is neural network if it's cpu vs cpu.

#arena = Arena.Arena(n1p, player2, g, display=DotsAndBoxesGame.display)
arena = Arena.Arena(n1p, player2, g,display=DotsAndBoxesGame.display)
print(arena.playGames(100, verbose=False))
