import time
import numpy as np
from board import Board

board_size = (100,100)

board = Board(board_size)
# board.plot_board()

# # Test turns
# board.move_and_plot((0,1), Board.LEFT)
# board.move_and_plot((1,0), Board.UP)
# board.move_and_plot((1,1), Board.LEFT)
# board.move_and_plot((2,1), Board.LEFT)
# board.move_and_plot((2,0), Board.UP)

# board.revert_and_plot()
# board.revert_and_plot()
# board.revert_and_plot()
# board.revert_and_plot()
# board.revert_and_plot()

moves = list(board.legal_moves)
l = len(moves)
for (pos, side) in np.random.permutation(moves):
    board.move(pos, side)