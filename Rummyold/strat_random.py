import random
from agents import Player
from algo_minscore import is_valid


class RandomAgent(Player):
    def __init__(self, name, drop=True):
        super().__init__(name)
        self.strategy = 'Random'
        self.drop = drop
    
    def reset(Self):
        pass
    
    def mv1(self, index, state, wcj, first, rules=[('Pseq',3),('Iseq',3)],maxscore=80):
        hand = state.hands[index]
        pilecards = state.pile.pile
        if self.drop:
            return random.choice(['D','P','F']) # deck / pile / fold
        return random.choice(['D','P']) # deck / pile
    
    def mv2(self, hand, wcj, deckorpile, card, rules=[('Pseq',3),('Iseq',3)],maxscore=80): # returns a card it rejects
        if deckorpile=='P':
            disc = random.choice(hand)
            hand.remove(disc)
            return disc, hand+[card,], is_valid(hand+[card,],wcj,rules)
        else:
            hand.append(card)
            disc = random.choice(hand)
            hand.remove(disc)
            return disc, hand, is_valid(hand,wcj,rules)
            
