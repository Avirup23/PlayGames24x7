library(readr)

data1 <- read_csv("C:\\Users\\chakr\\Desktop\\Academics\\Games\\Ludo\\Ludo_Bots\\Data\\FI-100_vs_A_size_11_tokens_3_moves_18.csv",show_col_types = FALSE)
  
colnames(data1)
summaries = function(d1,n)
{
  p1_score = d1$`Player1 Score`[seq(n,nrow(d1),n+1)]
  p2_score = d1$`Player 2 Score`[seq(n,nrow(d1),n+1)]
  
  store = c(round((mean(p1_score > p2_score) + 0.5 * mean(p1_score == p2_score))*100,2) , round(mean(p1_score),2), round(sd(p1_score),2), 
            round(mean(p2_score),2) , 
            round(sd(p2_score),2))
  return(cat(paste(store,'& ')))
}

summaries(data1, 18)
