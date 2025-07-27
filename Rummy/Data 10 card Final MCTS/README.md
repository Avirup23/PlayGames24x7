# MCTS Data
each row represents a single game outcome

init.hand1           = initial hand of 1st player (a list of numbers representing each cards)<br>
init.hand2           = initial hand of 2nd player (a list of numbers representing each cards)<br>
wcj                  = wild card chosen in the game<br>
score1               = minscore of the final hand of the 1st player<br>
score2               = minscore of the final hand of the 2nd player<br>
winner               = winner id (0/1)<br>
numrounds            = number of rounds after the game finishes<br>
finish.hand1         = final hand of 1st player (a list of numbers representing each cards)<br>
finish.hand2         = final hand of 2nd player (a list of numbers representing each cards)<br>
pure.seq.counts      = number of pure sequences in the winner's hand<br>
impure.seq.counts    = number of impure sequences in the winner's hand<br>
set.counts           = number of sets in the winner's hand<br>

\Rummy\Data 10 Card Final MCTS<br>
│<br>
|── Outputs mcts vs mcts        # csv data for mcts vs mcts strategies<br>
│   <tab>|── rummy.mcts1-<budget of 1st player> (MCTS-minscore).vs.mcts2-<budget of 2nd player> (MCTS-minscore).10.card.2.joker.csv<br>
│<br>
|── Outputs mcts vs rule        # csv data for mcts vs mindistopp strategies<br>
|   <tab>|── rummy.MindistOpp1 (Mindist + Opp).vs.mcts2-<budget of 2nd player> (MCTS-minscore).10.card.2.joker.csv<br>
|  <tab>|── rummy.mcts1-<budget of 1st player> (MCTS-minscore).vs.MindistOpp2 (Mindist + Opp).10.card.2.joker.csv<br>
