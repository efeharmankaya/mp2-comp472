# based on code from https://stackabuse.com/minimax-and-alpha-beta-pruning-in-python

import time
import numpy as np

# CODED ASSUMING THE FOLLOWING INPUTS #
"""
n: size of board
b: number of blocks
d: depth of search
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
    def __init__(self, n, b, d, coords,s, recommend = True):
        self.n = n
        self.b = b
        self.d = d
        self.coords = coords
        self.s =s
        self.move_num = 0
        
        # TODO: implement functionality
        self.t = 1
        self.d1 = 1
        self.d2 = 1
        
        self.initialize_game()
        self.recommend = recommend
        
        self.start_game_trace()
        
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
        
    def save_board(self):
        with open(self.trace_file, 'a') as file:
            file.write('  ' + ''.join([chr(ord('A') + x) for x in range(self.n)])) # writes the top X input view (ie. ABCD for n = 4)
            file.write(f"\t(move #{self.move_num})" if self.move_num > 0 else '\t(Starting Board)')
            file.write('\n +' + u'-'*self.n + "\n")
            for x in range(self.n):
                file.write(f"{x}|")
                for y in range(self.n):
                    file.write(self.current_state[x][y])
                file.write("\n")
                
        self.move_num += 1
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

    def h1_calculate_score(self, turn):
        """ 
        Calculates scores for the rows and columns of the board based on how many friendly cells there are.
        """
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

        return score
    
    
    def h2_calculate_score(self, turn):
        """
        Calculates scores for each empty cell of the board based on adjacent cells, while also considering whether a player might be about to win.
        """
        scores = np.empty((self.n,self.n))
        max_i = max_j = 0
        # Highest priority: first move center of the board
        center_board = np.ceil(self.n/2).astype(int)
        if self.current_state[center_board][center_board] == '.':
            score = 1e6
            return score

        for i in range(self.n):
            for j in range(self.n):
                if self.current_state[i][j] == '.':
                    score = 0
                    # Associate a score with each cell: +2 for friendly adjacent cells, -1 for adjacent blocks, neutral to adjacent enemy cells
                    # If this cell's row or column contains enough cells for a friendly or enemy win, +100
                    if 0<i<self.n-1 and 0<j<self.n-1:
                        if turn == "X":
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
                            
                            # Check is someone is about to win
                            # Check the row
                            my_count = opp_count = 0
                            for col in range(self.n):
                                if self.current_state[i][col] == 'O':
                                    my_count += 1
                                elif self.current_state[i][col] == 'X':
                                    opp_count += 1
                            if my_count >= self.s-1:
                                score += 100
                            if opp_count >= self.s-1:
                                score += 100

                            # Check the column
                            my_count = opp_count = 0
                            for row in range(self.n):
                                if self.current_state[row][j] == 'O':
                                    my_count += 1
                                elif self.current_state[row][j] == 'X':
                                    opp_count += 1
                            if my_count >= self.s-1:
                                score += 100
                            if opp_count >= self.s-1:
                                score += 100

                        elif turn == "O":
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
                            
                            # Check is someone is about to win
                            # Check the row
                            my_count = opp_count = 0
                            for col in range(self.n):
                                if self.current_state[i][col] == 'X':
                                    my_count += 1
                                elif self.current_state[i][col] == 'O':
                                    opp_count += 1
                            if my_count >= self.s-1:
                                score += 100
                            if opp_count >= self.s-1:
                                score += 100

                            # Check the column
                            my_count = opp_count = 0
                            for row in range(self.n):
                                if self.current_state[row][j] == 'X':
                                    my_count += 1
                                elif self.current_state[row][j] == 'O':
                                    opp_count += 1
                            if my_count >= self.s-1:
                                score += 100
                            if opp_count >= self.s-1:
                                score += 100
                            
        return score
    
    
    def minimax(self, depth, max=False, heuristic=None):
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

        if depth == 0:
            if heuristic == 1:
                if max:
                    value = self.h1_calculate_score('O')
                    return (value, x , y)
                else:
                    value = self.h1_calculate_score('X')
                    return (value, x , y)
            elif heuristic == 2:
                if max:
                    value = self.h2_calculate_score('O')
                    return (value, x , y)
                else:
                    value = self.h2_calculate_score('X')
                    return (value, x , y)
            else:
                return "Error: heuristic not specified!"

        for i in range(0, self.n):
            for j in range(0, self.n):
                if self.current_state[i][j] == '.':
                    if max:
                        self.current_state[i][j] = 'O'
                        (v, _, _) = self.minimax(depth-1, max=False, heuristic=heuristic)
                        if v > value:
                            value = v
                            x = i
                            y = j
                    else:
                        self.current_state[i][j] = 'X'
                        (v, _, _) = self.minimax(depth-1, max=True, heuristic=heuristic)
                        if v < value:
                            value = v
                            x = i
                            y = j
                    self.current_state[i][j] = '.'
        return (value, x, y)
        
    def alphabeta(self, depth, alpha=-2, beta=2, max=False, heuristic=None):
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

        if depth == 0:
            if heuristic == 1:
                if max:
                    value = self.h1_calculate_score('O')
                    return (value, x , y)
                else:
                    value = self.h1_calculate_score('X')
                    return (value, x , y)
            elif heuristic == 2:
                if max:
                    value = self.h2_calculate_score('O')
                    return (value, x , y)
                else:
                    value = self.h2_calculate_score('X')
                    return (value, x , y)
            else:
                return "Error: heuristic not specified!"

        for i in range(0, self.n):
            for j in range(0, self.n):
                if self.current_state[i][j] == '.':
                    if max:
                        self.current_state[i][j] = 'O'
                        (v, _, _) = self.alphabeta(depth-1, alpha, beta, max=False, heuristic=heuristic)
                        if v > value:
                            value = v
                            x = i
                            y = j
                    else:
                        self.current_state[i][j] = 'X'
                        (v, _, _) = self.alphabeta(depth-1, alpha, beta, max=True, heuristic=heuristic)
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

    
    def play(self,algo=None, heuristic=None, player_x=None,player_o=None):
        if algo == None:
            algo = self.ALPHABETA
        if player_x == None:
            player_x = self.HUMAN
        if player_o == None:
            player_o = self.HUMAN
        
        with open(self.trace_file, 'a') as file:    
            file.write(f"\nPlayer 1: {'HUMAN' if player_x == self.HUMAN else 'AI d=' + str(self.d1) + ' a=' + ('False (MINIMAX)' if algo == self.MINIMAX else 'True (ALPHABETA)') }")
            file.write(f"\nPlayer 2: {'HUMAN' if player_o == self.HUMAN else 'AI d=' + str(self.d2) + ' a=' + ('False (MINIMAX)' if algo == self.MINIMAX else 'True (ALPHABETA)') }\n\n")    

        self.save_board()
        
        while True:
            self.draw_board()
            if self.check_end():
                return self.save_end()
            start = time.time()
            if algo == self.MINIMAX:
                if self.player_turn == 'X':
                    (_, x, y) = self.minimax(self.d, max=False, heuristic=heuristic)
                else:
                    (_, x, y) = self.minimax(self.d, max=True, heuristic=heuristic)
            else: # algo == self.ALPHABETA
                if self.player_turn == 'X':
                    (m, x, y) = self.alphabeta(self.d, max=False, heuristic=heuristic)
                else:
                    (m, x, y) = self.alphabeta(self.d, max=True, heuristic=heuristic)
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
            
            # Save log
            with open(self.trace_file, 'a') as file:
                current_player = player_x if self.player_turn == 'X' else player_o
                file.write(f"\nPlayer {self.player_turn} under {'HUMAN' if current_player == self.HUMAN else 'AI'} controls plays: {chr(ord('A') + x)}{str(y)}\n")
                file.write(f"\ni\tEvaluation time: {round(end-start, 5)}s\n")
                file.write(f"ii\tHeuristic evaluations: {'TODO'}\n")
                file.write(f"iii\tEvaluations by depth: {'TODO'}\n")
                file.write(f"iv\tAverage evaluation depth: {'TODO'}\n")
                file.write(f"v\tAverage recursion depth: {'TODO'}\n\n")
                
            self.save_board()
            
            
            self.switch_player()

    def start_game_trace(self):
        self.trace_file = f"gameTrace-{self.n}{self.b}{self.s}{self.t}.txt"
        with open(self.trace_file, "w") as file:
            file.write(f"n={self.n} b={self.b} s={self.s} t={self.t}\n")
            file.write(f"blocs={self.coords}\n")
    
    def save_end(self):
        with open(self.trace_file, 'a') as file:
            file.write(f"\nThe winner is {self.player_turn}!\n")  
            

def main():
    n = 4
    b = 0
    d = 3
    coords = []
    s = 3
    g = Game(n, b, d, coords, s, recommend=True)
    g.play(algo=Game.ALPHABETA,heuristic=2,player_x=Game.AI,player_o=Game.AI)

if __name__ == "__main__":
    main()
