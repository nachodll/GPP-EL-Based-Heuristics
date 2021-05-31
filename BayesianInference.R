## Load library
if (!require("devtools")) {
  install.packages("devtools")
}
if (!require("rstan")) {
  install.packages("rstan")
}
options(mc.cores = 8)
rstan_options(auto_write = TRUE)
devtools::install_github("b0rxa/scmamp", force=TRUE)

getCredibleIntervalsWeights <- function(posterior.samples, interval.size=0.9) {
  qmin <- (1-interval.size)/2
  qmax <- 1-qmin
  lower.bound <- apply(posterior.samples, MARGIN=2, FUN=quantile, p=qmin) 
  upper.bound <- apply(posterior.samples, MARGIN=2, FUN=quantile, p=qmax) 
  expectation <- apply(posterior.samples, MARGIN=2, FUN=mean) 
  return (data.frame(Expected=expectation, Lower_bound=lower.bound, Upper_bound=upper.bound))
}
library("scmamp")

## Load data
setwd("C:/Repos/GPP-EL-Based-Heuristics")
df <- read.csv("results/250/medians250-k4.csv")

## Statistical Analysis
df[,2:length(df)] <- df[,2:length(df)] * -1
pl_model <-  bPlackettLuceModel(x.matrix=df[,2:length(df)], min=FALSE, nsim=4000, nchains=20, parallel=TRUE)
pl_model$expected.mode.rank
pl_model$expected.win.prob

## Plot
processed.results <- getCredibleIntervalsWeights(pl_model$posterior.weights, interval.size=0.9)
processed.results
df <- data.frame(Algorithm=rownames(processed.results), processed.results)
ggplot(df, aes(y=Expected, ymin=Lower_bound, ymax=Upper_bound, x=Algorithm)) + 
  geom_errorbar() + 
  geom_point(col="darkgreen", size=2) +  
  theme_bw() + 
  theme(text = element_text(size=25),
        axis.text.x = element_text(angle=0, hjust=1)) +
  theme(aspect.ratio=4/10) +
  coord_flip() + 
  labs(y="Probability of winning") +
  expand_limits(x = 0, y = 0.5)

