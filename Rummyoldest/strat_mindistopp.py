import random
from agents import Player, cards_from_decl,card_value
from algo_mindist import mdist
from algo_minscore import mscore,is_valid # needs all the modification


def related_cards(card:int):
    if card==52:
        return []
    rel = [card,card-1,card+1,]
    rel = rel + [card%13+13*i for i in range(4)]
    return rel

def related_cards2(cards:list,total_cards:list):
    rel = []
    for c in cards:
        rel = rel + related_cards(c)
    out1 = [] # related cards thhat are present
    out2 = [] # non-related cards thhat are present
    for c in total_cards:
        if c in rel:
            out1.append(c) 
        else:
            out2.append(c)
    return out1,out2

class MindistOpp2Agent(Player):
    def __init__(self, name,firstfold=2,drop=True):
        super().__init__(name)
        self.strategy = 'Mindist + Opp'
        self.currsc = None
        self.decl = None
        self.firstfold=firstfold
        self.opp_take = []
        self.opp_drop = []
        self.last_own_drop = None
        self.last_pilecard_len = 1
        self.drop = drop

    def reset(self):
        self.currsc = None
        self.decl = None
        self.opp_take = []
        self.opp_drop = []
        self.last_own_drop = None
        self.last_pilecard_len = 1

    def mv1(self,hand,wcj,pilecards,first,rules=[('Pseq',3),('Iseq',3)],maxscore=80):
        #print('hand',hand,pilecards)
        if self.currsc==None: # own first move
            if len(pilecards)==1:# first move of game
                pass
            else:
                self.opp_drop.append(pilecards[-1])
                self.last_pilecard_len=len(pilecards)
        else:
            self.opp_drop.append(pilecards[-1])
            if len(pilecards)==self.last_pilecard_len+1:
                self.opp_take.append(self.last_own_drop)
                self.last_pilecard_len+=1
            else:
                self.last_pilecard_len+=2


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
            self.last_own_drop = handmod[0]
            return self.last_own_drop,hand, (self.currsc==0)
        else: # choosing from deck
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
                self.last_own_drop = sorted(handmod,key=lambda x: card_value(x,wcj))[0]
                return self.last_own_drop,hand,(self.currsc==0)
            elif modsc==self.currsc: # then opponent modification is applied
                cards = []
                for m in decl:
                    cards=cards+m
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
                out1,out2 = related_cards2(self.opp_drop,handmod)
                out3,out4 = related_cards2(self.opp_take,handmod)
                self.last_own_drop = (sorted(out2+out3,key=lambda x:card_value(x,wcj))+sorted(out1+out4,key=lambda x:card_value(x,wcj)))[-1]
                hand.remove(self.last_own_drop)
                return self.last_own_drop,hand,is_valid(hand,wcj,rules)
            self.last_own_drop = card
            return self.last_own_drop,hand,False
            
