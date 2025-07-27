from random import shuffle
from cards import pprint_hand
from copy import deepcopy
from algo_minscore import is_valid

# Cards: 13*suit+value; suits: 0: Diamond 1: Clubs 2: Hearts 3: Spades; Values: 2-10: 
# i->i-2,next JQKA in order 9,10,11,12; printed joker: 52

class Game_state:
    def __init__(self, ndeck:int, njoker:int, player_index = 0):
        self.ndeck = ndeck
        self.njoker = njoker
        self.deck = Deck(ndeck, njoker)
        self.pile = Pile()
        self.hands = []
        self.observable_hands = []
        self.player_index = player_index
        self.counter = 0

    def clone(self):
        state = Game_state(self.ndeck,self.njoker,self.player_index)
        state.deck = deepcopy(self.deck)
        state.pile = deepcopy(self.pile)
        state.hands = deepcopy(self.hands)
        state.counter = self.counter
        return state

    def clone_and_randomize(self, num_player:int, handsize:int):
        state = Game_state(self.ndeck,self.njoker,self.player_index)
        state.pile = deepcopy(self.pile)
        known = self.hands[self.player_index]+ self.pile.pile
        all = [i for i in range(52)]*self.ndeck
        all+=[52]*self.njoker

        count = {}
        for x in all: count[x] = count.get(x, 0) + 1
        for x in known: count[x] -= 1
        unknown = [x for x in count for _ in range(count[x])]
        shuffle(unknown)
        state.deck.deck = unknown[:len(self.deck.deck)]
        unknown = unknown[len(self.deck.deck):]
        
        for i in range(num_player):
            if i != self.player_index:
                state.hands.append(unknown[:handsize])
                unknown = unknown[handsize:]
            else:
                state.hands.append(deepcopy(self.hands[self.player_index]))
        # print(state.pile.pile, state.hands)

        state.counter = self.counter
        return state

class Deck:
    def __init__(self,ndeck=2,njoker=2):
        self.njoker=njoker
        self.ndeck = ndeck
        self.deck = [i for i in range(52)]*self.ndeck
        self.deck+=[52]*self.njoker
        self.shuffle()

    def shuffle(self):
        shuffle(self.deck)

    def reset(self):
        self.deck = [i for i in range(52)]*2
        self.deck+=[52]*self.njoker
        self.shuffle()

    def peek(self): # cards are moved away from deck
        return self.deck[0]
    
    def draw(self,ncards=1):
        if ncards>len(self.deck):
            raise ValueError(f'Cards remaining in deck is less than {ncards}!')
        else:
            cards, self.deck = self.deck[:ncards],self.deck[ncards:]
            if ncards==1:
                return cards[0]
            return cards
        
    def draw_wcj(self):
        if len(self.deck)==0:
            raise ValueError(f'No Cards left!')
        i=0
        while i < len(self.deck):
            if self.deck[i]!=52:
                return self.deck.pop(i)
            i+=1
        raise ValueError(f'No Non Joker Cards left!')

        
class Pile:
    def __init__(self):
        self.pile = []

    def shuffle(self):
        shuffle(self.pile)

    def reset(self):
        self.pile = []

    def peek(self): # Cards are appended in pile
        return self.pile[-1]
    
    def draw(self,ncards=1):
        if ncards>len(self.pile):
            raise ValueError(f'Cards remaining in Pile is less than {ncards}!')
        else:
            cards, self.pile = self.pile[-ncards:],self.pile[:-ncards]
            if ncards==1:
                return cards[0]
            return cards
    def add(self,card):
        self.pile.append(card)

# sequences and sets, including pure and impures

MIN_SEQ,MIN_SET = 3,3

def all_same(l):
    return all([i==l[0] for i in l])

def is_pure_seq(cards): # returns True if pure sequence, False o.w.
    if 52 in cards:
        #print("Joker ISSUE")
        return False
    if (len(cards)<MIN_SEQ) or (len(cards)>13): # number of cards in a suit
        #print("SIZE ISSUE")
        return False
    if not all_same([i//13 for i in cards]):
        #print("SUIT ISSUE")
        return False
    values = sorted([i%13 for i in cards])
    if sorted(values)!=sorted(list(set(values))):
        return False
    if values[-1]==12: # Ace is there
        if values[0]==0: # A,2,3,...
            curr = -1
            for v in values[:-1:]:
                if v !=curr+1:
                    #print("A,2,3 ISSUE")
                    return False
                else:
                    curr+=1
            return True
        else: # start from backwards, A,K,Q,...
            curr = 12
            for v in values[-2::-1]:
                if v !=curr-1:
                    #print("A,K,Q ISSUE")
                    return False
                else:
                    curr-=1
            return True
    else:
        curr = values[-1]
        for v in values[-2::-1]:
            if v !=curr-1:
                #print(values)
                return False
            else:
                curr-=1
        return True

def is_impure_seq(cards,wildcard_joker):
    if (len(cards)<MIN_SEQ):
        return False
    jokers = [52,]+[wildcard_joker%13+13*i for i in range(4)]
    values = sorted([c for c in cards if c not in jokers])
    if not values: # all joker, not considered as impure sequence
        return False
    if not all_same([i//13 for i in values]):
        return False
    values = [v%13 for v in values]
    num_jokers = len(cards) - len(values)
    if sorted(values)!=sorted(list(set(values))):
        return False
    if values[-1]==12: # Ace is there, check for wrap around A,2,3,.., otherwise its same
        curr=-1
        j_used = 0
        for v in values[:-1:]:
            if v!=curr+1:
                j_used+=v-curr-1
                curr = v
            else:
                curr+=1
            if j_used>num_jokers:
                return False
        return True
    # now check from backwards
    curr = values[-1]
    j_used=0
    for v in values[-2::-1]:
        if v !=curr-1:
            j_used+=curr-1-v
            curr=v
        else:
            curr-=1
        if j_used>num_jokers:
            return False
    return True

def is_pure_set(cards):
    if 52 in cards:
        #print(1)
        return False
    if (len(cards)<MIN_SET) or (len(cards)>4):
        #print(2)
        return False
    if not all_same([i%13 for i in cards]): # same value
        #print(3)
        return False
    if sorted(list(set(cards)))!=sorted(cards): # duplicate
        #print(cards)
        #print(list(set(cards)))
        return False
    return True

def is_impure_set(cards,wildcard_joker):
    if (len(cards)<MIN_SET):
        return False
    jokers = [52,]+[wildcard_joker%13+13*i for i in range(4)]
    values = sorted([c for c in cards if c not in jokers])
    if not all_same([i%13 for i in values]): # same value
        return False
    if sorted(list(set(values)))!=sorted(values): # duplicate
        return False
    return True

# if __name__=='__main__':
#     while True:
#         print('---------------------------------------------')
#         cards = list(map(int,input("Enter card numbers (sep by space): ").split()))
#         wcj = int(input("Enter the Wild Card Joker: "))
#         print(f"The hand is: ",pprint_hand(sorted(cards),wcj))
#         print(f"The hand is a Pure Seq: ",int(is_pure_seq(cards)))
#         print(f"The hand is a Pure Set: ",int(is_pure_set(cards)))
#         print(f"The hand is a Impure Seq: ",int(is_impure_seq(cards,wcj)))
#         print(f"The hand is a Impure Set: ",int(is_impure_set(cards,wcj)))


#         if input("If you wish to stop, type X: ")=='X':
#             break