#!/usr/bin/python3
import requests, json, sys
api_id = sys.argv[1]
url = "https://%s.execute-api.us-east-1.amazonaws.com/production/testpath" % api_id
post_payload = {"City":"Korsa","Street":"Korsveien 3","PostCode":"19021","SN":"MD129F643H","id":"1","Model":"c12a","Output":"22"}
#post_response = requests.put(url, headers=headers, params=post_payload)
post_response = requests.put(url, params=post_payload)
print(post_response.text)
post_payload = {"City":"Korsa","Street":"Korsveien 3","PostCode":"19021","SN":"MD129F643H","id":"2","Model":"c12a","Output":"22"}
#post_response = requests.put(url, headers=headers, params=post_payload)
post_response = requests.put(url, params=post_payload)
print(post_response.text)
post_payload = {"City":"Korsa","Street":"Korsveien 3","PostCode":"19021","SN":"MD129F637H","id":"3","Model":"c12a","Output":"22"}
#post_response = requests.put(url, headers=headers, params=post_payload)
post_response = requests.put(url, params=post_payload)
print(post_response.text)
post_payload = {"City":"Korsa","Street":"Korsveien 3","PostCode":"19021","SN":"MD139F647H","id":"4","Model":"c12a","Output":"22"}
#post_response = requests.put(url, headers=headers, params=post_payload)
post_response = requests.put(url, params=post_payload)
print(post_response.text)
post_payload = {"City":"Korsa","Street":"Korsveien 3","PostCode":"19021","SN":"MD729F871H","id":"5","Model":"c12a","Output":"22"}
#post_response = requests.put(url, headers=headers, params=post_payload)
post_response = requests.put(url, params=post_payload)
print(post_response.text)
post_payload = {"City":"Korsa","Street":"Korsveien 3","PostCode":"19021","SN":"MD329F667H","id":"6","Model":"c12a","Output":"22"}
#post_response = requests.put(url, headers=headers, params=post_payload)
post_response = requests.put(url, params=post_payload)
print(post_response.text)
post_payload = {"City":"Korsa","Street":"Korsveien 3","PostCode":"19021","SN":"MD129X649H","id":"7","Model":"c12a","Output":"22"}
#post_response = requests.put(url, headers=headers, params=post_payload)
post_response = requests.put(url, params=post_payload)
print(post_response.text)
post_payload = {"City":"Korsa","Street":"Solli 29","PostCode":"19021","SN":"MD129F651X","id":"8","Model":"c12xl","Output":"150"}
#post_response = requests.put(url, headers=headers, params=post_payload)
post_response = requests.put(url, params=post_payload)
print(post_response.text)
post_payload = {"City":"Korsa","Street":"Solli 29","PostCode":"19021","SN":"MD129F641B","id":"9","Model":"c12xl","Output":"150"}
#post_response = requests.put(url, headers=headers, params=post_payload)
post_response = requests.put(url, params=post_payload)
print(post_response.text)
post_payload = {"City":"Korsa","Street":"Solli 29","PostCode":"19021","SN":"MD129F646C","id":"10","Model":"c12b","Output":"50"}
#post_response = requests.put(url, headers=headers, params=post_payload)
post_response = requests.put(url, params=post_payload)
print(post_response.text)
post_payload = {"City":"Korsa","Street":"Solli 29","PostCode":"19021","SN":"MD129F643D","id":"11","Model":"c12b","Output":"50"}
#post_response = requests.put(url, headers=headers, params=post_payload)
post_response = requests.put(url, params=post_payload)
print(post_response.text)
post_payload = {"City":"Korsa","Street":"Solli 29","PostCode":"19021","SN":"MD129F64CE","id":"12","Model":"c12b","Output":"50"}
#post_response = requests.put(url, headers=headers, params=post_payload)
post_response = requests.put(url, params=post_payload)
print(post_response.text)
post_payload = {"City":"Korsa","Street":"Solli 29","PostCode":"19021","SN":"MD129F644F","id":"13","Model":"c12b","Output":"50"}
#post_response = requests.put(url, headers=headers, params=post_payload)
post_response = requests.put(url, params=post_payload)
print(post_response.text)
post_payload = {"City":"Vola","Street":"Smievegen 16","PostCode":"19024","SN":"MD129F547A","id":"14","Model":"c12b","Output":"50"}
#post_response = requests.put(url, headers=headers, params=post_payload)
post_response = requests.put(url, params=post_payload)
print(post_response.text)
post_payload = {"City":"Vola","Street":"Smievegen 16","PostCode":"19024","SN":"MD129F547B","id":"15","Model":"c12b","Output":"50"}
#post_response = requests.put(url, headers=headers, params=post_payload)
post_response = requests.put(url, params=post_payload)
print(post_response.text)
post_payload = {"City":"Vola","Street":"Smievegen 16","PostCode":"19024","SN":"MD129F547C","id":"16","Model":"c12b","Output":"50"}
#post_response = requests.put(url, headers=headers, params=post_payload)
post_response = requests.put(url, params=post_payload)
print(post_response.text)
post_payload = {"City":"Vola","Street":"Smievegen 16","PostCode":"19024","SN":"MD129F547X","id":"17","Model":"c12b","Output":"50"}
#post_response = requests.put(url, headers=headers, params=post_payload)
post_response = requests.put(url, params=post_payload)
print(post_response.text)
post_payload = {"City":"Vola","Street":"Smievegen 16","PostCode":"19024","SN":"MD129F567D","id":"18","Model":"c12b","Output":"50"}
#post_response = requests.put(url, headers=headers, params=post_payload)
post_response = requests.put(url, params=post_payload)
print(post_response.text)
post_payload = {"City":"Vola","Street":"Smievegen 16","PostCode":"19024","SN":"MD129F540L","id":"19","Model":"c12b","Output":"50"}
#post_response = requests.put(url, headers=headers, params=post_payload)
post_response = requests.put(url, params=post_payload)
print(post_response.text)
post_payload = {"City":"Vola","Street":"Kulturplass 62","PostCode":"19024","SN":"AD129F246J","id":"20","Model":"c12b","Output":"50"}
#post_response = requests.put(url, headers=headers, params=post_payload)
post_response = requests.put(url, params=post_payload)
print(post_response.text)
post_payload = {"City":"Vola","Street":"Kulturplass 62","PostCode":"19024","SN":"AD129F245K","id":"21","Model":"c12bs","Output":"48"}
#post_response = requests.put(url, headers=headers, params=post_payload)
post_response = requests.put(url, params=post_payload)
print(post_response.text)
post_payload = {"City":"Vola","Street":"Kulturplass 62","PostCode":"19024","SN":"AD129F241L","id":"22","Model":"c12bs","Output":"48"}
#post_response = requests.put(url, headers=headers, params=post_payload)
post_response = requests.put(url, params=post_payload)
print(post_response.text)
post_payload = {"City":"Vola","Street":"Kulturplass 62","PostCode":"19024","SN":"AD129F232M","id":"23","Model":"c12bs","Output":"48"}
#post_response = requests.put(url, headers=headers, params=post_payload)
post_response = requests.put(url, params=post_payload)
print(post_response.text)
post_payload = {"City":"Vola","Street":"Kulturplass 62","PostCode":"19024","SN":"AD129F281N","id":"24","Model":"c12bs","Output":"48"}
#post_response = requests.put(url, headers=headers, params=post_payload)
post_response = requests.put(url, params=post_payload)
print(post_response.text)
post_payload = {"City":"Vola","Street":"Kulturplass 62","PostCode":"19024","SN":"AD129F294S","id":"25","Model":"c12bs","Output":"48"}
#post_response = requests.put(url, headers=headers, params=post_payload)
post_response = requests.put(url, params=post_payload)
print(post_response.text)

