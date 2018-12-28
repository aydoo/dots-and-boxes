def value_simple(player):
    return board.score[player] - board.score[-player]

def value_convnet(player):
    return net.predict_single(board)[0][(player+2)%3]

def alpha_beta(_value, _board, player, _max_depth, _net=None):
    global value, saved_move, board, max_depth, net, counter
    value, saved_move, board, max_depth, net, counter = _value, None, _board, _max_depth, _net, 0
    alpha_beta_helper(player, max_depth, -10000, 10000)
    #print(f'Moves evaluated: {counter}')
    return saved_move

def alpha_beta_helper(player, depth, alpha, beta):
    global counter
    #if counter % 1000 == 0: print(counter)
    if depth == 0 or board.check_game_over():
        counter += 1
        return value(player)
    max_val = alpha
    moves = board.legal_moves.copy()
    for move in moves:
        board.move_dirty(move)
        if player != board.turn:
            val = -alpha_beta_helper(board.turn, depth-1, -beta, -max_val)
        else:
            val = alpha_beta_helper(board.turn, depth-1, alpha, beta)
        board.revert()
        if val > max_val:
            max_val = val
            if max_val >= beta:
                break
            if depth == max_depth:
                #print('new saved_move')
                global saved_move
                saved_move = move
    return max_val