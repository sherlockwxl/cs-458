import base64

import requests

API_token = "a2b30c4b9f28f1b89957d3cd511773bdfae312b151e90b74e278a6a805cdaeb8"

message = "hello Jessie"
message_encoded = base64.b64encode(message.encode())


url = "https://whoomp.cs.uwaterloo.ca/458a3/api/plain/send"

querystring = {"api_token":API_token,
               "to":"jessie",
               "message":message_encoded}
payload = ""
headers = {
    'Content-Type': "application/json",
    'Accept': "application/json",
    }

response = requests.request("POST", url, data=payload, headers=headers, params=querystring)

print(response.text)

url_2 = "https://whoomp.cs.uwaterloo.ca/458a3/api/plain/inbox"

querystring_2 = {"api_token":API_token}

response_2 = requests.request("POST", url_2, data=payload, headers=headers, params=querystring_2)

print(response_2.text)
