"""
Tic Tac Toe Player
"""

import math
import copy
import cst_exceptions as cste
import random


X = "X"
O = "O"
EMPTY = None

class Node():
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action
        


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

    x_count = [i for sub in board for i in sub].count(X)
    o_count = [i for sub in board for i in sub].count(O)

    if x_count == o_count: return X
    else: return O




def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """

    actions = set()
    actions = {(i,j) for i,sub in enumerate(board,0) for j,v in enumerate(sub,0) if v == EMPTY}

    return actions

    


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    board_new = copy.deepcopy(board) 

    if action not in actions(board=board): raise cste.InvalidMoveException

    board_new[action[0]][action[1]] = player(board=board)

    
    return board_new


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    curr_player = player(board=board)
    match curr_player:
        case "X": curr_player = "O"
        case "O": curr_player = "X"


    diag1, diag2 = [],[]
    #check horizontal and vertical win
    for i,row in enumerate(board):
        
        #check horizontal
        row_check = [c for c in row if c == curr_player]
        if len(row_check) == 3: return curr_player

        #check vertical
        col_check = []
        for j in range(3):
            
            if board[j][i] == curr_player: 
                col_check.append(board[j][i])

        if len(col_check) == 3: return curr_player
        
        #check diagonal
        
        if board[i][i] == curr_player: diag1.append(curr_player)
        if board[len(row)-1-i][i] == curr_player: diag2.append(curr_player)

    if len(diag1) == 3 or len(diag2) == 3: return curr_player

    return None



def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    return (False if winner(board) == None and len(actions(board)) > 0 else True)



def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    
    if terminal(board):
        winner_util = winner(board)
        
        match winner_util:
            case "X": winner_util = 1
            case "O": winner_util = -1
            case None: winner_util = 0

        return winner_util
    
    return False



def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    if terminal(board): return None
    #If the board is empty, open with a random move
    if board == initial_state(): return random.choice(list(actions(board)))

    actions_opt = []
    recommended_action = ()


    if player(board) == "X": 
        utility_opt, actions_opt, d = maxValue(board)
    else: 
        utility_opt, actions_opt, d = minValue(board)
    
    if len(actions_opt) > 0: 
        min_moves = 99
        recommended_action = ()

        for a in actions_opt:
            if a[1] < min_moves:
                min_moves = a[1]
                recommended_action = a[0]
        
    else: 
        print("choosing anything")
        recommended_action = actions(board).pop()

    
    
    return recommended_action


def maxValue(board, d=0):

    value = -2
    actionValues = []

    di = d + 1
    if terminal(board):
        
        return utility(board), actionValues, d

    
    for a in actions(board):
        
        min_val = minValue(result(board, a), d = di)
        value = max(value, min_val[0])

        # recommended action will always take first in action array. so optimal solutions are inserted ad pos 0, draw-solutions at the end. 
        if value == 1: 
            actionValues.insert(0,[a, min_val[2]])
            break
        elif value == 0: actionValues.append([a, 0])

    return value, actionValues, min_val[2]


def minValue(board, d=0):
    
    value = 2
    actionValues = []

    di = d + 1
    if terminal(board):
        return utility(board), actionValues, d
    
    
    for a in actions(board):
        min_val = maxValue(result(board, a), d = di)
        value = min(value, min_val[0])
        
        # recommended action will always take first in action array. so optimal solutions are inserted ad pos 0, draw-solutions at the end. 
        if value == -1: 
            actionValues.insert(0,[a,min_val[2]])
            break
        elif value == 0: actionValues.append([a, 0])

    return value, actionValues, min_val[2]


def print_board(board):
    print("\n")
    for r in board:
        print(r, end="\n")
    print("\n")





