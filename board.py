import numpy as np
import matplotlib.pyplot as plt

class Board:
    UP = 1
    LEFT = 0
    
    def __init__(self, size, borders=True, num_players=2):
        self.num_players = num_players
        self.points = [0] * num_players
        self.turn = 0
        self.size = size
        self.board = np.zeros((size[0]+1,size[1]+1, 2), dtype='bool_')

        # Track whether game is over
        self.max_turns = (size[0] * (size[1] + 1)) + ((size[0] + 1) * size[1])
        self.turn_num = 0
        self.point_matrix = np.full((size[0]+1,size[1]+1), None)

        if borders: self.setBorders()

    def setBorders(self):
        self.board[0,:-1,self.UP] = 1 
        self.board[-1,:-1,self.UP] = 1 
        self.board[:-1,0,self.LEFT] = 1
        self.board[:-1,-1,self.LEFT] = 1
        self.max_turns -= sum(self.size) * 2

    def move(self, pos, side):
        if self.board[pos][side] == 0:
            self.board[pos][side] = 1
            points_gained = self.get_points_gained(pos, side)
            for p in points_gained: 
                self.points[self.turn] += 1
                self.point_matrix[p] = self.turn
            else:
                self.turn = (self.turn + 1) % self.num_players
            self.turn_num += 1
            if (self.turn_num >= self.max_turns):
                print(f'Game Over. Winner: {[i for i in range(self.num_players) if self.points[i] >= max(self.points)]}')
            return True
        else:
            return False
    
    def get_points_gained(self, pos, side):
        result = set()
        if self.check_box_complete(pos):
            result.add(pos)
        neighbour = self.get_neighbour(pos, side)
        if self.check_box_complete(neighbour):
            result.add(neighbour)
        return result

    def get_neighbour(self, pos, side):
        if side == self.UP:
            return (pos[0] - 1, pos[1])
        else:
            return (pos[0], pos[1] - 1)

    def check_box_complete(self, pos):
        return np.all(self.board[pos]) and \
           self.board[pos[0], pos[1] + 1, self.LEFT] and \
           self.board[pos[0] + 1, pos[1], self.UP]

    def move_and_plot(self, pos, side):
        self.move(pos, side)
        self.plot_board()

    def plot_board(self):
        print('#'*20)
        print(f'Turn: {self.turn} ({self.turn_num}/{self.max_turns})')
        print(f'Points: {self.points}')
        for x in range(self.size[0] + 1):
            up_row = ''
            left_row = ''
            for y in range(self.size[1] + 1):
                occupied = self.point_matrix[x,y] if self.point_matrix[x,y] is not None else ' '
                up_row += f'. {"_" if self.board[(x,y,self.UP)] else " "} '
                left_row += f'{"|" if self.board[(x,y,self.LEFT)] else " "} {occupied} '
            print(up_row)
            print(left_row)           