import requests

import json

url = "http://127.0.0.1:5000/Chat"

data = {'text': '你好'}

res = requests.post(url=url, data=data)

print(res.text)
