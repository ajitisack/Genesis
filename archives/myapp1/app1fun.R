

bse.readScriptList <- function(){
    colClass <- c("integer", "character", "character", "character", "character",
                  "numeric", "character", "character", "character"
    )
    bnames <- c("code", "id", "name", "status", "group", "facevalue", "isinno",
                "industry", "type")
    df <- read.table(file="ListOfScrips.csv", sep=",", header=F, skip=1, quote=NULL,
                     colClasses = colClass, col.names = bnames, strip.white=T, fill=T
    )
    df$name <- paste(df$name, " (", df$group, ")", sep="")
    df <- df[df$industry!="",c("code","id","name","industry")]
    df$id <- gsub("\\*|amp;", "", df$id)
    df$name <- gsub("\\.|amp;|-\\$", "", df$name)
    df$industry <- gsub("\\.|amp;|-\\$", "", df$industry)
    #assign("bsels", df, envir=parent.frame())
    return(df)
}

yahoo.plotBseEquityData <- function(symbol="JMTAUTOLTD", range="1d", plottype){
    url <- paste( "http://chartapi.finance.yahoo.com/instrument/1.0/",
                  symbol, ".BO/chartdata;type=quote;range=", range,"/csv",sep="")
    t <- readLines(url)
    l <- grep("^[0-9]", t, value=T)
    l <- strsplit(l , ",")
    m <- do.call(rbind, l)
    d <- as.data.frame(m, stringsAsFactors=F)
    names(d) <- c("date","close","high","low","open","volume")
    d$close <- as.numeric(d$close)
    d$high <- as.numeric(d$high)
    d$low <- as.numeric(d$low)
    d$open <- as.numeric(d$open)
    d$volume <- as.integer(d$volume)
    companyName <- grep("^Company-Name", t, value=T)
    companyName <- gsub("Company-Name:", "", companyName)
    if (substr(range, nchar(range), nchar(range)) == "d")
        d$date <- as.POSIXct(as.integer(d$date), origin = "1970-01-01") - 9000
    else
        d$date <- as.Date(d$date, format="%Y%m%d")
    #d.xts <- as.xts(select(d, open, high, low, close, volume), order.by=d$date)
    d.xts <- as.xts(d[,c("open","high","low","close","volume")], order.by=d$date)
    if (plottype=='c') candleChart(d.xts, name=companyName, theme='white')
    else if (plottype=='b') barChart(d.xts, name=companyName, theme='white')
    else lineChart(d.xts, name=companyName, theme='white')
}

yahoo.getBseEquityData <- function(symbol="JMTAUTOLTD", range="1d"){
    url <- paste( "http://chartapi.finance.yahoo.com/instrument/1.0/",
                  symbol, ".BO/chartdata;type=quote;range=", range,"/csv",sep="")
    t <- readLines(url)
    l <- grep("^[0-9]", t, value=T)
    l <- strsplit(l , ",")
    m <- do.call(rbind, l)
    d <- as.data.frame(m, stringsAsFactors=F)
    names(d) <- c("date","close","high","low","open","volume")
    d$close <- as.numeric(d$close)
    d$high <- as.numeric(d$high)
    d$low <- as.numeric(d$low)
    d$open <- as.numeric(d$open)
    d$volume <- as.integer(d$volume)
    companyName <- grep("^Company-Name", t, value=T)
    companyName <- gsub("Company-Name:", "", companyName)
    if (substr(range, nchar(range), nchar(range)) == "d")
        d$date <- as.POSIXct(as.integer(d$date), origin = "1970-01-01") - 9000
    else
        d$date <- as.Date(d$date, format="%Y%m%d")
    return(d)
}

