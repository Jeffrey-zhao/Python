import requests

#r=requests.get('http://httpbin.org/get')

# r = requests.put('https://httpbin.org/put', data = {'key':'value'})
# r = requests.delete('https://httpbin.org/delete')
# r = requests.head('https://httpbin.org/get')
# r = requests.options('https://httpbin.org/get')

#query
#payload = {'key1': 'value1', 'key2': 'value2'}
#r = requests.get('https://httpbin.org/get', params=payload)

import json

url = 'https://httpbin.org/post'
payload = {'some': 'data'}
r = requests.post(url, data=json.dumps(payload))
r2= requests.post(url, json=payload)
r3= requests.post(url, data=payload)
print(r.url)