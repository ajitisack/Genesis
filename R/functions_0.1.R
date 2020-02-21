

library(quantmod)
library(data.table)
library(parallel)
library(dplyr)
library(pryr)
library(magrittr)
library(rvest)
library(dygraphs)
library(pbapply)


# https://trading.cheno.net/downloading-google-intraday-historical-data-with-python/
# https://www.google.com/finance/getprices?p=1M&f=d,o,h,l,c,v&df=cpct&x=NSE&q=TCS
# https://www.google.com/finance/getprices?p=1d&i=300&f=d,o,h,l,c,v&df=cpct&x=NSE&q=TCS


### Function to read getprices url for daily historical data from google finance
getHistPrice <- function(symbol, freq="12Y"){
        cat("Dowloading", symbol, "data...", "\n")
        url <-"https://www.google.com/finance/getprices?f=d,o,h,l,c,v&x=NSE&q="
        url <- paste0(url, gsub("&", "%26", symbol),"&p=", freq)
        cat(url, "\n")
        col_names <- c("date", "close", "high", "low", "open", "volume")
        col_class <- c("character", "numeric", "numeric", "numeric", "numeric", "numeric")
        x <- read.csv(url, skip = 7, header = F, col.names = col_names, colClasses = col_class)
        if (nrow(x)==0) return(x)
        for (i in 1:nrow(x)){
                v <- x$date[i]
                if (substr(v,1,1) == "a") {
                        a <- sub("^a", "", v) %>% as.integer()
                        a <- as.POSIXct(a, origin="1970-01-01") %>% as.Date()
                        d <- a
                } else {
                        d <- a + as.integer(v)
                }
                x$date[i] <- d %>% as.integer() %>% as.Date()
        }
        x$symbol <- symbol
        x$date %<>% as.integer() %>% as.Date()
        return(x)
}


### Function to download historical price data of NSE EQ from google finance
getHistPriceAll <- function(symbols, freq="12Y", no_of_symbols=3, no_of_cores=0){
        symbols <- symbols$SYMBOL
        if(no_of_symbols != 0)
                symbols <- head(symbols, no_of_symbols)
        if (no_of_cores > 0) {
                cluster <- makeCluster(no_of_cores)
                clusterEvalQ(cluster, {library(magrittr); library(zoo)})
                l <- parLapplyLB(cluster, symbols, getHistPrice, freq)
                stopCluster(cluster)
        } else {
                l <- lapply(symbols, getHistPrice, freq)
        }
        d <- do.call(rbind, l) %>% data.table()
        return(d)
}


### Function to get intraday prices of a NSE EQ from google finance
getIntraDay <- function(symbol, lastndays=20, interval=300){
        url <-"https://www.google.com/finance/getprices?f=d,o,h,l,c,v&x=NSE&p="
        url <- paste0(url, lastndays, "d&i=", interval, "&q=")
        url <- paste0(url, gsub("&", "%26", symbol))
        col_names <- c("date", "close", "high", "low", "open", "volume")
        col_class <- c("character", "numeric", "numeric", "numeric", "numeric", "numeric")
        x <- read.csv(url, skip = 7, header = F, col.names = col_names, colClasses = col_class)
        for (i in 1:nrow(x)){
                v <- x$date[i]
                if (substr(v,1,1) == "a") {
                        a <- sub("^a", "", v) %>% as.integer()
                        d <- a
                } else {
                        d <- a + (interval * as.integer(v))
                }
                x$date[i] <- d
        }
        x$symbol <- symbol
        x$date %<>% as.integer %>% as.POSIXct(origin="1970-01-01", tz="Asia/Calcutta")
        return(x)
}


getIntraDayAll <- function(symbols, lastndays=20, interval=300, no_of_symbols=3, no_of_cores=0){
        symbols <- symbols$SYMBOL
        if(no_of_symbols != 0)
                symbols <- head(symbols, no_of_symbols)
        if (no_of_cores > 0) {
                cluster <- makeCluster(no_of_cores)
                clusterEvalQ(cluster, {library(magrittr); library(zoo)})
                l <- parLapplyLB(cluster, symbols, getIntraDay, lastndays, interval)
                stopCluster(cluster)
        } else {
                l <- lapply(symbols, getIntraDay, lastndays, interval)
        }
        d <- do.call(rbind, l) %>% data.table()
        return(d)
}


### Function to add more features(SMA, EMA etc.) to stock data of all symbols
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


### Print chartSeries of a stock
chart <- function(x){
        x <- deparse(substitute(x))
        name <- paste(x, symbols[SYMBOL==x]$`NAME OF COMPANY`, sep = " - ")
        getHistPrice(x) %>% select(-symbol) %>% as.data.table %>%
                as.xts.data.table() %>% chartSeries(name=name)
}


### Print chartSeries of a stock
chart.IntraDay <- function(x){
        x <- deparse(substitute(x))
        name <- paste(x, symbols[SYMBOL==x]$`NAME OF COMPANY`, sep = " - ")
        getIntraDay(x) %>% select(-symbol) %>% as.data.table %>%
                as.xts.data.table() %>% chartSeries(name=name)
}


### Get current trading price of a NSE Symbol from google finance
getPrice <- function(x){
        symbol <- deparse(substitute(x))
        url <- "https://www.google.com/finance/info?q=NSE:"
        url <- paste0(url, symbol)
        x <- readLines(url)[7]
        x <- gsub("\"", "", x)
        x <- gsub(",", "", x)
        x <- strsplit(x,":")[[1]][2] %>% as.numeric()
        return(x)
}


### Function to get crypto currency historical prices since 2013 Apr 28
getCryptoPrice <- function(x){
        enddt <- Sys.Date() %>% format("%Y%m%d")
        url <- "https://coinmarketcap.com/currencies/"
        url <- paste0(url, x, "/historical-data/?start=20130428&end=", enddt)
        cat(url)
        webpage <- read_html(url)
        x <- html_nodes(webpage,'.text-right') %>% html_text()
        n <- length(x) - 1
        x <- x[8:n]
        x <- gsub(" ", "", x)
        x <- gsub(",", "", x)
        x <- gsub("-", "", x)
        x <- strsplit(x,"\n")
        x <- do.call(rbind, x) %>% data.table
        names(x) <- c("date", "open", "high", "low", "close", "volume", "marketcap")
        x$date <- as.Date(x$date, "%b%d%Y")
        cols <- c("open", "high", "low", "close", "volume", "marketcap")
        x <- x[, (cols) := lapply(.SD, as.numeric), .SDcols=cols]
        x <- as.xts.data.table(x)
        chartSeries(x)
        return(x)
}


