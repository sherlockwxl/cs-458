import base64
import json

import nacl.utils
import requests
import nacl.hash
from nacl.public import PrivateKey, Box
import nacl.secret



# part one generate key
sk = PrivateKey.generate()
pk = sk.public_key

pk_base64 = pk.encode(encoder=nacl.encoding.Base64Encoder)


API_token = "a2b30c4b9f28f1b89957d3cd511773bdfae312b151e90b74e278a6a805cdaeb8"
url = "https://whoomp.cs.uwaterloo.ca/458a3/api/surveil/set-key"

querystring = {"api_token":API_token,
               "public_key":pk_base64}
payload = ""
headers = {
    'Content-Type': "application/json",
    'Accept': "application/json",
    }

response = requests.request("POST", url, data=payload, headers=headers, params=querystring)

print(response.text)




# step 2 download jessie public key
API_token = "a2b30c4b9f28f1b89957d3cd511773bdfae312b151e90b74e278a6a805cdaeb8"
url = "https://whoomp.cs.uwaterloo.ca/458a3/api/surveil/get-key"

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


# generate jessie key and box
Jessie_pk = nacl.public.PublicKey(encoded_publickey, encoder=nacl.encoding.Base64Encoder)
j_box = Box(sk, Jessie_pk)

govern_key = "NARrOpqAK5PVIXqp5G520V5JUoYdwEX0VbflBx/VVBQ="
govern_pk = nacl.public.PublicKey(govern_key, encoder=nacl.encoding.Base64Encoder)
g_box = Box(sk, govern_pk)

# step 4 - 5 random key
message = "this msg is encrypted by box with jessie key and govern key"
message_key = nacl.utils.random(nacl.secret.SecretBox.KEY_SIZE)
secret_box = nacl.secret.SecretBox(message_key)
message_nonce = nacl.utils.random(Box.NONCE_SIZE)
ciphertext = secret_box.encrypt(message, message_nonce).ciphertext

#step 6
recipient_nonce = nacl.utils.random(Box.NONCE_SIZE)
recipient_ciphertext = j_box.encrypt(message_key, recipient_nonce).ciphertext

#step 7
government_nonce = nacl.utils.random(Box.NONCE_SIZE)
government_ciphertext = g_box.encrypt(message_key, government_nonce).ciphertext


#step 8 build final message

final_message = recipient_nonce + recipient_ciphertext + government_nonce + government_ciphertext + message_nonce + ciphertext

encoded_final_message = base64.standard_b64encode(final_message)




url_2 = "https://whoomp.cs.uwaterloo.ca/458a3/api/surveil/inbox"
querystring_2 = {"api_token":API_token}

response_2 = requests.request("POST", url_2, data=payload, headers=headers, params=querystring_2)

json_data_2 = json.loads(response_2.text)
encrypted_msg = json_data_2[0]['message']

# decrypt message

decoded_message = base64.standard_b64decode(encrypted_msg)
gap = len(recipient_nonce) + len(recipient_ciphertext)
recipient_ciphertext_back = decoded_message[:gap]
message_ciphertext_back = decoded_message[2 * gap:]

secret_key = j_box.decrypt(recipient_ciphertext_back)
secret_box = nacl.secret.SecretBox(secret_key)

decrypted_message = secret_box.decrypt(message_ciphertext_back)

print(decrypted_message)


