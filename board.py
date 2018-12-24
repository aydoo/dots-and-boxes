import numpy as np
import matplotlib.pyplot as plt

class Board:
    UP = 1
    LEFT = 0
    
    def __init__(self, size, borders=True, num_players=2):
        self.num_players = num_players
        self.score = [0] * num_players
        self.turn = 0
        self.size = size
        self.board = np.zeros((size[0]+1,size[1]+1, 2), dtype='bool_')

        # Track whether game is over
        self.max_turns = (size[0] * (size[1] + 1)) + ((size[0] + 1) * size[1])
        self.turn_num = 0
        self.point_matrix = np.full((size[0]+1,size[1]+1), None)

        if borders: self.set_borders()
        self.legal_moves = self.init_legal_moves()

        # Vars to save state for reverting
        self.prev_scores = []
        self.prev_turns = []
        self.prev_turn_nums = []
        self.prev_moves = []

    def set_borders(self):
        self.board[0,:,self.UP] = 1 
        self.board[-1,:,:] = 1 
        self.board[:,0,self.LEFT] = 1
        self.board[:,-1,:] = 1
        self.max_turns -= sum(self.size) * 2

    def init_legal_moves(self):
        legal_moves = np.where(self.board == 0)
        return set((x,y,side) for x,y,side in zip(*legal_moves))

    def move_dirty(self, move):
        self.save_cur_state(move)
        self.legal_moves.remove(move)
        self.board[move] = 1
        points_gained = self.get_points_gained(move)
        for _ in points_gained: 
            self.score[self.turn] += 1
        if(len(points_gained) == 0):
            self.next_turn()
        self.turn_num += 1
        return True

    def move_verbose(self, move):
        print(f'[{self.turn}] Move: {(move[0], move[1])} {"UP" if move[2] == self.UP else "LEFT"}')
        if move in self.legal_moves:
            self.save_cur_state(move)
            self.legal_moves.remove(move)
            self.board[move] = 1
            points_gained = self.get_points_gained(move)
            for p in points_gained: 
                self.score[self.turn] += 1
                self.point_matrix[p] = self.turn
            if(len(points_gained) == 0):
                self.next_turn()
            self.turn_num += 1
            self.check_game_over()
            return True
        else:
            print('ILLEGAL MOVE PLAYED!')
            return False

    def save_cur_state(self, move):
        self.prev_scores.append(self.score.copy())
        self.prev_turns.append(self.turn)
        self.prev_turn_nums.append(self.turn_num)
        self.prev_moves.append(move)

    def revert(self):
        #print('REVERTING')
        self.score = self.prev_scores.pop()
        self.turn = self.prev_turns.pop()
        self.turn_num = self.prev_turn_nums.pop()
        move = self.prev_moves.pop()
        self.legal_moves.add(move)
        self.board[move] = 0
        
    def revert_and_plot(self):
        self.revert()
        self.plot_board()

    def next_turn(self):
        self.turn = (self.turn + 1) % self.num_players

    def check_game_over(self):
        if (self.turn_num >= self.max_turns):
            # print(f'Game Over.')
            # print(f'Score: {self.score}')
            # print(f'Winner(s): {[i for i in range(self.num_players) if self.score[i] >= max(self.score)]}')
            return True
        else:
            return False


    def get_points_gained(self, move):
        pos_x, pos_y, _ = move
        pos = (pos_x, pos_y)
        result = set()
        if self.check_box_complete(pos):
            result.add(pos)
        neighbour = self.get_neighbour(move)
        if self.check_box_complete(neighbour):
            result.add(neighbour)
        return result

    def get_neighbour(self, move):
        pos_x, pos_y, side = move
        if side == self.UP:
            return (pos_x - 1, pos_y)
        else:
            return (pos_x, pos_y - 1)

    def check_box_complete(self, pos):
        return np.all(self.board[pos]) and \
           self.board[pos[0], pos[1] + 1, self.LEFT] and \
           self.board[pos[0] + 1, pos[1], self.UP]

    def move_and_plot(self, move):
        self.move_verbose(move)
        self.plot_board()

    def plot_board(self):
        print(f'Turn: {self.turn} ({self.turn_num}/{self.max_turns})')
        print(f'Points: {self.score}')
        for x in range(self.size[0] + 1):
            up_row = ''
            left_row = ''
            for y in range(self.size[1] + 1):
                occupied = self.point_matrix[x,y] if self.point_matrix[x,y] is not None else ' '
                up_row += f'. {"_" if self.board[(x,y,self.UP)] else " "} '
                left_row += f'{"|" if self.board[(x,y,self.LEFT)] else " "} {occupied} '
            print(up_row[:-2])
            if x < self.size[0]: print(left_row)  
        print('#'*20)