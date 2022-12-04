import requests, json
url = "https://api.elbrusgroup.net/chargers"
post_payload = {"City":"Korsa","Street":"Korsveien 3","PostCode":"19021","SN":"MD129F643H","id":"1","Model":"c12a","Output":"22"}
post_response = requests.post(url, params=post_payload)
print(post_response.text)

