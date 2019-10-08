


webpage <- read_html("http://www.moneycontrol.com/stocks/marketstats/industry-classification/nse/banks-private-sector.html")
x <- html_nodes(webpage,'.stat_lflist') %>% html_text()
