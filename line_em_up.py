# based on code from https://stackabuse.com/minimax-and-alpha-beta-pruning-in-python

import time
import numpy as np

class Game:
    MINIMAX = 0
    ALPHABETA = 1
    HUMAN = 2
    AI = 3
    
    turn_time = 0
    
    def __init__(self, n, b, coords, s, d1, d2, t, a1, a2 = None, recommend = True):
        self.n = n
        self.b = b
        self.coords = coords
        self.s = s
        self.d1 = d1
        self.d2 = d2
        self.t = t
        self.a = a1
        self.a2 = a2
        self.move_num = 0
        self.arr_evals_by_depth = []
        

        if n < 3 or n > 10:
            print("Select a board size n between 3 and 10!")
            exit()
        
        if len(coords) != b:
            print("Number of blocks does not correspond to coordinates given!")
            exit()
        
        if s < 3 or s > n:
            print("Winning line-up size must be between 3 and board size n!")
            exit()
        
        self.initialize_game()
        self.recommend = recommend
        
        self.start_game_trace()
        
    def initialize_game(self):
        # Create initial game board state as a nxn array filled with '.'
        self.current_state = np.full((self.n,self.n), '.')
        # Place blocks
        for x,y in self.coords:
            self.current_state[x][y] = 'b'


        # Player white always plays first
        self.player_turn = 'X'
        self.move_num = 0
        
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

            for player in ["X", "O"]:
                player_win = np.array([player for _ in range(self.s)]) # generate required player win array (ie.s=3 ["X", "X", "X"])
                for j in range(len(rows) - self.s + 1):
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

    def e1(self, turn):
        """ 
        Simply counts the number of friendly cells, and enemy cells per row and column. Highest row/column score determines which cell is selected.
        """
        self.total_heuristic_evals += 1
        self.h_turn_evals += 1
        for i in range(self.n):
            for j in range(self.n):
                if self.current_state[i][j] == '.':
                    score = 0
                    # Count the number of friendly/enemy cells in the row and column
                    for col in range(self.n):
                        if self.current_state[i][col] == 'X':
                            score -= 1
                        elif self.current_state[i][col] == 'O':
                            score += 1
                    for row in range(self.n):
                        self.total_heuristic_evals += 1
                        if self.current_state[row][j] == 'X':
                            score -= 1
                        elif self.current_state[row][j] == 'O':
                            score += 1

        return score
    
    
    def e2(self, turn):
        """
        Calculates scores for each empty cell of the board based on adjacent cells, while also considering the effects of blocks.
        """
        self.total_heuristic_evals += 1
        self.h_turn_evals += 1
        for i in range(self.n):
            for j in range(self.n):
                if self.current_state[i][j] == '.':
                    score = X_score = O_score = 0
                    # Associate a score with each cell: +1 for friendly adjacent cells, -1 for adjacent blocks, +2 for 2 adjacent in a row
                    if j>0:
                        if self.current_state[i][j-1] == 'O':
                            O_score += 1
                            if j>1:
                                if self.current_state[i][j-2] == 'O':
                                    O_score += 2
                        elif self.current_state[i][j-1] == 'X':
                            X_score += 1
                            if j>1:
                                if self.current_state[i][j-2] == 'X':
                                    X_score += 2
                        elif self.current_state[i][j-1] == 'b':
                            O_score -= 1
                            X_score -= 1
                    
                    if i<self.n-1 and j>0:
                        if self.current_state[i+1][j-1] == 'O':
                            O_score += 1
                            if i<self.n-2 and j>1:
                                if self.current_state[i+2][j-2] == 'O':
                                    O_score += 2
                        elif self.current_state[i+1][j-1] == 'X':
                            X_score += 1
                            if i<self.n-2 and j>1:
                                if self.current_state[i+2][j-2] == 'X':
                                    X_score += 2
                        elif self.current_state[i+1][j-1] == 'b':
                            O_score -= 1
                            X_score -= 1
                    
                    if i<self.n-1:
                        if self.current_state[i+1][j] == 'O':
                            O_score += 1
                            if i<self.n-2:
                                if self.current_state[i+2][j] == 'O':
                                    O_score += 2
                        elif self.current_state[i+1][j] == 'X':
                            X_score += 1
                            if i<self.n-2:
                                if self.current_state[i+2][j] == 'X':
                                    X_score += 2
                        elif self.current_state[i+1][j] == 'b':
                            O_score -= 1
                            X_score -= 1

                    if i<self.n-1 and j<self.n-1:
                        if self.current_state[i+1][j+1] == 'O':
                            O_score += 1
                            if i<self.n-2 and j<self.n-2:
                                if self.current_state[i+2][j+2] == 'O':
                                    O_score += 2
                        elif self.current_state[i+1][j+1] == 'X':
                            X_score += 1
                            if i<self.n-2 and j<self.n-2:
                                if self.current_state[i+2][j+2] == 'X':
                                    X_score += 2
                        elif self.current_state[i+1][j+1] == 'b':
                            O_score -= 1
                            X_score -= 1

                    if j<self.n-1:
                        if self.current_state[i][j+1] == 'O':
                            O_score += 1
                            if j<self.n-2:
                                if self.current_state[i][j+2] == 'O':
                                    O_score += 2
                        elif self.current_state[i][j+1] == 'X':
                            X_score += 1
                            if j<self.n-2:
                                if self.current_state[i][j+2] == 'X':
                                    X_score += 2
                        elif self.current_state[i][j+1] == 'b':
                            O_score -= 1
                            X_score -= 1

                    if i>0 and j<self.n-1:
                        if self.current_state[i-1][j+1] == 'O':
                            O_score += 1
                            if i>1 and j<self.n-2:
                                if self.current_state[i-2][j+2] == 'O':
                                    O_score += 2
                        elif self.current_state[i-1][j+1] == 'X':
                            X_score += 1
                            if i>1 and j<self.n-2:
                                if self.current_state[i-2][j+2] == 'X':
                                    X_score += 2
                        elif self.current_state[i-1][j+1] == 'b':
                            O_score -= 1
                            X_score -= 1
                    
                    if i>0:
                        if self.current_state[i-1][j] == 'O':
                            O_score += 1
                            if i>1:
                                if self.current_state[i-2][j] == 'O':
                                    O_score += 2
                        elif self.current_state[i-1][j] == 'X':
                            X_score += 1
                            if i>1:
                                if self.current_state[i-2][j] == 'X':
                                    X_score += 2
                        elif self.current_state[i-1][j] == 'b':
                            O_score -= 1
                            X_score -= 1

                    if i>0 and j>0:
                        if self.current_state[i-1][j-1] == 'O':
                            O_score += 1
                            if i>1 and j>1:
                                if self.current_state[i-2][j-2] == 'O':
                                    O_score += 2
                        elif self.current_state[i-1][j-1] == 'X':
                            X_score += 1
                            if i>1 and j>1:
                                if self.current_state[i-2][j-2] == 'X':
                                    X_score += 2
                        elif self.current_state[i-1][j-1] == 'b':
                            O_score -= 1
                            X_score -= 1

        if O_score > X_score:
            score = 1 * O_score
        elif O_score < X_score:
            score = -1 * X_score             
        
        return score
    
    
    def minimax(self, depth, max=False, heuristic=None, start=False):
        # Minimizing for 'X' and maximizing for 'O'
        # Possible values are:
        # -1 - win for 'X'
        # 0  - a tie
        # 1  - loss for 'X'
        # We're initially setting it to 2 or -2 as worse than the worst case:
        if start:
            self.recursion_depth = 0
            self.h_turn_evals = 0
        else:
            self.recursion_depth += 1
            
        if self.evals_by_depth.get(depth):
            self.evals_by_depth[depth] += 1
        else:
            self.evals_by_depth.update({depth : 1})
        

        
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

        # Base case: if search is completed OR if time is running out
        if depth == 0 or (time.time() - self.turn_time) > 0.8*self.t:
            if heuristic == 1:
                if max:
                    value = self.e1('O')
                    return (value, x , y)
                else:
                    value = self.e1('X')
                    return (value, x , y)
            elif heuristic == 2:
                if max:
                    value = self.e2('O')
                    return (value, x , y)
                else:
                    value = self.e2('X')
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
        
    def alphabeta(self, depth, alpha=-2, beta=2, max=False, heuristic=None, start=False):
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

        if start:
            self.recursion_depth = 0
            self.h_turn_evals = 0
        else:
            self.recursion_depth += 1
            
        if self.evals_by_depth.get(depth):
            self.evals_by_depth[depth] += 1
        else:
            self.evals_by_depth.update({depth : 1})

        # Base case: if search is completed OR if time is running out
        if depth == 0 or (time.time() - self.turn_time) > 0.8*self.t:
            if heuristic == 1:
                if max:
                    value = self.e1('O')
                    return (value, x , y)
                else:
                    value = self.e1('X')
                    return (value, x , y)
            elif heuristic == 2:
                if max:
                    value = self.e2('O')
                    return (value, x , y)
                else:
                    value = self.e2('X')
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
    
    def findAMove(self):
        for x in range(self.n):
            for y in range(self.n):
                if self.current_state[x][y] == '.':
                    return x,y
        return -1,-1
    
    def play(self, algo=None, player_x=None, player_x_heuristic=None, player_x_depth=None, player_o=None, player_o_heuristic=None, player_o_depth=None, analysis=None, r=None):

        
        if algo == True:
            algo = self.ALPHABETA
        else:
            algo == self.MINIMAX

        if player_x == None:
            player_x = self.HUMAN
        if player_o == None:
            player_o = self.HUMAN
            
        self.analysis = analysis
        
        with open(self.trace_file, 'a') as file:    
            file.write(f"\nPlayer 1: {'HUMAN' if player_x == self.HUMAN else 'AI d=' + str(self.d1) + ' a=' + ('False (MINIMAX)' if algo == self.MINIMAX else 'True (ALPHABETA)') }")
            file.write(f" e{player_x_heuristic}")
            file.write(f"\nPlayer 2: {'HUMAN' if player_o == self.HUMAN else 'AI d=' + str(self.d2) + ' a=' + ('False (MINIMAX)' if algo == self.MINIMAX else 'True (ALPHABETA)') }")    
            file.write(f" e{player_o_heuristic}\n\n")

        self.save_board()
        
        # analysis params
        self.eval_times = [] # use to find evaluation average
        self.recursion_depths = [] # use to find recursion average
        self.total_heuristic_evals = 0
        self.evals_by_depth = {}
        self.total_moves = 0
        self.prev_evals = {}
        while True:
            self.draw_board()
            if self.check_end():
                self.save_end()
                break
            starting_h_evals = self.total_heuristic_evals
            self.prev_evals = {**self.evals_by_depth}
            
            # Start the "timer" 
            start = self.turn_time = time.time()
            
            if algo == self.MINIMAX:
                if self.player_turn == 'X':
                    (_, x, y) = self.minimax(self.d1, max=False, heuristic=player_x_heuristic, start=True)
                else:
                    (_, x, y) = self.minimax(self.d2, max=True, heuristic=player_o_heuristic, start=True)
            else: # algo == self.ALPHABETA
                if self.player_turn == 'X':
                    (m, x, y) = self.alphabeta(self.d1, max=False, heuristic=player_x_heuristic, start=True)
                else:
                    (m, x, y) = self.alphabeta(self.d2, max=True, heuristic=player_o_heuristic, start=True)
            end = time.time()
            if (self.player_turn == 'X' and player_x == self.HUMAN) or (self.player_turn == 'O' and player_o == self.HUMAN):
                    if self.recommend:
                        print(F'Evaluation time: {round(end - start, 7)}s')
                        print(F'Recommended move: x = {x}, y = {y}')
                    (x,y) = self.input_move()
            if (self.player_turn == 'X' and player_x == self.AI) or (self.player_turn == 'O' and player_o == self.AI):
                        print(F'Evaluation time: {round(end - start, 7)}s')
                        if round(end - start, 7) > self.t:
                            print('AI timed out.')
                            if self.player_turn == 'X':
                                print(f'The winner is O!')
                                self.winner = "O"
                                self.save_end("O")
                            else:
                                print(f'The winner is X!')
                                self.winner = "X"
                                self.save_end("X")
                            break
                        
                        else:   
                            print(F'Player {self.player_turn} under AI control plays: x = {x}, y = {y}')
            
            if(x == None or y == None):
                x,y = self.findAMove()
            if(x == -1 or y == -1):
                self.winner = "X" if self.player_turn == "O" else "O"
                self.save_end("X" if self.player_turn == "O" else "O")
            self.current_state[x][y] = self.player_turn
            
            evals_by_depth = {key : evals - (self.prev_evals.get(key) if self.prev_evals.get(key) else 0) for key, evals in self.evals_by_depth.items()}
            avg_eval_depth = 0 if len(self.evals_by_depth.values()) == 0 else round(self.weighted_avg(self.evals_by_depth), 4)
            avg_recursion_depth = 0 if len(self.recursion_depths) == 0 else round(sum(self.recursion_depths) / len(self.recursion_depths), 3)
            
            print()
            # Save log
            with open(self.trace_file, 'a') as file:
                current_player = player_x if self.player_turn == 'X' else player_o
                file.write(f"\nPlayer {self.player_turn} under {'HUMAN' if current_player == self.HUMAN else 'AI'} controls plays: {chr(ord('A') + y)}{str(x)}\n")
                file.write(f"\ni\tEvaluation time: {round(end-start, 5)}s\n")
                file.write(f"ii\tHeuristic evaluations: {sum([val for val in evals_by_depth.values()])}\n")
                file.write(f"iii\tEvaluations by depth: {evals_by_depth}\n")
                file.write(f"iv\tAverage evaluation depth: {avg_eval_depth}\n")
                file.write(f"v\tAverage recursion depth: {avg_recursion_depth}\n\n")
                
            self.save_board()
            
            
            self.switch_player()
            
            # analysis params update
            self.total_moves += 1
            self.eval_times.append(round(end-start, 7))
            self.recursion_depths.append(self.recursion_depth)

        winner = self.winner if not self.is_end() else self.is_end()
        return winner, self.eval_times, self.evals_by_depth, self.recursion_depths, self.total_moves

    def start_game_trace(self):
        self.trace_file = f"gameTrace-{self.n}{self.b}{self.s}{self.t}.txt"
        with open(self.trace_file, "w") as file:
            file.write(f"n={self.n} b={self.b} s={self.s} t={self.t}\n")
            file.write(f"blocs={self.coords}\n")
    
    def weighted_avg(self, evals_by_depth):
        sum(self.evals_by_depth.values()) / len(self.evals_by_depth.values())
        out = []
        for depth, evals in evals_by_depth.items():
            out.append(depth * evals)
        return sum(out) / sum(evals_by_depth.values())
    
    def save_end(self, winner = None):
        if winner: # used when a winner is determined artificially (ie timeout)
            winner = winner
        else:
            winner = self.is_end()
        avg_eval = 0 if len(self.eval_times) == 0 else round(sum(self.eval_times) / len(self.eval_times), 5)
        avg_eval_depth = 0 if len(self.evals_by_depth.values()) == 0 else round(self.weighted_avg(self.evals_by_depth), 4)
        avg_recursion_depth = 0 if len(self.recursion_depths) == 0 else sum(self.recursion_depths) / len(self.recursion_depths)
        with open(self.trace_file, 'a') as file:
            if winner != '.':
                file.write(f"\nThe winner is {winner}!\n")  
            else:
                file.write("\nIt's a tie!\n")
            file.write(f"\n6(b)i\tAverage evaluation time: {avg_eval}")
            file.write(f"\n6(b)ii\tTotal heuristic evaluations: {sum([val for val in self.evals_by_depth.values()])}")
            file.write(f"\n6(b)iii\tEvaluations by depth: {self.evals_by_depth}")
            file.write(f"\n6(b)iv\tAverage evaluation depth: {avg_eval_depth}")
            file.write(f"\n6(b)v\tAverage recursion depth: {avg_recursion_depth}")
            file.write(f"\n6(b)vi\tTotal moves: {self.total_moves}\n\n")
        
import random
def getRandomBlocks(n, b):
    out = []
    while(True):
        tup = (random.randint(0, n-1), random.randint(0, n-1))
        if tup not in out:
            out.append(tup)
        if len(out) >= b:
            break
    return out

def weighted_avg(evals_by_depth):
    out = []
    for depth, evals in evals_by_depth.items():
        out.append(depth * evals)
    return sum(out) / sum(evals_by_depth.values())

def run():
    with open("scoreboard.txt", 'w') as file:
        file.write("");
    r = 3 # 2 x r scoreboard
    runs = [        
        # demo test set
        {'n' : 3, 'b' : 3, 's' : 3, 't' : 4, 'd1' : 6, 'd2' : 5, 'a1' : False, 'a2' : False, 'coords' : [(2,1),(1,1),(2,0)]},
        
        # {'n' : 4, 'b' : 4, 's' : 3, 't' : 5, 'd1' : 6, 'd2' : 6, 'a1' : True, 'a2' : True, 'coords' : [(0,0),(0,3),(3,0),(3,3)]},
        # {'n' : 4, 'b' : 4, 's' : 3, 't' : 1, 'd1' : 6, 'd2' : 6, 'a1' : True, 'a2' : True, 'coords' : [(0,0),(0,3),(3,0),(3,3)]},
        # {'n' : 5, 'b' : 4, 's' : 4, 't' : 1, 'd1' : 2, 'd2' : 6, 'a1' : True, 'a2' : True, 'coords' : getRandomBlocks(5,4)},
        # {'n' : 5, 'b' : 4, 's' : 4, 't' : 5, 'd1' : 6, 'd2' : 6, 'a1' : True, 'a2' : True, 'coords' : getRandomBlocks(5,4)},
        # {'n' : 8, 'b' : 5, 's' : 5, 't' : 1, 'd1' : 2, 'd2' : 6, 'a1' : True, 'a2' : True, 'coords' : getRandomBlocks(8,5)},
        # {'n' : 8, 'b' : 5, 's' : 5, 't' : 5, 'd1' : 2, 'd2' : 6, 'a1' : True, 'a2' : True, 'coords' : getRandomBlocks(8,5)},
        # {'n' : 8, 'b' : 6, 's' : 5, 't' : 1, 'd1' : 6, 'd2' : 6, 'a1' : True, 'a2' : True, 'coords' : getRandomBlocks(8,6)},
        # {'n' : 8, 'b' : 6, 's' : 5, 't' : 5, 'd1' : 6, 'd2' : 6, 'a1' : True, 'a2' : True, 'coords' : getRandomBlocks(8,6)},
    ]
    for test in runs:
        with open('scoreboard.txt', 'a') as file:
            file.write(f"n={test.get('n')} b={test.get('b')} s={test.get('s')} t={test.get('t')}\n")
            file.write(f"\nPlayer 1: d={test.get('d1')} a= {'False (MINIMAX)' if not test.get('a1') else 'True (ALPHABETA)'}\n")
            file.write(f"Player 2: d={test.get('d2')} a={'False (MINIMAX)' if not test.get('a2') else 'True (ALPHABETA)'}\n\n")
            file.write(f"2x{r} games\n\n")
        
        
        g = Game(**test)
        wins = {'e1' : 0, 'e2' : 0, 'tie' : 0}
        total_eval_times = []
        total_evals_by_depth = []
        total_recursion_depths = []
        total_moves_arr = []
        for _ in range(r): # X = e1, O = e2
            winner, eval_times, evals_by_depth, recursion_depths, total_moves = g.play(algo=(Game.ALPHABETA if test.get('a1') else Game.MINIMAX),
                                                                                            player_x=Game.AI,
                                                                                            player_x_heuristic=1,
                                                                                            player_o=Game.AI,
                                                                                            player_o_heuristic=2,
                                                                                            analysis=True,
                                                                                            r=10
                                                                                        )
            if winner == "X":
                wins['e1'] += 1
            elif winner == "O":
                wins['e2'] += 1
            else:
                wins['tie'] += 1
            
            total_eval_times.append(eval_times)
            total_evals_by_depth.append(evals_by_depth)
            total_recursion_depths.append(recursion_depths)
            total_moves_arr.append(total_moves)
            g.initialize_game()
        # switch X/O between heuristics
        for _ in range(r): # X = e2, O = e1
            winner, eval_times, evals_by_depth, recursion_depths, total_moves = g.play(algo=(Game.ALPHABETA if test['a1'] else Game.MINIMAX),
                                                                                            player_x=Game.AI,
                                                                                            player_x_heuristic=2,
                                                                                            player_o=Game.AI,
                                                                                            player_o_heuristic=1,
                                                                                            analysis=True,
                                                                                            r=10
                                                                                        )
            if winner == "X":
                wins['e2'] += 1
            elif winner == "O":
                wins['e1'] += 1
            else:
                wins['tie'] += 1
            
            total_eval_times.append(eval_times)
            total_evals_by_depth.append(evals_by_depth)
            total_recursion_depths.append(recursion_depths)
            total_moves_arr.append(total_moves)
            g.initialize_game()
            
        
        avg_eval = 0
        count = 0
        for eval_times in total_eval_times:
            if len(eval_times) == 0:
                continue
            avg_eval += sum(eval_times)
            count += len(eval_times)
        avg_eval = 0 if count == 0 else round(avg_eval/count, 6)
                
        total_evals_by_depth_dict = {}
        for evals_by_depth in total_evals_by_depth:
            for depth, value in evals_by_depth.items():
                if total_evals_by_depth_dict.get(depth):
                    total_evals_by_depth_dict[depth] += value
                else:
                    total_evals_by_depth_dict[depth] = value
        
        avg_eval_depth = 0 if len(total_evals_by_depth_dict.values()) == 0 else round(weighted_avg(total_evals_by_depth_dict), 4)
        
        avg_recursion_depth = 0
        count = 0
        for recursion_depths in total_recursion_depths:
            avg_recursion_depth += sum(recursion_depths)
            count += len(recursion_depths)
        avg_recursion_depth = 0 if count == 0 else round(avg_recursion_depth/count, 4)
        
        total_moves = sum(total_moves_arr)    
        total_moves = 0 if len(total_moves_arr) == 0 else round(total_moves/len(total_moves_arr), 2)
        
        print(wins)
        with open("scoreboard.txt", 'a') as file:
            file.write(f"Total wins for heuristic e1: {wins.get('e1')} ({round(wins.get('e1') / sum(wins.values()) * 100, 1)}%)\n")
            file.write(f"Total wins for heuristic e2: {wins.get('e2')} ({round(wins.get('e2') / sum(wins.values()) * 100, 1)}%)\n\n")
            file.write(f"i\tAverage evaluation time: {avg_eval}")
            file.write(f"\nii\tTotal heuristic evaluations: {sum([val for val in total_evals_by_depth_dict.values()])}")
            file.write(f"\niii\tEvaluations by depth: {total_evals_by_depth_dict}")
            file.write(f"\niv\tAverage evaluation depth: {avg_eval_depth}")
            file.write(f"\nv\tAverage recursion depth: {avg_recursion_depth}")
            file.write(f"\nvi\tTotal moves: {total_moves}\n\n")
    
     
def main():

    print("Enter a board size between 3 and 10 - n:")
    n = int(input())
    print(f"Enter the number of blocks between 0 and {2*n} - b:")
    b = int(input())
    if b > 0:
        print("One at a time, enter the space-separated tuples representing the coordinates of the blocks (e.g. A 1) - coords:")
    
    # Map alphabetical coordinate inputs to integer values
    d = {'A':0, 'B':1, 'C':2, 'D':3, 'E':4, 'F':5, 'G':6, 'H':7, 'I':8, 'J':9}
    coords = []
    for i in range(b):
        col, row = input().split(' ')
        col = d[col]
        row = int(row)
        coords.append((col,row))

    print(f"Enter the winning line up size between 3 and {n} - s:")
    s = int(input())
    print("Enter the maximum search depth of player 1 (X) - d1:")
    d1 = int(input())
    print("Enter the maximum search depth of player 2 (O) - d2:")
    d2 = int(input())
    print("Enter the maximum allowed time for a move in seconds - t:")
    t = float(input())
    print("Select which algorithm to use; 'True' for alphabeta, 'False' for minimax  - a:")
    a = input()
    print("Should player X be 1 (human) or 2 (AI)?")
    playerX = int(input())
    print("Should player O be 1 (human) or 2 (AI)?")
    playerO = int(input())
    print("Should player X play with heuristic 1 or 2?")
    playerXheuristic = int(input())
    print("Should player O play with heuristic 1 or 2?")
    playerOheuristic = int(input())

    if a == "True":
        a = True
    else:
        a = False
    
    if playerX == 1:
        playerX = Game.HUMAN
    else:
        playerX = Game.AI

    if playerO == 1:
        playerO = Game.HUMAN
    else:
        playerO = Game.AI

    g = Game(n, b, coords, s, d1, d2, t, a, recommend=True)

    g.play(algo=a, player_x=playerX, player_x_heuristic=playerXheuristic, player_o=playerO, player_o_heuristic=playerOheuristic)

if __name__ == "__main__":
    #  main()
    run()

