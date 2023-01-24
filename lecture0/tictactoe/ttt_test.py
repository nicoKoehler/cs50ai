import tictactoe as ttt
import sys

boards= {
    "initial": [[ttt.EMPTY, ttt.EMPTY, ttt.EMPTY],[ttt.EMPTY, ttt.EMPTY, ttt.EMPTY],[ttt.EMPTY, ttt.EMPTY, ttt.EMPTY]

    ],
    "mid":[
        [ttt.X, ttt.X, ttt.O], [ttt.X, ttt.EMPTY,ttt.O], [ttt.EMPTY, ttt.EMPTY, ttt.EMPTY]
    ],
    "xwin-vert":[
        [ttt.X, ttt.X, ttt.O], [ttt.X, ttt.O,ttt.O], [ttt.X, ttt.EMPTY, ttt.EMPTY]
    ],
    "owin-hor":[
        [ttt.X, ttt.X, ttt.O], [ttt.O, ttt.O,ttt.O], [ttt.EMPTY, ttt.X, ttt.X]
    ],
    "draw":[
        [ttt.X, ttt.X, ttt.O], [ttt.O, ttt.X,ttt.X], [ttt.X, ttt.O, ttt.O]
    ],
    "xwin-diag":[
        [ttt.X, ttt.O, ttt.O], [ttt.X, ttt.X,ttt.O], [ttt.O, ttt.X, ttt.X]
    ],
    "dumb":[
        [ttt.X, ttt.X, ttt.EMPTY], [ttt.X, ttt.O, ttt.EMPTY], [ttt.O, ttt.EMPTY, ttt.EMPTY]
    ]
}

def print_board(board):
    for r in board:
        print(r, end="\n")


if __name__ == "__main__":
    
    if len(sys.argv) > 1:
        try: 
            board = boards[sys.argv[1]]
        except:
            print("Scenario not found. Defaulting to initial empty state")
            board = boards["initial"]
    else: 
        print("No argument provided, defaulting to initial setup")
        board = boards["initial"]

    actions = ttt.actions(board)

    print_board(board)
    print("\n")
    print(f"This turn: {ttt.player(board)}")
    print(f"Possible Actions: {actions}")
    print("\n")

    
    print("\n")
    print(f"Game over?: {ttt.terminal(board)}")
    print(f"Winner?: {ttt.winner(board)}")
    print(f"Winner Utility: {ttt.utility(board)}")
    print("\n")
    print(f"minMax: {ttt.minimax(board)}")