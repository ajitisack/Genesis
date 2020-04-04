#!/usr/bin/env Rscript

#source("/home/ajit/Projects/Genesis/functions_0.1.R")
source("functions_0.1.R")
nse_eq_url <- "https://www.nseindia.com/content/equities/EQUITY_L.csv"
symbols <- fread(nse_eq_url)[SERIES == "EQ"]


### for slow system
system.time(p <- getHistPriceAll(symbols[1:300], no_of_symbols = 0, no_of_cores = 6))
system.time(q <- getHistPriceAll(symbols[301:600], no_of_symbols = 0, no_of_cores = 6))
system.time(r <- getHistPriceAll(symbols[601:900], no_of_symbols = 0, no_of_cores = 6))
system.time(s <- getHistPriceAll(symbols[901:1200], no_of_symbols = 0, no_of_cores = 6))
system.time(t <- getHistPriceAll(symbols[1201:nrow(symbols)], no_of_symbols = 0, no_of_cores = 6))
d <- rbind(p, q, r, s, t)


### Load saved data and create nse and nse.xts
save(d, file="d.RData")
