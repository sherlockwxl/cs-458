import json

import nacl.secret
import nacl.utils
import base64
import requests


q2_key = "7ed599b0e340f806117d680f9515c045423d21714a8dd2f672843c593b319bb3".decode("hex")

nonce = nacl.utils.random(nacl.secret.SecretBox.NONCE_SIZE)

box = nacl.secret.SecretBox(q2_key)

API_token = "a2b30c4b9f28f1b89957d3cd511773bdfae312b151e90b74e278a6a805cdaeb8"
url = "https://whoomp.cs.uwaterloo.ca/458a3/api/psk/inbox"

querystring = {"api_token":API_token}
payload = ""
headers = {
    'Content-Type': "application/json",
    'Accept': "application/json",
    }

response = requests.request("POST", url, data=payload, headers=headers, params=querystring)

json_data = json.loads(response.text)
encrypted_message = json_data[0]['message']
decoded_message = base64.standard_b64decode(encrypted_message)
plaintext = box.decrypt(decoded_message)
print(plaintext.decode('utf-8'))

