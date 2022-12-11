#!/usr/bin/python3
import requests, json, sys
api_id = sys.argv[1]
url = "https://%s.execute-api.us-east-1.amazonaws.com/production/testpath" % api_id
payload = {"id" : "1"}
response = requests.get(url, params=payload)
response.json()
print(response.text)
