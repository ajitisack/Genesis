import stockdata as sd

sd.download(startdt='2010-01-01')

sql = 'select symbol from security where 1 = 1 and inbse = 0'
df = sd.getdata(sql)
