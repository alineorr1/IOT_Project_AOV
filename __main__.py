import requests 
url = 'https://api.ouraring.com/v2/usercollection/personal_info' 
params={ 
    'start_date': '2024-11-01', 
    'end_date': '2021-12-01' 
}
headers = { 
  'Authorization': 'Bearer JEPNM2ZIDZ72HI3GLURRN25ANCI257NA' 
}
response = requests.request('GET', url, headers=headers, params=params) 
print(response.text) 