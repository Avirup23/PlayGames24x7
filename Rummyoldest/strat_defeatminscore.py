from agents import Player
import random
from algo_minscore import mscore

def card_value(c,wcj):
    if c==53:
        return 0
    jokers = [52,]+[wcj%13+i*13 for i in range(4)]
    if c in jokers:
        return 0
    else:
        return min(10,(c % 13) + 2)

class DefeatMinscore(Player):
    def __init__(self, name, drop = True):
        super().__init__(name)
        self.strategy = 'Defeat Minscore'
        self.drop = drop
    
    def reset(self):
        self.currsc = None
    
    def mv1(self, hand, wcj, pilecards, first, rules=[('Pseq',3),('Iseq',3)],maxscore=80):
        if self.currsc==None:
            self.currsc = mscore(hand,wcj,rules,maxscore=maxscore)
        self.max_ = self.currsc
        self.argmax_ = None
        for i in range(len(hand)):
            hand_mod = hand.copy()
            hand_mod[i] = pilecards[-1]
            m = mscore(hand_mod,wcj,rules,maxscore=maxscore)
            if self.max_<m:
                self.max_ = m
                self.argmax_ = i
        if self.argmax_!=None:
            return 'P'
        return 'D'
    
    def mv2(self,hand, wcj, deckorpile, card, rules=[('Pseq',3),('Iseq',3)],maxscore=80): # returns a card it rejects
        if deckorpile == 'P':
            hand[self.argmax_],card = card,hand[self.argmax_]
            self.currsc=self.max_
            return card,hand,(self.currsc==0)
        elif deckorpile == 'D':
            self.max_ = self.currsc
            self.argmax_ = None
            for i in range(len(hand)):
                hand_mod = hand.copy()
                hand_mod[i] = card
                m = mscore(hand_mod,wcj,rules,maxscore=maxscore)
                if self.max_<m:
                    self.max_ = m
                    self.argmax_ = i
            if self.argmax_!=None:
                hand[self.argmax_],card = card,hand[self.argmax_]
                self.currsc=self.max_
                return card,hand,(self.currsc==0)
            return card,hand,(self.currsc==0)