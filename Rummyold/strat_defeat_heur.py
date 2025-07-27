from agents import Player
import random
from algo_minscore import mscore, is_pure_seq, is_impure_seq, is_pure_set, is_impure_set

def card_value(c,wcj):
    if c==53:
        return 0
    jokers = [52,]+[wcj%13+i*13 for i in range(4)]
    if c in jokers:
        return 0
    else:
        return min(10,(c % 13) + 2)
def meld_value(meld,wcj):
    return sum([card_value(c,wcj) for c in meld])

class DefeatHeur(Player):
    def __init__(self, name, drop = True):
        super().__init__(name)
        self.strategy = 'Defeat Heuristic'
        self.drop = drop
    
    def reset(self):
        pass
    
    def mv1(self, index, state, wcj, first, rules=[('Pseq',3),('Iseq',3)],maxscore=80):
        hand = state.hands[index]
        pilecards = state.pile.pile
        # do not let them make any sequence or set and remmove joker in decreasing order of priority
        self.which=None
        hand = hand + [pilecards[-1],]
        n = len(hand)
        for mask in range(1, 1 << n):  # Iterate through all subsets.
            subset = [hand[i] for i in range(n) if mask & (1 << i)]
            minlen = min([r[1] for r in rules]) if (rules!=[]) else 3
            if (rules==[]):
                pass
            elif (rules[0][1]==rules[1][1]) and (rules[1][1]==minlen) and ((len(subset)>2*minlen-1) or (len(subset)<minlen)): # have to modify 12111
                continue
            if is_pure_seq(subset) or is_impure_seq(subset,wcj) or is_pure_set(subset) or is_impure_set(subset,wcj):
                if mask>(1<<(n-1)):
                    return 'D'
                else:
                    self.which = sorted(subset, key = lambda x: card_value(x,wcj))[0]
                    return 'P'
        return 'D'
    
    def mv2(self,hand, wcj, deckorpile, card, rules=[('Pseq',3),('Iseq',3)],maxscore=80): # returns a card it rejects
        if deckorpile=='P':
            hand.remove(self.which)
            hand.append(card)
        else:
            hand.append(card)
            n = len(hand)
            for mask in range(1, 1 << n):  # Iterate through all subsets.
                subset = [hand[i] for i in range(n) if mask & (1 << i)]
                minlen = min([r[1] for r in rules]) if (rules!=[]) else 3
                if (rules==[]):
                    pass
                elif (rules[0][1]==rules[1][1]) and (rules[1][1]==minlen) and ((len(subset)>2*minlen-1) or (len(subset)<minlen)): # have to modify 12111
                    continue
                if is_pure_seq(subset) or is_impure_seq(subset,wcj) or is_pure_set(subset) or is_impure_set(subset,wcj):
                    self.which = sorted(subset, key = lambda x: card_value(x,wcj))[0]
                    hand.remove(self.which)
                    break
            else:
                self.which = sorted(hand,key = lambda x: card_value(x,wcj))[0]
                hand.remove(self.which)

        return self.which,hand,(mscore(hand,wcj,rules)==0)