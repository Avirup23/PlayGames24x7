def card_value(c,wcj):
    jokers = [52,]+[wcj%13+i*13 for i in range(4)]
    if c in jokers:
        return 0
    else:
        return min(10,(c % 13) + 2)
    
def cards_from_decl(decl):
    out = []
    for meld in decl:
        out= out+meld
    return out


class Player:
    def __init__(self,name):
        self.name = name
        self.strategy = "NA"

    def mv1(self,hand,wcj,pilecards,first,rules=[('Pseq',3),('Iseq',3)]):
        pass

    def mv2(self, hand, wcj, deckorpile, card, rules=[('Pseq',3),('Iseq',3)]): # returns a card it rejects
        pass

    def __repr__(self):
        return f"{self.name} ({self.strategy})"
