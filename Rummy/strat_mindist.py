import random
from agents import Player, cards_from_decl,card_value
from algo_mindist import mdist

 
class MindistAgent(Player):
    def __init__(self, name,firstfold=2,drop=True):
        super().__init__(name)
        self.strategy = 'Mindist'
        self.currsc = None
        self.decl = None
        self.firstfold=firstfold
        self.drop = drop

    def reset(self):
        self.currsc = None
        self.decl = None

    def mv1(self, index, state, wcj, first, rules=[('Pseq',3),('Iseq',3)],maxscore=80):
        hand = state.hands[index]
        pilecards = state.pile.pile
        if self.currsc==None:
            self.currsc = mdist(hand,wcj,rules,declr=False,shift=0)
        if first:
            if (self.currsc>self.firstfold) and self.drop:
                return 'F'
        modsc,decl = mdist(hand+[pilecards[-1],],wcj,rules,declr=True,shift=1,prior = self.currsc)
        if modsc<self.currsc:
            self.currsc = modsc
            self.decl = decl
            return 'P'
        else:
            return 'D'

    def mv2(self,hand, wcj, deckorpile, card, rules=[('Pseq',3),('Iseq',3)],maxscore=80): # returns a card it rejects
        #print('beforediscard',hand,card)
        if deckorpile=='P':
            cards = cards_from_decl(self.decl)
            handmod = hand+[card,]
            if len(cards)!=len(hand):
                raise Exception(f'declaration obtained not correct length {self.decl} {hand}')
            for c in cards:
                if c==53:
                    continue
                else:
                    handmod.remove(c)
            hand = hand+[card,]
            out = sorted(handmod,key=lambda x: card_value(x,wcj))[-1]
            hand.remove(out)
            return out,hand,(self.currsc==0)
        else:
            modsc,decl = mdist(hand+[card,],wcj,rules,declr=True,shift=1,prior=self.currsc)
            if modsc<self.currsc:
                self.currsc = modsc
                self.decl = decl
                cards = cards_from_decl(self.decl)
                #print('cfromdecl',cards)
                handmod = hand+[card,]
                if len(cards)!=len(hand):
                    raise Exception('declaration obtained not correct length')
                for c in cards:
                    if c == 53:
                        continue
                    else:
                        handmod.remove(c)
                hand = hand+[card,]
                #print('wtf',sorted(handmod,key=lambda x: card_value(x,wcj)))
                out = sorted(handmod,key=lambda x: card_value(x,wcj))[-1]
                hand.remove(out)
                #print('after discard',hand,out,handmod)
                return out,hand,(self.currsc==0)
            else:
                return card,hand,False
            
