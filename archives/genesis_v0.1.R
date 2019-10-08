
library(quantmod)
library(data.table)
library(parallel)
library(dplyr)
library(pryr)
library(magrittr)

rm(list=ls(all.names = T))

# REFERENCE
#=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=
# https://www.nseindia.com/products/content/equities/equities/eq_security.htm
# https://www.nseindia.com/corporates/content/securities_info.htm
# http://chartapi.finance.yahoo.com/instrument/1.0/ASTEC.NS/chartdata;type=quote;range=1d/csv
# range values
# d -> 1 to 15 [frequency 5 minutes]
# m -> 1 to 36 [frequency - daily]
# m -> 36+ [frequency - weekly]
# y -> 1 to 3 [frequency - daily]
# y -> 3 to  [frequency - weekly]
#=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=


# FUNCTIONS
#===============================================================================

#-function to read data from yahoo finance chartapi for one symbol
readFromYahooFinance <- function(symbol, freq){
        urlpart1 <- "http://chartapi.finance.yahoo.com/instrument/1.0/"
        urlpart2 <- ".NS/chartdata;type=quote;range="
        yahoourl <- paste0(urlpart1, symbol, urlpart2, freq, "/csv")
        d <- readLines(yahoourl)
        d <- grep("^[0-9]", d, value=T)
        if (length(d) == 0) return(NULL)
        colnames <- c("date","close","high","low","open","volume")
        colclasses <- c("character", "numeric", "numeric", "numeric", "numeric", "integer")
        d <- read.csv(text=d, header = F, colClasses = colclasses, col.names = colnames)
        d$symbol <- symbol
        return(d)
}


#-function to read data from yahoo finance chartapi for all symbols in parallel
getNseData <- function(symbols, freq="1d", no_of_cores=6){
        cluster <- makeCluster(no_of_cores)
        clusterEvalQ(cluster, library(magrittr))
        d <- parLapplyLB(cluster, symbols, readFromYahooFinance, freq=freq)
        stopCluster(cluster)
        d <- do.call(rbind, d) %>% data.table::data.table()
        orderedcols <- c("symbol", "date", "open", "high", "low", "close", "volume")
        data.table::setcolorder(d, orderedcols)
        f <- gsub("^.*(.)$", "\\1", freq)
        if (f == "d") d$date <- as.POSIXct(as.integer(d$date), origin="1970-01-01")
        else d$date <- as.Date(d$date, format="%Y%m%d")
        return(d)
}


#-function to add more features(SMA, EMA etc.) to stock data of all symbols
addFeatures <- function(d){
        for (i in 1:length(d)) {
                x <- d[[i]]
                n <- nrow(x)
                x$sma.10 <- x$sma.50 <- NA
                x$ema.10 <- x$ema.50 <- NA
                if (n>=10) {
                        x$sma.10 <- SMA(x$close, 10)
                        x$ema.10 <- EMA(x$close, 10)
                }
                if (n>=50) {
                        x$sma.50 <- SMA(x$close, 50)
                        x$ema.50 <- EMA(x$close, 50)
                }
                d[[i]] <- x
        }
        return(d)
}
#===============================================================================



# read NSE symbols from NSE website
nse_symbols <- fread("EQUITY_L.csv")[SERIES == "EQ"]$SYMBOL
nse_symbols <- grep("^.[0-9a-zA-Z]*$", nse_symbols, value = T)
nse_symbols <- head(nse_symbols,10)

system.time(d <- getNseData(nse_symbols, "3y", 8))
# user  system elapsed
# 67.449  29.862 200.832
# save(d, file="StockTrading/nse3y.Rdata")
# load("StockTrading/nse3y.Rdata")

nse <- d %>% select(-symbol) %>% split(f=d$symbol)
nse.xts <- lapply(nse, as.xts.data.table)
gc()
nse %<>% addFeatures()



# Adding SMA & EMA to nse data with window 10 and 50
# --------------------------------------------------

nse <- addFeatures(nse)

print(object.size(d), units= "Mb")
gc()
