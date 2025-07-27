import random
import pandas as pd
import multiprocessing
from game import RummyGame
from strat_defeat_heur import DefeatHeur
from strat_mindist import MindistAgent
from strat_minscore import MinscoreAgent
from strat_mindistscore import MindistscoreAgent
from strat_mindistopp import MindistOpp2Agent
from strat_random import RandomAgent
from strat_mcts import MCTSAgent
from time import time
from tqdm import tqdm
# from make_tables_games import make_table_rummy13,make_table_ginrummy

QUANTITY1 = 1000

def work1g(see,p1,p2,log,quantity=QUANTITY1): # 10 card desc
    if see !=None:
        random.seed(see)
    for j in range(2,3):
        data = pd.DataFrame(columns=['init.hand1','init.hand2','wcj','score1','score2','winnerid','numrounds','finish.hand1','finish.hand2','pure.seq.counts','impure.seq.counts','set.counts'])
        i = 0
        t1 = time()
        for i in tqdm(range(quantity)):
            p1.reset()
            p2.reset()
            game = RummyGame([p1,p2],1,j,10,[],seed = None,log=log,maxscore=60)
            out = game.playgame()
            data.loc[i] = [out['init.hand1'],out['init.hand2'],out['wcj'],out['score1'],out['score2'],out['winner'],out['numrounds'],out['finish.hand1'],out['finish.hand2'],out['pure.seq.counts'],out['impure.seq.counts'],out['set.counts']]
            # if i==quantity//2:
            #     print(f'ginrummy.game.{p1}.vs.{p2}.joker.{j}.seed.{see} halfway, {time()-t1} seconds in')
        print(f'ginrummy.game.{p1}.vs.{p2}.joker.{j}.seed.NA done, {time()-t1} seconds in')
        data.to_csv(f'Outputs/games/ginrummy.game.{p1}.vs.{p2}.joker.{j}.seed.NA.csv')

def work2g(see,p1,p2,quantity=QUANTITY1): # 13 card desc
    random.seed(see)
    data = pd.DataFrame(columns=['score1','score2','winnerid','numrounds','pure.seq.counts','impure.seq.counts','set.counts'])
    i = 0
    t1=time()
    while (i < quantity):
        p1.reset()
        p2.reset()
        game = RummyGame([p1,p2],2,2,13,log=False)
        out = game.playgame()
        data.loc[i] = [out['score1'],out['score2'],out['winner'],out['numrounds'],out['pure.seq.counts'],out['impure.seq.counts'],out['set.counts']]
        i+=1
    print(f'rummy13.game.{p1}.vs.{p2}.joker.seed.{see} done, {time()-t1} seconds in')
    data.to_csv(f'Outputs/games/rummy13.game.{p1}.vs.{p2}.seed.{see}.csv')
  
class Process2(multiprocessing.Process): 
    def __init__(self, id, seed, work, p1, p2,log, quantity=QUANTITY1): 
        super(Process2, self).__init__() 
        self.id = id
        self.seed = seed
        self.work = work # 1 or 2
        self.p1=p1
        self.p2=p2
        self.log = log
        if isinstance(self.p1,MinscoreAgent):
            if work==1:
                self.p1.firstfold=60
            else:
                self.p1.firstfold=80
        if isinstance(self.p2,MinscoreAgent):
            if work==1:
                self.p2.firstfold=60
            else:
                self.p2.firstfold=80
        self.quantity = quantity
                 
    def run(self): 
        t11 = time()
        if self.work==1:
            work1g(self.seed,self.p1,self.p2,self.log,quantity=self.quantity)
        elif self.work==2:
            work2g(self.seed,self.p1,self.p2,quantity=self.quantity)
        else:
            raise ValueError(f"Work no {self.work} not defined")
        
        print(f"Process {self.id}: Game {self.work} between {self.p1} and {self.p2} {time()-t11}")



def maing1(seed=None,drop=True,numgames=5,log = False):
    players1 = [
        # RandomAgent('Random1',drop=drop),
        # DefeatHeur('Defeat1',drop=drop),
        # MindistAgent('Mindist1',4,drop=drop),
        MinscoreAgent('Minscore1',80,piletake=3,drop=drop),
        MindistscoreAgent('Mindistscore1',4,drop=drop),
        MindistOpp2Agent('MindistOpp1',4,drop=drop),
        # MCTSAgent('mcts1-15',15,drop=drop),
        # MCTSAgent('mcts1-50',50,drop=drop),
        MCTSAgent('mcts1-100',100,drop=drop),
        MCTSAgent('mcts1-200',200,drop=drop),
        MCTSAgent('mcts1-500',500,drop=drop),
    ]
    players2 = [
        # RandomAgent('Random2',drop=drop),
        # DefeatHeur('Defeat2',drop=drop),
        # MindistAgent('Mindist2',4,drop=drop),
        MinscoreAgent('Minscore2',80,piletake=3,drop=drop),
        MindistscoreAgent('Mindistscore2',4,drop=drop),
        MindistOpp2Agent('MindistOpp2',4,drop=drop),
        # MCTSAgent('mcts2-15',15,drop=drop),
        # MCTSAgent('mcts2-50',50,drop=drop),
        MCTSAgent('mcts2-100',100,drop=drop),
        MCTSAgent('mcts2-200',200,drop=drop),
        MCTSAgent('mcts2-500',500,drop=drop),
    ]
    pool = [Process2(j-1+10*players1.index(p1)+100*players2.index(p2),seed,j,p1,p2,log,numgames) for p1 in players1 for p2 in players2 for j in [1,]]
    for p in pool:
        p.start()
    print("Games Started") 
    for p in pool:
        p.join()

def maing2(seed=167123,drop=True,numgames=5):
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
    pool = [Process2(j-1+10*players1.index(p1)+100*players2.index(p2),seed,j,p1,p2,numgames) for p1 in players1 for p2 in players2 for j in [2,]]
    #pool = pool+ [Process2(j-1+10*players1.index(p1)+100*players2.index(p2),seed,j,p1,p2,numgames) for p1 in players1 for p2 in players2 for j in [2,]]
    for p in pool:
        p.start()
    print("Games Started") 
    for p in pool:
        p.join()



if __name__=="__main__":

    # t10 = time()
    # maing1(seed,5)
    # t20 = time()
    # print(t20-t10,'seconds taken for rummy10')
    # for j in range(4):
    #     make_table_ginrummy(j,15512)

    # t10 = time()
    # maing2(seed,drop=True,numgames=10000)
    # t20 = time()
    # print(t20-t10,'seconds taken for rummy13 drop')

    t10 = time()
    maing1(drop=False,numgames=250,log=False)
    t20 = time()
    print(t20-t10,'seconds taken for rummy10 no drop')
    
    #make_table_rummy13(15512)





