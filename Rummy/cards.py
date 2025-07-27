suits = {
    0: 'Diamond',
    1: 'Clubs',
    2: 'Hearts',
    3: 'Spades'
}
vals = {
    0: '2',
    1: '3',
    2: '4',
    3: '5',
    4: '6',
    5: '7',
    6: '8',
    7: '9',
    8: '10',
    9: 'J',
    10: 'Q',
    11: 'K',
    12: 'A'
}
rev_vals = {
    '2':0,
    '3':1,
    '4':2,
    '5':3,
    '6':4,
    '7':5,
    '8':6,
    '9':7,
    '10':8,
    'J':9,
    'Q':10,
    'K':11,
    'A':12
}

uni = {
    'Spades':'\u2660',
    'Clubs':'\u2663',
    'Hearts':'\u2665',
    'Diamond':'\u2666',
    'Joker':'\U0001F0CF',
    'Any':'\U0001F0A0'
}

def to_num(c): 
    if c=='J':
        return 52
    elif len(c)!=2:
        raise ValueError("Not a valid card")
    else:
        if c[-1] == 'D':
            s = 0
        elif c[-1] == 'C':
            s = 1
        elif c[-1] == 'H':
            s = 2
        elif c[-1] == 'S':
            s = 3
        else:
            return ValueError("Not valid suit")
        return (13*s)+rev_vals(c[:-1])

def get_hand(shand):
    hand = []
    for sh in shand:
        hand.append(to_num(sh))
    return hand


def print_card(v:int,Print=True):
    if v==53:
        if Print:
            print('Any')
        return 'Any'
    if v==52:
        if Print:
            print('Joker')
        return 'Joker'
    else:
        val = v%13
        s = v//13
        if Print:
            print(vals[val] + ' of ' + suits[s])
        return vals[val] + ' of ' + suits[s]

def print_hand(hand,Print=True):
    hand = sorted(hand)
    #print("The hand is: ")
    if Print:
        print('   '.join([print_card(c,False) for c in hand]))
    return '   '.join([print_card(c,False) for c in hand])

def print_declr(declr,Print=True):
    pdeclr = []
    for meld in declr:
        pdeclr.append(print_hand(meld,Print=False))
    if Print:
        print('     '.join(pdeclr))
    return '     '.join(pdeclr)

def pprint_card(v,Print=True):
    if v==53:
        if Print:
            print(uni['Any'])
        return uni['Any']
    if v==52:
        if Print:
            print(uni['Joker'])
        return uni['Joker']
    else:
        val = v%13
        s = v//13
        if Print:
            print(vals[val] + uni[suits[s]])
        return vals[val] + uni[suits[s]]
    
def pprint_hand(hand,Print=True):
    hand = sorted(hand)
    if Print:
        print("The hand is: ",'  '.join([pprint_card(c,False) for c in hand]))
    return ' '.join([pprint_card(c,False) for c in hand])

def pprint_declr(declr,Print=False):
    pdeclr = []
    for meld in declr:
        pdeclr.append(pprint_hand(meld,False))
    if Print:
        print('   '.join(pdeclr))
    return '    '.join(pdeclr)



def tpprint_card(v,Print=True):
    if v==53:
        if Print:
            print('XX')
        return 'XX'
    if v==52:
        if Print:
            print('Jo')
        return 'Jo'
    else:
        val = v%13
        s = v//13
        if Print:
            print(vals[val]+suits[s][0])
        return vals[val]+suits[s][0]
    
def tpprint_hand(hand,Print=True):
    hand = sorted(hand)
    if Print:
        print("The hand is: ",'  '.join([tpprint_card(c,False) for c in hand]))
    return ' '.join([tpprint_card(c,False) for c in hand])

def tpprint_declr(declr,Print=False):
    pdeclr = []
    for meld in declr:
        pdeclr.append(tpprint_hand(meld,False))
    if Print:
        print('   '.join(pdeclr))
    return '    '.join(pdeclr)
