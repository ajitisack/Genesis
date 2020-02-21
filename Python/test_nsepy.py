# from datetime import date
# from nsepy import get_history
# sbin = get_history(symbol='SBIN', start=date(2018,1,1), end=date(2018,1,10))
#
#
# l = (i**2 for i in range(10))
# print(list(l))

import string

letters = string.ascii_lowercase
d = {i:j for i,j in zip(letters, range(1,len(letters)+1))}
print(d['i'])
