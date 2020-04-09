import stockdata as sd

sd.download(startdt='2010-01-01')

sql = 'select * from quotes where 1 = 1 limit 10'
df = sd.getdata(sql)
df
