# https://onestepcode.com/numpy-array-views-tic-tac-toe/
# https://numpy.org/devdocs/reference/generated/numpy.diagonal.html
# https://codereview.stackexchange.com/questions/24764/tic-tac-toe-victory-check

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
    ]),
    np.array([
        np.array(['X', '.', '.', '.']),
        np.array(['X', '.', '.', '.']),
        np.array(['X', '.', '.', '.']),
        np.array(['.', '.', '.', '.']),
    ]),
    np.array([
        np.array(['.', '.', '.', '.']),
        np.array(['.', 'X', 'X', 'X']),
        np.array(['.', '.', '.', '.']),
        np.array(['.', '.', '.', '.']),
    ]),
    np.array([
        np.array(['.', '.', '.', '.']),
        np.array(['.', 'X', '.', '.']),
        np.array(['.', '.', 'X', '.']),
        np.array(['.', '.', '.', 'X']),
    ]),
    np.array([
        np.array(['.', '.', '.', '.']),
        np.array(['.', '.', 'O', '.']),
        np.array(['.', 'O', '.', '.']),
        np.array(['O', '.', '.', '.']),
    ]),
    np.array([
        np.array(['O', 'O', 'X', '.']),
        np.array(['.', 'X', 'X', 'X']),
        np.array(['.', 'O', 'O', '.']),
        np.array(['.', '.', 'O', '.']),
    ]),
    np.array([
        np.array(['.', 'X', '.', '.']),
        np.array(['.', 'X', '.', '.']),
        np.array(['.', '.', '.', '.']),
        np.array(['.', 'O', 'O', '.']),
    ]),
    np.full((4,4), '.')
]
output = [("X","col"),("O","col"),("X","row"),("X","diag"),("X","col"),("X","row"),("X","diag"),("O", "diag"),("X","row"),(".",""),(".","")]
board_empty = np.full((n,n), '.')

def is_end(board):
    print(board)

    # working nxn len(s) tic tac toe algo
    for i in range(len(board)):
        rows = board[i, :]
        cols = board[:, i]
        diag_1 = np.diagonal(board, i)
        diag_2 = np.fliplr(board).diagonal(i)
        print(f"row[{i}] = {rows}")
        print(f"col[{i}] = {cols}")
        print(f"diag_1[{i}] = {diag_1}")
        print(f"diag_2[{i}] = {diag_2}")
        for player in ["X", "O"]:
            player_win = np.array([player for _ in range(s)])
            for j in range(len(rows) - s + 1):
                # if np.all(rows[j:j+s] == player_win):
                #     print(f"ROWS: i = {i}, j = {j}")
                #     return player, "row"
                # elif np.all(cols[j:j+s] == player_win):
                #     print(f"COLS: i = {i}, j = {j}")
                #     return player, "col"
                # elif len(diag_1) >= s and np.all(diag_1[j:j+s] == player_win):
                #     print("DIAG1")
                #     return player, "diag"
                # elif len(diag_2) >= s and np.all(diag_2[j:j+s] == player_win):
                #     print("DIAG2")
                #     return player, "diag"
            
                if(rows[j] == '.' and len(diag_1) < s and len(diag_2) < s): # skip iteration if starting cells are empty
                    continue
                    
                print(f'''
                ======
                rows = {rows}
                diag_1 = {diag_1}
                diag_2 = {diag_2}
                rows[j] = {rows[j]}
                ======
                ''')
                
                if(np.all(rows[j:j+s] == player_win)): # vertical win
                    return player, "row"
                if(np.all(cols[j:j+s] == player_win)): # horizontal win
                    return player, "col"
                if(len(diag_1) >= s and (j+s <= len(diag_1))):
                    print(f"j = {j}")

                    if(np.all(diag_1[j:j+s] == player_win)):
                        return player,"diag"
                if(len(diag_2) >= s and (j+s <= len(diag_1))):
                    print(f"j = {j}")

                    if(np.all(diag_2[j:j+s] == player_win)):
                        return player,"diag"
                # if(np.all(rows[j:j+s] == player_win) # vertical win
                #     or np.all(cols[j:j+s] == player_win) # horizontal win
                #     or (len(diag_1) >= s and np.all(diag_1[j:j+s] == player_win)) # diag 1 win
                #     or (len(diag_2) >= s and np.all(diag_2[j:j+s] == player_win)) # diag 2 win
                # ):
                #     return player


        # for player in ["X", "O"]:
        #     player_win = np.array([player for _ in range(s)])
        #     print(u"=" * 20)
        #     print(cols)
        #     print(player_win)
        #     print(u"=" * 20)

        #     out = ""
        #     if np.all(cols == player_win): # vertical win
        #         print("COLS")
        #         out = "col"
        #     elif np.all(rows == player_win): # horizontal win
        #         print("ROWS")
        #         out = "row"
        #     elif (len(diag_1) >= s and np.all(diag_1 == player_win)): # length check to ensure win condition is even possible
        #         print("DIAG1")
        #         out = "diag"
        #     elif (len(diag_2) >= s and np.all(diag_2 == player_win)):
        #         print("DIAG2")
        #         out = "diag"
        #     else:
        #         continue

        #     return player, out # reached if a condition other than else was executed
    return False            
        

for board, result in zip(boards, output):
    out = is_end(board)
    print(out)
    if type(out) is not bool:
        assert out[0] == result[0]
        assert out[1] == result[1]
    print("========")
