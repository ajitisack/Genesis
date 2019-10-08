

source("functions_0.1.R")

ripple <- getCryptoPrice("ripple")
ripple %>% chartSeries()
addSMA(col = "white")
addEMA(col = "red")
zoomChart("2017-03::")


bitcoin <- getCryptoPrice("bitcoin")
bitcoin %>% chartSeries()
bitcoin['2017-06/'] %>% chartSeries()
addSMA(col = "white")
addEMA(col = "red")
zoomChart("2017-03::")


bitcoin <- getCryptoPrice("etherum")
bitcoin %>% chartSeries()
bitcoin['2017-06/'] %>% chartSeries()
addSMA(col = "white")
addEMA(col = "red")
zoomChart("2017-03::")
