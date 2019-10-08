
library(dplyr)
library(quantmod)

g.sd <- function(df, from, to, l, u, d){
    fsd <- function(x) {
        if(length(x) == 1) 0 else round(sd(x),2)
    }
    if (d != 0) from <- Sys.Date() - d
    df <- filter(df, date>=from & date<=to & open >= l & open <=u)
    aggcols <- cbind(df$open, df$high, df$low, df$close)
    df <- aggregate(aggcols ~ id, df, fsd)
    names(df) <- c("id", "open", "high", "low", "close")
    df <- filter(df, open > 0.0) %>% arrange(desc(open))
    return(df)
}

g.select <- function(df, x){
    df <- filter(df, id==x) %>%
            select(date, id, open, high, low, close, volume) %>%
                arrange(desc(date))
    return(df)
}

g.chart <- function(df, code, period, type) {
    df <- g.select(df, code)
    d <- as.xts(select(df, open, high, low, close, volume), order.by=df$date)
    name <- head(df$name,1)
    if (type=='c' || type=='C') candleChart(d[period], name=name, theme='white')
    else if (type=='b' || type=='B') barChart(d[period], name=name, theme='white')
    else lineChart(d[period], name=name, theme='white')
}

bse.sd <- function(from=as.Date("2015-01-01"), to=Sys.Date(), l=1, u=100, d=10){
    bsesd <- g.sd(bse, from, to, l, u, d)
    assign("bsesd", bsesd, envir=.GlobalEnv)
    View(bsesd)
}

bse.select <- function(id){
    bsestock <- g.select(id, df=bse)
    View(bsestock)
}

bse.chart <- function(code, period, type="b"){
    g.chart(bse, code, period, type)
}

nse.select <- function(cd){
    nsestock <- g.select(cd, df=nse)
    View(nsestock)
}

nse.sd <- function(from=as.Date("2015-01-01"), to=Sys.Date(), l=1, u=100, d=10){
    nsesd <- g.sd(nse, from, to, l, u, d)
    assign("nsesd", nsesd, envir=.GlobalEnv)
    View(nsesd)
}

nse.chart <- function(code, period, type="l"){
    g.chart(nse, code, period, type)
}

g.dad <- function(df, cd, period){
    df <- filter(df, code==cd) %>%
            arrange(date) %>%
                select(code, name, open, high, low, close)
    name <- head(df$name, 1)
    dad <- 0.0
    n <- if (nrow(df) >= period) period else nrow(df)
    for (i in 1:n) {
        avg_d1 <- sum(df[i,"open"], df[i,"low"], df[i,"high"], df[i,"close"]) / 4
        if ( !exists("avg_d2") ) avg_d2 <- avg_d1
        dad <- dad + (avg_d2 - avg_d1)
        avg_d2 <- avg_d1
    }
    dad <- round(dad,2)
    df <- data.frame(cd, name, dad, stringsAsFactors = F)
    names(df) <- c("code", "name", "dad")
    return(df)
}

bse.dad <- function(cd, period=5){
    g.dad(bse, cd, period)
}


{
# pdf('myplots.pdf', onefile=TRUE)
# for (i in head(bsesd$code,20)) bse.chart(i)
# graphics.off()
# rm(i)

# nsescripts <- read.csv("EQUITY_L.csv", header = T)
# bsescripts <- read.csv("ListOfScrips.csv", header = T)

# http://www.marketcalls.in/amibroker/exploring-yahoo-realtime-data-feed.html
# https://code.google.com/p/yahoo-finance-managed/wiki/YahooFinanceAPIs
# http://chartapi.finance.yahoo.com/instrument/1.0/JMTAUTOLTD.BO/chartdata;type=quote;range=1d/csv

# View(t)
# t <- as.xts(select(t, open, high, low, close, volume), order.by=t$time)
# name <- "JMTAUTOLTD"
# if (type=='c' || type=='C') candleChart(t, name=name, theme='white')
# else if (type=='b' || type=='B') barChart(t, name=name, theme='white')
# else lineChart(t, name=name, theme='white')

# http://www.marketcalls.in/amibroker/exploring-yahoo-realtime-data-feed.html
}

bsescripts <- read.table("ListOfScrips.csv",header = T, sep = ",",
                         colClasses = c("integer", "character", "character", "factor", "factor",
                                        "numeric", "character", "character", "character"),
                         col.names = c("code", "id", "name", "status", "group", "facevalue", "isin",
                                       "industry", "instrument")
                        ) %>% select(code, id, name, group, industry, facevalue, isin) %>% arrange(id)
bsescripts$id <- sub("\\*","",bsescripts$id)
bsescripts$industry <- sub("\\&amp;", "\\&", bsescripts$industry)



#http://chartapi.finance.yahoo.com/instrument/1.0/JMTAUTOLTD.BO/chartdata;type=quote;range=1d/csv

bse.getIntraDay <- function(stockname="JMTAUTOLTD", d=1){
    l <- if (d==1) 17 else 18 + d
    url <- paste( "http://chartapi.finance.yahoo.com/instrument/1.0/",
                  stockname,
                  ".BO/chartdata;type=quote;range=",
                  d,
                  "d/csv",
                  sep="")
    stock <- read.csv(url, header=F, skip=l)
    names(stock) <- c("datetime","close","high","low","open","volume")
    stock$datetime <- as.POSIXlt("1970-01-01 05:30:00") + stock$datetime
    stock <- stock[order(stock$datetime),]
    assign(stockname, stock, envir=parent.frame())
    View(stock)
    plot(stock$datetime, stock$close, type="l")
}



bse.trades <- function(){
    t <- read.csv("trades.txt")
    x <- lapply(t$stock, function(s){
        url <- paste( "http://chartapi.finance.yahoo.com/instrument/1.0/",
                      s,
                      ".BO/chartdata;type=quote;range=1d/csv",
                      sep="")
        stock <- read.csv(url, header=F, skip=17)
        return(tail(stock,1)$V2)
    })
    x <- do.call(rbind, x)
    t <- cbind(t,x)
    colnames(t)[6] <- "currentprice"
    t$x <- t$currentprice - t$avgprice
    colnames(t)[7] <- "pricediff"
    t$x <- t$pricediff * t$quantity
    colnames(t)[8] <- "gainORloss"
    print(t)
    net <- round(sum(t$gainORloss), 2)
    msg <- if (net > 0) "Gain" else "Loss"
    cat(paste("\n\t\tNet Investment =", sum(t$totalvalue)))
    cat(paste("\n\t\tNet", msg, "      =", net, "\n\n"))
}



#ASTEC - 260 - 20 - 6000
#KATWAUD - 96 - 200
#RUSHIL - 101 - 200

#Stock Selection - Method 1

method1 <- function () {
  d0 <- tail(bse,1)$date
  d4 <- head(tail(sort(unique(bse$date)),4),1)
  d8 <- head(tail(sort(unique(bse$date)),8),1)

  p <- bse[bse$date==d0 & bse$close <=300,c("id", "date", "close")]
  q <- bse[bse$date==d4 & bse$id %in% p$id, c("id", "date", "close")]
  r <- bse[bse$date==d8 & bse$id %in% p$id, c("id", "date", "close")]

  s <- merge(p,q,by="id")
  s <- merge(s,r,by="id")
  s$diff4 <- s$close.x - s$close.y
  s$diff8 <- s$close.x - s$close

  s <- s[s$diff4 >0 & s$diff8>0,]
  s <- s[order(-s$diff8,-s$diff4),]

  rm(p,q,r,d0,d4,d8)

  View(s)
}

#Stock selection method 2
method2 <- function () {
  d0 <- tail(bse,1)$date
  bse0 <- bse[bse$date==d0 & bse$close <= 200,]
  bse0$hl <- bse0$high - bse0$low
  bse0 <- bse0[order(-bse0$hl),]
  rm(d0)
  View(bse0)
}


#Select stock with consistent variation in low and high value

method3 <- function () {
  d0 <- tail(bse,1)$date
  d8 <- head(tail(sort(unique(bse$date)),8),1)
  id <- bse[bse$date==d0 & bse$close <= 200,1]
  bse0 <- bse[bse$date>=d8 & bse$id %in% id,]
  bse0$hl <- bse0$high - bse0$low
  x <- aggregate(hl ~ id, bse0, mean)
  x <- x[order(-x$hl),]
  row.names(x) <- NULL
  View(x)
}
