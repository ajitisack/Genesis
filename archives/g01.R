
library(quantmod)
library(data.table)
library(parallel)
library(foreach)
library(doParallel)
library(dplyr)
library(pryr)
library(smooth)

rm(list=ls(all.names = T))


# https://www.nseindia.com/products/content/equities/equities/eq_security.htm
# https://www.nseindia.com/corporates/content/securities_info.htm
nse_symbols <- fread("StockTrading/EQUITY_L.csv")[SERIES == "EQ"]$SYMBOL
nse_symbols <- grep("^.[0-9a-zA-Z]*$", nse_symbols, value = T)
nse_symbols <- head(nse_symbols,100)


#
# http://chartapi.finance.yahoo.com/instrument/1.0/ASTEC.NS/chartdata;type=quote;range=1d/csv
https://chartapi.finance.yahoo.com/instrument/1.0/ASTEC.NS/chartdata;type=quote;range=1d/csv
# range values
# d -> 1 to 15 [frequency 5 minutes]
# m -> 1 to 36 [frequency - daily]
# m -> 36+ [frequency - weekly]
# y -> 1 to 3 [frequency - daily]
# y -> 3 to  [frequency - weekly]
#

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

getNseData <- function(symbols, freq="1d", no_of_cores=6){
        cluster <- makeCluster(no_of_cores)
        clusterEvalQ(cluster, library(magrittr))
        d <- parLapplyLB(cluster, symbols, readFromYahooFinance, freq=freq)
        stopCluster(cluster)
        d <- do.call(rbind, d) %>% data.table::data.table()
        data.table::setcolorder(d, c("symbol", "date", "open", "high", "low", "close", "volume"))
        f <- gsub("^.*(.)$", "\\1", freq)
        if (f == "d") d$date <- as.POSIXct(as.integer(d$date), origin="1970-01-01")
        else d$date <- as.Date(d$date, format="%Y%m%d")
        return(d)
}

system.time(d <- getNseData(nse_symbols, "3y", 8))
# save(d, file="StockTrading/nse3y.Rdata")
# load("StockTrading/nse3y.Rdata")

nse <- d %>% select(-symbol) %>% split(f=d$symbol)
nse.xts <- lapply(nse, as.xts.data.table)
gc()


# Analysis 01
# -----------
x <- d[date=="2017-01-10", .(symbol, close)]
x$group <- cut(x$close
               , breaks = c(0, 10, 20, 50, 100, 200, 300, 400, 500, 1000, Inf)
               , labels = c("0-10", "10-20", "20-50", "50-100", "100-200", "200-300"
                            , "300-400", "400-500", "500-1000", "1000+")
               )
x %>% count(group)


# Analysis 02- Simple Moving Average
# -----------------------------------

system.time({
for (i in 1:length(nse)){
        nse[[i]]$sma.10 <- SMA(nse[[i]]$close, 10)
        nse[[i]]$sma.50 <- SMA(nse[[i]]$close, 20)
        #nse[[i]]$ema.10 <- EMA(nse[[i]]$close, 10)
        #nse[[i]]$ema.50 <- EMA(nse[[i]]$close, 50)
}
})
# user  system elapsed
# 0.84    0.00    0.84


system.time({
lapply(nse, function(x){
        cbind(x,sma.10=SMA(x$close, 10))
})
})
# user  system elapsed
# 1.44    0.00    1.43


system.time({
registerDoParallel(6)
x <- foreach(i = 1:length(nse), .multicombine = TRUE)  %dopar% {
        cbind(nse[[i]], sma.10 = TTR::SMA(nse[[i]]$close,10))
        nse[[i]] <- data.table::data.table(nse[[i]])
}
stopImplicitCluster()
})
# user  system elapsed
# 1.49    1.92    6.39


system.time({
cluster <- makeCluster(6)
#clusterEvalQ(cluster, suppressPackageStartupMessages(library(data.table)))
clusterEvalQ(cluster, suppressPackageStartupMessages(library(TTR)))
parLapplyLB(cluster, nse, function(x){
        cbind(x,sma.10=TTR::SMA(x$close, 10))
        #x[,sma.10:=SMA(close, 10)]
})
stopCluster(cluster)
})
# user  system elapsed
# 0.33    0.45    3.14



library(dplyr)
library(parallelMap)

source('myapp1/app1fun.R')

#http://chartapi.finance.yahoo.com/instrument/1.0/ASTEC.BO/chartdata;type=quote;range=3y/csv
#system("defaults write org.R-project.R force.LANG en_US.UTF-8")

downloadBSEYahooEQ <- function(){
    l <- lapply(head(bsels$id,1000), function(x){
                url <- paste("http://chartapi.finance.yahoo.com/instrument/1.0/", x,
                             ".BO/chartdata;type=quote;range=3y/csv", sep = "")
                tryCatch({
                    t <- read.table(url, header = F, skip = 18, sep=",", colClasses=c("character", "numeric",
                                    "numeric", "numeric", "numeric", "integer"))
                    t <- cbind(id=x, code=head(bsels[bsels$id==x,c("code")],1), t)
                    return(t)
                },  error = function(e) NULL, warning = function(w) NULL)
    })
    t <- do.call(rbind, l)
    t$id <- as.character(t$id)
    names(t) <- c("id", "code", "date", "close", "high", "low", "open", "volume")
    t$date <- as.Date(t$date, format = "%Y%m%d")
    return(t)
}

parDownloadBSEYahooEQ <- function(n=100) {
    stime <- Sys.time()
    print(stime)
    bsels <- bse.readScriptList()
    parallelStart("socket",cpus = 4)
    l <- parallelLapply(head(bsels$id,n), function(x){
        tryCatch({
            url <- paste("http://chartapi.finance.yahoo.com/instrument/1.0/", x,
                       ".BO/chartdata;type=quote;range=3y/csv", sep = "")
            t <- read.table(url, header = F, skip = 18, sep=",", colClasses=c("character", "numeric",
                          "numeric", "numeric", "numeric", "integer"))
            t <- cbind(id=x, t)
            return(t)
        }, error = function(e) NULL, warning = function(w) NULL)
    })
    t <- do.call(rbind, l)
    parallelStop()
    t$id <- as.character(t$id)
    names(t) <- c("id", "date", "close", "high", "low", "open", "volume")
    t$date <- as.Date(t$date, format = "%Y%m%d")
    assign("bse", t, envir=.GlobalEnv)
    print(Sys.time())
    Sys.time()-stime
}
