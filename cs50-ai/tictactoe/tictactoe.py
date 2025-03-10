"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None

def initial_state():
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]

def player(board):
    xCounter = 0
    oCounter = 0
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == X:
                xCounter += 1
            elif board[i][j] == O:
                oCounter += 1
    if xCounter > oCounter:
        return O
    else:
        return X

def actions(board):
    possibleActions = set()
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == EMPTY:
                possibleActions.add((i, j))
    return possibleActions

def result(board, action):
    if action[0] < 0 or action[0] >= len(board) or action[1] < 0 or action[1] >= len(board[0]):
        raise ValueError("Action is out of bounds")
    if board[action[0]][action[1]] is not EMPTY:
        raise ValueError("Cell is already taken")
    result = copy.deepcopy(board)
    result[action[0]][action[1]] = player(board)
    return result

def winner(board):
    for row in board:
        if row[0] is not None and all(cell == row[0] for cell in row):
            return row[0]
    for col in range(3):
        if board[0][col] is not None and all(board[row][col] == board[0][col] for row in range(3)):
            return board[0][col]
    if board[0][0] is not None and board[0][0] == board[1][1] == board[2][2]:
        return board[0][0]
    if board[0][2] is not None and board[0][2] == board[1][1] == board[2][0]:
        return board[0][2]
    return None

def terminal(board):
    return winner(board) is not None or all(EMPTY not in row for row in board)

def utility(board):
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0

def minimax(board):
    if terminal(board):
        return None
    if player(board) == X:
        value, move = max_value(board)
    else:
        value, move = min_value(board)
    return move

def max_value(board):
    if terminal(board):
        return utility(board), None
    v = float('-inf')
    move = None
    for action in actions(board):
        aux, _ = min_value(result(board, action))
        if aux > v:
            v = aux
            move = action
            if v == 1:
                break
    return v, move

def min_value(board):
    if terminal(board):
        return utility(board), None
    v = float('inf')
    move = None
    for action in actions(board):
        aux, _ = max_value(result(board, action))
        if aux < v:
            v = aux
            move = action
            if v == -1:
                break
    return v, move
