# This file contains algorithms like min_score, min_dist etc for original rummy , modify code 12111
MIN_SEQ = 3
MIN_SET = 3
# from tqdm import trange

def all_same(l):
    return all([i==l[0] for i in l])

def is_pure_seq53(cards):
    if (len(cards)<MIN_SEQ):
        return False
    if 52 in cards:
        return False
    jokers = [53,]
    values = [c for c in cards if c not in jokers]
    if values == []:
        return True
    elif None in values:
        print(values,cards)
    values = sorted(values)
    if not all_same([i//13 for i in values]):
        return False
    values = [v%13 for v in values]
    num_jokers = len(cards) - len(values)
    if sorted(values)!=sorted(list(set(values))):
        return False
    if values==[]:
        return True
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
def is_impure_seq53(cards,wildcard_joker):
    if (len(cards)<MIN_SEQ):
        return False
    jokers = [52,53,]+[wildcard_joker%13+13*i for i in range(4)]
    values = [c for c in cards if c not in jokers]
    if values == []:
        return True
    values = sorted(values)
    #values = sorted([c for c in cards if c not in jokers])
    if not values: # all joker, not considered as impure sequence
        return False
    if not all_same([i//13 for i in values]):
        return False
    values = [v%13 for v in values]
    if sorted(values)!=sorted(list(set(values))):
        return False
    num_jokers = len(cards) - len(values)
    if values==[]:
        return True
    # print(values,num_jokers)
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

def is_pure_set53(cards):
    if 52 in cards:
        return False
    if (len(cards)<MIN_SET) or (len(cards)>4):
        return False
    values = sorted([c for c in cards if c!=53])
    if not all_same([i%13 for i in values]): # same value
        return False
    if sorted(list(set(values)))!=sorted(values): # duplicate
        return False
    return True

def is_impure_set53(cards,wildcard_joker):
    if (len(cards)<MIN_SET):
        return False
    jokers = [52,53,]+[wildcard_joker%13+13*i for i in range(4)]
    values = sorted([c for c in cards if c not in jokers])
    if not all_same([i%13 for i in values]): # same value
        return False
    if sorted(list(set(values)))!=sorted(values): # duplicate
        return False
    return True

# def card_value(c,wcj):
#     jokers = [52,]+[wcj%13+i*13 for i in range(4)]
#     if c in jokers:
#         return 0
#     else:
#         return min(10,(c % 13) + 2)

def getreq(typ,minlen):
    def req(meld,wcj):
        if typ == 'Pseq':
            return is_pure_seq53(meld) and (len(meld)>=minlen)
        elif typ == 'Iseq':
            return is_impure_seq53(meld,wcj) and (len(meld)>=minlen)
        elif typ == 'Pset':
            return is_pure_set53(meld) and (len(meld)>=minlen)
        elif typ == 'Iset':
            return is_impure_set53(meld,wcj) and (len(meld)>=minlen)
        return (len(meld)>=minlen)
    return req

class MinDist:
    def __init__(self,hand,wcj,req=[('Pseq',3),('Iseq',3)],maxdist=9,minlen=3,declr=False,shift=0):
        if sum([rr[1] for rr in req])>len(hand)-shift:
            raise AssertionError("Requirement can not be satisfied with given cards!")
        while ((len(hand)-sum([r[1] for r in req])-shift)//minlen)>0:
            req.append(('',minlen))
        self.levels = len(req)
        self.minlen = minlen
        self.shift = shift
        self.req = req
        self.hand = hand
        self.wcj = wcj
        self.maxdist = maxdist
        self.declr = declr
        self.n = len(hand)
        self.valid_melds = [] # Precompute all subsets that form valid melds.
        if None in hand:
            print(hand)
        for mask in range(1, 1 << self.n):  # Iterate through all subsets.
            subset = [hand[i] for i in range(self.n) if mask & (1 << i)]
            if (req[0][1]==req[1][1]) and (req[1][1]==minlen) and ((len(subset)>2*minlen-1) or (len(subset)<minlen)): # have to modify 12111
                continue
            if is_pure_seq53(subset) or is_impure_seq53(subset,wcj) or is_pure_set53(subset) or is_impure_set53(subset,wcj):
                self.valid_melds.append(mask)

    def compute(self,mask,state,new_cards,needed):
        new_n = len(new_cards)
        declr1 = self.declr
        if declr1:
            if self.dp[mask][state] != float('inf'):
                return self.dp[mask][state],self.meld_dp[mask][state]
        else:              
            if self.dp[mask][state] != float('inf'):
                return self.dp[mask][state]
            # Calculate deadwood score for current mask.
        deadwood_score = len([i for i in range(new_n) if mask & (1 << i)])
        self.dp[mask][state] = deadwood_score
        if declr1:
            self.meld_dp[mask][state] = mask

        for meld in self.valid_melds:
            if declr1:
                tmp = (float('inf'),mask)
            else:
                tmp = float('inf')
            if mask & meld == meld:  # Check if meld is a subset of the current mask.
                new_mask = mask ^ meld  # Remove meld cards from current mask.
                # Update requirement state based on the meld type.
                subset = [new_cards[i] for i in range(new_n) if meld & (1 << i)]
                if len(subset)>needed:
                    continue
                for i in range(self.levels):
                    if getreq(*self.req[i])(subset,self.wcj) and (state==self.levels-i-1):
                        tmp = self.compute(new_mask, state-1,new_cards,needed-len(subset))
                        break
                # if getreq(*self.req[0])(subset,self.wcj) and (state==3):
                #     tmp = self.compute(new_mask, state-1,new_cards,needed-len(subset))
                # elif getreq(*self.req[1])(subset,self.wcj) and (state==2):
                #     tmp = self.compute(new_mask, state-1,new_cards,needed-len(subset))
                # elif getreq(*self.req[2])(subset,self.wcj) and (state==1):
                #     tmp = self.compute(new_mask, state-1,new_cards,needed-len(subset))
                # elif getreq(*self.req[3])(subset,self.wcj) and (state==0):
                #     tmp = self.compute(new_mask, state-1,new_cards,needed-len(subset))
                if declr1:
                    if (tmp[0]!=float('inf')) and (tmp[0]<self.dp[mask][state]):
                        self.dp[mask][state] = tmp[0]
                        self.meld_dp[mask][state] = meld # from this you can backtrack your optimal path and get the minimised soln
                else:
                    if (tmp!=float('inf')) and (tmp<self.dp[mask][state]):
                        self.dp[mask][state] = tmp
        if declr1:
            return self.dp[mask][state],self.meld_dp[mask][state]
        return self.dp[mask][state]

    def waste_cards(self,new_cards): 
        needed = len(self.hand)-self.shift
        new_n = len(new_cards)
        self.valid_melds = [] # Precompute all subsets that form valid melds.
        for mask in range(1, 1 << new_n):  # Iterate through all subsets.
            subset = [new_cards[i] for i in range(new_n) if mask & (1 << i)]
            if (self.req[0][1]==self.req[1][1]) and (self.req[1][1]==self.minlen) and ((len(subset)>2*self.minlen-1) or (len(subset)<self.minlen)):
                continue # have to change???? 12111
            if is_pure_seq53(subset) or is_impure_seq53(subset,self.wcj) or is_pure_set53(subset) or is_impure_set53(subset,self.wcj):
                self.valid_melds.append(mask)
        
        # DP table to store minimum score for each (mask, requirementState).
        self.dp = [[float('inf')] * self.levels for _ in range(1 << new_n)]
        self.dp[0][0] = 0  # Base case: no cards left, no requirements fulfilled, score = 0.
        if self.declr:
            self.meld_dp = [[float('inf')] * self.levels for _ in range(1 << new_n)]
            self.meld_dp[0][0] = 0  # Base case: no cards left, no requirements fulfilled, score = 0.

        result = self.compute((1 << new_n) - 1, self.levels-1,new_cards,needed)
        if self.declr == False:
            return result
        
        declar = [[new_cards[i] for i in range(new_n) if self.meld_dp[(1<<new_n)-1][self.levels-1] & (1 << i)],]
        masks = [self.meld_dp[(1<<new_n)-1][self.levels-1],]
        curr = ((1<<new_n)-1)^(self.meld_dp[(1<<new_n)-1][self.levels-1])
        #print(declar)
        s = self.levels-2
        while s>=0:
            if (self.dp[curr][s]!=float('inf')) and (self.meld_dp[curr][s]!=0):
                masks.append(self.meld_dp[curr][s])
                declar.append([new_cards[i] for i in range(new_n) if self.meld_dp[curr][s] & (1 << i)])
                #print(masks)
                curr = curr^int(masks[-1])
                #print(declar)
                s -= 1
                if sum(list(map(len,declar)))>=len(self.hand)-self.shift:
                    break
            else:
                break
        return result[0],declar
    def min_dist(self):
        for i in range(self.maxdist+1):
            new_cards = self.hand+[53,]*i
            w = self.waste_cards(new_cards)
            if self.declr:
                if w[0]==i+self.shift:
                    return i,w[1]
            else:
                if w==i+self.shift:
                    return i
        print(self.hand,self.wcj,sep='\n')
        raise TimeoutError(f"Minimum Distance > {self.maxdist}")
    def min_dist_with_prior(self,prior): # 1-alteration mindist=prior, hence curr mindist can only be prior/pr-1/pr+1 if we cannot reject any card
        if prior==0:
            options = [prior,prior+1]
        else:
            options = [prior-1,prior,prior+1]
        for i in options:
            new_cards = self.hand+[53,]*i
            w = self.waste_cards(new_cards)
            if self.declr:
                if w[0]<=i+self.shift:
                    return i,w[1]
            else:
                if w<=i+self.shift:
                    return i
        raise TimeoutError(f"Wrong prior {prior} for hand {self.hand} wcj {self.wcj} shift {self.shift}")
def mdist(hand,wcj,req=[('Pseq',3),('Iseq',3)],maxdist=9,declr=False,shift=0,prior=None):
    m = MinDist(hand,wcj,req=req,maxdist=maxdist,declr=declr,shift=shift)
    if prior!=None:
        return m.min_dist_with_prior(prior=prior)
    return m.min_dist()

