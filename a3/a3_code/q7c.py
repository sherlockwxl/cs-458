import nacl.encoding
import nacl.signing
import requests
from nacl.public import PrivateKey, Box
import base64
import json

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



# q7b
#step 1 get jessie key

url_2 = "https://whoomp.cs.uwaterloo.ca/458a3/api/prekey/get-identity-key"

querystring = {"api_token":API_token,
               "user":"jessie"}
payload = ""
headers = {
    'Content-Type': "application/json",
    'Accept': "application/json",
    }

response = requests.request("POST", url_2, data=payload, headers=headers, params=querystring)
print(response.text)
json_data = json.loads(response.text)

jessie_ivkey = json_data['public_key']

decoded_jessie_ivkey = base64.standard_b64decode(jessie_ivkey)


url_3 = "https://whoomp.cs.uwaterloo.ca/458a3/api/prekey/get-signed-prekey"
response = requests.request("POST", url_3, data=payload, headers=headers, params=querystring)
print(response.text)
json_data = json.loads(response.text)

jessie_signed_prekey = json_data['public_key']

decoded_jessie_signed_prekey= base64.standard_b64decode(jessie_signed_prekey)

#step 5 verify
verify_key_for_jessie = nacl.signing.VerifyKey(decoded_jessie_ivkey, encoder=nacl.encoding.RawEncoder)
jessie_public_key_content = verify_key_for_jessie.verify(decoded_jessie_signed_prekey)
jessie_public_key = nacl.public.PublicKey(jessie_public_key_content, encoder=nacl.encoding.RawEncoder)
# step 6
message = " q7 message"
box = Box(sk, jessie_public_key)
message_nonce = nacl.utils.random(Box.NONCE_SIZE)
encrypted_message = box.encrypt(message, message_nonce)
encoded_message = base64.standard_b64encode(encrypted_message)

url_4 = "https://whoomp.cs.uwaterloo.ca/458a3/api/prekey/send"
querystring_4 = {"api_token":API_token,
                 "to":"jessie",
               "message":encoded_message}
response = requests.request("POST", url_4, data=payload, headers=headers, params=querystring_4)
print(response.status_code)



# q7c
url_5 = "https://whoomp.cs.uwaterloo.ca/458a3/api/prekey/inbox"
querystring_5 = {"api_token":API_token}

response_2 = requests.request("POST", url_5, data=payload, headers=headers, params=querystring_5)

json_data_2 = json.loads(response_2.text)
encrypted_msg = json_data_2[0]['message']

decrypted_message = box.decrypt(base64.standard_b64decode(encrypted_msg))
print(decrypted_message)