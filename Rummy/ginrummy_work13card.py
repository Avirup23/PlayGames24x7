import os
import csv
import random
import pandas as pd
import multiprocessing as mp
from game import RummyGame
from time import time
from tqdm import tqdm

from strat_defeat_heur import DefeatHeur
from strat_mindist import MindistAgent
from strat_minscore import MinscoreAgent
from strat_mindistscore import MindistscoreAgent
from strat_mindistopp import MindistOpp2Agent
from strat_random import RandomAgent
from strat_mcts import MCTSAgent

# Define the output path globally so child processes can use it
OUTPUT_DIR = 'Outputs 13 version 1/'
NUM_GAMES = 250

def gameplay(args):
    p1, p2= args
    game = RummyGame([p1, p2], ndeck=2, njoker=2, handsize=13, seed=None, log=False, maxscore=80)
    out = game.playgame()

    # Append to CSV dynamically
    filename = f'{OUTPUT_DIR}rummy.{p1}.vs.{p2}.13.card.2.joker.csv'
    fieldnames = list(out.keys())
    write_header = not os.path.exists(filename)

    with open(filename, mode='a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if write_header:
            writer.writeheader()
        writer.writerow(out)
    return out

def run_parallel_games(num_games,p1,p2, num_workers=None):
    if num_workers is None:
        num_workers = mp.cpu_count() - 1  # Leave 1 core free

    with mp.Pool(processes=num_workers) as pool:
        for _ in tqdm(pool.imap_unordered(gameplay, [(p1,p2) for _ in range(num_games)]), total=num_games, desc=f"{p1} vs {p2}"):
            pass 

if __name__ == '__main__':
    mp.freeze_support()  # For Windows compatibility
    print("13 card game simulations-------------------")
    agent_pairs = [
                   (MCTSAgent('mcts1-50',50,drop=False),MCTSAgent('mcts2-0',0,drop=False)),
                #    (MCTSAgent('mcts1-0',0,drop=False),MCTSAgent('mcts2-50',50,drop=False)),
                #    (MCTSAgent('mcts1-50',50,drop=False),MCTSAgent('mcts2-0',0,drop=False)),
                   ]

    for p1,p2 in agent_pairs:
        t10 = time()
        run_parallel_games(NUM_GAMES,p1,p2)
        t20 = time()
        print(t20-t10,f'seconds taken for {p1} vs {p2}')