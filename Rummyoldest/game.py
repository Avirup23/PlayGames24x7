from decks import Deck,Pile
import random
from algo_minscore import mscore, is_valid, count_seq_set_decl
from algo_mindist import mdist
import time
from cards import tpprint_card as pprint_card
from cards import tpprint_hand as pprint_hand
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
    def __init__(self,players,ndeck=2,njoker=2,handsize=13,rules=[('Pseq',3),('Iseq',3)],seed=None,log=True,logfile='out.txt',maxscore=80,maxround=None):
        if seed:
            random.seed(seed)
        RummyGame.ID+=1
        self.seed = seed
        self.rules = rules
        self.deck = Deck(ndeck,njoker)
        self.pile = Pile()
        self.handsize = handsize
        self.maxscore = maxscore
        if maxround:
            self.maxround=maxround
        else:
            if handsize==10:
                self.maxround=25
            else:
                self.maxround=100

        self.players = players
        self.n = len(players)
        self.isfolded = [False]*self.n
        self.hands = [] 
        self.scores = [None]*self.n
        self.gameover = False
        self.log = log
        self.logfile = logfile

    def playgame(self,ts=False):
        if self.log:
            login = [f'Game {self.ID} begins...\n',]
            if self.seed:
                login.append(f'Game Seed: {self.seed}\n')
        stime = time.time()
        winner = None
        #aborted = False
        winnerid = None
        self.wcj = self.deck.draw_wcj()
        if self.log:
            login.append(f'Game has chosen {pprint_card(self.wcj,False)} as the wildcard joker!\n')
        self.hands = [self.deck.draw(self.handsize) for i in range(self.n)]
        # for h in self.hands:
        #     if None in h:
        #         print('game has None,',h)
        if self.log:
            for i in range(self.n):
                login.append(f'Player {self.players[i]} hand: {pprint_hand(self.hands[i],False)}, score:{mscore(self.hands[i],self.wcj,self.rules,maxscore=self.maxscore)}, distance:{mdist(self.hands[i],self.wcj,self.rules,)}\n')
        self.pile.add(self.deck.draw(1))
        counter = -1
        n = self.n
        if self.log:
            login.append('Playing begins now!\n')
        while counter<self.maxround*n:
            #print(counter)
            if ts:
                print(counter,login[-1])
            counter += 1
            if sum(self.isfolded)==n-1:
                break
            if self.deck.deck == []:
                self.deck.deck = self.pile.pile
                self.deck.shuffle()
                self.pile.pile=[]
                self.pile.add(self.deck.draw(1))
            if self.isfolded[counter%n]==False: # the player plays
                #print(self.hands[counter%n],sep='\n')
                m1 = self.players[counter%n].mv1(hand=self.hands[counter%n],wcj=self.wcj,pilecards=self.pile.pile,first=(counter<n),rules=list(self.rules),maxscore=self.maxscore) # deck pile or fold
                #print('counter',counter,'m1',m1)
                if m1 == 'F':
                    #print('Folded')
                    self.isfolded[counter%n] = True
                    self.scores[counter%n] = 40 - 20*int(counter<n)
                    if self.log:
                        login.append(f'Round {counter//n}: Player {self.players[counter%n]} folded.\n')
                    continue
                elif m1 == 'P':
                    icard = self.pile.peek()
                    disc,hand,declared = self.players[counter%n].mv2(self.hands[counter%n],self.wcj,'P',self.pile.draw(1),rules=self.rules,maxscore=self.maxscore)
                    if self.log:
                        login.append(f'Round {counter//n}: Player {self.players[counter%n]} took {pprint_card(icard,False)} from pile and returned {pprint_card(disc,False)} to pile.\n')
                    self.pile.add(disc)
                    self.hands[counter%n]=hand
                    if declared:
                        if is_valid(self.hands[counter%n],self.wcj,self.rules):
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
                elif m1 == 'D':
                    icard = self.deck.draw(1)
                    disc,hand,declared = self.players[counter%n].mv2(self.hands[counter%n],self.wcj,'D',icard,rules=self.rules,maxscore=self.maxscore)
                    if self.log:
                        login.append(f'Round {counter//n}: Player {self.players[counter%n]} took {pprint_card(icard,False)} from deck and returned {pprint_card(disc,False)} to pile.\n')
                    self.pile.add(disc)
                    self.hands[counter%n]=hand
                    if declared:
                        if is_valid(self.hands[counter%n],self.wcj,self.rules):
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
        if (counter==self.maxround*n):
            if self.log:
                login.append(f'Game terminated {self.maxround} rounds.\n')
        etime = time.time()
        for i in range(self.n):
            if self.scores[i]==None:
                self.scores[i] = mscore(self.hands[i],self.wcj,self.rules,maxscore=self.maxscore)
        if (winner == None) and (sum(self.isfolded)==self.n-1):
            for i in range(self.n):
                if self.isfolded[i]==False:
                    winner = self.players[i]
                    winnerid = i
                    break
        elif (winner==None): # the player with minimum score amongst who are not folded
            notfolded = [i for i in range(n) if not self.isfolded[i]]
            winnerid = sorted(notfolded,key=lambda i: (self.scores[i],*indiv_scores(self.hands[i],self.wcj),i))[0]
            winner = self.players[winnerid]
        
        if self.log:
            self.mdists = [mdist(h,self.wcj,self.rules) for h in self.hands]
            login.append(f'Winner: Player {winner}\n\n')
            login.append('Player | Score | Mdist\n')
            for i in range(self.n):
                login.append(f'Player {self.players[i]} | {self.scores[i]} | {self.mdists[i]}\n')
            login.append(f'Game ended (time taken: {etime-stime}).\n\n-------------------------------------------\n\n')
            with open(self.logfile,'a') as f:
                f.writelines(login)
        pseqc,iseqc,setc = count_seq_set_decl(self.hands[winnerid],self.wcj,req=self.rules)
        return {'sc1':self.scores[0],'sc2':self.scores[1],'winner':winnerid,'numrounds':round((counter/n)+0.49),'pseqc':pseqc,'iseqc':iseqc,'setc':setc}
