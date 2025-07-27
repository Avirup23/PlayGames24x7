import random
from agents import Player, cards_from_decl,card_value
from algo_mindist import mdist
from algo_minscore import mscore,is_valid # needs all the modification


class MindistscoreAgent(Player):
    def __init__(self, name,firstfold=2,drop=True):
        super().__init__(name)
        self.strategy = 'Mindist + minscore'
        self.currsc = None
        self.decl = None
        self.firstfold=firstfold
        self.drop = drop

    def reset(self):
        self.currsc = None
        self.decl = None

    def mv1(self,hand,wcj,pilecards,first,rules=[('Pseq',3),('Iseq',3)],maxscore=80):
        #print('hand',hand,pilecards)
        if self.currsc==None:
            self.currsc = mdist(hand,wcj,rules,declr=False,shift=0)
        if first:
            if (self.currsc>self.firstfold) and self.drop:
                return 'F'
        modsc,decl = mdist(hand+[pilecards[-1]],wcj,rules,declr=True,shift=1)
        if modsc<self.currsc:
            self.currsc = modsc
            self.decl = decl
            return 'P'
        else:
            return 'D'

    def mv2(self,hand, wcj, deckorpile, card, rules=[('Pseq',3),('Iseq',3)],maxscore=80): # returns a card it rejects
        if deckorpile=='P':
            cards = []
            for m in self.decl:
                cards+=m
            handmod = hand+[card,]
            if len(cards)>13:
                cards = cards[:13]
            for c in cards:
                if c==53:
                    continue
                else:
                    handmod.remove(c)
            hand = hand+[card,]
            #print('hand',hand)
            hand.remove(sorted(handmod,key=lambda x: card_value(x,wcj))[0])
            return handmod[0],hand, (self.currsc==0)
        else:
            modsc,decl = mdist(hand+[card,],wcj,rules,declr=True,shift=1)
            if modsc<self.currsc:
                self.currsc=modsc
                cards = []
                for m in decl:
                    cards+=m
                handmod = hand+[card,]
                if len(cards)>13:
                    cards = cards[:13]
                for c in cards:
                    if c == 53:
                        continue
                    else:
                        handmod.remove(c)
                hand = hand+[card,]
                #print('hand',hand)
                hand.remove(sorted(handmod,key=lambda x: card_value(x,wcj))[0])
                return sorted(handmod,key=lambda x: card_value(x,wcj))[0],hand,(self.currsc==0)
            elif modsc==self.currsc:
                currsco = mscore(hand+[card,],wcj,rules,maxscore=maxscore)
                modsc,decl = mscore(hand+[card,],wcj,rules,True,1,maxscore=maxscore)
                if modsc < currsco:
                    cards = []
                    for m in decl:
                        cards+=m
                    handmod = hand+[card,]
                    if len(cards)>13:
                        cards = cards[:13]
                    for c in cards:
                        handmod.remove(c)
                    hand = hand+[card,]
                    #print('hand',hand)
                    hand.remove(handmod[0])
                    return handmod[0],hand,is_valid(hand,wcj,rules)
            return card,hand,False
            
