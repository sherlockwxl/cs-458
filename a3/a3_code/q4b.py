import base64

import nacl.encoding
import nacl.signing
import requests

f = open("signing_key", "r")
signing_key_text = f.read()
signing_key = nacl.signing.SigningKey(signing_key_text, encoder=nacl.encoding.Base64Encoder)

signed_msg = signing_key.sign("this is a signed msg by xl")
message_encoded = base64.b64encode(signed_msg)

API_token = "a2b30c4b9f28f1b89957d3cd511773bdfae312b151e90b74e278a6a805cdaeb8"
url = "https://whoomp.cs.uwaterloo.ca/458a3/api/signed/send"

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