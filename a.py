import stockdata as sd
import pandas as pd

df = sd.getdata("select * from histprice where 1=1")

x = df[df.symbol=='HDFCBANK'].reset_index(drop=True)


sd.addIndicators(x)




n = 3
weights= list(reversed([(n - i) * n for i in range(n)]))

def wma(w):
    def g(x):
        return sum(w*x)/sum(w)
    return g

x.close.rolling(n).apply(wma(weights))
