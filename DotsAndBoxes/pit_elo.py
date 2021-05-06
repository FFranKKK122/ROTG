import Arena_elo
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

human_vs_cpu = False


g = DotsAndBoxesGame(3)

# all players
rp = RandomPlayer(g).play
hp = HumanPlayer(g).play

iters = [1,11,23,34,43,50,60,70,83,90,101,110,122,131,140,152,160,171,183,190,203,210,221,229,243,
        250,260,271,282,290,303,309]
iters_ori = [1,11,22,31,41,50,59,69,80,90,101,110,122,130,140,153,160,170,181,190,200,211,221,231,240]

for i in range( 1 , len(iters) ):
    # nnet players
    n1 = NNet(g)
    weight1 = 'checkpoint_' + str(iters[i]) + '.pth.tar'
    n1.load_checkpoint('./pretrained_models/exact_win/', weight1)
    args1 = dotdict({'numMCTSSims': 400, 'cpuct':3.75})
    mcts1 = MCTS(g, n1, args1)
    n1p = lambda x: np.argmax(mcts1.getActionProb(x, temp=0))
    if human_vs_cpu:
        player2 = hp
    else:
        n2 = NNet(g)
        weight2 = 'checkpoint_' + str(iters[i-1]) + '.pth.tar'
        # weight2 = 'checkpoint_' + str(iters_ori[i]) + '.pth.tar'
        n2.load_checkpoint('./pretrained_models/exact_win/',weight2)
        args2 = dotdict({'numMCTSSims': 400, 'cpuct': 3.75})
        mcts2 = MCTS(g, n2, args2)
        n2p = lambda x: np.argmax(mcts2.getActionProb(x, temp=0))
        player2 = n2p  # Player 2 is neural network if it's cpu vs cpu.

    p1_name = str(iters[i]) + '-exact_win_400'
    p2_name = str(iters[i-1]) + '-exact_win_400'
    # p2_name = str(iters_ori[i]) + '-ori'
    arena = Arena_elo.Arena_elo(n1p, player2, g, p1_name, p2_name, display=DotsAndBoxesGame.display)
    print(arena.playGames(100, verbose=False))

script_name = './log/script.txt'
f = open(script_name, 'a')
f.write('elo\n')
f.write('mm\n')
f.write('exactdist\n')
f.write('ratings\n\n')
f.close()
