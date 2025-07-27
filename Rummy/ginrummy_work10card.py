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
from algo_minscore import mscore

# Define the output path globally so child processes can use it
OUTPUT_DIR = 'Outputs 10 version 1/'
NUM_GAMES = 2000

def gameplay(args):
    p1, p2= args
    game = RummyGame([p1, p2], ndeck=1, njoker=2, handsize=10, rules=[], seed=None, log=False, maxscore=60)
    out = game.playgame()

    # Append to CSV dynamically
    filename = f'{OUTPUT_DIR}RulevsRule_EloData.csv'
    fieldnames = ["init.score1","init.score2","init.hand1","init.hand2","Strategy 1","Strategy 2","P1 Score","P2 Score","Winner_ID"]
    write_header = not os.path.exists(filename)
    newout = {"init.score1":mscore(list(map(int, out['init.hand1'].split())),int(out['wcj']),[],False,0,maxscore=60),
              "init.score2":mscore(list(map(int, out['init.hand2'].split())),int(out['wcj']),[],False,0,maxscore=60),
              "init.hand1": out['init.hand1'],
              "init.hand2": out['init.hand2'],
              "Strategy 1":p1.strategy,
              "Strategy 2":p2.strategy,
              "P1 Score":out['score1'],
              "P2 Score":out['score2'],
              "Winner_ID":out['winner']}
    
    # print(newout)

    with open(filename, mode='a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if write_header:
            writer.writeheader()
        writer.writerow(newout)
    return out

def run_parallel_games(num_games,p1,p2, num_workers=None):
    if num_workers is None:
        num_workers = mp.cpu_count() - 1  # Leave 1 core free

    with mp.Pool(processes=num_workers) as pool:
        for _ in tqdm(pool.imap_unordered(gameplay, [(p1,p2) for _ in range(num_games)]), total=num_games, desc=f"{p1} vs {p2}"):
            pass 

if __name__ == '__main__':
    mp.freeze_support()  # For Windows compatibility
    print("10 card game simulations-------------------")
    drop = False
    players1 = [
        RandomAgent('Random1',drop=drop),
        DefeatHeur('Defeat1',drop=drop),
        MindistAgent('Mindist1',4,drop=drop),
        MinscoreAgent('Minscore1',80,piletake=3,drop=drop),
        MindistscoreAgent('Mindistscore1',4,drop=drop),
        MindistOpp2Agent('MindistOpp1',4,drop=drop)
    ]
    players2 = [
        RandomAgent('Random2',drop=drop),
        DefeatHeur('Defeat2',drop=drop),
        MindistAgent('Mindist2',4,drop=drop),
        MinscoreAgent('Minscore2',80,piletake=3,drop=drop),
        MindistscoreAgent('Mindistscore2',4,drop=drop),
        MindistOpp2Agent('MindistOpp2',4,drop=drop)
    ]
    agent_pairs = [(p1, p2) for p1 in players1 for p2 in players2 if p1.strategy != p2.strategy]

    for p1,p2 in agent_pairs:
        t10 = time()
        run_parallel_games(NUM_GAMES,p1,p2)
        t20 = time()
        print(t20-t10,f'seconds taken for {p1} vs {p2}')
