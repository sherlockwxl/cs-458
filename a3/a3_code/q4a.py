import nacl.encoding
import nacl.signing
import requests

signing_key = nacl.signing.SigningKey.generate()

verify_key = signing_key.verify_key

signing_key_base64 = signing_key.encode(encoder=nacl.encoding.Base64Encoder)
verify_key_base64 = verify_key.encode(encoder=nacl.encoding.Base64Encoder)


f = open("signing_key", "w")
f.write(signing_key_base64)
f.close()

API_token = "a2b30c4b9f28f1b89957d3cd511773bdfae312b151e90b74e278a6a805cdaeb8"
url = "https://whoomp.cs.uwaterloo.ca/458a3/api/signed/set-key"

querystring = {"api_token":API_token,
               "public_key":verify_key_base64}
payload = ""
headers = {
    'Content-Type': "application/json",
    'Accept': "application/json",
    }

response = requests.request("POST", url, data=payload, headers=headers, params=querystring)

print(response.text)