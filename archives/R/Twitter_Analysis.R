
# load required libraries
library(twitteR)
library(stringr)
library(dplyr)
library(tm)
library(wordcloud)
library(data.table)



# setup twitter authentication
#-----------------------------
consumer_key        <- "41H8IucTlyDhRIVX2jgZwO1eX"
consumer_secret     <- "H4AB9NPfn4TEnBjd5avtHyRAz6GWZd2NYilGCSaj7ACJhZf5OX"
access_token        <- "3162262183-sHRZmsokM4mqtd0PALlGLeFA78mAcl2mbMeYBjB"
access_token_secret <- "5DenCkrotlnulzsiVqLXyrAHqLukSTjoMfCgXiCKUsyAL"

setup_twitter_oauth(consumer_key, consumer_secret, access_token, access_token_secret)


# search for sample tweets to check the connection
#-------------------------------------------------
search_string <- "ripple"
t <- searchTwitter(search_string, n=100, lang=c("en"), resultType="recent")
t <- lapply(t, twitteR::as.data.frame)
t <- do.call(rbind, t)

t$statusSource <- gsub("<.*>(.*)<.*>", "\\1", t$statusSource)
t$text <- gsub("\n", " ", t$text)
t$created <- format(t$created, tz="Asia/Kuala_Lumpur",usetz=TRUE)

