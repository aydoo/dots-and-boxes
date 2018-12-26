import time
import numpy as np
from board import Board
from board_2 import Board_2
from ai import alpha_beta
import random

import cProfile

profile = cProfile.Profile()
profile.enable()

# board_2 = Board_2(size=(3,3), borders = 1)
# # board_2.move_and_plot((1,0))
# # board_2.move_and_plot((0,1))
# board_2.move_and_plot((2,1))
# board_2.move_and_plot((1,2))

# print(board_2.legal_moves)
# print(len(board_2.legal_moves))
for i in range(1):
    size=(6,6)
    board_ai = Board_2(size=size)
    board_play = Board_2(size=size)

    # Random first 4 moves
    for i in range(4):
        random_move = random.choice(list(board_play.legal_moves))
        board_ai.move_and_plot(random_move)
        board_play.move_and_plot(random_move)

    while(not board_ai.check_game_over()):
        if(board_ai.turn == 1):
            move = alpha_beta(board_ai, 1, 4)
            # move = random.choice(list(board.legal_moves))#eval(input())
        else:
            move = alpha_beta(board_ai, -1, 4)
        board_ai.move_dirty(move)
        board_play.move_and_plot(move)

profile.disable()
profile.print_stats(sort='cumtime')