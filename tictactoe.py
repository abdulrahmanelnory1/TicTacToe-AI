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

def emptyState(board):
    for i in range(3):
        for j in range(3):
            if board[i][j] != EMPTY:
               return False
    
    return True

def player(board):
    """
    Returns player who has the next turn on a board.
    """
    # the player has the lower number of moves has the next turn on the board 
    if terminal(board) :
        return None
    
    Xs = 0
    Os = 0

    for row in board :
        for cell in row :
            if cell == O :
                Os = Os + 1

            if cell == X :
                Xs = Xs + 1

    return O if Xs > Os else X

def deepCopy(board):

    newBoard = []

    for i in board:
        row = []
        for j in i:
            row.append(j)
        
        newBoard.append(row)
    
    return newBoard

def isValidAction(x , y):
    return x <= 2 and y <= 2


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """

    if terminal(board) :
        return None
    
    actions = set()

    for i in range(3) :
        for j in range(3) :
            if board[i][j] == EMPTY:
                action = (i , j)
                actions.add(action)

    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    
    x , y = action
    newBoard = deepCopy(board)

    if action not in actions(board):
        raise ValueError("Invalid action")
    

    newBoard[x][y] = player(board)

    return newBoard



def winner(board):

    """
    Returns the winner of the game, if there is one.
    """
     
    # check the rows
    for row in range(3) :
        if board[row][0] == board[row][1] == board[row][2] and board[row][0] != EMPTY:
            return board[row][0]
    

        
    # check the columns
    for col in range(3) :
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] != EMPTY:
            return board[0][col]


    # check the left dialogue
    if board[0][0] == board[1][1] == board[2][2] and board[1][1] != EMPTY :
        return board[1][1]
    
    # check the right dialogue
    if board[0][2] == board[1][1] == board[2][0] and board[1][1] != EMPTY :
        return board[1][1]
    
    # Draw => No winner
    return None

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    if winner(board) is not None : # there is winner, so the game is over
        return True

    # the game is not over if there is at least one EMPTY squre
    for row in board :
        for cell in row : 
            if cell == EMPTY :
                return False
    
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X :
        return 1
    
    if winner(board) == O :
        return -1
    
    return 0

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board) :
        return None
    
    if emptyState(board) : 
        action = (1 , 1) # dump square to avoid too much computions 
        return action
    
    Actions = actions(board)
    current_player = player(board)
    bestAction = None
    bestValue = -math.inf if current_player == X else math.inf
    lessMoves = 0
    
    global moves

    for action in Actions:

        moves = 0

        if current_player  == O:
           
           value = max_value(result(board , action))

           if value <= bestValue:
                
                if value == bestValue: # in this case we have two actions with the same results
                   if moves < lessMoves: # the best one has less moves (dont miss an immediate winning move) 
                       bestAction = action 
                       
                else:
                    bestAction = action
                    bestValue = value

                lessMoves = moves
                           
        
        else :
           value = min_value(result(board , action))      

           if value >= bestValue:
                
                if value == bestValue:
                   if moves < lessMoves:
                       bestAction = action
                       
                else:
                    bestAction = action
                    bestValue = value

                lessMoves = moves       
        
    
    return bestAction



def max_value(board):

    if terminal(board):
        return utility(board)
    
    global moves
    moves = moves + 1   

    Actions = actions(board)

    v = -math.inf
    for action in Actions:
        v = max(v, min_value(result(board, action)))

    return v 

    


def min_value(board):

    if terminal(board):
        return utility(board)
    
    global moves
    moves = moves + 1   


    Actions = actions(board)

    v = math.inf
    for action in Actions:
        v = min(v, max_value(result(board, action)))

    return v
    

