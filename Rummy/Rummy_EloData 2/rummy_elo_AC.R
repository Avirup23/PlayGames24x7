d <- read.csv("~/Desktop/internship-25/Rummy/Rummy_EloData 2/newdata/RulevsRule_EloData2.csv")

det_K = function(x)
{
  if(x <= 5)
  {
    K = 40
  }else if(x <= 10)
  {
    K = 20
  }else
  {
    K = 10
  }
  return(K)
}
set.seed(1234)
d = d[sample(1:nrow(d)),]

users = unique(c(d$`Strategy.1`,d$`Strategy.2`))
users

ratings = rep(1000,length(users))
dynamic_ratings =  matrix(data = NA, nrow = 20000,ncol = length(users))
games = rep(0,length(users))

P1_rating = numeric(length = nrow(d))
P2_rating = P1_rating
change = numeric(length = nrow(d))
change_prev = numeric(length = nrow(d))
for(i in 1:nrow(d))
{
  index1 = which(users == d$`Strategy.1`[i])
  index2 = which(users == d$`Strategy.2`[i])
  
  games[index1] = games[index1] + 1
  games[index2] = games[index2] + 1
  
  score_diff = abs(d$`P1.Score`[i]-d$`P2.Score`[i])
  score_multiplier = score_diff/30
  
  K1 = det_K(games[index1])
  K2 = det_K(games[index2])
  
  A1 = as.numeric(d$Winner_ID[i] == 0)
  A2 = as.numeric(d$Winner_ID[i] != 0)
  D = ratings[index1] - ratings[index2]
  
  E1 = 1/(1 + 10^(-D/400))
  E2 = 1 - E1
  
  change[i] = abs(round((K1+K2)/2 * score_multiplier * (A1 - E1)))
  change_prev[i]=abs(round((K1+K2)/2 * (A1 - E1)))
  
  ratings[index1] = ratings[index1] + round(K1 * score_multiplier * (A1 - E1))
  dynamic_ratings[games[index1],index1] = ratings[index1]
  
  ratings[index2] = ratings[index2] + round(K2 * score_multiplier * (A2 - E2))
  dynamic_ratings[games[index2],index2] = ratings[index2]
  
  P1_rating[i] = ratings[index1]
  P2_rating[i] = ratings[index2]
}

d = cbind.data.frame(d,P1_rating,P2_rating,"Avg Change in Ratings" = change,"Avg Change in Ratings without score modifications" = change_prev)

colnames(dynamic_ratings) = users

cbind(users,ratings)

boxplot(dynamic_ratings[3000:nrow(dynamic_ratings),order(ratings)],ylim = c(0,1500))

summary(dynamic_ratings)

# Load libraries
library(ggplot2)
library(tidyr)
library(dplyr)

# Convert matrix to data frame with row index as 'Games'
df <- as.data.frame(dynamic_ratings)
df$Games <- 1:nrow(df)

# Convert to long format for ggplot
df_long <- pivot_longer(df, cols = -Games, names_to = "Series", values_to = "Value")

# Compute average values per series
avg_lines <- df_long %>%
  group_by(Series) %>%
  summarise(Average =mean(Value, na.rm = TRUE))

main_colors <- c(
  "Mindist"             = "#e41a1c",  # vibrant red
  "Random"              = "#377eb8",  # bright blue
  "Minscore"            = "#4daf4a",  # bright green
  "Mindist+Opp"         = "#984ea3",  # rich purple
  "Mindist+minscore"    = "#ff7f00",  # vivid orange
  "DefeatHeuristic"     = "#ffe111"   # bright yellow
)
# Plot
ggplot(df_long, aes(x = Games, y = Value, color = Series)) +
  geom_line(size = 0.7) +

  # Add horizontal average lines with lighter color
  geom_hline(data = avg_lines, 
             aes(yintercept = Average, color = Series), 
             size = 2, alpha = 0.5, show.legend = TRUE) +

  # Manual color scale for main lines
  scale_color_manual(values = main_colors) +

  labs(title = "Dynamic Plot of Strategy Ratings",
       x = "Game Index",
       y = "Dynamic Ratings",
       color = "Strategy",fontsize = 2) +
  theme(
    plot.title = element_text(size = 18, face = "bold"),
    axis.title.x = element_text(size = 16),
    axis.title.y = element_text(size = 16),
    axis.text = element_text(size = 14),
    legend.title = element_text(size = 16),
    legend.text = element_text(size = 14)
  )

# Hist
hist(change, col=rgb(1,0,0,0.5),ylim = c(0,25000),xlim = c(0,20), main="Overlapping Histograms", xlab="Value", breaks=55)
hist(change_prev, col=rgb(0,0,1,0.5), add=TRUE, breaks=35)
legend("topright", legend=c("Modified Rating Change", "Previous Rating Change"), fill=c(rgb(1,0,0,0.5), rgb(0,0,1,0.5)), cex =0.7)

# write.csv(d, "~/Desktop/internship-25/Rummy/Rummy_EloData 2/RulevsMCTS_Elo.csv")


data = list(MCTSvsMCTS_Elo,
           RulevsMCTS_Elo,
           RulevsRule_Elo)
names = list("MCTS vs MCTS",
             "Rule vs MCTS",
             "Rule vs Rule")
# Hist
for (i in 1:3) {
  change<-data[[i]]$`Avg Change in Ratings`
  change_prev<-data[[i]]$`Avg Change in Ratings without score modifications`
  hist(change_prev, col=rgb(0,0,1,0.5),xlim = c(0,20), breaks=40, main=names[[i]], xlab="Value")
  hist(change, col=rgb(1,0,0,0.5), add=TRUE, breaks=60)
  legend("topright", legend=c("Modified Rating Change", "Previous Rating Change"), fill=c(rgb(1,0,0,0.5), rgb(0,0,1,0.5)), cex =0.7)
}
