from abc import ABC,abstractmethod
from decks import Game_state

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


class Player(ABC):
    def __init__(self,name):
        self.name = name
        self.strategy = "NA"

    @abstractmethod
    def mv1(self, index:int, state:Game_state, wcj:int, first:bool,rules:list=[('Pseq',3),('Iseq',3)], maxscore:int=80) -> int:
        raise NotImplementedError()

    @abstractmethod
    def mv2(self, hand:list[int], wcj:int, deckorpile:str, card:int, rules:list=[('Pseq',3),('Iseq',3)], maxscore:int=80) -> tuple[int,list,bool]: # returns a card it rejects
        raise NotImplementedError()

    def __repr__(self):
        return f"{self.name} ({self.strategy})"
