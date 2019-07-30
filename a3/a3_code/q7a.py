import nacl.encoding
import nacl.signing
import requests
from nacl.public import PrivateKey
import base64

signing_key = nacl.signing.SigningKey.generate()

verify_key = signing_key.verify_key

signing_key_base64 = signing_key.encode(encoder=nacl.encoding.Base64Encoder)
verify_key_base64 = verify_key.encode(encoder=nacl.encoding.Base64Encoder)


f = open("signing_key_q7", "w")
f.write(signing_key_base64)
f.close()

API_token = "a2b30c4b9f28f1b89957d3cd511773bdfae312b151e90b74e278a6a805cdaeb8"
url = "https://whoomp.cs.uwaterloo.ca/458a3/api/prekey/set-identity-key"

querystring = {"api_token":API_token,
               "public_key":verify_key_base64}
payload = ""
headers = {
    'Content-Type': "application/json",
    'Accept': "application/json",
    }

response = requests.request("POST", url, data=payload, headers=headers, params=querystring)

print(response.text)

#step 2
sk = PrivateKey.generate()
pk = sk.public_key
encoded_pk = pk.encode(encoder=nacl.encoding.RawEncoder)

signed_preky = signing_key.sign(encoded_pk)
encoded_pk_base_64 = base64.standard_b64encode(signed_preky)

API_token = "a2b30c4b9f28f1b89957d3cd511773bdfae312b151e90b74e278a6a805cdaeb8"
url = "https://whoomp.cs.uwaterloo.ca/458a3/api/prekey/set-signed-prekey"

querystring = {"api_token":API_token,
               "public_key":encoded_pk_base_64}
payload = ""
headers = {
    'Content-Type': "application/json",
    'Accept': "application/json",
    }

response = requests.request("POST", url, data=payload, headers=headers, params=querystring)

print(response.text)
