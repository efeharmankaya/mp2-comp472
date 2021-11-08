# based on code from https://stackabuse.com/minimax-and-alpha-beta-pruning-in-python

import time
import numpy as np

# CODED ASSUMING THE FOLLOWING INPUTS #
"""
n: size of board
b: number of blocks
coords: positions of the blocks
s: winning line-up size
"""

class Game:
    MINIMAX = 0
    ALPHABETA = 1
    HUMAN = 2
    AI = 3
    
    # Params to add
    # + max depth: d1,d2
    # + max ai computation time: t
    def __init__(self, n, b, coords,s, recommend = True):
        self.n = n
        self.b = b
        self.coords = coords
        self.s =s
        self.initialize_game()
        self.recommend = recommend
        
    def initialize_game(self):
        # Create initial game board state as a nxn array filled with '.'
        # self.current_state = np.full((self.n,self.n), '.')
        self.current_state = np.full((self.n,self.n), '.')
        # Place blocks
        for i in range(len(self.current_state)):
            for c in self.coords:
                if c == i:
                    # Set this coordinate as a block
                    self.current_state[i] = 'b'

        # Player white always plays first
        self.player_turn = 'X'

    def draw_board(self):
        print()
        for y in range(0, self.n):
            for x in range(0, self.n):
                print(F'{self.current_state[x][y]}', end="")
            print()
        print()

    def is_valid(self, px, py):
        if px < 0 or px > self.n or py < 0 or py > self.n:
            return False
        elif self.current_state[px][py] != '.':
            return False
        else:
            return True

    def is_end(self):
        for i in range(self.n):
            rows = self.current_state[i, :]
            cols = self.current_state[:, i]
            diag_1 = np.diagonal(self.current_state, i)
            diag_2 = np.fliplr(self.current_state).diagonal(i)
            # print(f"row[{i}] = {rows}")
            # print(f"col[{i}] = {cols}")
            # print(f"diag_1[{i}] = {diag_1}")
            # print(f"diag_2[{i}] = {diag_2}")
            for player in ["X", "O"]:
                player_win = np.array([player for _ in range(self.s)]) # generate required player win array (ie.s=3 ["X", "X", "X"])
                for j in range(len(rows) - self.s + 1):
                    # print(f"rows = {rows}")
                    # print(f"diag_1 = {diag_1}")
                    # print(f"diag_2 = {diag_2}")
                    # if(rows[j] == '.' and (len(diag_1) -1 > j and diag_1[j] == '.') and (len(diag_2) -1 > j and diag_2[j] == '.')):#        and len(diag_1) < self.s and len(diag_2) < self.s): # skip iteration if starting cells are empty
                    if(rows[j] == '.' and len(diag_1) < self.s and len(diag_2) < self.s): # skip iteration if starting cells are empty
                        continue
                    
                    if(np.all(rows[j: j + self.s] == player_win)): # vertical win
                        return player
                    if(np.all(cols[j: j + self.s] == player_win)): # horizontal win
                        return player
                    if(len(diag_1) >= self.s and (j + self.s <= len(diag_1))):
                        if(np.all(diag_1[j: j + self.s] == player_win)):
                            return player
                    if(len(diag_2) >= self.s and (j + self.s <= len(diag_1))):
                        if(np.all(diag_2[j: j + self.s] == player_win)):
                            return player




                    # if(np.all(rows[j:j+self.s] == player_win) # vertical win
                    #     or np.all(cols[j:j+self.s] == player_win) # horizontal win
                    #     or (len(diag_1) >= self.s and np.all(diag_1[j:j+self.s] == player_win)) # diag 1 win
                    #     or (len(diag_2) >= self.s and np.all(diag_2[j:j+self.s] == player_win)) # diag 2 win
                    # ):
                    #     return player
    
        for i in range(self.n): # check if board is empty
            for j in range(self.n):
                if self.current_state[i][j] == '.': # if empty cell is found game is not done
                    return None
        # It's a tie!
        return '.'

    def check_end(self):
        self.result = self.is_end()
        # Printing the appropriate message if the game has ended
        if self.result != None:
            if self.result == 'X':
                print('The winner is X!')
            elif self.result == 'O':
                print('The winner is O!')
            elif self.result == '.':
                print("It's a tie!")
            self.initialize_game()
        return self.result

    def input_move(self):
        while True:
            print(F'Player {self.player_turn}, enter your move:')
            px = int(input('enter the x coordinate: '))
            py = int(input('enter the y coordinate: '))
            if self.is_valid(px, py):
                return (px,py)
            else:
                print('The move is not valid! Try again.')

    def switch_player(self):
        if self.player_turn == 'X':
            self.player_turn = 'O'
        elif self.player_turn == 'O':
            self.player_turn = 'X'
        return self.player_turn

    def minimax(self, max=False):
        # Minimizing for 'X' and maximizing for 'O'
        # Possible values are:
        # -1 - win for 'X'
        # 0  - a tie
        # 1  - loss for 'X'
        # We're initially setting it to 2 or -2 as worse than the worst case:
        value = 2
        if max:
            value = -2
        x = None
        y = None
        result = self.is_end()
        if result == 'X':
            return (-1, x, y)
        elif result == 'O':
            return (1, x, y)
        elif result == '.':
            return (0, x, y)
        for i in range(self.n):
            for j in range(self.n):
                if self.current_state[i][j] == '.':
                    if max:
                        self.current_state[i][j] = 'O'
                        (v, _, _) = self.minimax(max=False)
                        if v > value:
                            value = v
                            x = i
                            y = j
                    else:
                        self.current_state[i][j] = 'X'
                        (v, _, _) = self.minimax(max=True)
                        if v < value:
                            value = v
                            x = i
                            y = j
                    self.current_state[i][j] = '.'
        return (value, x, y)

    def alphabeta(self, alpha=-2, beta=2, max=False):
        # Minimizing for 'X' and maximizing for 'O'
        # Possible values are:
        # -1 - win for 'X'
        # 0  - a tie
        # 1  - loss for 'X'
        # We're initially setting it to 2 or -2 as worse than the worst case:
        value = 2
        if max:
            value = -2
        x = None
        y = None
        result = self.is_end()
        if result == 'X':
            return (-1, x, y)
        elif result == 'O':
            return (1, x, y)
        elif result == '.':
            return (0, x, y)
        for i in range(self.n):
            for j in range(self.n):
                if self.current_state[i][j] == '.':
                    if max:
                        self.current_state[i][j] = 'O'
                        (v, _, _) = self.alphabeta(alpha, beta, max=False)
                        if v > value:
                            value = v
                            x = i
                            y = j
                    else:
                        self.current_state[i][j] = 'X'
                        (v, _, _) = self.alphabeta(alpha, beta, max=True)
                        if v < value:
                            value = v
                            x = i
                            y = j
                    self.current_state[i][j] = '.'
                    if max: 
                        if value >= beta:
                            return (value, x, y)
                        if value > alpha:
                            alpha = value
                    else:
                        if value <= alpha:
                            return (value, x, y)
                        if value < beta:
                            beta = value
        return (value, x, y)

    def play(self,algo=None,player_x=None,player_o=None):
        if algo == None:
            algo = self.ALPHABETA
        if player_x == None:
            player_x = self.HUMAN
        if player_o == None:
            player_o = self.HUMAN
        while True:
            self.draw_board()
            if self.check_end():
                return
            start = time.time()
            if algo == self.MINIMAX:
                if self.player_turn == 'X':
                    (_, x, y) = self.minimax(max=False)
                else:
                    (_, x, y) = self.minimax(max=True)
            else: # algo == self.ALPHABETA
                if self.player_turn == 'X':
                    (m, x, y) = self.alphabeta(max=False)
                else:
                    (m, x, y) = self.alphabeta(max=True)
            end = time.time()
            if (self.player_turn == 'X' and player_x == self.HUMAN) or (self.player_turn == 'O' and player_o == self.HUMAN):
                    if self.recommend:
                        print(F'Evaluation time: {round(end - start, 7)}s')
                        print(F'Recommended move: x = {x}, y = {y}')
                    (x,y) = self.input_move()
            if (self.player_turn == 'X' and player_x == self.AI) or (self.player_turn == 'O' and player_o == self.AI):
                        print(F'Evaluation time: {round(end - start, 7)}s')
                        print(F'Player {self.player_turn} under AI control plays: x = {x}, y = {y}')
            self.current_state[x][y] = self.player_turn
            self.switch_player()

def main():
    n = 4
    b = 0
    coords = []
    s = 3
    g = Game(n, b, coords,s, recommend=True)
    g.play(algo=Game.ALPHABETA,player_x=Game.AI,player_o=Game.AI)
    g.play(algo=Game.MINIMAX,player_x=Game.AI,player_o=Game.HUMAN)

if __name__ == "__main__":
    main()

