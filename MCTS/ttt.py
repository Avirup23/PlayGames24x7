import random
import math
from copy import deepcopy
from tqdm import tqdm
import csv 
import multiprocessing as mp
import os

class Node:
    def __init__(self, state:'TicTacToe', parent=None, move=None):
        self.state = state
        self.parent = parent
        self.move = move
        self.children = []
        self.visits = 0
        self.wins = 0

    def is_fully_expanded(self):
        return len(self.children) == len(self.state.get_legal_moves())

    def best_child(self, c_param=1.4):
        choices = [
            (child.wins / child.visits) + c_param * math.sqrt(math.log(self.visits) / child.visits)
            for child in self.children
        ]
        return self.children[choices.index(max(choices))]
    
    def print_tree(self, level=0):
        if level<2:
            indent = "  " * level
            move_str = f"Move: {self.move}" if self.parent is not None else "Root"
            if level != 0:
                print(f"{indent}{move_str}, Wins/Visits: {self.wins}/{self.visits}={round(self.wins/self.visits,2)}, UCB = {round((self.wins / self.visits) + 1.4 * math.sqrt(math.log(self.parent.visits) / self.visits),2)}, player_index = {self.state.player_turn}")
            else:
                print(f"{indent}{move_str}, Visits: {self.visits}")
            for child in self.children:
                child.print_tree(level + 1)

class TicTacToe:
    def __init__(self):
        self.board = [' '] * 9
        self.player_turn = 'X'

    def clone(self)->'TicTacToe':
        clone = TicTacToe()
        clone.board = self.board.copy()
        clone.player_turn = self.player_turn
        return clone

    def get_legal_moves(self):
        return [i for i in range(9) if self.board[i] == ' ']

    def make_move(self, move):
        self.board[move] = self.player_turn
        self.player_turn = 'O' if self.player_turn == 'X' else 'X'

    def is_terminal(self):
        return self.get_winner() is not None or all(s != ' ' for s in self.board)

    def get_winner(self):
        wins = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]
        for i,j,k in wins:
            if self.board[i] == self.board[j] == self.board[k] != ' ':
                return self.board[i]
        return None

    def get_result(self, player):
        winner = self.get_winner()
        return 1 if winner == player else 0.5 if winner == None else 0
    
 
def mcts(start_node:Node, deterministic_player, iter_limit = 500):
    for _ in range(iter_limit):
        node = start_node
        state = start_node.state.clone()
        # Selection
        while node.children and node.is_fully_expanded():
            node = node.best_child()
            state.make_move(node.move)

        # Expansion
        if not state.is_terminal():
            legal_moves = state.get_legal_moves()
            tried_moves = [child.move for child in node.children]
            for move in legal_moves:
                if move not in tried_moves:
                    new_state = state.clone()
                    new_state.make_move(move)
                    child_node = Node(new_state, parent=node, move=move)
                    node.children.append(child_node)
                    node = child_node
                    state = new_state
                    break

        # Simulation
        state = state.clone()
        while not state.is_terminal():
            move = random.choice(state.get_legal_moves())
    
            state.make_move(move)

        # Backpropagation
        result = state.get_result(start_node.state.player_turn)
        result = result if node.state.player_turn == deterministic_player else 1-result
        while node:
            node.visits += 1
            node.wins += result
            node = node.parent
            result = 1-result
    return start_node  # Greedy choice for actual move

# Display board
def print_board(board):
    print('\n')
    for i in range(3):
        data = []
        for j in range(3):
            x = board[3*i+j]
            if (x == ' '):
                data.append(str(3*i+j))
            else:
                data.append(x)
        print(' | '.join(data))
        if i < 2:
            print('--+---+--')
    print('\n')

# This is the minimax function. It considers all 
# the possible ways the game can go and returns 
# the value of the board
minimax_call = 0
def minimax(state:TicTacToe, player:str, depth, isMax) :
    global minimax_call
    minimax_call+=1
    score = state.get_result(player)

    # If Maximizer has won the game return his/her 
    # evaluated score 
    if (score == 1) : 
        return score

    # If Minimizer has won the game return his/her 
    # evaluated score 
    if (score == 0) :
        return score

    # If there are no more moves and no winner then 
    # it is a tie 
    if (len(state.get_legal_moves()) == 0) :
        return 0.5

    # If this maximizer's move 
    if (isMax) :     
        best = -1000 

        # Traverse all cells
        for move in state.get_legal_moves():
            newstate = state.clone()
            newstate.make_move(move)
            best = max(best, minimax(newstate, player, depth+1, not isMax))

        return best

    # If this minimizer's move 
    else :
        best = 1000 

        # Traverse all cells
        for move in state.get_legal_moves():
            newstate = state.clone()
            newstate.make_move(move)
            best = min(best, minimax(newstate, player, depth+1, not isMax))

        return best

# This will return the best possible move for the player 
def findBestMove(state:TicTacToe, player:str) : 
    bestVal = -1000 
    bestMove = -1

    # Traverse all cells, evaluate minimax function for 
    # all empty cells. And return the cell with optimal 
    # value.
    for move in state.get_legal_moves():
        newstate = state.clone()
        newstate.make_move(move)

        moveVal = minimax(newstate, player, 0, False)
        if (moveVal > bestVal) :                
            bestMove = move
            bestVal = moveVal
    return bestMove

def single_game(args):
    deterministic_player, mcts_iter = args
    game = TicTacToe()
    root = Node(game)
    parent = root

    while not game.is_terminal():
        if game.player_turn == deterministic_player:
            move = findBestMove(game.clone(), game.player_turn)
            matching_child = next((c for c in parent.children if c.move == move), None)
            if matching_child:
                child = matching_child
            else:
                new_state = game.clone()
                new_state.make_move(move)
                child = Node(new_state, parent=parent, move=move)
                parent.children.append(child)
        else:
            parent = mcts(parent, deterministic_player, iter_limit=mcts_iter)
            child = parent.best_child(c_param=0)
            move = child.move

        game.make_move(move)
        parent = child

    winner = game.get_winner()
    if winner:
        return winner
    return 'draw'

def play_game_parallel(num_games:int, deterministic_player:str, mcts_iter:int, num_workers=None):
    if num_workers is None:
        num_workers = max(1, mp.cpu_count() - 1)

    args = [(deterministic_player, mcts_iter)] * num_games
    with mp.Pool(processes=num_workers) as pool:
        results = list(tqdm(pool.imap_unordered(single_game, args), total=num_games, desc=f"{deterministic_player} vs MCTS({mcts_iter})"))

    win = {'X': 0, 'O': 0, 'draw': 0}
    for result in results:
        win[result] += 1
    return win

if __name__ == '__main__':
    iteration_counts = [10, 50, 100, 200, 300, 500, 1000, 1500, 1750, 2000, 2250, 2500]
    total_games = 10000

    for deterministic_player in ['X']:
        outer_loop = tqdm(iteration_counts, desc="MCTS Iteration Levels")
        for iters in outer_loop:
            outer_loop.set_postfix({'Iters': iters, 'Player': deterministic_player})
            print(f"\nRunning {total_games} games | MCTS iterations: {iters} | Deterministic: {deterministic_player}")

            win = play_game_parallel(total_games, deterministic_player, mcts_iter=iters)

            results = {
                'MCTS_Iterations': iters,
                'Deterministic_Player': deterministic_player,
                'Wins_X': win['X']/total_games,
                'Wins_O': win['O']/total_games,
                'Draws': win['draw']/total_games
            }

            filename = 'mcts_vs_deterministic_results2.csv'
            fieldnames = list(results.keys())
            write_header = not os.path.exists(filename)
            # Save results to CSV
            with open(filename, 'a', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                if write_header:
                    writer.writeheader()
                writer.writerow(results)

    print("All results saved to mcts_vs_deterministic_results2.csv")