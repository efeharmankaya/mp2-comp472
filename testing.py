# https://onestepcode.com/numpy-array-views-tic-tac-toe/
# https://numpy.org/devdocs/reference/generated/numpy.diagonal.html

import json
import numpy as np
def pr(b):
    for x in b:
        print(x)

n = 3
s = 3
boards = [
    np.array([
        np.array(['X', '.', '.']),
        np.array(['X', '.', '.']),
        np.array(['X', '.', '.'])
    ]),
    np.array([
        np.array(['.', '.', 'O']),
        np.array(['.', '.', 'O']),
        np.array(['.', '.', 'O'])
    ]),
    np.array([
        np.array(['.', '.', '.']),
        np.array(['X', 'X', 'X']),
        np.array(['.', '.', '.'])
    ]),
    np.array([
        np.array(['X', '.', '.']),
        np.array(['.', 'X', '.']),
        np.array(['.', '.', 'X'])
    ])
]
board_empty = np.full((n,n), '.')

def is_end(board):
    print(board)
    for i in range(n):
        rows = board[i, :]
        cols = board[:, i]
        diag_1 = np.diagonal(board, i)
        diag_2 = np.fliplr(board).diagonal(i)
        print(f"row[{i}] = {rows}")
        print(f"col[{i}] = {cols}")
        print(f"diag_1[{i}] = {diag_1}")
        print(f"diag_2[{i}] = {diag_2}")
        # for j in range(len(rows) - s + 1):
        #     print("entered target loop")
        #     if rows[j:j+s] == ["X" for _ in range(s)]:
        #         print(f"ROWS: i = {i}, j = {j}")
        #         return True
        #     elif cols[j:j+s] == ['X' for _ in range(s)]:
        #         print(f"COLS: i = {i}, j = {j}")
        #         return True
        #     print("===")
        #     print(cols[j:j+s])
        #     print("===")

        for player in ["X", "O"]:
            player_win = [player for _ in range(s)] 
            if np.all(cols == player_win): # vertical win
                print("COLS")
            elif np.all(rows == player_win): # horizontal win
                print("ROWS")
            elif (len(diag_1) >= s and np.all(diag_1 == player_win)): # length check to ensure win condition is even possible
                print("DIAG1")
            elif (len(diag_2) >= s and np.all(diag_2 == player_win)):
                print("DIAG2")
            else:
                continue

            return player # reached if a condition other than else was executed
    return False            
        

# print(board_empty)
for board in boards:
    print(is_end(board))
    print("========")
