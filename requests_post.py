

import requests

url = 'https://www.bseindia.com/corporates/List_Scrips.aspx'

response=requests.post(url = url, data=data)
response
print(response.text)


with requests.session() as s:
    url = 'https://www.bseindia.com/corporates/List_Scrips.aspx'
    data = {'ctl00$ContentPlaceHolder1$ddSegment':'Equity', 'ctl00$ContentPlaceHolder1$ddlStatus':'Active', 'ctl00$ContentPlaceHolder1$btnSubmit':"Submit"}
    response_post = s.post(url, data=data)
    response = s.get(url)

print(response.text)

url = "https://api.bseindia.com/bseindia/api/Sensex/getSensexData?json={'fields':'1,2,3,4,5,6,7,8'}"
response = requests.get(url)
response.text
