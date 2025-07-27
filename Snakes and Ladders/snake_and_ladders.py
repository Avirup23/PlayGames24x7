from abc import ABC, abstractmethod
import random
import copy
from tqdm import tqdm

class GameState:
    """This class single handedly updates everything"""
    def __init__(self, board_size:int, num_players:int, num_dice:int, snakes:dict[int,int], ladders:dict[int,int]):
        self.num_dice = num_dice
        self.num_players = num_players
        self.board_size = board_size
        self.snakes = snakes    # dict {from: to}
        self.ladders = ladders  # dict {from: to}
        self.dice_options = [] # list of move per turn
        self.positions = [0] * num_players
        self.turn = 0  # total turns
        self.move = 0  # within each turn there are num_dice many moves

    def move_player(self, player_idx, move):
        new_pos = self.positions[player_idx] + move
        self.dice_options.remove(move)

        if new_pos > self.board_size:
            return  # Invalid

        # Snakes or Ladders
        new_pos = self.snakes.get(new_pos, new_pos)
        new_pos = self.ladders.get(new_pos, new_pos)
        self.positions[player_idx] = new_pos

    def is_winner(self, player_idx):
        return self.positions[player_idx] == self.board_size

    def next_turn(self):
        self.turn += 1

    def next_move(self):
        self.move  += 1
        self.move = self.move % self.num_dice

    def roll_dice(self):
        self.dice_options = random.choices(range(1, 7), k = self.num_dice)

    def clone(self):
        """Returns a deep copy for strategy simulations"""
        return copy.deepcopy(self)

class Strategy(ABC):
    """Strategy class to create various child strategies"""
    def __init__(self):
        pass

    @abstractmethod
    def choose_dice(self, game_state: GameState) -> int:
        """Return a value from game_state.dice_options"""
        raise NotImplementedError()

class RandomStrategy(Strategy):
    def choose_dice(self, game_state: GameState) -> int:
        # the turn began with this player
        if game_state.move == 0:
            pass

        # the turn does not with this player
        elif game_state.move == 1:
            pass

        # no choice remain (if num_dice = 3)
        elif game_state.move == 2:
            pass

        return random.choice(game_state.dice_options)

class LongStrategy(Strategy):
    def choose_dice(self, game_state: GameState) -> int:
        # Try to land farthest
        return max(game_state.dice_options)
    
class MCTSStrategy(Strategy):
    def __init__(self,iter:int):
        self.iter = iter

    def choose_dice(self, game_state: GameState) -> int:
        if len(game_state.dice_options) == 1:
            return game_state.dice_options
        for i in range(iter):
            # exploitation
            # exploration
            # play-out strategy
            # backpropagation
            pass

class GameRunner:
    def __init__(self, strategies, num_dice, board_size=100, snakes=None, ladders=None):
        if snakes is None: snakes = {97: 41, 89: 53, 76: 58, 66: 45, 56: 31, 43: 18, 40: 3, 27: 5}
        if ladders is None: ladders = {4: 25, 13: 25, 33: 49, 42: 63, 50: 69, 62: 81, 74: 92}
        self.snakes = snakes
        self.ladders = ladders
        self.board_size  = board_size
        self.num_dice = num_dice
        self.strategies = strategies  # list of Strategy objects
        self.state = None
        self.result = {j:0 for j in range(len(self.strategies))}

    def play(self, iter:int, verbose=False):
        for i in tqdm(range(iter)):
            self.state = GameState(self.board_size, len(strategies), self.num_dice, self.snakes, self.ladders)
            while True:
                # when the move becomes zero roll again
                if self.state.move == 0 :
                    self.state.roll_dice()

                # find the player whose turn it is and get the move based on the turn
                current = (self.state.turn + self.state.move) % self.state.num_players
                strat = self.strategies[current]
                chosen_roll = strat.choose_dice(self.state.clone())

                # move the players and update the options
                self.state.move_player(current, chosen_roll)

                # update move and turn
                self.state.next_move()
                if self.state.move == 0:
                    self.state.next_turn()

                # print if required and check winner
                # if verbose:
                #     print(f"Turn: {self.state.turn} Move: {self.state.move} Player: {current} options: {self.state.dice_options} roll: {chosen_roll} moves to: {self.state.positions[current]}")
                if self.state.is_winner(current):
                    # if verbose:
                    #     print(f"Player {current} wins!")
                    self.result[current] += 1
                    break
        self.result = {index:(100*wins/iter) for index,wins in self.result.items()}
        if verbose:
            print(f"Result: {self.result}")
        return self.result

if __name__ == "__main__":
    strategies = [RandomStrategy(), LongStrategy()]
    runner = GameRunner(strategies,3)

    runner.play(2000,True)