import base64
import json

import nacl.utils
import requests
import nacl.hash
from nacl.public import PrivateKey, Box
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


sk = PrivateKey.generate()
pk = sk.public_key

pk_base64 = pk.encode(encoder=nacl.encoding.Base64Encoder)


API_token = "a2b30c4b9f28f1b89957d3cd511773bdfae312b151e90b74e278a6a805cdaeb8"
url = "https://whoomp.cs.uwaterloo.ca/458a3/api/pke/set-key"

querystring = {"api_token":API_token,
               "public_key":pk_base64}
payload = ""
headers = {
    'Content-Type': "application/json",
    'Accept': "application/json",
    }

response = requests.request("POST", url, data=payload, headers=headers, params=querystring)

print(response.text)


# step 3 encrypt message
Jessie_pk = nacl.public.PublicKey(encoded_publickey, encoder=nacl.encoding.Base64Encoder)
j_box = Box(sk, Jessie_pk)



url_2 = "https://whoomp.cs.uwaterloo.ca/458a3/api/pke/inbox"
querystring_2 = {"api_token":API_token}

response_2 = requests.request("POST", url_2, data=payload, headers=headers, params=querystring_2)

json_data_2 = json.loads(response_2.text)
encrypted_msg = json_data_2[0]['message']
decoded_msg = base64.standard_b64decode(encrypted_msg)
decrypted_msg = j_box.decrypt(decoded_msg)
print(decrypted_msg)