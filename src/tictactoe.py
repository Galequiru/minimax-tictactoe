from copy import deepcopy
from functools import cache

X: str = 'X'
O: str = 'O'
EMPTY = None
Board = tuple[tuple[str, str, str], tuple[str, str, str], tuple[str, str, str]]

def initial_state() -> Board:
    '''
    returns starting state of the board.
    '''
    return tuple(
        (EMPTY, EMPTY, EMPTY) for _ in range(3)
    )

def player(board: Board) -> str:
    '''
    returns player who has the next turn on a board.
    '''
    # number of X - number of O in the board
    counter = sum((row.count(X) - row.count(O)) for row in board)

    # if counter is bigger than 0, there are more X than O
    return O if counter > 0 else X

def actions(board: Board) -> set[tuple[int, int]]:
    '''
    returns set of all possible actions (i, j) available on the board.
    '''
    return {(i, j)
        for i, row in enumerate(board)
        for j, cell in enumerate(row) if cell == EMPTY
    }

def result(board: Board, action: tuple[int, int], currentPlayer: str = None) -> Board:
    '''
    returns the board that results from making move (i, j) on the board.
    '''
    # only iterates the entire board if necessary
    if currentPlayer == None: currentPlayer = player(board)

    return tuple(
        tuple(
            cell if (i, j) != action else currentPlayer
            for j, cell in enumerate(row)
        )
        for i, row in enumerate(board)
    )

def winner(board: Board) -> str:
    '''
    returns the winner of the game, if there is one.
    '''
    # check rows and columns
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != EMPTY or \
           board[0][i] == board[1][i] == board[2][i] != EMPTY:
            return board[i][i]

    # check diagonals
    if board[0][0] == board[1][1] == board[2][2] != EMPTY or \
       board[0][2] == board[1][1] == board[2][0] != EMPTY: 
        return board[1][1]
    
    return None

def terminal(board: Board) -> bool:
    '''
    returns True if game is over, False otherwise.
    '''
    # if there's a winner, the game is over
    if winner(board) != None: return True

    # if there are no empty cells, returns true
    return sum(row.count(EMPTY) for row in board) == 0

def utility(board: Board) -> int:
    '''
    returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    '''
    match winner(board):
        case "X": return 1
        case "O": return -1
        case _: return 0

def minimax(board: Board) -> tuple[int, int]:
    '''
    returns the optimal action for the current player on the board.
    '''
    bot = player(board)

    # calculates the value of each possible action
    actionValuePairs = [(action, actionValue(board, action, bot)) for action in actions(board)]

    # sort the actions by their values
    actionValuePairs.sort(key= lambda pair: pair[1])

    # return the action that gives maximum value to the bot
    if bot == X: return actionValuePairs[-1][0]
    return actionValuePairs[0][0]

@cache
def actionValue(board: Board, action: tuple[int, int], currentPlayer: str) -> int:
    '''
    return 1 if action leads to an X win, -1 if leads to an O win, otherwise 0
    '''
    outcome = result(board, action, currentPlayer)

    # if the action end the game, return the value of the winner
    if terminal(outcome): return utility(outcome)

    # calculates the value of each action that the oponent can take
    oponentActionValues = [
        actionValue(outcome, newAction, O if currentPlayer == X else X)
        for newAction in actions(outcome)
    ]

    # if was maximizing, now minimizes, and vice-versa
    if currentPlayer == X: 
        return min(oponentActionValues)
    return max(oponentActionValues)