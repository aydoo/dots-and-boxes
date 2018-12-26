# ChecksAndBoxes with AI

An implementation of the game 'Checks and Boxes' with an AI opponents

## Structure

###Board
(width*2+1)*(height*2+1) matrix

Example:
'''
. _ . _ . _ . _ .
| 1 | 1 | 1 | 1 |
. _ . _ . _ . _ .
| 1 | 1 |   |-1 |
. _ . _ .   . _ .
|       |   |-1 |
.   .   . _ . _ .
|       |-1 |-1 |
. _ . _ . _ . _ .
'''