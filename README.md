# DotsAndBoxes with AI

An implementation of the game 'Dots and Boxes' with a alpha-beta / convnet based AI.

## Structure

The board W*H sized board is represented by a (W*2+1)*(H*2+1) matrix.

```
. _ . _ . _ . _ .
| 1 | 1 | 1 | 1 |
. _ . _ . _ . _ .
| 1 | 1 |   |-1 |
. _ . _ .   . _ .
|       |   |-1 |
.   .   . _ . _ .
|       |-1 |-1 |
. _ . _ . _ . _ .
```

A move is described as a tuple (x,y), which describes the coordinate of the 'line' which will be drawn.

## How to use

`Board(size, border)` - Initializes board of given size and optionally sets border (i.e. outer lines of board).\
`Board.legal_moves` - Holds the possible moves for the given boards state.\
`Board.move(m)` - Executes move `m`. Illegal moves get rejected.\
`Board.print_board_board()` - Prints board in stdout.\
`Board.dirty_move(m)` - Executes move `m` without checking for validity. (Reduces execution time and is mainly used by the AI.)\
`ai.alpha_beta(board, player, max_depth)` - Minimax algorithm with alpha-beta pruning to calculate a move for a specific `board`, `player` and `max_depth`.\
