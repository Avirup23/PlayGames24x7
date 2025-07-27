# Rummy Codes and Data
Contributers<br>
|── Purrushottam Saha<br>
|── Tathagata Banerjee<br>
|── Avirup Chakraborty<br>
|── Shirsha Maitra<br>

Rummy<br>
│<br>
|── Data Folders<br>
|   Data 10 card Final MCTS  # all 10 card game simulations for mcts based strategies<br>
|   Data 10 card Final Rule  # all 10 card game simulations for only rule based strategies<br>
|   Data 13 card Final MCTS  # all 13 card game simulations for mcts based strategies<br>
|   Data 13 card Final Rule  # all 13 card game simulations for only rule based strategies<br>
|   Data Hands               # Mindist & Minscore calculations for a random hand<br>
│<br>
|── Main backends<br>
│   ginrummy_work10card.py   # Simulation Code For 10 card games (Multiprocessing)<br>
│   ginrummy_work13card.py   # Simulation Code For 13 card games (Multiprocessing)<br>
│   game.py                  # Code for running a single game<br>
│   decks.py                 # Code for classes Deck, Pile, Game_state<br>
│   cards.py                 # Functions for printing cards<br>
│   algo_mindist.py          # Algorithms to calculate Mindist<br>
│   algo_minscore.py         # Algorithms to calculate Minscore<br>
│   agents.py                # Player class for different Strategies<br>
│<br>
|── Different Strategies<br>
│   strat_defeat_heur.py     # Defeat seeker<br>
│   strat_defeatminscore.py  # Defeat seeker with some minscore modification<br>
│   strat_random.py          # Plays randomly<br>
│   strat_mindist.py         # Based on mindist<br>
│   strat_minscore.py        # Based on minscore<br>
│   strat_mindistscore.py    # Based on mindist and minscore both<br>
│   strat_mindistopp.py      # Based on mindist and opponent's selections<br>
│   strat_mcts.py            # Based on monte carlo tree search strategies<br>
│<br>
|── Scraps<br>
│   scrap.ipynb              # Just scraps<br>
│   mindist_minscore.ipynb   # Some calculations for mindist and minscores of a random hand<br>
│<br>
|── README.md                # Descriptions of codes<br>
