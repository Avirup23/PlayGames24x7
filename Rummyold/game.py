from decks import Deck,Pile,Game_state
import random
from algo_minscore import mscore, is_valid, count_seq_set_decl
from algo_mindist import mdist
import time
from cards import tpprint_card as pprint_card
from cards import tpprint_hand as pprint_hand
from agents import Player

# from cards import pprint_card
# from cards import pprint_hand

def card_value(c,wcj):
    jokers = [52,]+[wcj%13+i*13 for i in range(4)]
    if c in jokers:
        return 0
    else:
        return min(10,(c % 13) + 2)

def indiv_scores(cards,wcj):
    scores = [0,0,0,0]
    for c in cards:
        if c!=52:
            scores[c//13]+=card_value(c%13,wcj)
    return scores

class RummyGame:
    ID = 0
    def __init__(self,players:list[Player],ndeck=2,njoker=2,handsize=13,rules=[('Pseq',3),('Iseq',3)],seed=None,log=True,logfile='out.txt',maxscore=80,maxround=None):
        # game variables
        if seed:
            random.seed(seed)
        self.seed = seed
        RummyGame.ID+=1
        self.rules = rules
        self.handsize = handsize
        self.maxscore = maxscore
        if maxround:
            self.maxround=maxround
        else:
            if handsize==10:
                self.maxround=25
            else:
                self.maxround=100

        # game state object
        self.state = Game_state(ndeck,njoker)

        # player variables
        self.players = players
        self.n = len(players)
        self.isfolded = [False]*self.n
        self.scores = [None]*self.n

        # game booleans
        self.gameover = False
        self.log = log
        self.logfile = logfile

        # initialize game
        self.wcj = self.state.deck.draw_wcj()
        self.state.hands = [self.state.deck.draw(self.handsize) for _ in range(self.n)]
        # self.state.observable_hands = [[] for _ in range(self.n)]
        self.state.pile.add(self.state.deck.draw(1))
        self.state.counter = -1
        self.init_hands = []


    def playgame(self,ts=False):
        if self.log:
            login = [f'Game {self.ID} begins...\n',]
            if self.seed:
                login.append(f'Game Seed: {self.seed}\n')
            login.append(f'Game has chosen {pprint_card(self.wcj,False)} as the wildcard joker!\n')
        stime = time.time()

        n = self.n
        winner = None
        winnerid = None

        if self.log:
            for i in range(self.n):
                login.append(f'Player {self.players[i]} hand: {pprint_hand(self.state.hands[i],False)}, score:{mscore(self.state.hands[i],self.wcj,self.rules,maxscore=self.maxscore)}, distance:{mdist(self.state.hands[i],self.wcj,self.rules,)}\n')
            login.append('Playing begins now!\n')

        self.init_hands = self.state.hands.copy()
        # game starts
        while self.state.counter+1<self.maxround*n:
            if ts:
                print(self.state.counter,login[-1])
            self.state.counter +=1
            counter = self.state.counter
            self.state.player_index = counter%n

            # finish game if one but everyone folds
            if sum(self.isfolded) == n-1:
                break

            # re-shuffle pile if deck is empty
            if self.state.deck.deck == []:
                self.state.deck.deck = self.state.pile.pile
                self.state.deck.shuffle()
                self.state.pile.pile=[]
                self.state.pile.add(self.state.deck.draw(1))

            # if the player has not yet folded
            if self.isfolded[counter%n]==False:
                # 1st choice of the player, fold ('F'), deck ('D') or pile ('P')
                m1 = self.players[counter%n].mv1(index = counter%n, state = self.state.clone(),wcj=self.wcj,first=(counter<n),rules=list(self.rules),maxscore=self.maxscore) # deck pile or fold
                
                # cards are folded 
                if m1 == 'F':
                    self.isfolded[counter%n] = True
                    self.scores[counter%n] = 40 - 20*int(counter<n)
                    if self.log:
                        login.append(f'Round {counter}: Player {self.players[counter%n]} folded. Hand {pprint_hand(self.state.hands[counter%n],False)}\n')
                    continue
                # pile card is chosen
                elif m1 == 'P':
                    # chosen card
                    icard = self.state.pile.peek()
                    # everyone can see it
                    # self.state.observable_hands[self.state.player_index].append(icard)
                    # 2nd choice of the player, discard any card
                    disc,hand,declared = self.players[counter%n].mv2(self.state.hands[counter%n],self.wcj,'P',self.state.pile.draw(1),rules=self.rules,maxscore=self.maxscore)
                    # if disc in self.state.observable_hands[counter%n] and disc!=icard:
                    #     self.state.observable_hands[counter%n].remove(disc)
                    self.state.pile.add(disc)
                    self.state.hands[counter%n]=hand
                    
                    if self.log:
                        login.append(f'Round {counter//2+1}: Player {self.players[counter%n]} took {pprint_card(icard,False)} from pile and returned {pprint_card(disc,False)} to pile. Hand {pprint_hand(self.state.hands[counter%n],False)}\n')
                        # login.append(f'Round {counter//n}: Observable Hand {[pprint_card(c,False) for c in self.state.observable_hands[counter%n]]}\n')
                    # if declared
                    if declared:
                        if is_valid(self.state.hands[counter%n],self.wcj,self.rules):
                            self.scores[counter%n] = 0
                            if self.log:
                                login.append(f'     Player {self.players[counter%n]} produced valid declaration.\n')
                            winner = self.players[counter%n]
                            winnerid = counter%n
                            break
                        else:
                            self.scores[counter%n] = self.maxscore
                            self.isfolded[counter%n] = True
                            if self.log:
                                login.append(f'     Player {self.players[counter%n]} produced wrong declaration.\n')
                            print(f'wrong declar by {self.players[counter%n]}')
                            continue
                # deck card is chosen
                elif m1 == 'D':
                    # chosen card
                    icard = self.state.deck.draw(1)
                    # 2nd choice of the player, discard any card
                    disc,hand,declared = self.players[counter%n].mv2(self.state.hands[counter%n],self.wcj,'D',icard,rules=self.rules,maxscore=self.maxscore)
                    # if disc in self.state.observable_hands[counter%n]:
                    #     self.state.observable_hands[counter%n].remove(disc)
                    
                    self.state.pile.add(disc)
                    self.state.hands[counter%n]=hand
                    if self.log:
                        login.append(f'Round {counter//2+1}: Player {self.players[counter%n]} took {pprint_card(icard,False)} from deck and returned {pprint_card(disc,False)} to pile. Hand {pprint_hand(self.state.hands[counter%n],False)}\n')
                    # if declared
                    if declared:
                        if is_valid(self.state.hands[counter%n],self.wcj,self.rules):
                            self.scores[counter%n] = 0
                            if self.log:
                                login.append(f'     Player {self.players[counter%n]} produced valid declaration.\n')
                            winner = self.players[counter%n]
                            winnerid = counter%n
                            break
                        else:
                            self.scores[counter%n] = self.maxscore
                            self.isfolded[counter%n] = True
                            if self.log:
                                login.append(f'     Player {self.players[counter%n]} produced wrong declaration.\n')
                            print(f'wrong declar by {self.players[counter%n]}')
                            continue
        if self.log:
            if (self.state.counter+1==self.maxround*n):
                login.append(f'Game terminated {self.maxround} rounds.\n')
        etime = time.time()

        # compute scores of each player
        for i in range(self.n):
            if self.scores[i]==None:
                self.scores[i] = mscore(self.state.hands[i],self.wcj,self.rules,maxscore=self.maxscore)
        
        # if one but everyone folds he is the winner
        if (winner == None) and (sum(self.isfolded)==self.n-1):
            for i in range(self.n):
                if self.isfolded[i]==False:
                    winner = self.players[i]
                    winnerid = i
                    break
        # the player with minimum score amongst who are not folded is the winner
        elif (winner==None): 
            notfolded = [i for i in range(n) if not self.isfolded[i]]
            winnerid = sorted(notfolded,key=lambda i: (self.scores[i],*indiv_scores(self.state.hands[i],self.wcj),i))[0]
            winner = self.players[winnerid]
        
        if self.log:
            self.mdists = [mdist(h,self.wcj,self.rules) for h in self.state.hands]
            login.append(f'Winner: Player {winner}\n\n')
            login.append('Player | Score | Mdist\n')
            for i in range(self.n):
                login.append(f'Player {self.players[i]} | {self.scores[i]} | {self.mdists[i]}\n')
            login.append(f'Game ended (time taken: {etime-stime}).\n\n-------------------------------------------\n\n')
            with open(self.logfile,'a') as f:
                f.writelines(login)
        
        # counts of sequence and sets
        pseqc,iseqc,setc = count_seq_set_decl(self.state.hands[winnerid],self.wcj,req=self.rules)
        return {
            'init.hand1': ' '.join(str(i) for i in self.init_hands[0]),
            'init.hand2': ' '.join(str(i) for i in self.init_hands[1]),
            'wcj': self.wcj,
            'score1':self.scores[0],
            'score2':self.scores[1],
            'winner':winnerid,
            'numrounds':round((self.state.counter/n)+0.49),
            'finish.hand1': ' '.join(str(i) for i in self.state.hands[0]),
            'finish.hand2': ' '.join(str(i) for i in self.state.hands[1]),
            'pure.seq.counts':pseqc,
            'impure.seq.counts':iseqc,
            'set.counts':setc
        }
