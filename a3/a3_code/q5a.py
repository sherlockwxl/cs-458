import base64
import json

import nacl.hash
import requests


# step 1 get user public key
API_token = "a2b30c4b9f28f1b89957d3cd511773bdfae312b151e90b74e278a6a805cdaeb8"
url = "https://whoomp.cs.uwaterloo.ca/458a3/api/pke/get-key"

querystring = {"api_token":API_token,
               "user":"jessie"}
payload = ""
headers = {
    'Content-Type': "application/json",
    'Accept': "application/json",
    }

response = requests.request("POST", url, data=payload, headers=headers, params=querystring)
json_data = json.loads(response.text)

encoded_publickey = json_data['public_key']

#step 2 decode:
publickey = base64.standard_b64decode(encoded_publickey)

#step 3 compute fingerprint
HASHER = nacl.hash.blake2b
hashed_public_key = HASHER(publickey, encoder=nacl.encoding.HexEncoder)





