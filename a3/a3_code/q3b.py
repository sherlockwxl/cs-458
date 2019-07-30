
import nacl.utils
import base64
import requests
from nacl import pwhash, secret, utils
import json

preshared_pwd="tall public"
salt = "0f6d805f0ed05bd41d781e8350c81f6ccb5bf152ccd2a29aa2e8879c256e2bd2".decode("hex")
operation_limit = 524288
memory_limit = 16777216

kdf = nacl.pwhash.scrypt.kdf

recv_key = kdf(secret.SecretBox.KEY_SIZE, preshared_pwd, salt,
               opslimit=operation_limit, memlimit=memory_limit)
recv_box = secret.SecretBox(recv_key)


API_token = "a2b30c4b9f28f1b89957d3cd511773bdfae312b151e90b74e278a6a805cdaeb8"
url = "https://whoomp.cs.uwaterloo.ca/458a3/api/psp/inbox"

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
plaintext = recv_box.decrypt(decoded_message)
print(plaintext.decode('utf-8'))