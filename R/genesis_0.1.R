
#rm(list=ls(all.names = T))


source("functions_0.1.R")
symbols <- fread("https://www.nseindia.com/content/equities/EQUITY_L.csv")[SERIES == "EQ"]
load("d.RData")


### get 12 years of stock data from google for all NSE symbols
system.time(d <- getHistPriceAll(symbols, no_of_symbols = 0, no_of_cores = 4))
save(d, file = "d.RData")


#nse <- d %>% select(-symbol) %>% split(f=d$symbol) %>% lapply(as.xts.data.table)
#nse %<>% addFeatures()


### select latest date values for each stock symbol
### break close price into buckets
###  1 ->   0-10
###  2 ->  10-20
###  3 ->  20-30
###  4 ->  30-40
###  5 ->  40-50
###  6 ->  50-100ww
###  8 -> 150-200
###  9 -> 200-300
### 10 -> 300-400
### 11 -> 400-500
### 12 -> 500-1000
### 13 -> 1000&above
d1 <- d[, .SD[which.max(date)], .(symbol)]
d1$range <- cut(d1$close
	, breaks=c(0,10,20,30,40,50,100,150,200,300,400,500,1000,1000000)
	, labels = FALSE)
d1[,clop := close-open][,hilo := high-low]
d1 <- d1 %>% select(-range) %>% split(f=d1$range) %>% lapply(arrange, -volume)
lapply(d1, head, 20)




