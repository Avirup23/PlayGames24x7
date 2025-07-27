# Rule Data (games folder)
each row represents a single game outcome

sc1                  = minscore of the final hand of the 1st player<br>
sc2                  = minscore of the final hand of the 2nd player<br>
winnerid             = winner id (0/1)<br>
numrounds            = number of rounds after the game finishes<br>
pseqc                = number of pure sequences in the winner's hand<br>
iseqc                = number of impure sequences in the winner's hand<br>
setc                 = number of sets in the winner's hand<br>

\Rummy\Data 10 Card Final MCTS<br>
│<br>
|── games            # csv data for game simulations<br>
│   |── ginrummy.game.<1st player>.vs.<2nd player>.joker.<numjoker>.seed<seed>.csv<br>
|── tables           # csv tables for reports<br>
