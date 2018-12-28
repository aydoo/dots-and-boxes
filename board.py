import numpy as np
import matplotlib.pyplot as plt

class Board:
    UP = 1
    LEFT = 0
    
    def __init__(self, size=(5,5), borders=True):
        self.num_players = 2
        self.score = {1:0,-1:0}
        self.turn = 1
        self.size = size
        self.board = np.zeros((size[0]*2+1,size[1]*2+1), dtype='int8')

        # Track whether game is over
        self.max_turns = (size[0] * (size[1] + 1)) + ((size[0] + 1) * size[1])
        self.turn_num = 0

        if borders: self.set_borders()
        self.move_type_lookup = {}
        self.legal_moves = self.init_legal_moves(borders)

        # Vars to save state for reverting
        self.prev_scores = []
        self.prev_turns = []
        self.prev_turn_nums = []
        self.prev_moves = []

    def set_borders(self):
        self.board[0,1::2] = 1 
        self.board[-1,1::2] = 1
        self.board[1::2,0] = 1
        self.board[1::2,-1] = 1
        self.max_turns -= sum(self.size) * 2

    def init_legal_moves(self, borders):
        legal_moves = set()
        for x in range(0+2*borders,self.size[0]*2+1-borders,2):
            for y in range(1,self.size[1]*2+1,2):
                self.move_type_lookup[(x,y)] = 'H'
                legal_moves.add((x,y))
        for x in range(1,self.size[0]*2+1,2):
            for y in range(0+2*borders,self.size[1]*2+1-borders,2):
                self.move_type_lookup[(x,y)] = 'W'
                legal_moves.add((x,y))
        return legal_moves

    def move_dirty(self, move):
        self.save_cur_state(move)
        self.legal_moves.remove(move)
        self.board[move] = 1
        points_gained = self.get_points_gained(move)
        for p in points_gained: 
            self.score[self.turn] += 1
            self.board[p] = self.turn
        if(len(points_gained) == 0):
            self.next_turn()
        self.turn_num += 1
        return True

    def move(self, move):
        print(f'[{self.turn}] Move: {move}')
        if move in self.legal_moves:
            self.save_cur_state(move)
            self.legal_moves.remove(move)
            self.board[move] = 1
            points_gained = self.get_points_gained(move)
            for p in points_gained: 
                self.score[self.turn] += 1
                self.board[p] = self.turn
            if(len(points_gained) == 0):
                self.next_turn()
            self.turn_num += 1
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
        if self.move_type_lookup[move] == 'H':
            self.board[(move[0]-1,move[1])] = 0
            self.board[(move[0]+1,move[1])] = 0
        else:
            self.board[(move[0],move[1]-1)] = 0
            self.board[(move[0],move[1]+1)] = 0
    def revert_and_plot(self):
        self.revert()
        self.print_board()

    def next_turn(self):
        self.turn = -self.turn

    def check_game_over(self):
        return self.turn_num >= self.max_turns

    def winners(self):
        if self.check_game_over():
            return [i for i in self.score.keys() if self.score[i] >= max(self.score.values())]

    def get_points_gained(self, move):
        r = set()
        if self.move_type_lookup[move] == 'H':
            if self.check_box_complete((move[0]-1,move[1])): r.add((move[0]-1,move[1]))
            if self.check_box_complete((move[0]+1,move[1])): r.add((move[0]+1,move[1]))
        else:
            if self.check_box_complete((move[0],move[1]-1)): r.add((move[0],move[1]-1))
            if self.check_box_complete((move[0],move[1]+1)): r.add((move[0],move[1]+1))
        return r
    
    def check_box_complete(self, pos):
        try: return self.board[pos[0]-1,pos[1]] and \
                    self.board[pos[0]+1,pos[1]] and \
                    self.board[pos[0],pos[1]-1] and \
                    self.board[pos[0],pos[1]+1]
        except: return False

    def move_and_plot(self, move):
        self.move(move)
        self.print_board()

    def print_board(self):
        print(f'Turn: {self.turn} ({self.turn_num}/{self.max_turns})')
        print(f'Points: {self.score}')
        for x in range(0, self.size[0]*2, 2):
            h_row = '.'
            v_row = ''
            for y in range(0, self.size[1]*2, 2):
                h_row += f' {"_" if self.board[(x,y+1)] else " "} .'
                occupied = self.board[x+1,y+1] if self.board[x+1,y+1] != 0 else ' '
                v_row += f'{"|" if self.board[(x+1,y)] else " "}{" "+str(occupied) if occupied != -1 else occupied} '
            print(h_row)
            print(v_row + f'{"|" if self.board[(x+1,self.size[1]*2)] else " "}')
        print('.'+''.join([f' {"_" if self.board[(self.size[0]*2,y+1)] else " "} .' for y in range(0, self.size[1]*2, 2)]))
        print('#'*20)
        if self.check_game_over():
            print(f'Game Over.')
            print(f'Score: {self.score}')
            print(f'Winner(s): {self.winners()}')

