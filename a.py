import stockdata as sd


df = sd.getdata("select * from histprice where symbol='HDFC'")

sd.addMA(df, 5)
