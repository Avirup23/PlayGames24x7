from decks import Game_state
import math
import random
from game import RummyGame
from strat_random import RandomAgent
from cards import tpprint_card as pprint_card
from cards import tpprint_hand as pprint_hand
from agents import Player, cards_from_decl
from algo_minscore import mscore,is_valid
from copy import deepcopy

class Node:
    def __init__(self, move_str = None, parent = None):
        self.parent:Node = parent
        self.children:dict[Node] = {}
        self.visits = 0
        self.value = 0.0
        self.move_str = move_str  # either 'F' or 'D' or 'P'

    def is_fully_expanded(self, drop):
        if drop:
            return len(self.children) == 3
        else:
            return len(self.children) == 2

    def best_child(self, c_param=1.41):
        return max(
            self.children.values(),
            key=lambda child: (child.value / (child.visits) + 
                              c_param * math.sqrt(math.log(self.visits) / (child.visits + 1e-4)))
        )
    
    def print_tree(self, level=0):
        if self.move_str == None:
            print("    " * level + f"root : {round(self.value/(self.visits+1e-3),2)}" )
        else:
            print("    " * level + f"{self.move_str} : {round(self.value/(self.visits+1e-3),2)} {round(self.value / (self.visits + 1e-4) + 1.41 * math.sqrt(math.log(self.parent.visits) / (self.visits + 1e-4)),2)}" )
        for child in list(self.children.values()):
            child.print_tree(level + 1)

class MCTSAgent(Player):
    def __init__(self, name, iterations, drop=True, print_log = False):
        super().__init__(name)
        self.iterations = iterations
        self.drop = drop
        self.strategy = 'MCTS-minscore'
        self.root = None
        self.print_log = print_log
        self.version = 2
        print("MCTS version ",self.version)

    def reset(self):
        pass

    def mv1(self, index, state:Game_state, wcj, first, rules=[('Pseq',3),('Iseq',3)],maxscore=80):
        if self.print_log:
            print("-----------------------------")
            print("round",state.counter%2+1)
        # zero iteration means random choice
        if self.iterations <= 0:
            return random.choice(self.get_legal_actions())
        
        # when the state is already terminal
        if self.is_terminal(state,wcj,rules):
            return 'D'

        # initializing the tree
        if self.root is None:
            self.root = Node()
        # pruning the opponent's move from the tree
        elif len(state.player_choices[(state.player_index-1)%len(state.hands)]) > 0:
            if self.print_log:
                print("opponent's choice",state.player_choices[(state.player_index-1)%len(state.hands)][-1])
            opponents_node = self.root.children.get(state.player_choices[(state.player_index-1)%len(state.hands)][-1],Node())
            opponents_node.parent = None
            opponents_node.move_str = None
            self.root = opponents_node

        if self.print_log:
            self.root.print_tree()
        for _ in range(self.iterations):
            node = self.root
            init_state:Game_state = state.clone_and_randomize(len(state.hands),len(state.hands[0]))

            # Selection
            while node.is_fully_expanded(self.drop) and not self.is_terminal(init_state,wcj,rules):
                # traverse through the tree
                node:Node = node.best_child()
                self.do_action(init_state, node.move_str,wcj,rules,maxscore)
                init_state.counter+=1
                init_state.player_index = (init_state.player_index+1)%len(init_state.hands) 

            # Expansion
            if not self.is_terminal(init_state,wcj,rules):
                for action in self.get_legal_actions():
                    if action not in node.children:
                        child_node = Node(parent=node, move_str=action)
                        node.children[action] = child_node
                        node = child_node

                        self.do_action(init_state,action,wcj,rules,maxscore)
                        init_state.counter+=1
                        init_state.player_index = (init_state.player_index+1)%len(init_state.hands) 
                        break
            
            # Simulation
            outcome = self.rollout(node, init_state,wcj,rules,maxscore)
            reward = [outcome['score1'],outcome['score2']]

            # Backpropagation
            player_order = 1-init_state.player_index
            while node.parent is not None:
                node.visits += 1
                node.value += (1-reward[player_order]/maxscore)
                node = node.parent
                player_order = 1-player_order
            node.visits += 1
            
            if self.print_log:
                print(f"iteration:{_}")
                self.root.print_tree()
                print("-----------------------------")

        # Return the action with the highest average value
        best_node:Node = max(self.root.children.values(), key=lambda n: round(n.value/(n.visits+1e-3)))
        best_move = best_node.move_str
        
        best_node.parent = None
        best_node.move_str = None
        self.root = best_node
        if self.print_log:
            self.root.print_tree()
            print("bestmove",best_move)
            # exit(0)
        return best_move

    def rollout(self,node:Node, state:Game_state,wcj,rules,maxscore):
        """Performs a simulation until terminal state using random (or heuristic) play."""
        
        p1 = RandomAgent('Random1',drop=self.drop)
        p2 = RandomAgent('Random2',drop=self.drop)
        game = RummyGame([p1,p2],state.ndeck,state.njoker,len(state.hands[0]),rules,log=False,maxscore = maxscore)
        game.state = state.clone()
        game.wcj = wcj
        game.state.counter-=1
        return game.playgame()
    
    # returns a card it rejects (strat_miscore)
    def mv2(self, hand, wcj, deckorpile, card, rules=[('Pseq',3),('Iseq',3)],maxscore=80):
        currsc = mscore(deepcopy(hand),wcj,rules,False,0,maxscore=maxscore)
        modsc,decl = mscore(deepcopy(hand+[card,]),wcj,rules,True,1,maxscore=maxscore)
        if modsc < currsc:
            currsc = modsc
            decl = decl
            cards = cards_from_decl(decl)
            if len(cards)!=len(hand):
                raise Exception('declaration obtained not correct length')
            handmod = hand+[card,]
            if len(cards)>13:
                cards = cards[:13]
            for c in cards:
                handmod.remove(c)
            hand = cards

            return handmod[0],hand,(currsc==0)
        else:
            return card,hand,False
        
    def is_terminal(self,state:Game_state,wcj:int,req):
        # print(f"player index = {self.player_index} hands {self.hands}")
        return is_valid(state.hands[state.player_index],wcj,req,0)
    
    def do_action(self, state:Game_state, action:str,wcj,rules,maxscore)->int:
        if action == 'P':
            icard = state.pile.peek()
            # everyone can see it
            # state.observable_hands[state.player_index].append(icard)
            disc,hand,declared = self.mv2(state.hands[state.player_index],wcj,action,icard,rules,maxscore)
            # if disc in state.observable_hands[state.player_index] and disc!=icard:
            #     state.observable_hands[state.player_index].remove(disc)
            state.pile.add(disc)
            state.hands[state.player_index]=hand
            # print(f'Round {state.counter//2+1}: Player {state.player_index} took {pprint_card(icard,False)} from pile and returned {pprint_card(disc,False)} to pile.\n')
            # pprint_hand(state.hands[0])
            # pprint_hand(state.hands[1])
        if action == 'D':
            if state.deck.deck == []:
                state.deck.deck = state.pile.pile
                state.deck.shuffle()
                state.pile.pile=[]
                state.pile.add(state.deck.draw(1))
            icard = state.deck.draw(1)
            disc,hand,declared = self.mv2(state.hands[state.player_index],wcj,action,icard,rules,maxscore)
            # if disc in state.observable_hands[state.player_index] :
            #     state.observable_hands[state.player_index].remove(disc)
            state.pile.add(disc)
            state.hands[state.player_index]=hand
            # print(f'Round {state.counter//2+1}: Player {state.player_index} took {pprint_card(icard,False)} from deck and returned {pprint_card(disc,False)} to pile.\n')
            # pprint_hand(state.hands[0])
            # pprint_hand(state.hands[1])

    def get_legal_actions(self):
        if self.drop:
            actions = ['F','D','P']
        else:
            actions = ['D','P']
        return actions