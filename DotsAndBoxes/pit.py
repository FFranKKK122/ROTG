import Arena
from MCTS import MCTS
from MCTS_ori import MCTS_ori
from DotsAndBoxes.DotsAndBoxesGame import DotsAndBoxesGame
from DotsAndBoxes.DotsAndBoxesPlayers import *
from DotsAndBoxes.keras.NNet import NNetWrapper as NNet


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
n1 = NNet(g)
n1.load_checkpoint('./pretrained_models/exact_win/','checkpoint_282.pth.tar')
args1 = dotdict({'numMCTSSims': 800, 'cpuct':2.5})
mcts1 = MCTS(g, n1, args1)
n1p = lambda x: np.argmax(mcts1.getActionProb(x, temp=0))
if human_vs_cpu:
    player2 = hp
else:
    n2 = NNet(g)
    n2.load_checkpoint('./pretrained_models/temp/','1217-25-exact_win.pth.tar')
    args2 = dotdict({'numMCTSSims': 200, 'cpuct': 3.75})
    mcts2 = MCTS(g, n2, args2)
    n2p = lambda x: np.argmax(mcts2.getActionProb(x, temp=0))
    player2 = n2p  # Player 2 is neural network if it's cpu vs cpu.

#arena = Arena.Arena(n1p, player2, g, display=DotsAndBoxesGame.display)
arena = Arena.Arena(n1p, player2, g,display=DotsAndBoxesGame.display)
print(arena.playGames(2, verbose=True))
