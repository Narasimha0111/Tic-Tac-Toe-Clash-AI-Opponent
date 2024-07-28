"""
Tic Tac Toe Player
"""

import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    cnt_X = 0
    cnt_o = 0
    # Count X and O's on the game board
    for i in range(3):
        for j in range(3): 
            if board[i][j] == X:
                cnt_X += 1
            elif board[i][j] == O:
                cnt_o += 1

    if cnt_X == cnt_o:
        return X
    elif cnt_X > cnt_o:
        return O
    else:
        return X



def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    # Each action is represented as a tuple (i, j) where i corresponds to the row of the move (0, 1, or 2) and j corresponds to which cell in the row corresponds to the move (also 0, 1, or 2).
    actions = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == None:
                actions.add((i, j))
    
    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # If action is not a valid action for the board, the program should raise an exception
    if action not in actions(board):
        raise Exception("Invalid Action")
    
    #  Make a copy of the board (Important, else can run into some hard to debug state errors)
    new_board = [row[:] for row in board]

    # making move (i, j) on the board
    new_board[action[0]][action[1]] = player(board)

    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Return tictactoe winner if there is one
    for i in range(3):
        # Check rows
        if board[i][0] == board[i][1] == board[i][2]:
            if board[i][0] != None:
                return board[i][0]
        
        # Check columns
        if board[0][i] == board[1][i] == board[2][i]:
            if board[0][i] != None:
                return board[0][i]

    # Check Diagonals
    if board[0][0] == board[1][1] == board[2][2]:
        if board[0][0] != None:
            return board[0][0]
    if board[0][2] == board[1][1] == board[2][0]:
        if board[0][2] != None:
            return board[0][2]
    
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # Check if there is a winner
    if winner(board) != None:
        return True
    else:
        # Check if the board is full
        for i in range(3):
            for j in range(3):
                if board[i][j] == None:
                    return False
        return True

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0


def max_value(board, alpha, beta):
    """
    Returns the maximum value for the current player on the board 
    using alpha-beta pruning.
    """
    if terminal(board):
        return utility(board)
    v = -math.inf
    for action in actions(board):
        v = max(v, min_value(result(board, action), alpha, beta))
        alpha = max(alpha, v)
        if alpha >= beta:
            break
    return v

def min_value(board, alpha, beta):
    """
    Returns the minimum value for the current player on the board 
    using alpha-beta pruning.
    """
    if terminal(board):
        return utility(board)
    v = math.inf
    for action in actions(board):
        v = min(v, max_value(result(board, action), alpha, beta))
        beta = min(beta, v)
        if alpha >= beta:
            break
    return v

def minimax(board):
    """
    Returns the optimal action for the current player on the board 
    using the minimax algorithm with alpha-beta pruning.
    """
    if terminal(board):
        return None

    if player(board) == X:
        v = -math.inf
        opt_action = None
        for action in actions(board):
            new_value = min_value(result(board, action), -math.inf, math.inf)
            if new_value > v:
                v = new_value
                opt_action = action
        return opt_action
    
    elif player(board) == O:
        v = math.inf
        opt_action = None
        for action in actions(board):
            new_value = max_value(result(board, action), -math.inf, math.inf)
            if new_value < v:
                v = new_value
                opt_action = action
        return opt_action