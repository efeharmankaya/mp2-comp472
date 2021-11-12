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
        # for i in range(len(self.current_state)):
        #     for c in self.coords:
        #         if c == i:
        #             # Set this coordinate as a block
        #             self.current_state[i] = 'b'

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
        if px < 0 or px > self.n-1 or py < 0 or py > self.n-1:
            return False
        elif self.current_state[px][py] != '.':
            print("This cell is not empty!")
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

    
    def heuristic1(self, max, value, algo):
        """
        Heuristic 1 is simpler, it assigns scores to every empty cell on the board based on the count of friendly/block/enemy cells in the row and column
        """
        center_board = np.ceil(self.n/2).astype(int)
        if max: # O
            # Highest priority: first move center of the board
            if self.current_state[center_board][center_board] == '.':
                self.current_state[center_board][center_board] = 'O'
                if algo == "minimax":
                    (v, _, _) = self.minimax(max=False, heuristic=1)
                elif algo == "alphabeta":
                    (v, _, _) = self.alphabeta(max=False, heuristic=1)
                else:
                    print("Specified algorithm is incorrect!")
                if v > value:
                    value = v
                    x = center_board
                    y = center_board
                self.current_state[center_board][center_board] = '.'

            else: # center taken
                scores = self.calculate_score("O")
                
                max_i, max_j = np.unravel_index(np.argmax(scores), (self.n,self.n))
                # Place a marker on the cell with the highest score
                self.current_state[max_i][max_j] = 'O'
                if algo == "minimax":
                    (v, _, _) = self.minimax(max=False, heuristic=1)
                elif algo == "alphabeta":
                    (v, _, _) = self.alphabeta(max=False, heuristic=1)
                else:
                    print("Specified algorithm is incorrect!")
                if v > value:
                    value = v
                    x = max_i
                    y = max_j
                self.current_state[max_i][max_j] = '.'
        
        else: # min; X
            # Highest priority: first move center of the board
            if self.current_state[center_board][center_board] == '.':
                self.current_state[center_board][center_board] = 'X'
                if algo == "minimax":
                    (v, _, _) = self.minimax(max=True, heuristic=1)
                elif algo == "alphabeta":
                    (v, _, _) = self.alphabeta(max=True, heuristic=1)
                else:
                    print("Specified algorithm is incorrect!")
                if v < value:
                    value = v
                    x = center_board
                    y = center_board
                self.current_state[center_board][center_board] = '.'

            else: # center taken
                scores = self.calculate_score("X")

                max_i, max_j = np.unravel_index(np.argmax(scores), (self.n,self.n))
                # Place a marker on the cell with the highest score
                self.current_state[max_i][max_j] = 'X'
                if algo == "minimax":
                    (v, _, _) = self.minimax(max=True, heuristic=1)
                elif algo == "alphabeta":
                    (v, _, _) = self.alphabeta(max=True, heuristic=1)
                else:
                    print("Specified algorithm is incorrect!")
                if v < value:
                    value = v
                    x = max_i
                    y = max_j
                self.current_state[max_i][max_j] = '.'
        
        return (value, x, y)       
    
    def heuristic2(self, max, value, algo):
        """
        Heuristic 2 is more thorough, it assigns scores to every empty cell on the board based on the count of friendly/block/enemy cells in adjacent cells
        """
        center_board = np.ceil(self.n/2).astype(int)
        if max:
            # Highest priority: first move center of the board
            if self.current_state[center_board][center_board] == '.':
                self.current_state[center_board][center_board] = 'O'
                if algo == "minimax":
                    (v, _, _) = self.minimax(max=False, heuristic=2)
                elif algo == "alphabeta":
                    (v, _, _) = self.alphabeta(max=False, heuristic=2)
                else:
                    print("Specified algorithm is incorrect!")
                if v > value:
                    value = v
                    x = center_board
                    y = center_board
                self.current_state[center_board][center_board] = '.'

            else:
                scores = np.empty((self.n,self.n))
                max_i = max_j = 0
                for i in range(self.n):
                    for j in range(self.n):
                        if self.current_state[i][j] == '.':
                            score = 0
                            # Associate a score with each cell: +2 for friendly adjacent cells, -1 for adjacent blocks, neutral to adjacent enemy cells
                            if 0<i<self.n-1 and 0<j<self.n-1:
                                if self.current_state[i][j-1] == 'O':
                                    score += 2
                                elif self.current_state[i][j-1] == 'b':
                                    score -= 1
                                if self.current_state[i+1][j-1] == 'O':
                                    score += 2
                                elif self.current_state[i+1][j-1] == 'b':
                                    score -= 1
                                
                                if self.current_state[i+1][j] == 'O':
                                    score += 2
                                elif self.current_state[i+1][j] == 'b':
                                    score -= 1

                                if self.current_state[i+1][j+1] == 'O':
                                    score += 2
                                elif self.current_state[i+1][j+1] == 'b':
                                    score -= 1

                                if self.current_state[i][j+1] == 'O':
                                    score += 2
                                elif self.current_state[i][j+1] == 'b':
                                    score -= 1

                                if self.current_state[i-1][j+1] == 'O':
                                    score += 2
                                elif self.current_state[i-1][j+1] == 'b':
                                    score -= 1

                                if self.current_state[i-1][j] == 'O':
                                    score += 2
                                elif self.current_state[i-1][j] == 'b':
                                    score -= 1

                                if self.current_state[i-1][j-1] == 'O':
                                    score += 2
                                elif self.current_state[i-1][j-1] == 'b':
                                    score -= 1

                            # Record the score at this board position
                            scores[i][j] = score
                
                max_i, max_j = np.unravel_index(np.argmax(scores), (self.n,self.n))
                # Place a marker on the cell with the highest score
                self.current_state[max_i][max_j] = 'O'
                if algo == "minimax":
                    (v, _, _) = self.minimax(max=False, heuristic=2)
                elif algo == "alphabeta":
                    (v, _, _) = self.alphabeta(max=False, heuristic=2)
                else:
                    print("Specified algorithm is incorrect!")
                if v > value:
                    value = v
                    x = max_i
                    y = max_j
                self.current_state[max_i][max_j] = '.'
        
        else:
            # Highest priority: first move center of the board
            if self.current_state[center_board][center_board] == '.':
                self.current_state[center_board][center_board] = 'X'
                if algo == "minimax":
                    (v, _, _) = self.minimax(max=True, heuristic=2)
                elif algo == "alphabeta":
                    (v, _, _) = self.alphabeta(max=True, heuristic=2)
                else:
                    print("Specified algorithm is incorrect!")
                if v < value:
                    value = v
                    x = center_board
                    y = center_board
                self.current_state[center_board][center_board] = '.'

            else:
                scores = np.empty((self.n,self.n))
                max_i = max_j = 0
                for i in range(self.n):
                    for j in range(self.n):
                        if self.current_state[i][j] == '.':
                            score = 0
                            # Associate a score with each cell: +2 for friendly adjacent cells, -1 for adjacent blocks
                            if 0<i<self.n-1 and 0<j<self.n-1:
                                if self.current_state[i][j-1] == 'X':
                                    score += 2
                                elif self.current_state[i][j-1] == 'b':
                                    score -= 1
                                if self.current_state[i+1][j-1] == 'X':
                                    score += 2
                                elif self.current_state[i+1][j-1] == 'b':
                                    score -= 1
                                
                                if self.current_state[i+1][j] == 'X':
                                    score += 2
                                elif self.current_state[i+1][j] == 'b':
                                    score -= 1

                                if self.current_state[i+1][j+1] == 'X':
                                    score += 2
                                elif self.current_state[i+1][j+1] == 'b':
                                    score -= 1

                                if self.current_state[i][j+1] == 'X':
                                    score += 2
                                elif self.current_state[i][j+1] == 'b':
                                    score -= 1

                                if self.current_state[i-1][j+1] == 'X':
                                    score += 2
                                elif self.current_state[i-1][j+1] == 'b':
                                    score -= 1

                                if self.current_state[i-1][j] == 'X':
                                    score += 2
                                elif self.current_state[i-1][j] == 'b':
                                    score -= 1

                                if self.current_state[i-1][j-1] == 'X':
                                    score += 2
                                elif self.current_state[i-1][j-1] == 'b':
                                    score -= 1
                                    
                            # Record the score at this board position
                            scores[i][j] = score
                
                max_i, max_j = np.unravel_index(np.argmax(scores), (self.n,self.n))
                # Place a marker on the cell with the highest score
                self.current_state[max_i][max_j] = 'X'
                if algo == "minimax":
                    (v, _, _) = self.minimax(max=True, heuristic=2)
                elif algo == "alphabeta":
                    (v, _, _) = self.alphabeta(max=True, heuristic=2)
                else:
                    print("Specified algorithm is incorrect!")
                if v < value:
                    value = v
                    x = max_i
                    y = max_j 
                self.current_state[max_i][max_j] = '.'
        return (value, x, y)       

    def calculate_score(self, turn):
        scores = np.zeros((self.n,self.n))
        for i in range(self.n):
            for j in range(self.n):
                if self.current_state[i][j] == '.':
                    score = 0
                    # Associate a score with the row and column: +2 for friendly cells, -1 for blocks, -1 for enemy cells
                    for col in range(self.n):
                        if turn == "X":
                            if self.current_state[i][col] == 'X':
                                score += 2
                            elif self.current_state[i][col] == 'O' or self.current_state[i][col] == 'b':
                                score -= 1
                        else: # turn == "O"
                            if self.current_state[i][col] == 'O':
                                score += 2
                            elif self.current_state[i][col] == 'X' or self.current_state[i][col] == 'b':
                                score -= 1
                    for row in range(self.n):
                        if turn == "X":
                            if self.current_state[row][j] == 'X':
                                score += 2
                            elif self.current_state[row][j] == 'O' or self.current_state[row][j] == 'b':
                                score -= 1
                        else: # turn == "O"
                            if self.current_state[row][j] == 'O':
                                score += 2
                            elif self.current_state[row][j] == 'X' or self.current_state[row][j] == 'b':
                                score -= 1
                    # Record the score at this board position
                    scores[i][j] = score
        return scores

    def minimax(self, max=False, heuristic=1):
        
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

        if heuristic == 1:
            return self.heuristic1(max, value, "minimax")
        elif heuristic == 2:
            return self.heuristic2(max, value, "minimax")
        else:
            return "Error: heuristic not specified!"
        

    def alphabeta(self, alpha=-2, beta=2, max=False, heuristic=1):
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

        if heuristic == 1:
            return self.heuristic1(max, value, "alphabeta")
        elif heuristic == 2:
            return self.heuristic2(max, value, "alphabeta")
        else:
            return "Error: heuristic not specified!"

    def play(self,algo=None, heuristic=1, player_x=None,player_o=None):
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
                    (_, x, y) = self.minimax(max=False, heuristic=heuristic)
                else:
                    (_, x, y) = self.minimax(max=True, heuristic=heuristic)
            else: # algo == self.ALPHABETA
                if self.player_turn == 'X':
                    (m, x, y) = self.alphabeta(max=False, heuristic=heuristic)
                else:
                    (m, x, y) = self.alphabeta(max=True, heuristic=heuristic)
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
    #g.play(algo=Game.ALPHABETA, heuristic=2, player_x=Game.HUMAN,player_o=Game.HUMAN)
    #print("alphabeta heuristic 1 done")
    g.play(algo=Game.MINIMAX,heuristic=1,player_x=Game.HUMAN,player_o=Game.AI)
    print("minimax heuristic 1 done")

if __name__ == "__main__":
    main()
    
