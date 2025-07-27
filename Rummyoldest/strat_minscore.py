import random
from agents import Player, cards_from_decl
from algo_minscore import mscore,is_valid

class MinscoreAgent(Player):
    def __init__(self, name,firstfold=79,piletake=1,drop=True):
        super().__init__(name)
        self.strategy = 'Minscore'
        self.decl = None
        self.currsc = None
        self.firstfold = firstfold
        self.piletake = piletake
        self.drop = drop

    def reset(self):
        self.decl = None
        self.currsc = None

    def mv1(self,hand,wcj,pilecards,first,rules=[('Pseq',3),('Iseq',3)],maxscore=80):
        if self.currsc==None:
            self.currsc = mscore(hand,wcj,rules,False,0,maxscore=maxscore)
        if first:
            if (self.currsc>=self.firstfold) and self.drop:
                return 'F'
        modsc,decl = mscore(hand+[pilecards[-1]],wcj,rules,True,1,maxscore=maxscore)
        if modsc<=max(self.currsc-self.piletake,0):
            self.currsc = modsc
            self.decl = decl
            return 'P'
        return 'D'

    def mv2(self,hand, wcj, deckorpile, card, rules=[('Pseq',3),('Iseq',3)],maxscore=80): # returns a card it rejects
        if deckorpile=='P':
            cards = cards_from_decl(self.decl)
            if len(cards)!=len(hand):
                raise Exception('declaration obtained not correct length')
            handmod = hand+[card,]
            for c in cards:
                handmod.remove(c)
            hand = cards 
            return handmod[0],hand,(self.currsc==0)
        else:
            modsc,decl = mscore(hand+[card,],wcj,rules,True,1,maxscore=maxscore)
            if modsc < self.currsc:
                self.currsc = modsc
                self.decl = decl
                cards = cards_from_decl(self.decl)
                if len(cards)!=len(hand):
                    raise Exception('declaration obtained not correct length')
                handmod = hand+[card,]
                if len(cards)>13:
                    cards = cards[:13]
                for c in cards:
                    handmod.remove(c)
                hand = cards
                return handmod[0],hand,(self.currsc==0)
            else:
                return card,hand,False
            