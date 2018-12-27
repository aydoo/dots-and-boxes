import time
import numpy as np
from board import Board
from alpha_beta import alpha_beta
from convnet import ConvNet
import random
# import cProfile
# profile = cProfile.Profile()
# profile.enable()

def generate_games(path, num = 1, size=(5,5), alpha_beta_max_depth = 4):
    logs=[]
    for i in range(num):
        print(i)
        log_move = []
        # log_turn = []
        board = Board(size=size)

        # Random first 4 moves
        for i in range(6):
            random_move = random.choice(list(board.legal_moves))
            log_move.append(random_move)
            # log_turn.append(log_turn)
            board.move_dirty(random_move)

        while(not board.check_game_over()):
            move = alpha_beta(board, board.turn, alpha_beta_max_depth)
            log_move.append(move)
            # log_turn.append(board.turn)
            board.move_dirty(move)
        
        logs.append(log_move)
        # logs.append(log_turn)
        logs.append(list(board.score.values()))

    f = open(path, 'a')
    for i in logs:
        f.write(str(i)[1:-1]+'\n')
    f.close()

def load_games(path, size):
    f = open(path, 'r')
    lines = f.readlines()
    f.close()
    game_moves = lines[0::2][:100]
    game_results = lines[1::2][:100]

    X = {}
    X['board'] = []
    X['turn'] = []
    y = []
    print(f'Loading {len(game_moves)} games...')
    for g in range(len(game_moves)):
        board = Board(size, borders=True)
        for m in eval(game_moves[g]):
            board.move_dirty(m)
            X['board'].append(board.board.copy())
            X['turn'].append(board.turn)
            y.append(np.matrix(eval(game_results[g])) // max(eval(game_results[g])))
    print('Done.')
    X['board'] = np.array(X['board'])
    shape = X['board'].shape
    X['board'] = X['board'].reshape((shape[0],shape[1],shape[2],1))
    X['turn'] = np.array(X['turn'])
    y = np.array(y)
    y = y.reshape((y.shape[0], y.shape[2]))
    return X, y

##########################################################
##########################################################
##########################################################

size = (5,5)
path = rf'games/games_{size[0]}x{size[1]}.txt'
num = 1000
depth = 4

#generate_games(path, num, size, depth)

X, y = load_games(path, size)

net = ConvNet((size[0]*2+1,size[1]*2+1))

hist = net.train(X,y, batch_size=40)

print(hist)