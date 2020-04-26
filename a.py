import stockdata as sd

df = sd.downloadsectorclassify()
sd.loadtable(df, 'sectormc')

sd.downloaddetailsmc()
