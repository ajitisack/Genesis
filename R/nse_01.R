library(quantmod)
library(data.table)
library(parallel)
library(dplyr)
library(pryr)
library(magrittr)
library(rvest)
library(dygraphs)
library(pbapply)


nse <- fread("../nse.csv")
nse[,TIMESTAMP := as.Date(TIMESTAMP, "%d-%b-%Y")]
nse.xts <- nse[SERIES == "EQ", .(DATE = TIMESTAMP, SYMBOL, OPEN, HIGH, LOW, CLOSE, LAST, PREVCLOSE, VOLUME = TOTTRDQTY)] %>%
        split(by = "SYMBOL", keep.by = F) %>%
        lapply(as.xts.data.table)


