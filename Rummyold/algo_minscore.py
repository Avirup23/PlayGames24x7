# This file contains algorithms like min_score, min_dist etc for original rummy
MIN_SEQ = 3
MIN_SET = 3

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
                #print('yesss ffff',j_used,num_jokers)
                curr = v
            else:
                curr+=1
            if j_used>num_jokers:
                break
        else:
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
    if j_used<=num_jokers:
        return True
    return False

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

def card_value(c,wcj):
    jokers = [52,]+[wcj%13+i*13 for i in range(4)]
    if c in jokers:
        return 0
    else:
        return min(10,(c % 13) + 2)

def getreq(typ,minlen):
    def req(meld,wcj):
        if typ == 'Pseq':
            return is_pure_seq(meld) and (len(meld)>=minlen)
        elif typ == 'Iseq':
            return is_impure_seq(meld,wcj) and (len(meld)>=minlen)
        elif typ == 'Pset':
            return is_pure_set(meld) and (len(meld)>=minlen)
        elif typ == 'Iset':
            return is_impure_set(meld,wcj) and (len(meld)>=minlen)
        return (len(meld)>=minlen)
    return req

class MinScore:
    def __init__(self,hand,wcj,req=[('Pseq',3),('Iseq',3)],shift=0,minlen=3,declr=False,maxscore=80):
        if sum([rr[1] for rr in req])>len(hand)-shift:
            raise AssertionError("Requirement can not be satisfied with given cards!")
        while ((len(hand)-sum([r[1] for r in req])-shift)//minlen)>0:
            req.append(('',minlen))
        self.req = req
        self.levels = len(req)
        self.hand = hand
        self.wcj = wcj
        self.declr = declr
        self.n = len(hand)
        self.shift = shift
        self.maxscore=maxscore
        if None in hand:
            print(hand)
        self.card_values = [card_value(card,wcj) for card in hand] # Card values (Ace and Face cards = 10).
        self.valid_melds = [] # Precompute all subsets that form valid melds.
        for mask in range(1, 1 << self.n):  # Iterate through all subsets.
            subset = [hand[i] for i in range(self.n) if mask & (1 << i)]
            if (req[0][1]==req[1][1]) and (req[1][1]==minlen) and ((len(subset)>2*minlen-1) or (len(subset)<minlen)): # have to modify 12111
                continue
            if is_pure_seq(subset) or is_impure_seq(subset,wcj) or is_pure_set(subset) or is_impure_set(subset,wcj):
                self.valid_melds.append(mask)

        # DP table to store minimum score for each (mask, requirementState).
        self.dp = [[float('inf')] * self.levels for _ in range(1 << self.n)]
        self.dp[0][0] = 0  # Base case: no cards left, no requirements fulfilled, score = 0.
        if self.declr or (self.shift!=0):
            self.meld_dp = [[float('inf')] * self.levels for _ in range(1 << self.n)]
            self.meld_dp[0][0] = 0  # Base case: no cards left, no requirements fulfilled, score = 0.

    def compute(self,mask,state,nreqd):
        declr1 = self.declr
        if declr1 or (self.shift!=0):
            if self.dp[mask][state] != float('inf'):
                return self.dp[mask][state],self.meld_dp[mask][state]
        else:              
            if self.dp[mask][state] != float('inf'):
                return self.dp[mask][state]
            # Calculate deadwood score for current mask.
        deadwood_score = sum(self.card_values[i] for i in range(self.n) if mask & (1 << i))
        self.dp[mask][state] = deadwood_score
        if declr1 or (self.shift!=0):
            self.meld_dp[mask][state] = mask

        for meld in self.valid_melds:
            if declr1 or (self.shift!=0):
                tmp = (float('inf'),mask)
            else:
                tmp = float('inf')
            if mask & meld == meld:  # Check if meld is a subset of the current mask.
                new_mask = mask ^ meld  # Remove meld cards from current mask.
                # Update requirement state based on the meld type.
                subset = [self.hand[i] for i in range(self.n) if meld & (1 << i)]
                s = len(subset)
                if s>nreqd:
                    continue
                for i in range(self.levels):
                    if getreq(*self.req[i])(subset,self.wcj) and (state==self.levels-i-1):
                        tmp = self.compute(new_mask, state-1,nreqd-s)
                        break
                if declr1 or (self.shift!=0):
                    if (tmp[0]!=float('inf')) and (tmp[0]<self.dp[mask][state]):
                        self.dp[mask][state] = tmp[0]
                        self.meld_dp[mask][state] = meld # from this you can backtrack your optimal path and get the minimised soln
                else:
                    if (tmp!=float('inf')) and (tmp<self.dp[mask][state]):
                        self.dp[mask][state] = tmp
        if declr1 or (self.shift!=0):
            return self.dp[mask][state],self.meld_dp[mask][state]
        return self.dp[mask][state]

    def min_score(self): 
        self.nreqd = self.n-self.shift
        result = self.compute((1 << self.n) - 1, self.levels-1,nreqd = self.nreqd)
        if (self.declr == False) and (self.shift==0):
            return min(result,self.maxscore)
        result = result[0]
        declar = [[self.hand[i] for i in range(self.n) if self.meld_dp[(1<<self.n)-1][self.levels-1] & (1 << i)],]
        masks = [self.meld_dp[(1<<self.n)-1][self.levels-1],]
        curr = ((1<<self.n)-1)^(self.meld_dp[(1<<self.n)-1][self.levels-1])
        s = self.levels-2
        while s>=0:
            if (self.dp[curr][s]!=float('inf')) and (self.meld_dp[curr][s]!=0):
                masks.append(self.meld_dp[curr][s])
                declar.append([self.hand[i] for i in range(self.n) if self.meld_dp[curr][s] & (1 << i)])
                #print(masks)
                curr = curr^int(masks[-1])
                #print(declar)
                s -= 1
            else:
                #print("Terminated")
                break
        if curr!=0:
            declar.append([self.hand[i] for i in range(self.n) if curr & (1 << i)])
        if (self.shift!=0): # so extra cards are present in declar[-1], which we need to remove
            result -= sum(sorted([card_value(c,self.wcj) for c in declar[-1]])[-self.shift:])
            #print('sorted',sorted([card_value(c,self.wcj) for c in declar[-1]])[-self.shift:])
            declar[-1] = sorted(declar[-1],key=lambda x: card_value(x,self.wcj))[:-self.shift]
            if declar[-1]==[]:
                declar.pop(-1)
        if self.declr==False:
            return min(result,self.maxscore)
        return min(result,self.maxscore),declar

def mscore(hand,wcj,req=[('Pseq',3),('Iseq',3)],declr=False,shift=0,maxscore=80):
    m = MinScore(hand,wcj,req=req,declr=declr,shift=shift,maxscore=maxscore)
    return m.min_score()

def is_valid(hand,wcj,req=[('Pseq',3),('Iseq',3)],shift=0):
    return mscore(hand,wcj,req=req,shift=shift) == 0



def count_seq_set_decl(hand,wcj,req=[('Pseq',3),('Iseq',3)],shift=0):
    msc, decl = mscore(hand,wcj,req,True,shift)    
    pseqcount = 0
    iseqcount = 0
    setcount = 0
    for meld in decl:
        if is_pure_seq(meld):
            pseqcount+=1
        elif is_impure_seq(meld,wcj):
            iseqcount+=1
        elif is_pure_set(meld) or is_impure_set(meld,wcj):
            setcount+=1
    return pseqcount,iseqcount,setcount